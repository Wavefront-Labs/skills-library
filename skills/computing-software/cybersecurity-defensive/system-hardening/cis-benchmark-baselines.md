---
id: computing-software.cybersecurity-defensive.system-hardening.cis-benchmark-baselines
name: cis-benchmark-baselines
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [system-hardening, cis-benchmarks, security-baseline, configuration-management, microsoft-security-baselines, security-compliance-toolkit, group-policy, disa-stig, openscap, compliance-scanning, drift-detection, kube-bench]
level: practitioner
status: gated
description: "Adopt CIS Benchmarks as a tailored, versioned baseline: pick profile levels, document deviations, apply via GPO/Intune/Ansible, scan with OpenSCAP for drift and roll out safely."
sources: ["https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10", "https://static.open-scap.org/openscap-1.3/oscap_user_manual.html", "https://csrc.nist.gov/pubs/sp/800/70/r4/final", "https://github.com/aquasecurity/kube-bench", "https://pages.nist.gov/800-63-4/sp800-63b.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIS Benchmark baselines - hardened by default, deviations on paper

**Goal:** turn a benchmark of hundreds of items into a baseline your organisation actually runs: tailored to each
platform role, enforced as code, measured continuously, and with every "we don't do that" decision written down.

## 1. Choose the benchmark and profile
- One benchmark per platform version you run (operating system releases, Kubernetes, cloud provider). Benchmarks
  are versioned - record the exact version in the baseline.
- CIS profile levels: Level 1 is the low-impact default and Level 2 is defence in depth for sensitive systems
  (gated: unconfirmed, source is paywalled or blocked). Test Level 2 harder. Windows has role-specific profiles
  (domain controller vs member server); apply the right one.
- Consider Microsoft's security baselines for Windows through the Security Compliance Toolkit; they cover Windows 10
  and 11, Windows Server releases, Microsoft 365 Apps and Edge. DISA STIGs if you serve US government.
- The NIST National Checklist Program (SP 800-70) describes how to find and use configuration checklists. Rev. 4 is
  marked withdrawn (May 2026) and superseded by Rev. 5 on the NIST page, so cite Rev. 5.

## 2. Tailor and document
Create a baseline document (spreadsheet or YAML in Git) with columns: rule ID, title, expected value, **decision**
(apply / modify / exempt), rationale, compensating control, approver, review date. Typical deviations:
- Disabling services your role needs (e.g. a print server needs the Spooler).
- Password expiry rules superseded by your identity provider and NIST SP 800-63B, which says verifiers must not
  require subscribers to change passwords periodically.
- Settings that break management tooling (WinRM, remote registry for scanners).
Deviations approved once apply to every system of that role; don't let individual servers drift.

## 3. Apply as code
- **Windows:** Group Policy, using the Security Compliance Toolkit. It includes Policy Analyzer (compare GPO sets and
  local policy) and LGPO.exe (apply Registry.pol, security templates and audit files to local policy; export local
  policy to a GPO backup). Or Intune.
- **Linux:** configuration management (Ansible, image builds) or OpenSCAP remediation:
  `oscap xccdf eval --remediate --profile <PROFILE_ID> --results-arf results.xml <SSG_DATASTREAM_XML>`.
  List the profiles in a data stream with `oscap info <datastream>`; profile IDs look like
  `xccdf_org.ssgproject.content_profile_<name>` and differ per distribution content.
- **Kubernetes:** kube-bench runs checks against the CIS Kubernetes Benchmark.

## 4. Roll out safely
Lab, then a pilot ring that includes unusual applications, then broad deployment; hold each ring long enough to
surface breakage (SMB signing/NTLM restrictions, TLS and cipher hardening, SSH cipher lists, `noexec` on `/tmp`,
audit rules filling disks). Have the rollback (unlink the GPO, revert the playbook) tested.

## 5. Measure and detect drift
- Scan with OpenSCAP: `oscap xccdf eval --profile <PROFILE_ID> --results-arf results.xml --report report.html
  <datastream>`; or a commercial scanner, or Intune/Defender compliance reports.
- Report the score per role against your tailored baseline, not the raw benchmark - approved deviations should not
  count as failures.
- Alert on regressions: a host dropping several points week over week usually means an unlinked GPO, a new image or
  manual changes.

## Gotchas
- Chasing 100 percent of the raw benchmark creates outages; judge against the tailored baseline.
- Benchmarks update; re-baseline on major version changes and OS upgrades - settings move or are renamed.
- Configuration applied only at build time drifts; use continuous enforcement (GPO refresh, Intune, scheduled
  configuration management, or immutable rebuilds).
- Scanners may check a setting a different way than you applied it (registry vs policy CSP) and report false
  failures - validate a sample manually.
- Hardening the OS while leaving local admin rights and unsupported software intact misses the bigger risk.

## Verify
- [ ] Each platform role maps to a specific benchmark version and profile level.
- [ ] Every deviation has rationale, approver and review date in the baseline repo.
- [ ] Baseline is applied by code (GPO/Intune/configuration management/image), not by hand.
- [ ] Compliance scans run on a schedule against the tailored profile.
- [ ] Rollback for the last baseline change was tested in the pilot ring.
- [ ] Drift alerts exist and have an owner.

Related: computing-software.cybersecurity-defensive.nessus.authenticated-scanning

## Checked
2026-10-31. Confirmed: Microsoft Security Compliance Toolkit page (baseline list, Policy Analyzer, LGPO), OpenSCAP
user manual 1.3 (`oscap xccdf eval`, `--profile`, `--results-arf`, `--report`, `--remediate`, `oscap info`, profile
ID prefix), NIST SP 800-70 Rev. 4 page (withdrawn, superseded by Rev. 5), NIST SP 800-63B-4 (no periodic password
change requirement), kube-bench README (CIS Kubernetes Benchmark). Gated: the CIS Level 1/Level 2 definitions, because
cisecurity.org requires registration. Removed: specific benchmark version numbers, the CIS-hardened-image and
CIS-CAT Pro claims, third-party scanner names, Ansible-Lockdown and Packer specifics, Pod Security Admission
`restricted`, the `cis_server_l1` profile ID, typical score ranges and ring percentages/durations.
Method: documentation only; no commands were run.
