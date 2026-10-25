#!/usr/bin/env python3
"""Reference validator for AWMM v0.1.0."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "awmm.schema.json"
SUPPORTED_VERSION = "0.1.0"

SUSPICIOUS_SECRET_KEYS = {
    "apikey", "api_key", "password", "passwd", "access_token", "refreshtoken",
    "refresh_token", "privatekey", "private_key", "secretvalue", "secret_value",
}
SECRET_VALUE_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]


def load_document(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    raise ValueError(f"unsupported manifest extension: {path.suffix}")


def collect_manifest_paths(inputs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in {".json", ".yaml", ".yml"}))
        else:
            paths.append(path)
    return paths


def duplicate_ids(items: list[dict[str, Any]], label: str) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for item in items:
        identifier = item.get("id")
        if not identifier:
            continue
        if identifier in seen:
            errors.append(f"{label}: duplicate id {identifier!r}")
        seen.add(identifier)
    return errors


def scan_for_secret_values(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_")
            if normalized in SUSPICIOUS_SECRET_KEYS and not normalized.endswith("_ref"):
                errors.append(f"{path}.{key}: secret-like key is not permitted; use an opaque reference")
            errors.extend(scan_for_secret_values(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(scan_for_secret_values(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: value resembles secret material; store only an opaque reference")
                break
    return errors


def semantic_errors(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if doc.get("specVersion") != SUPPORTED_VERSION:
        errors.append(f"unsupported specVersion {doc.get('specVersion')!r}; validator supports {SUPPORTED_VERSION!r}")

    collections = {
        "assets": doc.get("assets", []),
        "dependencies": doc.get("dependencies", []),
        "transformations": doc.get("transformations", []),
        "risks": doc.get("risks", []),
        "baselines": doc.get("baselines", []),
        "acceptanceGates": doc.get("acceptanceGates", []),
        "evidence": doc.get("evidence", []),
    }
    for label, items in collections.items():
        errors.extend(duplicate_ids(items, label))

    asset_ids = {x.get("id") for x in collections["assets"]}
    baseline_ids = {x.get("id") for x in collections["baselines"]}
    gate_ids = {x.get("id") for x in collections["acceptanceGates"]}
    evidence_ids = {x.get("id") for x in collections["evidence"]}

    for tx in collections["transformations"]:
        for ref in tx.get("assetRefs", []):
            if ref not in asset_ids:
                errors.append(f"transformation {tx.get('id')!r}: unknown assetRef {ref!r}")
        for ref in tx.get("evidenceRefs", []):
            if ref not in evidence_ids:
                errors.append(f"transformation {tx.get('id')!r}: unknown evidenceRef {ref!r}")

    for risk in collections["risks"]:
        for ref in risk.get("acceptanceGateRefs", []):
            if ref not in gate_ids:
                errors.append(f"risk {risk.get('id')!r}: unknown acceptanceGateRef {ref!r}")

    for gate in collections["acceptanceGates"]:
        baseline_ref = gate.get("baselineRef")
        if baseline_ref and baseline_ref not in baseline_ids:
            errors.append(f"gate {gate.get('id')!r}: unknown baselineRef {baseline_ref!r}")
        for ref in gate.get("result", {}).get("evidenceRefs", []):
            if ref not in evidence_ids:
                errors.append(f"gate {gate.get('id')!r}: unknown evidenceRef {ref!r}")

    for evidence in collections["evidence"]:
        for ref in evidence.get("gateRefs", []):
            if ref not in gate_ids:
                errors.append(f"evidence {evidence.get('id')!r}: unknown gateRef {ref!r}")

    rollback = doc.get("rollback", {})
    for ref in rollback.get("evidenceRefs", []):
        if ref not in evidence_ids:
            errors.append(f"rollback: unknown evidenceRef {ref!r}")

    target = doc.get("conformanceTarget", "core")
    if target in {"migration-ready", "evidence-complete"}:
        gates = collections["acceptanceGates"]
        if not gates:
            errors.append("migration-ready: at least one acceptance gate is required")
        if not rollback:
            errors.append("migration-ready: rollback plan is required")

        transformed_assets = {ref for tx in collections["transformations"] for ref in tx.get("assetRefs", [])}
        for asset in collections["assets"]:
            if not asset.get("required"):
                continue
            portability = asset.get("portability")
            if portability in {"unknown", "unsupported"}:
                errors.append(f"migration-ready: required asset {asset.get('id')!r} has portability {portability!r}")
            if portability == "transform-required" and asset.get("id") not in transformed_assets:
                errors.append(f"migration-ready: required transform-required asset {asset.get('id')!r} has no transformation")

        for dep in collections["dependencies"]:
            if dep.get("required") and dep.get("migrationTreatment") == "unresolved":
                errors.append(f"migration-ready: required dependency {dep.get('id')!r} is unresolved")

    if target == "evidence-complete":
        if not collections["evidence"]:
            errors.append("evidence-complete: evidence is required")
        for gate in collections["acceptanceGates"]:
            if not gate.get("blocking"):
                continue
            result = gate.get("result")
            if not result:
                errors.append(f"evidence-complete: blocking gate {gate.get('id')!r} has no result")
                continue
            status = result.get("status")
            if status in {"failed", "not-run"}:
                errors.append(f"evidence-complete: blocking gate {gate.get('id')!r} is {status!r}")
            evidence_refs = result.get("evidenceRefs", [])
            if gate.get("evidenceRequired") and not evidence_refs:
                errors.append(f"evidence-complete: blocking gate {gate.get('id')!r} requires evidence")
            if status == "waived" and not evidence_refs:
                errors.append(f"evidence-complete: waived blocking gate {gate.get('id')!r} requires waiver evidence")

        if rollback.get("validated") and not rollback.get("evidenceRefs"):
            errors.append("evidence-complete: validated rollback requires rollback evidence")

    errors.extend(scan_for_secret_values(doc))
    return errors


def validate(path: Path, schema: dict[str, Any]) -> list[str]:
    try:
        doc = load_document(path)
    except Exception as exc:
        return [f"parse error: {exc}"]

    if not isinstance(doc, dict):
        return ["manifest root must be an object"]

    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
        where = "$" + "".join(f"[{part!r}]" for part in error.absolute_path)
        errors.append(f"{where}: {error.message}")

    if not errors:
        errors.extend(semantic_errors(doc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AWMM v0.1.0 manifests")
    parser.add_argument("paths", nargs="+", help="manifest files or directories")
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    paths = collect_manifest_paths(args.paths)
    if not paths:
        print("No manifest files found.", file=sys.stderr)
        return 2

    failed = False
    for path in paths:
        errors = validate(path, schema)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
