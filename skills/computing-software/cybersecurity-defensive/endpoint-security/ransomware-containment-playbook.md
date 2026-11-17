---
id: computing-software.cybersecurity-defensive.endpoint-security.ransomware-containment-playbook
name: ransomware-containment-playbook
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [ransomware, containment, edr, backup-isolation, lateral-movement, shadow-copy-deletion, encryption-detection, kill-switch, network-segmentation, business-continuity, extortion, double-extortion]
level: advanced
status: draft
description: "First 60 minutes of a suspected ransomware event: stop the spread, protect backups, decide isolation scope, and avoid the common mistakes that turn one host into the whole estate."
sources: ["CISA #StopRansomware Guide (public)", "NIST SP 800-61 Rev. 3", "SANS Ransomware Response playbook guidance (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransomware containment playbook — the first hour decides the blast radius

**Goal:** when mass file encryption or shadow-copy deletion is observed, act fast
enough to stop lateral spread and protect backups, without destroying the evidence
needed to understand scope — speed matters more here than in almost any other
incident type because the encryption process is actively running.

## 1. Signals that mean "act now, don't wait for full confirmation"
Mass file renames/extension changes across a share, ransom note files appearing in
multiple directories, `vssadmin delete shadows` / shadow copy deletion events,
sudden CPU spike tied to a process touching thousands of files, or EDR flagging a
known ransomware family. Any of these justifies isolating the affected host(s)
**immediately**, before full root-cause analysis — unlike most incidents, the cost
of delaying containment here (more hosts encrypted) usually exceeds the cost of
losing some investigative tidiness.

## 2. Protect backups before anything else
Many ransomware operators specifically target backup infrastructure (delete backup
jobs, encrypt backup repositories, revoke backup service accounts) before or during
the encryption phase, because a recoverable org has no reason to pay. Immediately:
disconnect or air-gap backup systems from the network if they're reachable from the
compromised segment, verify the most recent backups are intact and from before the
event (don't assume — check), and rotate/disable credentials used by backup
service accounts if there's any sign they were touched.

## 3. Stop lateral spread
Isolate the known-affected hosts via EDR immediately. Then move faster than normal
triage speed to contain the *likely* spread vector: if the encryption is
propagating via SMB/admin shares, consider temporarily blocking SMB between
workstation segments at the firewall/switch level (not just the one host) while
you scope; if a specific account shows signs of being used across many hosts
(domain admin, service account), disable it. This is a case where acting on
strong suspicion before full confirmation is the right trade — a false-positive
segment block is reversible; an uncontained spread is not.

## 4. Decide: isolate aggressively vs. preserve evidence, explicitly
Ransomware is the clearest case where containment speed can outrank evidence
preservation for already-encrypting hosts (the data is being destroyed right now
regardless of what you do) — but for hosts that are compromised but *not yet*
encrypting, still capture volatile evidence (process/memory) before isolating,
because that tells you the entry vector, which determines whether rebuilding into
the same network closes or reopens the door. Make this call per-host, with the IC,
rather than applying one policy to every machine in the incident.

## 5. Don't negotiate or decide on payment at the technical layer
Whether to engage a negotiator or consider payment is a legal/executive/insurance
decision with regulatory and sanctions implications (paying a sanctioned entity can
itself be illegal in some jurisdictions) — security's job here is evidence
(ransom note, encryption extension, any leak-site posting for double-extortion
cases) and technical options (decryptor availability via nomoreransom.org-style
projects, backup viability), not the negotiation itself.

## Gotchas
- Rebuilding/restoring before the entry vector is identified and closed very
  commonly leads to reinfection within hours to days — this is the single most
  repeated mistake in public post-incident reports.
- Shutting down a host (power off) instead of isolating it can lose memory
  evidence and, on some ransomware families, trigger worse behaviour on next boot
  (file corruption from an incomplete encryption pass) — prefer network isolation
  over power-off unless the device is actively worsening something.
- Shadow copies deleted does not always mean backups are unrecoverable — check
  offsite/immutable backups and cloud snapshot history before assuming total loss.
- Double-extortion (data theft before encryption) changes the response —
  treat it as a confirmed data breach requiring the same notification analysis as
  any exfiltration incident, not just a recovery problem.

## Verify
- [ ] Backup infrastructure was checked/isolated and recent backup integrity
      confirmed within the first response actions.
- [ ] Known-affected hosts were isolated immediately; suspected spread vector was
      blocked at the network level, not just per-host.
- [ ] A per-host call on evidence-preservation-vs-speed was made deliberately, not
      defaulted.
- [ ] No restore/rebuild happened before the entry vector was identified.
- [ ] Payment/negotiation questions were routed to legal/executive, not decided
      by the technical responder.

Related: computing-software.cybersecurity-defensive.endpoint-security.endpoint-isolation-and-forensic-triage,
computing-software.cybersecurity-defensive.security-operations.incident-response-coordination,
computing-software.cybersecurity-defensive.network-defence.firewall-and-egress-policy
