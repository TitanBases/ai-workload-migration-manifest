# Examples

These manifests are **illustrative fixtures**, not claims about real customer migrations or vendor compatibility.

- `core-inventory.json` — minimum discovery/inventory document.
- `model-endpoint-migration.json` — Migration-Ready model/runtime substitution with behavioral acceptance.
- `mcp-agent-runtime-migration.json` — Migration-Ready agent runtime move with MCP dependencies, memory transformation, permission rebinding and secret references.
- `enterprise-agent-evidence-complete.json` — Evidence-Complete example showing gate results, evidence linkage and validated rollback.

All example names, providers, evidence URNs and measurements are synthetic.

Validate them with:

```bash
python scripts/validate.py examples/
```
