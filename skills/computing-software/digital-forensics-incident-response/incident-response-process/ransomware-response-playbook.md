---
id: computing-software.digital-forensics-incident-response.incident-response-process.ransomware-response-playbook
name: ransomware-response-playbook
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ransomware, ransomware-negotiation, ofac-sanctions, double-extortion, data-leak-site, decryptor, no-more-ransom, backup-recovery, isolation, lateral-movement, ransomware-payment, business-continuity, dfir, incident-response]
level: advanced
status: draft
description: "Run a ransomware incident: isolate without tipping off a still-moving actor, assess backups/shadow copies for real recovery, and weigh payment-decision factors (OFAC, leak sites, decryptors)."
sources: ["https://www.cisa.gov/stopransomware", "https://ofac.treasury.gov/", "https://www.nomoreransom.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransomware response playbook

**Goal:** apply
computing-software.digital-forensics-incident-response.incident-response-process.incident-lifecycle-playbook's
generic containment/eradication/recovery phases to ransomware's specific shape: an
actor who is often still in the environment when encryption is noticed, a recovery
path that depends entirely on what survived, and a payment decision with legal
exposure that generic IR doesn't have.

## 1. First hour: contain without destroying evidence or tipping off
- **Isolate, don't power off**, hosts still being encrypted if at all avoidable —
  pulling network (not power) stops lateral spread while preserving memory for
  acquisition (see
  computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3).
  Powering off a host mid-encryption loses volatile evidence and sometimes corrupts
  files further; the actor's tooling is already on disk regardless.
- Assume the actor has had access for **days to weeks** before deploying encryption
  (most ransomware is the last stage of an intrusion, not the whole attack) —
  encryption timestamp is not the intrusion start; scope backward using the full
  lifecycle's scoping step before declaring containment complete, or you contain the
  encryptor and miss the still-active access the actor used to deploy it.
- Check for **double extortion**: data staged/exfiltrated before encryption. Network
  forensics (see
  computing-software.digital-forensics-incident-response.wireshark-forensics.pcap-triage-and-session-reconstruction
  if full packet capture exists) and cloud/egress logs for large outbound transfers in
  the days before encryption; this changes the regulatory/notification picture even if
  no ransom is paid.

## 2. Recovery assessment — backups first, always
- Check backup integrity and **isolation from the production domain** — ransomware
  groups routinely target backup infrastructure (deleting snapshots, encrypting
  backup repositories) specifically to force payment; a backup reachable from a
  compromised domain admin account is not a reliable backup.
- Check Volume Shadow Copies before assuming deletion was complete (see
  computing-software.digital-forensics-incident-response.disk-memory-forensics.volume-shadow-copy-and-restore-point-forensics)
  — `vssadmin delete shadows` is common but not always run on every host, especially
  ones encrypted automatically by worming rather than hands-on-keyboard.
- Check **No More Ransom** and vendor decryptor lists for the specific ransomware
  family/variant before assuming payment is the only path — some families have had
  key leaks or flawed crypto yielding free decryptors; verify the family via the
  ransom note format and file extension against current identification resources, not
  assumption, since affiliates reuse and rebrand builder code.

## 3. The payment decision — factors, not a recommendation
This skill states the factors; the decision is the client's/counsel's, informed by
a ransomware-experienced negotiator where payment is being considered:
- **OFAC sanctions exposure** — some ransomware groups/affiliates are on sanctioned-
  entity lists; paying a sanctioned actor carries liability regardless of intent.
  Check current OFAC guidance and the specific group's status before any payment
  discussion proceeds.
- **No guarantee of a working decryptor**, or of actual data deletion after payment
  on double-extortion cases — payment buys a chance at both, not a certainty; some
  "specialist" ransomware negotiation firms exist specifically to vet the actor's
  reliability and negotiate terms, which has measurable value over going direct.
  **Unconfirmed: success-rate figures for specific groups' decryptors are not
  something to cite from memory — this moves and should be checked against current
  incident-response-vendor reporting (e.g. Coveware, CISA advisories) at the time.**
- **Business continuity cost vs recovery cost** — the comparison that actually drives
  most decisions, informed by the backup assessment above, not by the ransom note's
  framing of urgency.

## Verify
- Confirm scoping went back further than the encryption timestamp before calling
  containment complete.
- Confirm backup isolation from production was checked, not assumed, before ruling out
  backup-based recovery.
- If payment occurs, confirm OFAC screening of the receiving wallet/entity was
  performed by counsel/a specialist firm before funds move.
