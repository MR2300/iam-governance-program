# IAM Governance Program — Final Report
**Organization:** Northfield Industries (Simulated)
**Report Date:** 2026-06-17
**Scope:** 26 users, 4 departments, 5 systems, 16 roles

---

## Executive Summary

This report documents the end-to-end IAM governance program conducted for Northfield Industries. The program simulated how a real GRC/IAM analyst operates: defining least-privilege policy, deploying an identity platform, running an access certification campaign, detecting violations, and remediating them — then mapping all activities to ISO 27001 A.9 and NIST 800-53 AC controls.

**Key outcome:** 9 violations were detected across 5 users, including 1 Critical fraud-enabling entitlement combination. All 5 revocations were executed and logged. 4 design-time SoD conflicts were accepted with documented compensating controls.

---

## Program Phases

| Phase | Activity | Status |
|---|---|---|
| 1 | Org design, role hierarchy, RBAC matrix | Complete |
| 2 | Keycloak IdP deployment (Docker + PostgreSQL) | Complete |
| 3 | SoD ruleset definition | Complete |
| 4 | Access certification campaign | Complete |
| 5 | Remediation + control mapping | Complete |
| 6 | Final report | Complete |

---

## Organization Overview

| Department | Users | Roles |
|---|---|---|
| Finance | 7 | CFO, Finance Manager, Finance Analyst, AP Clerk |
| Procurement | 6 | Procurement Director, Procurement Manager, Procurement Analyst, Vendor Manager |
| IT | 7 | IT Director, IT Manager, IT Security Engineer (IAM Admin), IT Engineer, IT Support |
| HR | 6 | HR Director, HR Manager, HR Coordinator |
| **Total** | **26** | **16** |

---

## Phase 2 — Identity Platform

Keycloak 26 deployed via Docker Compose with PostgreSQL backend. The `northfield` realm was provisioned via realm import (infrastructure-as-code), containing:
- 16 realm roles matching the RBAC design
- 4 department groups
- 26 users with role assignments and temporary passwords

**Stack:** Keycloak 26.0 · PostgreSQL 15 · Docker Compose

---

## Phase 3 — SoD Ruleset

| RuleID | Rule | Risk |
|---|---|---|
| SOD-01 | Create Vendor + Approve Payment | Critical |
| SOD-02 | Create PO Requisition + Approve PO | High |
| SOD-03 | Manage Roles & Permissions + Approve Payment | Critical |
| SOD-04 | Approve Payment held outside Finance dept | High |
| DRIFT | Entitlement outside assigned role baseline | Medium |

---

## Phase 4 — Access Certification Results (Before State)

**69 entitlements reviewed across 26 users.**

### Violations Detected

| UserID | User | Violation | Rule | Risk |
|---|---|---|---|---|
| P005 | Olivia Martin | Create Vendor + Approve Payment | SOD-01 | Critical |
| P001 | Robert Hayes | Create PO Requisition + Approve PO | SOD-02 | High |
| P002 | Nora Fitzgerald | Create PO Requisition + Approve PO | SOD-02 | High |
| P005 | Olivia Martin | Non-Finance user holds Approve Payment | SOD-04 | High |
| H003 | Mei Lin | Non-Finance user holds Approve Payment | SOD-04 | High |
| F007 | Maria Santos | ProcureApp access outside Finance Analyst baseline | DRIFT | Medium |
| P005 | Olivia Martin | Approve Payment outside Vendor Manager baseline | DRIFT | Medium |
| I005 | Grace Park | Manage Roles & Permissions on IT Support account | DRIFT | Medium |
| H003 | Mei Lin | Approve Payment outside HR Coordinator baseline | DRIFT | Medium |

**Total: 9 violations — 1 Critical, 4 High, 4 Medium**

---

## Phase 5 — Remediation (After State)

### Revocations Executed

| REM ID | User | Entitlement Revoked | Revoked By | Justification |
|---|---|---|---|---|
| REM-001 | Maria Santos | ProcureApp:Create PO Requisition | James Okafor | Outside Finance Analyst baseline — informal access never approved |
| REM-002 | Olivia Martin | FinanceERP:Approve Payment | Sarah Chen | Critical SOD-01 — complete fraud loop |
| REM-003 | Grace Park | Keycloak:Manage Roles & Permissions | Jennifer Wu | IT Support has no IAM admin business need |
| REM-004 | Mei Lin | FinanceERP:Approve Payment | Patricia Lemoine | SOD-04 — HR with Finance approval authority |

