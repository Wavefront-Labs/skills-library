---
id: computing-software.systems-network-administration.patch-management.configuration-baselines-as-code
name: configuration-baselines-as-code
category: computing-software
field: systems-network-administration
product: patch-management
tags: [baseline-as-code, configuration-baseline, git, version-control, inspec, ci-pipeline, config-baselines]
level: advanced
status: draft
description: "Version configuration baselines as code: Git repositories for GPO backups, DSC, Ansible and OpenSCAP tailoring, semantic versions, PR review, CI tests and controlled releases."
sources:
  - https://docs.chef.io/inspec/
  - https://www.open-scap.org/resources/documentation/customizing-scap-security-guide-for-your-use-case/
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-service-configuration-management
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioning baselines as code

**Goal:** every baseline change is reviewed, tested, versioned and traceable, so "which settings were in force on 3 March?" has a precise answer.

## Repository layout
```text
baselines/
  windows-server-2022/   gpo-backups/, dsc/, deviations.yml, CHANGELOG.md
  rhel9/                 ansible-role/, tailoring.xml (OpenSCAP), deviations.yml
  tests/                 inspec profiles per platform
```
- Map each setting to its source control ID (CIS rule, Microsoft baseline setting, internal standard).
- Deviations as data (`deviations.yml`: rule, scope, reason, approver, expiry) consumed by the automation.

## Versioning
Semantic versions: major for breaking hardening changes, minor for new settings, patch for fixes. Tag releases (`rhel9-baseline-v3.2.0`); deployments reference tags, never a branch head.

## Workflow
1. Change on a branch, pull request with reason and ticket link.
2. CI: lint (ansible-lint, PSScriptAnalyzer), build a test VM (Packer or Vagrant), apply, run InSpec/Goss tests and an OpenSCAP scan; fail on regressions.
3. Peer and security review; merge; tag.
4. Roll out the tag by ring through the normal change process.

## Evidence
CI artefacts (scan reports per version), the changelog and Git history give auditors the history of the baseline. Record which version each host runs (fact, tag, or CMDB attribute).

## Gotchas
- GPO backups are XML blobs; store the human-readable report (`Get-GPOReport -ReportType Html`) alongside to make diffs reviewable.
- Expired deviations should fail CI so they get reviewed.

## Verify
Pick a host: its recorded baseline version matches a Git tag, and running that tag's tests on the host passes.
