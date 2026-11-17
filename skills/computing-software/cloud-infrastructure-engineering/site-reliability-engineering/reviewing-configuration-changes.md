---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.reviewing-configuration-changes
name: reviewing-configuration-changes
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, configuration-design, config-change-review, change-management, canarying-config, gitops]
level: practitioner
status: docs-checked
description: "Make configuration changes safe: semantic validation at commit, ownership and versioning, gradual rollout, rollback and avoiding loss of operator control."
sources: ["https://sre.google/workbook/configuration-design/", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing configuration changes

**Goal:** config changes, a common trigger of incidents, get the same rigour as code. The SRE Workbook says a majority of incidents at Google are triggered by binary or configuration pushes.

## Make config reviewable and traceable
- Peer review and version control are expected of automation because it is code-based.
- Each configuration snippet should have a clear owner (for example a directory owned by one production group), so it is easy to know who changed what.
- Version configuration, including configuration ingested by web UI or remote APIs, so you can see what it looked like at any point in time. Consider tighter coupling between configuration and the software configured, to avoid configuring features not yet available or no longer supported.
- Log both changes to configuration and the resulting application of it: committing a new version does not always mean it is applied. During an incident this lets you find the full set of edits, roll back confidently and notify affected parties.

## Automated checks
- Go beyond syntax: do semantic validation (the config references a nonexistent directory, or asks for a thousand times more RAM than exists because units were misread). For every possible misconfiguration, ask whether it can be prevented at commit time.
- Use a linter and an automatic formatter to cut formatting discussion and avoid indentation mistakes in whitespace-oriented configs.
- Prefer safe defaults, for example dry-run by default instead of requiring the user to choose.

## Safe application (three properties)
1. Deployed gradually, avoiding an all-or-nothing change; avoid a global all-at-once push so a problematic push can be aborted before a 100% outage (Kubernetes rolling updates are an example).
2. Able to roll back if it proves dangerous. Rolling back the offending configuration mitigates an outage faster than patching, which has inherently lower confidence.
3. Automatic rollback, or at minimum the ability to stop progress, if the change leads to loss of operator control (for example firewalling yourself out of the system, or a display-settings countdown that resets if unconfirmed).
- To roll forward and back, configuration must be hermetic. Configuration that depends on external resources that can change, for example a file in version control that references data on a network filesystem, is hard to roll back.
- The same principles apply to binary upgrades and data set pushes.

## Verify
- [ ] Each production config change has an owner, is in version control, passes validation and has a stated gradual rollout and rollback path.

## Checked
Method: docs-checked 2026-11-09 against the SRE Workbook chapters "Configuration Design and Best Practices" (tooling, ownership and change tracking, safe application) and "Canarying Releases" (incident share and peer review/version control). The SRE Book "Release Engineering" page was not used for claims and was dropped. Removed: CODEOWNERS, rendered-diff and plan commands (helm diff, terraform plan, kubeconform, promtool), OPA/Kyverno policy, the blast-radius approval flag, the review checklist and the dashboard annotation advice, none stated on the pages read.
