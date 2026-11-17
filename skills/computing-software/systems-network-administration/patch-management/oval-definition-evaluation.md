---
id: computing-software.systems-network-administration.patch-management.oval-definition-evaluation
name: oval-definition-evaluation
category: computing-software
field: systems-network-administration
product: patch-management
tags: [oval-definitions, oval, openscap, patch-verification, vulnerability-scanning, linux]
level: practitioner
status: docs-checked
description: "Verify Linux patch state with vendor OVAL definitions: download Red Hat/Ubuntu/SUSE OVAL feeds, run oscap oval eval, read results and handle backported fixes correctly."
sources:
  - https://github.com/OpenSCAP/openscap/blob/main/docs/manual/manual.adoc
  - https://security.access.redhat.com/data/oval/v2/
  - https://security-metadata.canonical.com/oval/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OVAL definition evaluation for patch verification

OVAL (Open Vulnerability and Assessment Language) feeds from distros express "vulnerable if package X version < fixed-version-with-backport". Evaluating them locally gives a scanner-grade answer without a commercial scanner, and handles backports correctly.

## Get the feed
```sh
# RHEL 9
curl -sO https://security.access.redhat.com/data/oval/v2/RHEL9/rhel-9.oval.xml.bz2 && bunzip2 rhel-9.oval.xml.bz2
# Ubuntu 22.04 (USN-based)
curl -sO https://security-metadata.canonical.com/oval/com.ubuntu.jammy.usn.oval.xml.bz2 && bunzip2 com.ubuntu.jammy.usn.oval.xml.bz2
# SUSE: https://ftp.suse.com/pub/projects/security/oval/
```

## Evaluate
```sh
dnf install openscap-scanner        # or apt install openscap-scanner on Debian 12 / Ubuntu 24.04 and newer (older releases use a different package; see the OpenSCAP manual)
oscap oval eval --results results.xml rhel-9.oval.xml
```
Each definition is a patch advisory or CVE; a `true` result means the definition's criteria matched (for a vulnerability definition, the system is affected). Read the results file written by `--results`.

## Use in fleets
- Run from Ansible/cron, ship `results.xml` or the `true` list to a central store.
- Many vulnerability scanners consume the same OVAL data; local runs can explain discrepancies.

## Gotchas
- Use the feed matching the exact stream (RHEL 9 vs RHEL 9 EUS; Ubuntu USN vs CVE OVAL). Wrong feed = false results.
- Red Hat publishes patched-only feeds (`rhel-9.oval.xml.bz2`) and separate `-including-unpatched` feeds; Ubuntu publishes CVE, USN and PKG feeds. CVE-oriented feeds can report unfixed CVEs as affected indefinitely; patch-oriented feeds only list fixes that exist.
- Evaluating large feeds takes time and CPU; schedule it off-peak.
- Red Hat feeds are per product and stream (separate EUS feeds exist); third-party packages are not covered.

## Verify
After patching, rerun: advisories you just applied flip to `false`; spot-check one against `rpm -q --changelog <pkg> | grep CVE-...` or `apt changelog`.

## Checked
Date: 2026-10-27. Documentation checked: OpenSCAP manual (`oscap oval eval --results <file> <oval-file>`, `openscap-scanner` on RHEL-family and on Debian 12 / Ubuntu 24.04 and newer), the live Red Hat OVAL v2 directory listing (`RHEL9/rhel-9.oval.xml.bz2`, `-including-unpatched` and EUS feeds) and the live Ubuntu OVAL index (`com.ubuntu.jammy.usn.oval.xml.bz2` exists alongside CVE and PKG feeds). Removed `--report`, the grep-on-output line and the example definition ID, which the manual does not confirm, and replaced the dead OVAL.mitre.org link.

Method: documentation only; no commands were run.
