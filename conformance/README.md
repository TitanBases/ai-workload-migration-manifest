# AWMM Conformance

AWMM separates **structural validity** from **migration readiness** and **evidence completeness**.

## AWMM Core

A Core document:

- validates against `schema/awmm.schema.json`;
- identifies the workload, source and target;
- inventories at least one asset;
- uses unique identifiers within each collection;
- contains no embedded secret values.

Core is appropriate during discovery and inventory. Core does not mean the workload is ready to migrate.

## AWMM Migration-Ready

A Migration-Ready document satisfies Core and also:

- sets `conformanceTarget` to `migration-ready`;
- defines at least one acceptance gate;
- defines rollback;
- has no required asset with `unknown` or `unsupported` portability;
- supplies a transformation for every required `transform-required` asset;
- has no required dependency with an `unresolved` migration treatment.

Migration-Ready means the contract is sufficiently explicit to enter a controlled migration process. It does not mean the migration has succeeded.

## AWMM Evidence-Complete

An Evidence-Complete document satisfies Migration-Ready and also:

- sets `conformanceTarget` to `evidence-complete`;
- includes evidence records;
- records a result for every blocking acceptance gate;
- has no blocking gate in `failed` or `not-run` state;
- links evidence for each blocking gate that requires evidence;
- links waiver evidence for any waived blocking gate;
- links rollback evidence when rollback is declared validated.

Evidence-Complete means the manifest contains the minimum evidence linkage required by this specification. It does not certify the quality, truthfulness, independence or sufficiency of that evidence for every organization.

## Validator behavior

The reference validator performs:

1. JSON Schema Draft 2020-12 validation;
2. identifier uniqueness checks;
3. cross-reference checks;
4. conformance-target semantic checks;
5. best-effort detection of obviously embedded secret material.

Run:

```bash
python -m pip install -r requirements.txt
python scripts/validate.py examples/
```

A conforming implementation MAY implement stricter organizational policy on top of AWMM, but MUST NOT weaken the normative meaning of an AWMM conformance level while still claiming that level.
