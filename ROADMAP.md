# Roadmap

This roadmap is directional and non-normative. It does not commit TitanBases or contributors to dates.

## v0.1 — foundation

Status: current draft.

- migration-contract vocabulary;
- JSON Schema;
- Core, Migration-Ready and Evidence-Complete conformance;
- reference validator;
- representative examples;
- ecosystem boundary and security guidance.

## v0.2 — implementation feedback

Candidate work, subject to public review:

- extension-registration guidance;
- stronger artifact provenance semantics;
- explicit migration-phase metadata;
- richer policy/permission mapping examples;
- reference mappings for common agent, RAG and multi-agent workloads;
- validator diagnostics and machine-readable validation output;
- independent implementation feedback.

## Pre-v1.0 exit criteria

Before calling AWMM 1.0 stable, the project should have:

- multiple real migration case studies using materially different stacks;
- at least one implementation independent of the initial reference validator;
- evidence that core terminology is understandable outside TitanBases;
- resolved security review of secret handling, evidence integrity and extension behavior;
- a compatibility policy suitable for stable versioning;
- governance reviewed against actual contributor/adopter participation.

## Explicit non-goals for the roadmap

The project does not plan to become:

- an agent runtime;
- a replacement for MCP or A2A;
- a universal durable-memory format;
- a secret-transfer mechanism;
- a benchmark leaderboard;
- a certification authority.

If an adjacent project solves a lower-layer problem well, AWMM should integrate by reference rather than absorb it.
