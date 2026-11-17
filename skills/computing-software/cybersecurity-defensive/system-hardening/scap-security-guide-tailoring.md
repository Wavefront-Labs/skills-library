---
id: computing-software.cybersecurity-defensive.system-hardening.scap-security-guide-tailoring
name: scap-security-guide-tailoring
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [cis-benchmarks, scap-tailoring, scap-security-guide, openscap, tailoring-file, autotailor, xccdf, compliance-as-code]
level: advanced
status: docs-checked
description: "Tailor SCAP Security Guide profiles: tailoring files via autotailor or SCAP Workbench, value overrides, justified rule deselection, and scanning with oscap."
sources: ["https://github.com/ComplianceAsCode/content/blob/master/docs/manual/user/10_install.md", "https://github.com/ComplianceAsCode/content/blob/master/docs/manual/user/20_scanning.md", "https://github.com/OpenSCAP/openscap/blob/main/utils/autotailor.8", "https://github.com/OpenSCAP/openscap/blob/main/utils/oscap.8", "https://github.com/OpenSCAP/openscap/blob/main/utils/oscap-ssh.8", "https://github.com/OpenSCAP/openscap/blob/main/utils/oscap-podman.8"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCAP Security Guide tailoring

SCAP Security Guide (ComplianceAsCode) ships XCCDF profiles (for example STIG and PCI-DSS, as used in the OpenSCAP and ComplianceAsCode examples) for RHEL,
Debian-family and other systems. Nobody runs a profile unmodified: tailoring records your deviations in a file instead of
editing the content.

## Find content and profiles
```
dnf install scap-security-guide openscap-scanner        # apt: ssg-debderived (Debian derivatives), ssg-debian, ssg-nondebian, ssg-applications
ls /usr/share/xml/scap/ssg/content/
oscap info /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml   # lists the profile IDs, components and data streams
```

## Create a tailoring file
CLI with `autotailor` (documented in the OpenSCAP repository as a tool that produces tailoring files from a data stream and a base profile ID; IDs are validated against the data stream unless `--no-validate` is used):
```
autotailor -o tailoring.xml --new-profile-id cis_l1_acme \
  --unselect xccdf_org.ssgproject.content_rule_partition_for_var_log_audit \
  --var-value xccdf_org.ssgproject.content_value_var_accounts_passwords_pam_faillock_deny=5 \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml <base-profile-id-from-oscap-info>
```
The new profile ID gets the `xccdf_org.ssgproject.content_profile_` prefix (here `xccdf_org.ssgproject.content_profile_cis_l1_acme`); if `--new-profile-id` is omitted, `_customized` is appended to the base profile ID. `--select`, `--rule-severity` and `--rule-role` are also available, and `--local-path` helps tools such as Red Hat Satellite that cannot resolve local file paths.
The rule and variable IDs above are illustrative; autotailor validates IDs against the data stream, so list real ones from the content first.
Keep `tailoring.xml` in Git with a comment/ticket for every unselected rule (why, compensating control, owner).

## Scan and remediate
```
oscap xccdf eval --tailoring-file tailoring.xml --profile xccdf_org.ssgproject.content_profile_cis_l1_acme \
  --results results.xml --report report.html /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
oscap xccdf generate fix --fix-type ansible --tailoring-file tailoring.xml \
  --profile xccdf_org.ssgproject.content_profile_cis_l1_acme \
  /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml > remediate.yml        # every rule in the profile; review before running
```
To remediate only the rules that failed in a scan, pass `--result-id <TestResult ID>` and the results file instead; result-oriented fixes take precedence over `--profile`.
`oscap` exits 0 when all rules pass, 1 on an evaluation error and 2 when at least one rule fails or is unknown.
Also: `oscap-ssh` runs oscap on a remote host over SSH (needs oscap installed there), `oscap-podman` scans container images and containers (cannot run rootless).

## Practice
- Start from the least restrictive profile that meets your requirement; tailor; remediate in images (golden image pipeline) rather than at runtime.
- Re-scan on schedule; track pass rate per host group; differences between hosts usually mean drift.
- Re-run autotailor (which validates rule and variable IDs against the data stream) after upgrading `scap-security-guide`.

## Gotchas
- Automatic remediation executes the content's fix elements; the oscap manual says to use it at your own risk and only with trusted content, so test generated fixes in staging.
- Review every non-pass result, not just failures: a rule that was not evaluated is not a pass.

## Verify
Report shows the tailored profile ID, only justified rules are unselected, and the pass rate meets the
target on a fresh image and on a sample of production hosts.

## Checked
Checked 2026-10-25 against the ComplianceAsCode user manual (install and scanning chapters; ComplianceAsCode/content, last commit 2026-10-23) and the OpenSCAP manual pages autotailor(8), oscap(8), oscap-ssh(8) and oscap-podman(8) (openscap/openscap, 2026-10-22). Confirmed: content path `/usr/share/xml/scap/ssg/content/`, the `scap-security-guide` and Debian-family `ssg-*` package names, autotailor options (`-o`, `--new-profile-id`, `--unselect`, `--var-value`, `--local-path`, `--no-validate`) and generated profile ID rules, oscap `--tailoring-file`, `--profile`, `--results`, `--report`, `generate fix --fix-type`, `--result-id` precedence over `--profile`, exit codes. Corrections: `autotailor --output` is documented as `-o`; the fix command's `--result-id ""` was not a documented form. Removed unconfirmed: CIS profile ID, SCAP Workbench steps, Insights/Satellite upload, kickstart addon and rule-ID churn claims. Red Hat documentation was not read.

Method: documentation only; no commands were run.
