# AI Workload Migration Manifest (AWMM)

[![Validate AWMM](https://github.com/TitanBases/ai-workload-migration-manifest/actions/workflows/validate.yml/badge.svg)](https://github.com/TitanBases/ai-workload-migration-manifest/actions/workflows/validate.yml)

> **Status:** Draft Specification v0.1.0  
> **Maintainer:** TitanBases Technology  
> **License:** Apache-2.0

AWMM is an open, vendor-neutral draft specification for describing and validating the migration of an AI workload across runtimes, platforms, model providers, infrastructure boundaries, or operating environments.

AWMM does **not** define how an agent is built, how tools communicate, how durable agent state is serialized, or how a runtime executes an agent. It defines the **migration contract** around those systems: what must move, what must be transformed or rebound, what may be lost, what risks exist, what acceptance gates apply, what evidence proves the result, and how rollback is handled.

## Why AWMM exists

Interoperability, portability, and migration are related but different engineering concerns.

- **Interoperability** asks whether systems can communicate or cooperate.
- **Portability** asks whether an asset can be represented or reused elsewhere.
- **Migration** asks whether an operational workload can move from a source environment to a target environment while satisfying explicit acceptance criteria.

A workload can be interoperable without being portable, portable without being migration-ready, and successfully imported without being behaviorally acceptable.

AWMM makes those distinctions machine-readable.

## What an AWMM manifest can describe

An AWMM manifest can declare:

- source and target environments;
- workload identity and criticality;
- instructions, skills, tools, models, memory, retrieval data, workflow state, identity, permissions, policies, secret references, observability and evaluation assets;
- external dependencies and protocols;
- transformation and rebinding requirements;
- migration risks and mitigations;
- behavioral and operational baselines;
- blocking acceptance gates;
- validation evidence and provenance;
- rollback requirements and rollback evidence.

## What AWMM deliberately does not replace

AWMM is designed to reference and coexist with ecosystem specifications rather than duplicate them.

| Technology / format | Primary concern | AWMM relationship |
| --- | --- | --- |
| Model Context Protocol (MCP) | application/agent access to tools, resources and prompts | declare MCP dependencies and migration treatment |
| Agent2Agent (A2A) | agent-to-agent interoperability and collaboration | declare A2A endpoints/capabilities as dependencies |
| Agent Skills | portable procedural capability packages | reference skill artifacts and their portability status |
| Agent Life Format (ALF) | durable agent-state serialization | reference an ALF artifact when used for state transfer |
| Autonomous Agent Interchange Format (AAIF) | portable agent definition/state model | reference AAIF artifacts if used by an implementation |
| Runtime-specific migration systems | execution-state transfer and runtime mechanisms | record the mechanism and evidence, not redefine it |

See [Ecosystem Mapping](docs/ECOSYSTEM-MAPPING.md).

## Minimal example

```yaml
specVersion: "0.1.0"
manifestId: "urn:awmm:example:customer-support-agent:001"
status: draft

workload:
  id: customer-support-agent
  name: Customer Support Agent
  kind: agent
  criticality: high

source:
  environmentId: source-prod
  runtime: vendor-a-agent-runtime
  provider: vendor-a

target:
  environmentId: target-prod
  runtime: vendor-b-agent-runtime
  provider: vendor-b

assets:
  - id: core-instructions
    category: instructions
    required: true
    portability: portable

  - id: long-term-memory
    category: memory
    required: true
    format: vendor-specific
    portability: transform-required

acceptanceGates:
  - id: critical-scenarios
    domain: behavioral
    criterion: Critical scenario pass rate must equal the approved baseline.
    blocking: true
    evidenceRequired: true

rollback:
  required: true
  strategy: Restore the source snapshot and re-enable source routing.
```

The full examples live in [examples/](examples/).

## Conformance levels

AWMM defines three conformance levels:

1. **AWMM Core** — structurally valid manifest with workload, source, target and asset inventory.
2. **AWMM Migration-Ready** — adds dependencies, transformations, risks, acceptance gates and rollback planning.
3. **AWMM Evidence-Complete** — adds completed gate results and linked evidence sufficient to substantiate the declared migration outcome.

The JSON Schema validates the structural contract. The reference validator adds cross-reference and conformance checks that are difficult to express safely in JSON Schema alone.

See [Conformance](conformance/README.md).

## Repository layout

```text
.
├── SPECIFICATION.md
├── schema/
│   └── awmm.schema.json
├── examples/
├── conformance/
│   └── README.md
├── docs/
│   ├── DESIGN-PRINCIPLES.md
│   └── ECOSYSTEM-MAPPING.md
├── scripts/
│   └── validate.py
├── SECURITY.md
├── GOVERNANCE.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Validate manifests

```bash
python -m pip install -r requirements.txt
python scripts/validate.py examples/
```

Validation checks JSON Schema compliance, identifier uniqueness, cross-references and the selected conformance target.

## Security rule: manifests must not contain secrets

AWMM manifests MUST NOT embed API keys, passwords, access tokens, private keys or equivalent secret material. A manifest may contain an opaque reference to an external secret store and may state that a credential must be rebound or recreated in the target environment.

See [SECURITY.md](SECURITY.md).

## Specification status

v0.1.0 is a **draft**, not a claim of industry-standard status or universal migration equivalence. Breaking changes may occur before v1.0. The project is published early to make terminology, design decisions and provenance reviewable.

## Contributing

Issues and pull requests are welcome. Material changes to normative semantics should include rationale, compatibility impact and updated examples or fixtures where applicable.

See [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), and the non-normative [ROADMAP.md](ROADMAP.md). Citation metadata is available in [CITATION.cff](CITATION.cff).

## License

Copyright 2026 TitanBases Technology Co., Ltd.

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
