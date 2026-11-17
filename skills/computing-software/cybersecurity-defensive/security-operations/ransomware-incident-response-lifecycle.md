---
id: computing-software.cybersecurity-defensive.security-operations.ransomware-incident-response-lifecycle
name: ransomware-incident-response-lifecycle
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, ransomware-response, ransomware, strain-identification, no-more-ransom, ofac, restore-sequencing, cisa-stopransomware]
level: advanced
status: docs-checked
description: "Run a ransomware incident past containment: strain identification, decryptor checks, legal and sanctions questions, evidence, restore sequencing, and preventing re-entry."
sources: ["https://www.nomoreransom.org/", "https://ofac.treasury.gov/media/912981/download?inline", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ransomware incident response lifecycle

Containment (isolating hosts, protecting backups) is covered by the endpoint ransomware
containment playbook. This is the rest of the incident.

## 1. Identify what you are dealing with
- Ransom note text, file extension, note filename; submit a note and one encrypted sample to
  a ransomware identification service.
- Check No More Ransom for a free decryptor. Its site says not every type of ransomware has a solution, but it is cheap to check.
- Look up the group on CISA #StopRansomware advisories for known TTPs, initial access vectors
  and IOCs to hunt.
- Check leak sites (via your CTI provider) for whether data has been posted: data theft changes
  notification obligations even if you restore everything.

## 2. Scope
- Initial access (VPN appliance, RDP, phishing, valid accounts from infostealer logs) and dwell
  time: ransomware is the end of the intrusion, often weeks after entry.
- Accounts used (often domain admin); persistence (remote-management tools, scheduled
  tasks, new accounts); exfiltration (outbound transfer volumes).
- Which systems are encrypted vs merely accessed.

## 3. Decisions that are not technical
Bring in legal, executives, insurer (often requires use of their panel IR firm and counsel), and
law enforcement (FBI IC3/field office, national CERT). Payment questions involve sanctions
screening (the US OFAC advisory describes sanctions risks for making and facilitating ransomware payments) and regulatory reporting. Document who decided what and when.

## 4. Evidence
Before wiping: memory and disk images of patient zero, a DC, and representative encrypted hosts;
firewall, VPN, EDR and cloud logs exported (retention may be short).

## 5. Recovery sequencing
1. Clean, isolated recovery environment; rebuild identity first: domain controllers from known-good
   backup (pre-intrusion) or forest recovery; rotate privileged and service
   account credentials and keys (CISA lists this as a containment activity).
2. Core infrastructure: DNS, DHCP, PKI, backup servers, management tools.
3. Business-critical applications by BIA tier; scan restored data and verify backups predate the
   intrusion (not just the encryption).
4. Endpoints: reimage rather than clean.
Monitor restored segments heavily (EDR in block mode, new detections from the IOCs) before reconnecting.

## 6. Prevent re-entry
Close the initial access vector, enforce MFA on remote access, remove unauthorised RMM tools,
block known C2, and hunt for persistence again after recovery.

## Gotchas
- Restoring a backup that contains the attacker's persistence re-infects you.
- Decryptors from the attacker are slow and buggy; test on copies.
- Notification deadlines under applicable law and contracts run in parallel with recovery; confirm them with counsel.

## Verify
No IOC hits or new suspicious privileged activity for an agreed period after reconnection, and a
post-incident review with the root cause and fixes signed off.

## Checked
2026-11-01. Confirmed: No More Ransom site (free decryptors, not every type has one), US OFAC updated advisory on sanctions risks for facilitating ransomware payments, CISA incident response playbooks (forensic images, credential and key rotation, reimage from clean backups, lessons learned), NIST SP 800-61r3 page. Removed: tool names (ID Ransomware, Crypto Sheriff, rclone, MEGA, AnyDesk, ScreenConnect), the krbtgt double reset, the GDPR and SEC clock figures. The CISA ransomware guide page returned 403 and was dropped from sources.
Method: documentation only; no commands were run.
