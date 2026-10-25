# Governance

## Project status

AWMM is an open **Draft Specification** maintained by TitanBases Technology. v0.x releases are pre-1.0 and may change incompatibly.

The project does not claim standards-body status. The goal is to develop a precise, reviewable and implementation-informed specification in public.

## Maintainer responsibilities

Maintainers are responsible for:

- preserving the distinction between interoperability, portability and migration;
- preventing scope expansion into protocols or artifact formats already owned by other projects;
- reviewing normative changes for compatibility and security impact;
- keeping the schema, prose specification, validator and examples aligned;
- documenting breaking changes;
- avoiding unsupported claims about adoption or industry status.

## Change classes

### Editorial

Spelling, examples, links and clarifications that do not change normative meaning.

### Compatible normative

New optional fields, enumerations or rules that do not invalidate previously conforming documents within the same declared compatibility policy.

### Breaking normative

Changes that alter required fields, field meaning, conformance requirements or validation behavior.

Before v1.0, breaking changes may occur in a minor release. They must be called out in the changelog.

## Proposal process

Material normative changes should be proposed through an issue or pull request containing:

1. problem statement;
2. proposed semantics;
3. alternatives considered;
4. compatibility impact;
5. security/privacy impact;
6. schema changes;
7. updated examples/tests.

Maintainers may request an experimental extension before promoting a field into core.

## Decision model

TitanBases maintainers currently make final merge decisions. Significant design disagreements should be resolved in public issue/PR discussion with rationale recorded in the repository.

If independent adoption and maintainership materially expand, the governance model should be revisited toward broader maintainer representation.

## Releases

A release should include:

- versioned specification text;
- matching JSON Schema;
- passing reference-validator CI;
- changelog entry;
- examples compatible with the released schema.

## Trademark and naming

"AI Workload Migration Manifest" and "AWMM" identify this specification. Conformance claims must identify the version and level, for example:

`AWMM 0.1.0 Migration-Ready`

Use of the name must not imply endorsement by TitanBases or by any external protocol project.
