import csv
from collections import defaultdict

# Load user entitlements
entitlements = defaultdict(list)
user_info = {}

with open("user_entitlements.csv") as f:
    for row in csv.DictReader(f):
        uid = row["UserID"]
        entitlements[uid].append((row["System"], row["Entitlement"]))
        user_info[uid] = (row["FullName"], row["Department"])

# Load baseline (rbac_matrix) — what each role SHOULD have
baseline = defaultdict(set)
with open("rbac_matrix.csv") as f:
    for row in csv.DictReader(f):
        baseline[row["RoleID"]].add((row["System"], row["Entitlement"]))

# Load users to get RoleID
users = {}
with open("users.csv") as f:
    for row in csv.DictReader(f):
        users[row["UserID"]] = row["RoleID"]

violations = []

def has(uid, system, entitlement):
    return (system, entitlement) in entitlements[uid]

for uid, ents in entitlements.items():
    name, dept = user_info[uid]
    ent_set = set(ents)

    # SOD-01: Create Vendor + Approve Payment
    if has(uid, "ProcureApp", "Create Vendor") and has(uid, "FinanceERP", "Approve Payment"):
        violations.append({
            "UserID": uid, "FullName": name, "Department": dept,
            "RuleID": "SOD-01", "RuleName": "Fictitious Vendor Fraud",
            "RiskLevel": "Critical",
            "Detail": "Has both ProcureApp:Create Vendor and FinanceERP:Approve Payment"
        })

    # SOD-02: Create PO Requisition + Approve PO
    if has(uid, "ProcureApp", "Create PO Requisition") and has(uid, "ProcureApp", "Approve PO"):
        violations.append({
            "UserID": uid, "FullName": name, "Department": dept,
            "RuleID": "SOD-02", "RuleName": "PO Self-Approval",
            "RiskLevel": "High",
            "Detail": "Has both ProcureApp:Create PO Requisition and ProcureApp:Approve PO"
        })

    # SOD-03: Manage Roles & Permissions + Approve Payment
    if has(uid, "Keycloak Admin Console", "Manage Roles & Permissions") and has(uid, "FinanceERP", "Approve Payment"):
        violations.append({
            "UserID": uid, "FullName": name, "Department": dept,
            "RuleID": "SOD-03", "RuleName": "IAM Admin + Financial Approval",
            "RiskLevel": "Critical",
            "Detail": "Has both Keycloak:Manage Roles & Permissions and FinanceERP:Approve Payment"
        })

    # SOD-04: Approve Payment outside Finance
    if has(uid, "FinanceERP", "Approve Payment") and dept != "Finance":
        violations.append({
            "UserID": uid, "FullName": name, "Department": dept,
            "RuleID": "SOD-04", "RuleName": "Cross-Department Finance Access",
            "RiskLevel": "High",
            "Detail": f"Non-Finance user ({dept}) holds FinanceERP:Approve Payment"
        })

    # Baseline drift — entitlements outside assigned role
    role_id = users.get(uid)
    if role_id:
        allowed = baseline[role_id]
        for sys, ent in ent_set:
            if (sys, ent) not in allowed:
                violations.append({
                    "UserID": uid, "FullName": name, "Department": dept,
                    "RuleID": "DRIFT", "RuleName": "Entitlement Outside Role Baseline",
                    "RiskLevel": "Medium",
                    "Detail": f"{sys}:{ent} not in baseline for {role_id}"
                })

# Write violations
with open("sod_violations.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["UserID","FullName","Department","RuleID","RuleName","RiskLevel","Detail"])
    writer.writeheader()
    writer.writerows(violations)

# Print summary
print(f"\n{'='*60}")
print(f"SoD VIOLATION REPORT — Northfield Industries")
print(f"{'='*60}")

by_rule = defaultdict(list)
for v in violations:
    by_rule[v["RuleID"]].append(v)

for rule_id in ["SOD-01", "SOD-02", "SOD-03", "SOD-04", "DRIFT"]:
    vs = by_rule.get(rule_id, [])
    if vs:
        print(f"\n[{rule_id}] {vs[0]['RuleName']} ({vs[0]['RiskLevel']}) — {len(vs)} violation(s)")
        for v in vs:
            print(f"  • {v['FullName']} ({v['Department']}): {v['Detail']}")

print(f"\n{'='*60}")
print(f"Total violations: {len(violations)}")
critical = sum(1 for v in violations if v["RiskLevel"] == "Critical")
high     = sum(1 for v in violations if v["RiskLevel"] == "High")
medium   = sum(1 for v in violations if v["RiskLevel"] == "Medium")
print(f"  Critical: {critical}  |  High: {high}  |  Medium: {medium}")
print(f"{'='*60}\n")
