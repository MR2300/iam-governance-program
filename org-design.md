# Org Design — Simulated Organization

## Company Profile

A fictional 26-person mid-market company ("Northfield Industries") with four departments. Small enough to fully document by hand, large enough that access governance problems emerge naturally — role drift, cross-department residual access, and orphaned admin rights.

| Department  | Headcount | Director-level | Manager-level | IC-level |
|-------------|-----------|-----------------|---------------|----------|
| Finance     | 7         | 1 (CFO)         | 1             | 5        |
| Procurement | 6         | 1               | 1             | 4        |
| IT          | 7         | 1               | 1             | 5        |
| HR          | 6         | 1               | 2             | 3        |
| **Total**   | **26**    |                 |               |          |

## Systems in Scope

| System                  | Purpose                                  |
|-------------------------|-------------------------------------------|
| FinanceERP               | General ledger, accounts payable, payment approval |
| ProcureApp               | Purchase requisitions, vendor master data, PO approval |
| HRIS                     | Employee records, payroll changes |
| ITSM                     | IT ticketing and change management |
| Keycloak Admin Console   | Identity platform administration (users, groups, roles) |

## Role Hierarchy & Least-Privilege Design Philosophy

Each department has 3–4 role levels (IC → Manager → Director), and each level only receives the entitlements it strictly needs to perform its function — approval rights are reserved for Manager level and above, and administrative rights are reserved for a single named role per system rather than granted broadly.

Full role definitions: see `data/roles.csv`.
Full role → entitlement mapping: see `data/rbac_matrix.csv`.

## Entitlement Catalog

| System    | Entitlement                  | Sensitivity |
|-----------|-------------------------------|--------------|
| FinanceERP | View Financial Reports        | Low |
| FinanceERP | Process AP Transactions       | Medium |
| FinanceERP | Approve Payment                | High |
| ProcureApp | View Vendor/PO Data            | Low |
| ProcureApp | Create PO Requisition          | Medium |
| ProcureApp | Create Vendor                  | High |
| ProcureApp | Approve PO                     | High |
| HRIS       | View Employee Records          | Low |
| HRIS       | Edit Employee Records          | Medium |
| HRIS       | Approve Payroll Change         | High |
| HRIS       | Admin HRIS                     | Critical |
| ITSM       | View Tickets                    | Low |
| ITSM       | Manage Tickets                  | Medium |
| ITSM       | Approve Change Request          | High |
| Keycloak Admin Console | View Realm        | Low |
| Keycloak Admin Console | Manage Users/Groups | High |
| Keycloak Admin Console | Manage Roles & Permissions | Critical |

## SoD-Sensitive Entitlement Pairs (identified at design time)

These pairs are flagged now so the Phase 3 SoD ruleset and Phase 4 access review have something concrete to enforce/detect:

1. **ProcureApp: Create Vendor** + **FinanceERP: Approve Payment** — a single person could create a fictitious vendor and approve payment to it.
2. **ProcureApp: Create PO Requisition** + **ProcureApp: Approve PO** — self-approval of purchase orders.
3. **Keycloak Admin Console: Manage Roles & Permissions** + **FinanceERP: Approve Payment** — identity administration combined with financial approval authority (a person could grant themselves access and approve their own transaction).

A fourth, less formal policy: no Finance entitlement should be held by anyone outside the Finance department without a documented exception — this is the kind of "soft" rule that real orgs often violate informally (e.g., covering for a colleague on leave) and that access reviews are designed to surface.

## Next Steps

Phase 2 will stand up Keycloak with these departments as groups and these 26 users with their *intended* (baseline) entitlements from `rbac_matrix.csv`. Phase 4's access review will compare `user_entitlements.csv` (actual current access) against this baseline to find drift.
