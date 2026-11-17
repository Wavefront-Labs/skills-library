---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.release-policy-enforcement-and-deployment-gates
name: release-policy-enforcement-and-deployment-gates
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [release-policy-enforcement, deployment-gates, release-engineering, branch-protection, environments, policy-as-code]
level: practitioner
status: docs-checked
description: "Enforce release policies in tooling: who may release, required reviews and checks, and deployment gates using GitHub branch protection and environments."
sources: ["https://sre.google/sre-book/release-engineering/", "https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Enforcing release policies and deployment gates

SRE Book, Release Engineering, "Enforcement of Policies and Procedures": several layers of security and access
control determine who can perform specific operations when releasing a project. Gated operations at Google
include approving source code changes, specifying the actions of the release process, creating a new release,
approving the initial integration proposal and later cherry picks, deploying a new release, and changing a
project's build configuration. Almost all changes to the codebase require a code review, and the automated
release system produces a report of every change in a release, archived with the build artifacts, which speeds
troubleshooting. During release the unit tests are re-run on the release branch with an audit trail, because
cherry picks can make the release branch differ from anything on the mainline. Policies only written in docs
are not enforced: put them in the tooling.

## GitHub controls that map to those gates
| Policy | GitHub mechanism (documented) |
|---|---|
| Code reviewed before merge | Branch protection: require pull request reviews with a set number of approvals; optionally require review from code owners |
| Tests pass | Branch protection: require status checks before merging (strict by default: branch must be up to date with base; loose does not require that) |
| Only chosen people deploy | Environment required reviewers: up to 6 people or teams, only one needs to approve; optionally prevent self-review |
| Delay before deploy | Environment wait timer, set in minutes |
| Only certain refs deploy | Environment deployment branches and tags rule |
| Custom checks | Custom deployment protection rules created with GitHub Apps |
| Secrets only after approval | Environment secrets are available to jobs only after configured rules pass |
| Admins cannot bypass | Environment option: deselect "Allow administrators to bypass configured protection rules" |

Notes: environments on GitHub Free are configurable only for public repositories; if a repository goes from
public to private, configured protection rules and environment secrets are ignored. With required status checks,
keep job names unique across workflows, since duplicates cause ambiguous results that can block merges.

## GitHub Actions environment gate
```yaml
jobs:
  deploy-prod:
    environment: production    # reviewers, wait timer and branch rules configured on the environment
    runs-on: ubuntu-latest
    steps:
    - name: Deploy
      run: ./deploy.sh
```

## Beyond GitHub
Freeze windows, error-budget checks, canary analysis and image signature verification are policies you build
from your own tooling (see `error-budget-policy-threshold-actions` and `canary-metrics-selection-and-evaluation`);
check the docs of the admission or policy tool you choose, as none are covered by the sources here.

## Gotchas
- Gates need an audited emergency path; otherwise people bypass them.
- Gates enforced only in CI are bypassed by anyone with direct write access to the target system.

## Verify
- [ ] An unreviewed commit cannot reach production (try it).
- [ ] Emergency deploys are logged and reviewed.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Release Engineering page (policy enforcement section), the GitHub documentation page on using environments for deployment (reviewers, wait timer, admin bypass, branch rules, secrets, plan limits) and the GitHub protected-branches page (required reviews, code owners, status checks strict versus loose, unique job names). Removed: the Kyverno cluster policy, the freeze-date shell check, kubectl set image, the "include administrators" branch-protection advice and the signed-image rows, none of which appeared on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
