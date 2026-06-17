import csv
from collections import defaultdict

rows = []
with open("access_certification.csv") as f:
    rows = list(csv.DictReader(f))

reviewed   = [r for r in rows if r["ReviewerDecision"]]
revoked    = [r for r in reviewed if r["ReviewerDecision"] == "REVOKE"]
exceptions = [r for r in reviewed if r["ReviewerDecision"] == "EXCEPTION"]
certified  = [r for r in rows if not r["ReviewerDecision"]]

print(f"\n{'='*60}")
print(f"ACCESS CERTIFICATION SUMMARY — Northfield Industries")
print(f"Campaign Date: 2026-06-17")
print(f"{'='*60}")
print(f"\nTotal entitlements reviewed : {len(rows)}")
print(f"  Certified (no action)     : {len(certified)}")
print(f"  Revoked                   : {len(revoked)}")
print(f"  Exception granted         : {len(exceptions)}")

print(f"\n--- REVOCATIONS ({len(revoked)}) ---")
for r in revoked:
    print(f"  [{r['CertificationID']}] {r['FullName']} ({r['Department']})")
    print(f"    {r['System']}:{r['Entitlement']}")
    print(f"    Reviewed by: {r['ReviewedBy']} | Risk: {r['RiskLevel']}")
    print(f"    Reason: {r['RemediationAction'][:80]}...")
    print()

print(f"--- EXCEPTIONS GRANTED ({len(exceptions)}) ---")
for r in exceptions:
    print(f"  [{r['CertificationID']}] {r['FullName']} ({r['Department']})")
    print(f"    {r['System']}:{r['Entitlement']} — Rule: {r['ViolationRule']}")
    print(f"    {r['RemediationAction'][:80]}...")
    print()

print(f"{'='*60}")
print(f"Campaign status: COMPLETE")
print(f"Next step: Execute revocations in Keycloak, file exception records")
print(f"{'='*60}\n")
