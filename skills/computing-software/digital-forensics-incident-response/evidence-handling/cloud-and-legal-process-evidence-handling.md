---
id: computing-software.digital-forensics-incident-response.evidence-handling.cloud-and-legal-process-evidence-handling
name: cloud-and-legal-process-evidence-handling
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [cloud-forensics, legal-hold, preservation-letter, subpoena, search-warrant, ecpa, log-retention, provider-logs, aws-cloudtrail, m365-audit-log, legal-process, data-custodian, dfir, cross-border-data]
level: advanced
status: draft
description: "Preserve and lawfully obtain evidence that lives in a third-party's cloud: preservation letters vs subpoenas/warrants, provider log retention windows, and legal-hold scoping."
sources: ["https://www.justice.gov/criminal-ccips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud and legal-process evidence handling

**Goal:** know that the evidence you most need is often not on a disk you can image —
it's a log row inside a SaaS provider's backend that rolls off in days, and getting it
requires the right legal instrument served the right way, fast enough to beat the
retention clock.

## 1. Preservation request vs compelled production — different things
- A **preservation letter / litigation hold notice** sent to a provider asks them to
  *stop deleting* data they already hold (per retention policy or normal rotation) —
  it does not compel them to *hand it over*. Under US law (18 U.S.C. §2703(f), the
  "ECPA preservation request") a provider must preserve on request without a warrant,
  but production of content still needs a subpoena, court order, or warrant depending
  on data type and jurisdiction. Send the preservation request the moment you know a
  provider holds relevant data — this is cheap, fast, and buys time while the actual
  legal process is prepared. Missing this step is the single most common reason
  relevant cloud logs are gone by the time a subpoena arrives.
- **Subpoena/court order/search warrant** — which instrument is required depends on
  data category (basic subscriber info vs stored content vs real-time
  interception) and jurisdiction; this determines what you can lawfully compel and
  from whom. Involve legal counsel to pick the instrument — this skill is about
  knowing the preservation step exists and acting on it immediately, not drafting
  legal process.
- **Cross-border data** adds a second layer: a US-headquartered provider holding data
  on EU customers may require mutual legal assistance treaty (MLAT) process or
  invoke the CLOUD Act, materially changing timeline. Scope this early, not after a
  deadline slips.

## 2. Know each provider's retention window before you need it
Retention is provider- and plan-tier-specific, and often shorter than people assume:
- Microsoft 365 **Unified Audit Log** retention depends on licence tier (historically
  90 days on lower tiers, longer on E5/with add-ons) — verify current tier/retention
  for the specific tenant, this changes with licensing updates.
- AWS **CloudTrail** management-event history is retained 90 days in the free
  default event history view; anything needed longer must already be flowing to an
  S3 bucket/CloudWatch Logs configured *before* the incident — there is no
  after-the-fact way to recover CloudTrail data past that window if no trail was
  configured to persist it.
- Consumer cloud/email/social providers vary widely and change policy; don't assume
  last year's retention figure still holds — check the provider's current law
  enforcement/preservation guidelines page for the engagement.
The practical rule: **send preservation requests to every plausible provider as soon
as scope suggests they might hold relevant data**, even before you're sure you'll need
it — reversing an unnecessary hold is free; losing expired data is not.

## 3. Legal-hold scoping for the incident itself
Separate from provider-side preservation, your own organisation's legal hold must
identify custodians and data sources broadly enough to not need a second round
(which signals poor scoping to a court) but not so broadly it's unworkable — scope
against the incident timeline and known-affected systems/accounts from the IR
lifecycle's scoping phase (see
computing-software.digital-forensics-incident-response.incident-response-process.incident-lifecycle-playbook),
and revisit scope as the investigation's understanding of impact grows.

## Verify
- Confirm a preservation request was sent (and acknowledged) for every provider
  plausibly holding relevant data, within days of discovering the incident, not weeks.
- For any provider log you intend to cite, record its stated retention window and the
  date you requested/pulled it — a gap here is a gap in your evidentiary chain.
- Confirm with counsel which legal instrument applies before assuming a preservation
  letter alone secures content, not just a stop-deletion commitment.

Unconfirmed: this skill is process/legal-landscape knowledge, not jurisdiction-specific
legal advice — retention windows, licensing tiers and applicable statutes change; verify
current figures and the governing law for the specific provider/jurisdiction/case
with counsel before relying on any number above.
