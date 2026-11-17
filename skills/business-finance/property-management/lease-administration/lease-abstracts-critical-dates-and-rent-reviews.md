---
id: business-finance.property-management.lease-administration.lease-abstracts-critical-dates-and-rent-reviews
name: lease-abstracts-critical-dates-and-rent-reviews
category: business-finance
field: property-management
product: lease-administration
tags: [property-management, lease-administration, lease-abstract, lease-abstraction, critical-dates, critical-date-tracking, rent-review, rent-escalation, cpi-indexation, open-market-rent-review, break-option, break-clause, lease-renewal, option-to-renew, notice-periods, time-of-the-essence, lease-compliance, estoppel, ifrs-16, asc-842, lease-accounting, landlord, tenant]
level: practitioner
status: docs-checked
description: "Administer leases over their life: abstract each lease to a standard template, track critical dates with lead times, process rent reviews and escalations, and serve break and renewal notices validly."
sources: ["https://www.legislation.gov.uk/ukpga/Eliz2/2-3/56/part/II"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lease abstracts, critical dates and rent reviews

**Goal:** never miss a date that costs money (a break option, a review trigger, a
renewal window) and always bill or pay the rent the lease actually requires. Works from
either the landlord's or the occupier's side. **Lease wording governs**; this skill is
process, not legal advice. Involve a lawyer for notices and disputes.

## 1. Abstract every lease to one template
Fields (minimum): parties (exact legal entities), premises and measured area, term
start/expiry, rent and payment frequency/dates, **rent review** (dates, basis, upward-only?,
cap/collar, arbitration/expert), **escalations** (fixed steps or index: which index,
base month, lag), **break options** (who, dates, notice period, conditions such as
vacant possession and no arrears), **renewal options** and notice windows, service
charge/CAM provisions, repair obligations, alienation (assignment/subletting),
permitted use, insurance, guarantor, deposit/security, statutory renewal rights (e.g. in
England & Wales, whether the lease is inside or contracted out of the Landlord and Tenant
Act 1954 security of tenure).
Each field cites **clause number and page**, plus all deeds of variation, side letters
and licences, which often change the original terms.
Have a second person **QA every abstract** against the source; abstraction errors are
the root of most missed dates and billing errors.

## 2. Critical-date tracking
- Put every date in a system (lease admin module in Yardi/MRI/VTS, a dedicated tool,
  or at minimum a shared calendar plus a register) with **two people** notified.
- For each date record the **action date** (last day to act), not just the event date:
  e.g. break date 30 June 2027 with 6 months' notice → notice must be *received* by
  30 December 2026 (check the lease's service clause for deemed-receipt rules).
- Reminders at, for example, 12, 6, 3 and 1 months before the action date, plus a
  review of strategy (exercise or not) well before.
- Assume **time is of the essence** for breaks and options unless confirmed otherwise: a late notice can lose the right.

## 3. Rent reviews and escalations
- **Fixed steps**: diarise and bill automatically; verify the first invoice after each step.
- **Indexation** (CPI/RPI etc.): use the exact index series and base month named in
  the lease; apply caps/collars; show the calculation in the notice/invoice.
- **Open-market reviews**: compile comparable evidence, respect any trigger notices,
  negotiate, and if unresolved follow the lease's dispute mechanism (expert or arbitrator)
  within its time limits. Agree interim rent and any balancing payment with interest per lease.
- Record the outcome in a signed **rent review memorandum** filed with the lease.

## 4. Breaks and renewals: serving notices validly
- Serve exactly as the lease specifies: correct parties (current landlord/tenant after
  any transfers), correct address, method (recorded delivery, hand, sometimes email not
  allowed), content, and dates. Keep proof of service.
- Conditional breaks: meet every condition (rent paid to date, vacant possession,
  sometimes compliance with covenants). Small arrears have defeated break notices.
- Renewals: start negotiations early enough to leave room for statutory procedures
  where they apply.

## 5. Ongoing compliance and reporting
- Monthly: rent roll vs abstracts, arrears, upcoming 12-month critical dates report.
- Tenants: occupiers using IFRS 16 / ASC 842 need lease data (term, payments, options
  reasonably certain to be exercised) for right-of-use asset accounting; keep abstracts
  aligned with what finance books.
- Estoppel certificates / tenant confirmations on sale or refinance draw on the abstract;
  confirm against source documents before signing.

## Gotchas
- Abstracting only the original lease and missing a deed of variation.
- Tracking the event date instead of the notice deadline.
- Wrong legal entity named in a notice (group companies with similar names).
- Index rebasing or series discontinuation: check the lease's fallback wording.

## Verify
- [ ] Every lease abstracted, clause-referenced and QA'd by a second person.
- [ ] Critical dates stored as action deadlines with two notified owners.
- [ ] Each rent change has a calculation or memorandum on file.
- [ ] Notices served per the lease service clause, with proof retained.
- [ ] Rolling 12-month critical-dates report reviewed monthly.

## Checked

Date checked: 2026-10-25. Jurisdiction: England and Wales (Landlord and Tenant Act 1954); lease wording governs elsewhere.
Source read: legislation.gov.uk Landlord and Tenant Act 1954 Part II, "Security of Tenure for Business, Professional and other Tenants" (s.24(1): a tenancy to which Part II applies does not end unless terminated under the Part; s.23: business occupation). The skill's reference to checking whether a lease is inside or contracted out of the 1954 Act is therefore accurate; the contracting-out section (s.38A) was not read.
The break-notice date arithmetic is an illustrative example; the lease's own counting and service rules govern. Removed the unconfirmed claim about how courts treat late notices. Not legal advice.

Method: documentation only; no commands were run.
