# Contributing

Contributions are welcome through GitHub issues and pull requests.

## Before proposing a core field

Ask whether the information is truly part of the **migration contract**.

A core field is a good fit when it describes one of:

- migration scope;
- asset portability;
- dependency treatment;
- required transformation or rebinding;
- migration risk;
- baseline;
- acceptance gate;
- evidence;
- rollback;
- provenance.

A core field is probably the wrong fit when it attempts to redefine:

- MCP transport or tool semantics;
- A2A communication;
- Agent Skills packaging;
- an agent-state serialization format;
- model runtime internals;
- secret transport.

Use `extensions` for organization- or vendor-specific metadata until a broadly useful core requirement is demonstrated.

## Pull request requirements

Normative changes should update, as applicable:

- `SPECIFICATION.md`;
- `schema/awmm.schema.json`;
- `scripts/validate.py`;
- examples;
- conformance documentation;
- `CHANGELOG.md`.

Run locally:

```bash
python -m pip install -r requirements.txt
python scripts/validate.py examples/
```

## Compatibility

v0.x is pre-1.0. Breaking changes are allowed but must be explicit.

Do not silently change the meaning of an existing field. Prefer a new version when semantics change.

## Security

Never include real credentials, customer secrets or sensitive production evidence in an example or test fixture.

Security-sensitive reports should follow [SECURITY.md](SECURITY.md).
