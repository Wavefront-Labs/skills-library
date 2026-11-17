---
id: business-finance.property-management.property-management-software.tenancy-setup-ledgers-work-orders-and-owner-reports
name: tenancy-setup-ledgers-work-orders-and-owner-reports
category: business-finance
field: property-management
product: property-management-software
tags: [property-management, property-management-software, yardi, yardi-voyager, yardi-breeze, appfolio, buildium, rentmanager, mri-software, entrata, propertyware, doorloop, arthur-online, fixflo, tenancy-setup, lease-setup, recurring-charges, rent-roll, tenant-ledger, maintenance-tickets, work-orders, owner-portal, owner-statements, month-end-close, data-migration]
level: practitioner
status: draft
description: "Work in property-management platforms (Yardi, AppFolio, Buildium class): tenancy setup so charges post right, clean ledgers, work orders, and month-end close into owner reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tenancy setup, ledgers, work orders and owner reports

**Goal:** the system produces correct charges, ledgers and owner statements without
spreadsheet patching. Concepts below apply across Yardi (Voyager/Breeze), AppFolio,
Buildium, Rent Manager, MRI, Entrata and UK tools like Arthur Online; screen names and
exact workflows differ by product and version, so check your vendor's help centre for
the precise clicks.

## 1. Setup order matters (top down)
1. **Chart of accounts and bank accounts** (operating, trust/client, deposit/escrow per
   jurisdiction) before anything posts. Map GL accounts for rent, late fees, deposits
   (a liability, not income), service charges, maintenance expense, management fees.
2. **Owners / portfolios**: legal entity, ownership %, payment details, reserve/float
   amount, management fee terms, tax IDs where needed.
3. **Properties and units**: address, unit type, area (sqft/m²; needed for
   apportionments), market rent, amenities.
4. **Tenancies/leases**: tenants (all named occupants and guarantors), start/end dates,
   **recurring charges** with start dates and frequencies, deposit received, escalation
   schedule, late-fee rules, payment methods (enable tenant portal/ACH/direct debit).
Get the recurring charges right: most ledger problems trace back to a wrong start date,
a missing proration, or a charge set to the wrong GL account.

## 2. Daily ledger hygiene
- Receipts posted against specific open charges; avoid "prepayment" piles unless real.
- Bank feeds/auto-reconciliation help but still need human review of unmatched lines.
- Corrections by **reversing entries**, never by deleting history (keeps the audit trail).
- Move-outs: final charges, deposit disposition with itemised deductions, close the
  tenancy so recurring charges stop. Forgetting to end recurring charges is a classic error.
- Late fees: verify automated rules match local law (caps, grace periods) before
  enabling auto-post.

## 3. Work orders / maintenance tickets
- Tenants submit via portal with photos; set categories and priority (emergency /
  urgent / routine) with target response times.
- Assign to vendors stored with insurance/licence expiry dates (block assignment when
  expired), not-to-exceed amounts, and owner approval thresholds.
- Track status to completion; attach the invoice and completion photos; the bill posts
  to the right property and GL account and feeds the owner statement.
- Report weekly: open tickets by age, average time to close, repeat issues per unit.

## 4. Month-end close
A typical checklist (adapt to your firm's procedures):
1. All receipts and bills for the period posted; bank and trust accounts reconciled.
2. Late fees and recurring charges for the new period checked before release.
3. Management fees calculated by the system and reviewed.
4. Owner reserves topped up/held; owner distributions calculated and paid.
5. Owner statements generated and published to the owner portal.
6. Period locked so back-dated edits can't change reported numbers.

## 5. Reports you'll live in
Rent roll; delinquency/aged receivables; vacancy and lease expirations; work-order
ageing; owner statement; trust/client account reconciliation; 1099 (US) or tax summaries
for owners and vendors at year end. Save filtered versions as memorised/custom reports.

## 6. Migrations between systems
Migrate opening balances by tenant and owner at a cut-off date rather than years of
transaction history (unless required). Run old and new in parallel for one month-end
and reconcile ledgers line by line before switching off the old one.

## Gotchas
- Deposits posted as income.
- Recurring charges not prorated for mid-month starts.
- Shared logins: lose the audit trail; give each user their own role-based account.
- Integrations (screening, payments, accounting sync) failing silently; check sync logs.

## Verify
- [ ] GL mapping reviewed by an accountant before go-live.
- [ ] Every active tenancy's recurring charges match its lease abstract.
- [ ] Bank and trust accounts reconcile each month with zero unexplained items.
- [ ] Work orders show vendor, cost, completion evidence and owner approval where needed.
- [ ] Period locked after owner statements are published.
