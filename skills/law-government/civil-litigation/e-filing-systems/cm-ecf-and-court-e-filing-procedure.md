---
id: law-government.civil-litigation.e-filing-systems.cm-ecf-and-court-e-filing-procedure
name: cm-ecf-and-court-e-filing-procedure
category: law-government
field: civil-litigation
product: e-filing-systems
tags: [e-filing-systems, civil-litigation, e-filing, efiling, electronic-filing, cm-ecf, pacer, nextgen-cm-ecf, state-e-filing, tyler-odyssey, file-and-serve, ce-file, caselines, nef, notice-of-electronic-filing, electronic-service, docket, docket-monitoring, docketing, deadline-calculation, rule-6, pdf-a, text-searchable-pdf, redaction, rule-5-2, sealed-filing, filing-event, courtlistener, recap, court-fees, filing-deadline]
level: practitioner
status: docs-checked
description: "Filing and retrieving court documents through CM/ECF, PACER and state or national e-filing portals: account setup, PDF requirements, events, service, docket monitoring and deadline capture."
sources: ["https://www.law.cornell.edu/rules/frcp/rule_5.2", "https://www.law.cornell.edu/rules/frcp/rule_6", "https://pacer.uscourts.gov/pacer-pricing-how-fees-work"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CM/ECF and court e-filing procedure

**Goal:** file the right document, in the right form, under the right event, on time —
and never miss a deadline triggered by someone else's filing. US federal courts use
**CM/ECF** (with **PACER** for access); state courts and courts abroad use their own portals.
Each court's ECF procedures and local rules govern.

## 1. Accounts and setup
- US federal: one **PACER** account, then request e-filing privileges from each court.
  Pro hac vice admission must be granted before filing in some courts.
- Your login is your signature (`/s/ Name`) — never share credentials; staff file under
  their own credentials where permitted or under the attorney's with authorisation per
  local rules.
- Keep email addresses for **Notices of Electronic Filing (NEFs)** current and monitored by
  more than one person.

## 2. Preparing the PDF
- **Text-searchable PDF** converted from the word processor, not scanned, wherever possible.
- Size limits per file (vary by court); split large exhibits into separately labelled
  attachments.
- Strip metadata; embed fonts; some courts require PDF/A.
- **Privacy redactions** (US: FRCP 5.2) — only last four digits of SSN and financial account
  numbers, birth year only, minors' initials. The filer is responsible.
- Sealed or restricted documents follow a separate procedure — usually a motion for leave
  to seal first. Filing a sealed document publicly by mistake can be irreversible.

## 3. Filing
1. Choose the case and the **event** (motion type, response, notice). The event drives
   the docket text and sometimes triggers automatic deadlines — choose the most specific.
2. Link to related entries (a response links to the motion).
3. Upload main document then attachments with descriptive labels ("Exhibit 3 – Supply
   Agreement dated 2021-04-12").
4. Review docket text before submitting; pay fees online where applicable.
5. Save the **NEF/receipt** — proof of filing time and of service on registered users.

## 4. Service
Registered users are served by the NEF. Parties not registered (pro se litigants,
new parties) need service by other means and a certificate of service. Check the service rules for initial process
(summons and complaint); do not assume an ECF notice serves a new party.

## 5. Deadlines and time
- Filing time is the court's local time; most courts accept filings up to midnight, but
  some judges or event types differ — check.
- Compute deadlines under the governing rule (US federal: FRCP 6 — count every day,
  exclude the trigger day, include the last day unless it's a weekend/holiday; service by
  electronic means no longer adds three days).
- **Docket every NEF** into a calendar system the day it arrives, with a second person
  checking computed deadlines. Court-ordered deadlines override rule defaults.

## 6. Monitoring and retrieval
- PACER charges $0.10 per page, capped at $3 per document, and waives fees if you spend $30 or less in a
  calendar quarter (check the current schedule). A party who receives a Notice of Electronic Filing gets one free
  copy of the document; download it then.
- Free sources: RECAP/CourtListener archives documents others purchased.
- Set alerts for cases you're watching but not a party to.

## Gotchas
- Wrong event or wrong case number — file a notice of corrected filing promptly and follow
  the clerk's instructions; don't just re-file silently.
- Hyperlinks to exhibits must work; broken internal links frustrate chambers.
- Portal outages: courts have rules for technical failures — document the outage and
  file as soon as possible, with a motion if needed.

## Verify
- [ ] Filer is admitted and registered in this court.
- [ ] PDF is searchable, redacted per privacy rules and within size limits.
- [ ] Correct event chosen and linked; NEF saved.
- [ ] Every new NEF docketed with deadlines double-checked.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States federal courts (CM/ECF, PACER, FRCP 5.2 and 6).
- Confirmed against official sources (see `sources`): FRCP 5.2(a) redaction limits (last four digits of SSN, taxpayer ID and financial account numbers, year of birth, minor initials); FRCP 6(a)(1) counting rules; FRCP 6(d) no longer adds three days for electronic service (2016 amendment); PACER fee schedule ($0.10 per page, $3 per-document cap, $30 quarterly waiver, one free copy per notice).
- Corrected or removed: Removed the Tyler Odyssey, CE-File and NextGen single-sign-on claims and the "never served via ECF" absolute (not confirmed on a free official page); the summons-service sentence now tells the reader to check the service rules. The "most courts accept filings up to midnight" statement is retained only as a prompt to check local rules.

Method: documentation only; no commands were run.
