---
id: computing-software.devops-ci-cd.gitlab-ci.license-scanning-and-approval-policies
name: license-scanning-and-approval-policies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, license-scanning, license-approval-policy, license-compliance, denied-licenses]
level: advanced
status: docs-checked
description: "Detect dependency licenses in GitLab via CycloneDX-based license scanning and block merges that add denied licenses with merge request approval policies."
sources: ["https://docs.gitlab.com/user/compliance/license_scanning_of_cyclonedx_files/", "https://docs.gitlab.com/user/compliance/license_approval_policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# License scanning and license approval policies (Ultimate)

## 1. Scanning
License data comes from **dependency scanning** CycloneDX reports; the legacy license compliance analyzer (`License-Scanning.gitlab-ci.yml`) was removed in 17.0 and CycloneDX-based license scanning is the replacement. Turn on dependency scanning (the docs offer the dependency scanning template or a security configuration) and licenses appear in the dependency list. Third-party scanners work if they produce a CycloneDX report in the GitLab property taxonomy. The scanner recognises over 600 license types from the SPDX list.

## 2. License approval policy
License approval policies are merge request approval policies with a **License scanning** rule, created under Secure > Policies in a project linked to a security policy project (Owner role needed). They apply only to protected target branches.
- Deny list: require approval when any license in a list of prohibited licenses is detected.
- Allow list: require approval when any license is detected except those explicitly acceptable.
- Comparison with the default branch: a denied license can require approval only when it comes from a newly added dependency, or also when it exists in components already on the default branch.
A violating merge request is blocked until the license is removed or an eligible approver approves.

## 3. Gotchas
- The policy relies on dependency scanning job output; without it the policy has no data and by default fails closed (`fallback_behavior` can set fail open).
- Licenses are matched by SPDX name; `unknown` is not an SPDX name, so PURL exclusions do not work for unknown licenses, and unknown licenses can block merges until you add `unknown` to the allowed list temporarily or fix the component.

## Verify
- [ ] An MR adding a dependency with a denied license is blocked until approved or fixed.

## Checked

2026-10-28. Confirmed on the license scanning of CycloneDX files and license approval policies pages: legacy analyzer removed in 17.0 (the draft said 16.3), dependency scanning as the data source, Ultimate tier, SPDX names and 600+ license types, protected target branches only, deny/allow criteria, default-branch comparison criteria, fail-closed default with fallback_behavior, unknown-license troubleshooting. Removed: the policy YAML (license_finding, match_on_inclusion_license, license_states, newly_detected, group_approvers) because the fetched page does not document those keys, and the template name.
Method: documentation only; no commands were run.
