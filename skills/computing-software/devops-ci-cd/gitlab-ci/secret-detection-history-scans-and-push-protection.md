---
id: computing-software.devops-ci-cd.gitlab-ci.secret-detection-history-scans-and-push-protection
name: secret-detection-history-scans-and-push-protection
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, secret-detection-historic, secret-push-protection, secret-detection-template, skip-secret-push-protection, history-scan, git-history-secrets]
level: practitioner
status: docs-checked
description: "Detect secrets in GitLab: pipeline secret detection, full-history scans with SECRET_DETECTION_HISTORIC_SCAN, secret push protection that blocks pushes, and skip options."
sources: ["https://docs.gitlab.com/user/application_security/secret_detection/pipeline/", "https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secret detection: history scans and push protection

## 1. Pipeline secret detection
```yaml
include:
  - template: Jobs/Secret-Detection.gitlab-ci.yml
```
By default scans the commits of the push/MR. One-off **full history** scan:
```yaml
secret_detection:
  variables:
    SECRET_DETECTION_HISTORIC_SCAN: "true"
```
Run it once via a manual pipeline (`Run pipeline` with that variable) when onboarding a repo
(GitLab recommends a historic scan right after enabling the analyzer). Other knobs: `SECRET_DETECTION_EXCLUDED_PATHS`,
`SECRET_DETECTION_LOG_OPTIONS` (git log range).
On Ultimate, results also appear in merge request reports, the pipeline security report and the vulnerability report.

## 2. Secret push protection (Ultimate)
Secure → Security configuration → **Secret push protection** on. Pushes containing
secret patterns (secret types such as GitLab personal access tokens and AWS access keys) are
**rejected** by the server, before the secret enters the repo.
Bypass (audited) when it is a false positive or test fixture:
```bash
git commit -m "add fixture [skip secret push protection]"
git push -o secret_push_protection.skip_all
```
Use exclusions for recurring fixtures. Personal access tokens with a custom prefix are not detected.

## 3. When a secret is found
Revoke/rotate first — removing it from git does not un-leak it (forks, clones, CI logs).
GitLab attempts to automatically revoke some types of leaked secrets; revoke the others manually.

## Gotchas
- Push protection only checks the diffs of pushed commits (diff-only scanning since 17.11), and is skipped when a push changes more than 3,150 paths or 350,000 lines; it is not a history scanner.
- `[skip secret push protection]` usage shows in audit events — review weekly.

## Verify
- [ ] Pushing a dummy token of a detectable type to a scratch branch is rejected.
- [ ] Historic scan report reviewed and every finding revoked or dismissed with a reason.

## Checked

2026-10-28. Confirmed on the pipeline secret detection and secret push protection pages: Jobs/Secret-Detection template, SECRET_DETECTION_HISTORIC_SCAN, SECRET_DETECTION_EXCLUDED_PATHS, SECRET_DETECTION_LOG_OPTIONS, Ultimate tier for push protection, Secure > Security configuration toggle, the git push option secret_push_protection.skip_all and the [skip secret push protection] commit message, diff-only scanning and the 3,150 path / 350,000 line threshold, automatic revocation of some secret types. Removed: glpat- prefix claim, ruleset file path, git filter-repo and job erase steps, auto-revoke-in-public-projects claim.
Method: documentation only; no commands were run.
