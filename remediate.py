import csv
from datetime import date

# Entitlements to revoke based on certification decisions
REVOCATIONS = {
    ("F007", "ProcureApp",              "Create PO Requisition"),
    ("P005", "FinanceERP",              "Approve Payment"),
    ("I005", "Keycloak Admin Console",  "Manage Roles & Permissions"),
    ("H003", "FinanceERP",              "Approve Payment"),
}

before_rows = []
with open("user_entitlements.csv") as f:
    before_rows = list(csv.DictReader(f))

after_rows   = []
revoked_rows = []

for row in before_rows:
    key = (row["UserID"], row["System"], row["Entitlement"])
    if key in REVOCATIONS:
        revoked_rows.append(row)
    else:
        after_rows.append(row)

# Write clean after-state
fieldnames = ["UserID","FullName","Department","RoleID","System","Entitlement","AssignedDate","LastUsedDate"]
with open("user_entitlements_after.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(after_rows)

# Write remediation log
today = date.today().isoformat()
log_fields = ["RemediationID","Date","UserID","FullName","Department","System","Entitlement","CertificationRef","RevokedBy","Justification"]
log_rows = [
    {"RemediationID":"REM-001","Date":today,"UserID":"F007","FullName":"Maria Santos",  "Department":"Finance",      "System":"ProcureApp",             "Entitlement":"Create PO Requisition",     "CertificationRef":"CERT-014","RevokedBy":"James Okafor",    "Justification":"Outside Finance Analyst baseline. Informal cross-dept access never approved."},
    {"RemediationID":"REM-002","Date":today,"UserID":"P005","FullName":"Olivia Martin",  "Department":"Procurement",  "System":"FinanceERP",             "Entitlement":"Approve Payment",           "CertificationRef":"CERT-028","RevokedBy":"Sarah Chen",      "Justification":"Critical SoD-01 violation. Vendor Manager + Approve Payment = fraud loop."},
    {"RemediationID":"REM-003","Date":today,"UserID":"I005","FullName":"Grace Park",     "Department":"IT",           "System":"Keycloak Admin Console", "Entitlement":"Manage Roles & Permissions","CertificationRef":"CERT-047","RevokedBy":"Jennifer Wu",     "Justification":"IT Support role has no IAM admin business need. Temporary access never removed."},
    {"RemediationID":"REM-004","Date":today,"UserID":"H003","FullName":"Mei Lin",        "Department":"HR",           "System":"FinanceERP",             "Entitlement":"Approve Payment",           "CertificationRef":"CERT-062","RevokedBy":"Patricia Lemoine","Justification":"SoD-04 violation. HR Coordinator outside Finance dept. No business justification."},
]

with open("remediation_log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=log_fields)
    w.writeheader()
    w.writerows(log_rows)

print(f"\n{'='*60}")
print(f"REMEDIATION EXECUTION REPORT — {today}")
print(f"{'='*60}")
print(f"\nEntitlements before remediation : {len(before_rows)}")
print(f"Entitlements revoked            : {len(revoked_rows)}")
print(f"Entitlements after remediation  : {len(after_rows)}")
print(f"\nRevocations executed:")
for r in log_rows:
    print(f"  [{r['RemediationID']}] {r['FullName']} ({r['Department']})")
    print(f"    {r['System']}:{r['Entitlement']}")
    print(f"    Revoked by: {r['RevokedBy']}")
    print()
print(f"Output files: user_entitlements_after.csv, remediation_log.csv")
print(f"{'='*60}\n")
