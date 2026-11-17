---
id: computing-software.systems-network-administration.patch-management.third-party-extended-lifecycle-support
name: third-party-extended-lifecycle-support
category: computing-software
field: systems-network-administration
product: patch-management
tags: [extended-lifecycle-support, tuxcare, end-of-life, extended-security-updates, eol-software, centos]
level: practitioner
status: draft
description: "Evaluate and operate extended lifecycle support for EOL systems: vendor ELS/ESU versus third-party (TuxCare, Freexian, OpenLogic), what is covered, onboarding, and exit plans."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://access.redhat.com/support/policy/updates/errata
  - https://ubuntu.com/pro
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extended lifecycle support for EOL systems

ELS buys time to migrate; it does not remove the need to migrate.

## Options
| Source | Examples | Notes |
|---|---|---|
| OS vendor | Red Hat ELS add-on, Microsoft ESU (via Azure Arc or volume licensing), SUSE LTSS, Ubuntu Pro (ESM to 10-12 years) | contractually backed; same tooling as before |
| Third party | TuxCare ELS (CentOS 6/7/8, Oracle Linux, Ubuntu, PHP, Python), Freexian (Debian ELTS), OpenLogic/Perforce (CentOS, runtimes), HeroDevs (frameworks) | covers distros the vendor abandoned; check SLA and scope |
| Self-support | backport fixes yourself | rarely realistic beyond a single package |

## Evaluation checklist
- **Scope**: which packages get fixes (often only High/Critical CVEs in a defined package
  set, e.g. base OS but not all of EPEL/AppStream)?
- **SLA**: time from CVE disclosure to patch for Critical.
- **Delivery**: repository + GPG key, compatible with existing tooling (yum/dnf/apt,
  Satellite/Foreman sync, scanners' OVAL support).
- **Scanner support**: will your scanner recognise ELS package versions as fixed? Otherwise
  every finding stays open (need vendor OVAL feed or exceptions with evidence).
- **Term and cost per host**, and certification/compliance acceptance (auditors, PCI).

## Onboarding (typical third-party Linux ELS)
1. Install the vendor's repo package/key on the host (or mirror into your repo manager).
2. Disable dead upstream repos (e.g. vault.centos.org) to avoid mixing.
3. `yum update` to ELS builds; verify `rpm -qi` vendor/packager fields.
4. Register in inventory as "ELS: <vendor> until <date>"; link exception records.

## Exit plan
ELS contract end date = migration deadline. Track each ELS host in the migration programme
with an owner and target platform; don't renew without a dated plan.

## Gotchas
- Mixing ELS and unofficial rebuild repos causes dependency conflicts.
- Kernel live patching may be a separate product.
- Language runtimes inside apps (Python 2, PHP 5) need app-level ELS, not OS ELS.

## Verify
ELS hosts receive and install fixes for a test CVE within the SLA; scanner treats them as
fixed or exceptions document it; every ELS host has a migration date.