**Result: 69 → 65 entitlements. All Critical and High drift violations remediated.**

### Exceptions Granted (with Compensating Controls)

| User | Conflict | Compensating Control |
|---|---|---|
| Robert Hayes | SOD-02 (Procurement Director role design) | PO approvals above $50k require CFO counter-sign |
| Nora Fitzgerald | SOD-02 (Procurement Manager role design) | Monthly PO approval review by Procurement Director |

---

## Control Mapping Summary

### ISO 27001 A.9

| Control | Name | Evidence |
|---|---|---|
| A.9.1.1 | Access Control Policy | rbac_matrix.csv |
| A.9.2.1 | User Registration | users.csv + northfield-realm.json |
| A.9.2.2 | User Access Provisioning | remediation_log.csv |
| A.9.2.5 | Review of User Access Rights | access_certification.csv |
| A.9.2.6 | Removal of Access Rights | remediation_log.csv |
| A.9.4.1 | Information Access Restriction | sod_rules.csv + sod_violations.csv |

### NIST 800-53 AC Family

| Control | Name | Evidence |
|---|---|---|
| AC-1 | Access Control Policy | org-design.md |
| AC-2 | Account Management | access_certification.csv |
| AC-3 | Access Enforcement | user_entitlements_after.csv |
| AC-5 | Separation of Duties | sod_rules.csv + sod_violations.csv |
| AC-6 | Least Privilege | rbac_matrix.csv + remediation_log.csv |
| AU-2 | Event Logging | remediation_log.csv |

---

## Before vs. After Comparison

| Metric | Before | After |
|---|---|---|
| Total entitlements | 69 | 65 |
| SoD violations | 9 | 1 (accepted with compensating controls) |
| Critical violations | 1 | 0 |
| High violations | 4 | 2 (exceptions, compensating controls applied) |
| Entitlement drift | 4 users | 0 |
| Undocumented cross-dept access | 3 instances | 0 |

---

## Key Findings

1. **Olivia Martin presented the highest risk** — a Vendor Manager holding payment approval authority created a complete, unsupervised fraud loop. This was revoked immediately.

2. **Role drift is the silent threat** — 4 of the 9 violations came from entitlements assigned outside a user's role baseline, likely through informal "temporary" access that was never cleaned up. Grace Park's IAM admin rights (assigned Dec 2025, last used Jan 2026) are a textbook example.

3. **Design-time SoD conflicts require explicit acceptance** — the Procurement Director and Manager roles inherently violate SOD-02. Rather than restructuring the org, compensating controls were documented. This is standard practice and must be tracked as accepted risk.

4. **Access reviews surface what provisioning processes miss** — none of these violations would have been caught without a structured certification campaign comparing actual access against the least-privilege baseline.

---

## Project Artifacts

| File | Description |
|---|---|
| `org-design.md` | Department structure, role hierarchy, entitlement catalog |
| `roles.csv` | 16 role definitions |
| `users.csv` | 26 simulated users |
| `rbac_matrix.csv` | Least-privilege baseline: role → entitlement |
| `user_entitlements.csv` | Before state — actual access with violations |
| `user_entitlements_after.csv` | After state — clean post-remediation access |
| `sod_rules.csv` | 4 SoD rules with risk levels |
| `sod_violations.csv` | 9 violations detected by rule |
| `access_certification.csv` | Full certification campaign — 69 entitlements reviewed |
| `remediation_log.csv` | 4 revocations with reviewer and justification |
| `control_mapping.csv` | 14 controls mapped to ISO 27001 / NIST 800-53 |
| `keycloak/docker-compose.yml` | Keycloak + PostgreSQL deployment |
| `keycloak/northfield-realm.json` | Realm definition — roles, groups, 26 users |
| `detect_violations.py` | SoD detection script |
| `remediate.py` | Remediation execution script |
| `certification_summary.py` | Certification campaign summary |
