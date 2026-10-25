# Ecosystem Mapping

AWMM is designed as a **migration-contract layer** above protocols and artifact formats.

## Model Context Protocol (MCP)

MCP standardizes how AI applications connect to tools, resources and prompts.

AWMM may record an MCP server as a dependency and may mark its binding as retained, rebound, replaced or transformed. Speaking MCP does not by itself prove that tool semantics, authorization, side effects or behavior are equivalent after migration.

**Typical AWMM mapping**

- dependency category: `protocol` or `tool`
- protocol: `MCP`
- migration treatment: `retain`, `rebind`, or `replace`
- acceptance domain: `tool-contract`, `identity-permissions`, `security`

## Agent2Agent (A2A)

A2A standardizes communication and collaboration between independent agents.

AWMM may record A2A endpoints or capabilities as dependencies. A2A interoperability does not require access to another agent's internal state, memory or tools, so AWMM does not interpret A2A connectivity as workload portability.

**Typical AWMM mapping**

- dependency category: `protocol`
- protocol: `A2A`
- migration treatment: `retain`, `rebind`, or `replace`
- acceptance domain: `functional`, `security`, `reliability`

## Agent Skills

Agent Skills packages reusable instructions and supporting resources around a `SKILL.md` entrypoint.

AWMM may treat a skills directory as an asset. A skill can be portable while the surrounding runtime permissions, tools, memory and behavior remain non-portable.

**Typical AWMM mapping**

- asset category: `skills`
- format: `Agent Skills`
- portability: often `portable` when the target runtime supports the same skill contract

## Agent Life Format (ALF)

ALF focuses on portable durable agent state, including memory and other agent-state layers.

AWMM does not duplicate ALF's serialization model. If ALF is used, an AWMM memory/state asset can reference an ALF artifact and describe how that artifact participates in the larger migration contract.

**Typical AWMM mapping**

- asset category: `memory`, `identity`, or `state`
- format: `ALF`
- artifact reference: external `.alf` package
- acceptance domain: `memory-integrity`, `state-continuity`

## Autonomous Agent Interchange Format (AAIF)

AAIF is a draft format for portable agent definitions and related state/configuration.

AWMM does not define a competing universal agent document. An implementation using AAIF may reference the AAIF artifact as one or more AWMM assets while AWMM captures migration risk, acceptance, evidence and rollback.

## Runtime-specific live migration systems

Systems that transfer runtime execution state, caches, checkpoints or runtime-specific memory solve a different layer of the problem. AWMM can record the artifact, mechanism, transformation and resulting evidence without prescribing the transport.

## Boundary summary

```text
Agent/tool communication     -> MCP
Agent/agent communication    -> A2A
Reusable procedural package  -> Agent Skills
Durable agent state format   -> ALF (when used)
Portable agent definition    -> AAIF (when used)
Runtime execution transfer   -> implementation-specific

Migration contract:
scope + mappings + transformations + risks
+ baselines + acceptance + evidence + rollback
                            -> AWMM
```

AWMM conformance never implies conformance with any external specification. External names and trademarks belong to their respective projects and owners.
