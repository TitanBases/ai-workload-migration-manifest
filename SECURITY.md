# Security Policy and Threat Model

## Scope

AWMM manifests are metadata, but they can expose sensitive architecture information. Treat them as security-sensitive configuration.

## Absolute rule: no secret material

An AWMM manifest MUST NOT contain raw:

- API keys;
- passwords;
- OAuth access or refresh tokens;
- private keys;
- session cookies;
- database credentials;
- cloud access credentials;
- signing secrets;
- equivalent authentication material.

Use an opaque reference instead, for example:

```json
{
  "id": "runtime-secrets",
  "category": "secrets",
  "required": true,
  "portability": "rebind-required",
  "sourceRef": "secret-store://source/research-agent",
  "targetRef": "secret-store://target/research-agent",
  "sensitivity": "restricted"
}
```

The reference validator performs best-effort checks for obvious secret patterns. That is defense in depth, not a substitute for secret scanning or repository controls.

## Threats considered

### Architecture disclosure

Environment identifiers, model choices, identity providers and tool dependencies may reveal system topology.

**Control:** minimize manifest content, use opaque references, apply repository access controls for non-public workloads.

### Secret exfiltration through migration packaging

Teams may be tempted to export credentials together with agent state.

**Control:** AWMM carries references only. Secret transfer and rotation belong to a dedicated secret-management process.

### Evidence tampering

A migration could claim success while linking mutable or fabricated evidence.

**Control:** prefer immutable evidence, record SHA-256 digests where practical, preserve provenance, and use independent review for high-criticality workloads.

### Permission expansion

Target runtime roles may accidentally gain broader authority.

**Control:** model permissions as an asset, use explicit rebinding, and create blocking identity/permission acceptance gates.

### Behavioral drift

Equivalent configuration does not guarantee equivalent behavior across models or runtimes.

**Control:** record approved baselines and blocking behavioral evaluation gates.

### Rollback failure

A migration can pass functional tests but leave no safe return path.

**Control:** require rollback planning for Migration-Ready conformance and attach rollback evidence when claiming validated rollback.

### Extension abuse

Vendor-specific extensions could be used to smuggle secret values or redefine core semantics.

**Control:** extensions cannot redefine core AWMM semantics and remain subject to the no-secrets rule.

## Reporting a vulnerability

For security-sensitive findings, do not publish exploit details in a public issue. Contact TitanBases through the security contact published on the TitanBases website and include the repository name, affected version, impact and a minimal reproduction when safe to do so.

For non-sensitive specification defects, open a normal GitHub issue.
