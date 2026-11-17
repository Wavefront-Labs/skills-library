---
id: computing-software.cybersecurity-defensive.security-operations.incident-recovery-validation
name: incident-recovery-validation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, incident-recovery, restoration, eradication, rebuild, monitoring, recovery-validation]
level: advanced
status: draft
description: "Recover from a security incident safely: rebuild vs clean decisions, staged restoration from known-good backups, credential resets, heightened monitoring and exit criteria."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/184/final", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovery and restoration validation

**Goal:** bring systems back without bringing the attacker back, and prove it.

## 1. Preconditions for recovery
- Eradication done: initial access vector closed, persistence removed (accounts, scheduled
  tasks, services, web shells, OAuth apps, mailbox rules, GPOs), attacker infrastructure
  blocked.
- Root cause understood well enough to prevent immediate reinfection.
- Credentials rotated in the right order (see below).

## 2. Rebuild or clean
- **Rebuild** from known-good media/golden images for anything with attacker admin-level
  execution: domain controllers, servers with confirmed implants. Cleaning cannot prove
  absence of persistence.
- **Clean** acceptable for low-privilege, well-understood malware on workstations with EDR
  confirming no further activity (many orgs reimage anyway).

## 3. Restore data
- Pick a restore point **before** the earliest attacker activity (from the timeline), not
  just before encryption; scan restored data and backups for implants and web shells.
- Restore into an isolated network first; validate integrity (checksums, application tests,
  database consistency checks) before reconnecting.
- Order by business priority and dependency: identity (AD/IdP), network services (DNS,
  DHCP), core apps, then the rest.

## 4. Credentials
Identity compromise recovery order: reset privileged accounts and service accounts, reset
KRBTGT twice (with replication wait between), rotate secrets in vaults and applications,
revoke all refresh tokens, reissue certificates if the CA or keys were touched, then user
passwords.

## 5. Heightened monitoring
For 30-90 days: alerts on the specific IOCs and TTPs seen, new admin accounts, logons from
the attacker's ASNs, and reappearance of persistence. Increase log retention for affected systems.

## 6. Exit criteria (agree up front)
Business owner confirms function; no attacker activity for an agreed period; open
eradication actions closed; monitoring rules in place; the IC formally closes recovery
and hands remaining items to normal change.

## Gotchas
- Restoring a backup that contains the backdoor reinfects the estate within hours.
- Bringing systems online one by one into a still-compromised network; isolate the
  recovery environment.
- Backups encrypted or deleted too: offline/immutable copies are the only reliable source.

## Verify
Each restored system has a checklist entry: source (image/backup date), integrity checks
passed, credentials rotated, EDR healthy, owner sign-off.
