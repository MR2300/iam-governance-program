# IAM Governance & Access Review Program (Simulated)

A simulated enterprise IAM governance program for a fictional 26-person, 4-department organization — built end-to-end to mirror how a real access governance function operates, not just to deploy an IdP.

**Scope:** org design → RBAC → identity platform deployment (Keycloak) → segregation-of-duties (SoD) enforcement → access certification campaign → remediation → control mapping (ISO 27001 A.9 / NIST 800-53 AC).

## Project Phases

- [x] **Phase 1 — Org design & RBAC matrix** (this commit)
- [x] Phase 2 — Keycloak deployment (IdP, realms, groups, users)
- [x] Phase 3 — SoD ruleset definition
- [x] Phase 4 — Simulated access certification campaign (entitlement export, violation detection)
- [x] Phase 5 — Remediation & control mapping (ISO 27001 A.9, NIST 800-53 AC family)
- [x] Phase 6 — Before/after report, architecture diagram, final write-up

## Repo Structure

```
docs/
  org-design.md            Department structure, role hierarchy, entitlement catalog
data/
  roles.csv                16 role definitions across 4 departments
  users.csv                26 simulated users
  rbac_matrix.csv          Least-privilege baseline: role -> system -> entitlement
  user_entitlements.csv    Current actual access assignments (the "before" state)
```

## Why this exists

Most IAM portfolio projects stop at "I deployed an IdP." This one simulates the governance *program* around it: defining least privilege, catching where reality drifts from policy, and producing the artifacts (matrices, certification reports, control mappings) that a GRC/IAM analyst actually produces in the role.
