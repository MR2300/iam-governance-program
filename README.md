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

## Screenshots

**Keycloak — 26 users provisioned in the northfield realm**
![Users](screenshots/project1_users.png)

**Keycloak — 16 realm roles across 4 departments**
![Realm Roles](screenshots/project1_realm%20roles.png)

**Keycloak — 4 department groups**
![Groups](screenshots/project1_groups.png)

**SoD violation detection — 9 violations found across 5 users**
![SoD Violations](screenshots/project1_SoD%20violation.png)

**Access certification campaign — 69 entitlements reviewed, 5 revoked**
![Certification Summary](screenshots/project1_certification%20summary.png)

**Remediation execution — 4 entitlements revoked with audit trail**
![Remediation](screenshots/project1_remediation.png)

## Repo Structure

| File | Description |
|---|---|
| `org-design.md` | Department structure, role hierarchy, entitlement catalog |
| `roles.csv` | 16 role definitions across 4 departments |
| `users.csv` | 26 simulated users |
| `rbac_matrix.csv` | Least-privilege baseline: role → system → entitlement |
| `user_entitlements.csv` | Before state — actual access with violations |
| `user_entitlements_after.csv` | After state — clean post-remediation access |
| `sod_rules.csv` | 4 SoD rules with risk levels |
| `sod_violations.csv` | 9 violations detected |
| `access_certification.csv` | Full certification campaign — 69 entitlements reviewed |
| `remediation_log.csv` | 4 revocations with reviewer and justification |
| `control_mapping.csv` | 14 controls mapped to ISO 27001 / NIST 800-53 |
| `final_report.md` | Complete before/after report |
| `keycloak/docker-compose.yml` | Keycloak + PostgreSQL deployment |
| `keycloak/northfield-realm.json` | Realm definition — roles, groups, 26 users |
| `detect_violations.py` | SoD detection script |
| `remediate.py` | Remediation execution script |
| `certification_summary.py` | Certification campaign summary |

## Why this exists

Most IAM portfolio projects stop at "I deployed an IdP." This one simulates the governance *program* around it: defining least privilege, catching where reality drifts from policy, and producing the artifacts (matrices, certification reports, control mappings) that a GRC/IAM analyst actually produces in the role.
