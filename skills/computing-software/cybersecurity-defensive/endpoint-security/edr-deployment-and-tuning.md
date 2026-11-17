---
id: computing-software.cybersecurity-defensive.endpoint-security.edr-deployment-and-tuning
name: edr-deployment-and-tuning
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [endpoint-security, edr, xdr, microsoft-defender-for-endpoint, crowdstrike-falcon, sentinelone, elastic-defend, attack-surface-reduction, asr-rules, tamper-protection, sensor-health, exclusions, prevention-policy, ring-deployment, host-isolation, live-response, sysmon, atomic-red-team, lsass-protection, vulnerable-driver-blocklist]
level: practitioner
status: draft
description: "Deploy EDR to full coverage in rings, move from detect to prevent safely, keep exclusions minimal, monitor sensor health, and test detections with emulation."
sources: ["Microsoft Defender for Endpoint documentation - onboarding, ASR rules, tamper protection", "MITRE ATT&CK Evaluations (Enterprise) methodology", "Red Canary Atomic Red Team project", "CISA / NSA guidance on EDR and endpoint hardening"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR deployment and tuning — full coverage, prevention on, few holes

**Goal:** get an EDR sensor healthy on every endpoint and server, switch from
"detect only" to blocking without breaking the business, and keep the exclusion list
short enough that it isn't an attacker's map.

## 1. Coverage first
- Reconcile three inventories weekly: EDR console, directory/MDM (AD, Entra/Intune,
  Jamf), and network/vuln scanner. Hosts in the scanner but not EDR are your gaps.
- Deploy via your existing tooling (Intune/SCCM/GPO, Jamf, Ansible, golden images,
  cloud launch templates) — include the sensor in server and VDI build images, with
  the vendor's VDI/non-persistent mode set so clones don't share an agent ID.
- Linux and macOS need extra permissions (macOS: system extension approval, Full
  Disk Access via MDM profile; Linux: supported kernel versions, eBPF vs kernel module).
- Target: >98% of managed assets with a sensor reporting in the last 24 h (set your number).

## 2. Ring deployment for agents and policy
Ring 0 IT/security (≈1–2%) → Ring 1 pilot across departments and server roles (≈10%)
→ Ring 2 broad → Ring 3 critical servers last. Hold 3–7 days per ring for agent
upgrades and policy changes. Pin critical servers to N-1 sensor versions where the
vendor supports it. The July 2024 CrowdStrike content-update outage showed that
vendor-pushed content can bypass your rings — ask your vendor which update channels
you can stage, and keep a tested recovery runbook (BitLocker recovery keys accessible).

## 3. Turn on prevention
- Enable tamper protection (so local admins/malware can't stop the sensor) and
  require an uninstall token/password.
- Set malware prevention to block, cloud-delivered protection on, PUA block.
- Microsoft Defender ASR rules: start in **Audit** for 2–4 weeks, review events
  (Advanced Hunting `DeviceEvents | where ActionType startswith "Asr"`), then Block.
  High-value rules: block credential stealing from LSASS, block Office apps creating
  child processes, block executable content from email/webmail, block abuse of
  exploited vulnerable signed drivers, block process creations from PSExec/WMI (watch
  for SCCM conflicts).
- Enable LSA protection (RunAsPPL) and Credential Guard where supported; enable
  the Microsoft vulnerable driver blocklist.
- Equivalent concepts: CrowdStrike prevention policy toggles, SentinelOne Protect
  mode, Elastic Defend prevention per protection.

## 4. Exclusions discipline
- Prefer narrow exclusions in order: by certificate/signer → by hash → by full path
  with process → path only. Never exclude whole drives, `%TEMP%`, user-writable folders
  or interpreters (`powershell.exe`, `python.exe`).
- Use vendor-published exclusions for known software (SQL, Exchange, backup agents)
  only as documented, and only on servers running it.
- Each exclusion: owner, reason, ticket, review date. Review quarterly.
- Prefer suppressing an *alert* (detection exception scoped to rule + host + process)
  over excluding a path from *scanning/monitoring*.

## 5. Response readiness
Pre-approve who can isolate hosts, run live response, and collect triage packages.
Test isolation on a lab host: confirm it still talks to the EDR cloud and nothing else.

## 6. Validate with emulation
Monthly, run Atomic Red Team tests (e.g. `Invoke-AtomicTest T1003.001` for LSASS
access) on a test host and confirm: blocked or alerted, correct technique, telemetry
present. Record results in a detection coverage matrix.

## Gotchas
- "Installed" ≠ healthy: check sensor last-seen, version, and policy assignment.
  Sensors in reduced-functionality mode (unsupported kernel, stopped service) look present.
- Third-party AV running alongside can put Defender in passive mode — intended or not.
- Exclusions copied from forums and old vendor docs silently widen attack surface.
- Cloned VMs without VDI settings appear as one flapping host.
- Attackers use BYOVD to kill EDR; driver blocklists and alerting on sensor
  disconnection are your defence.

## Verify
- [ ] Inventory reconciliation shows coverage at or above target, with gaps ticketed.
- [ ] Tamper protection is on and uninstall requires a token.
- [ ] ASR (or equivalent) rules are in Block after an audit period, with exceptions documented.
- [ ] Every exclusion has an owner and review date; none cover user-writable paths.
- [ ] Alert exists for sensors that stop reporting.
- [ ] A recent Atomic Red Team run was blocked/detected as expected.

Related: computing-software.cybersecurity-defensive.security-operations.alert-triage
