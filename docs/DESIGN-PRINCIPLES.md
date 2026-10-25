# Design Principles

## 1. Migration is not a synonym for model switching

An AI workload can depend on instructions, tools, memory, state, workflows, identity, permissions, policies, retrieval data, observability and evaluation assets. AWMM models migration at that workload boundary.

## 2. Declare semantics, do not infer them

AWMM avoids heuristics such as treating any file named `memory.json` as portable memory or assuming an MCP integration is migration-ready because both runtimes speak MCP. The manifest author declares portability and migration treatment explicitly.

## 3. Reference existing formats instead of absorbing them

If an implementation uses Agent Skills, ALF, AAIF, MCP, A2A or another format, AWMM references that artifact or dependency. AWMM does not fork those specifications.

## 4. Evidence is separate from intent

A plan can declare a target acceptance gate before migration. A completed migration can attach a result and evidence later. This separation lets the same manifest evolve from planning to validation without pretending planned outcomes have already occurred.

## 5. Required assets fail closed

A required asset with unknown or unsupported portability prevents Migration-Ready conformance. The burden is on the migration plan to resolve the gap, not on the validator to assume success.

## 6. Secrets stay outside the manifest

Migration metadata may identify a secret store or opaque secret reference. It must not become a secret transport.

## 7. Behavioral equivalence is a measured claim

Changing a model, prompt encoding, tool runtime or memory implementation can alter behavior even if configuration imports successfully. AWMM therefore treats behavioral acceptance as an explicit gate rather than a property inferred from syntax.

## 8. Rollback is part of migration design

Rollback is not an afterthought. Migration-Ready workloads must state how authority returns to the source or another known-good state.

## 9. Extensions are namespaced

Vendor-specific metadata belongs under `extensions`. Core AWMM fields remain portable and reviewable.

## 10. Draft status is explicit

v0.1 is intentionally a draft. The repository should earn adoption through precise semantics, useful examples and implementation feedback rather than claiming standard status by declaration.
