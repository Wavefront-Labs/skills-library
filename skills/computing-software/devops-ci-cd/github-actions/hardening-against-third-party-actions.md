---
id: computing-software.devops-ci-cd.github-actions.hardening-against-third-party-actions
name: hardening-against-third-party-actions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, action-supply-chain, sha-pinning, pinning-actions, actions-allowlist, allowed-actions-policy, verified-creators, pull-request-target-safety, untrusted-input, script-injection, least-privilege-permissions, default-workflow-permissions, fork-pull-requests, require-approval-for-fork, dependabot-actions, pinact, ratchet, zizmor, actionlint, tj-actions-incident, cache-poisoning, artifact-poisoning, egress-filtering, harden-runner, step-security]
level: advanced
status: docs-checked
description: "Lock down GitHub Actions against compromised actions and poisoned PRs: SHA pinning, script injection, pull_request_target, fork approval, runners."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/approving-workflow-runs-from-public-forks", "https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization", "https://github.com/woodruffw/zizmor", "https://github.com/suzuki-shunsuke/pinact", "https://github.com/step-security/harden-runner"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening against third-party actions

**Goal:** a compromised upstream action or a malicious fork PR cannot exfiltrate secrets or push to your repos.
Jobs in a workflow can interact with and compromise each other, so one compromised action can reach all
repository secrets and may use `GITHUB_TOKEN` to write to the repository.

## 1. Pin actions, then keep them updated
- Pin to a full-length commit SHA. GitHub's reasoning: a bad actor adding a backdoor would need a SHA-1
  collision for a valid Git object payload. Keep a version comment next to the SHA so it stays readable.
- Pinning to a tag is only reasonable if you trust the creator. The "Verified creator" Marketplace badge
  means GitHub verified the author's identity, but a tag can still be moved or deleted if the repository
  is compromised.
- Where a workflow dependency lockfile is available for your repository, GitHub's docs call it the strongest
  protection and say it supersedes SHA pinning; check the current docs for availability.
- Audit the action's source: confirm secrets are not sent to unintended hosts or logged.
- The same rules apply to reusable workflows.
- Use Dependabot version updates for GitHub Actions to keep pinned references current.

## 2. Control changes to workflow files
Add `.github/workflows` to `CODEOWNERS` so workflow changes need designated reviewers. Enable CodeQL
scanning of Actions workflows, and consider OpenSSF Scorecards to find risky workflow dependencies.

## 3. Untrusted input
Expressions such as `${{ github.event.pull_request.title }}` interpolated into `run:` scripts allow
script injection. Preferred fix from GitHub: set the expression into an intermediate environment variable
and reference it as a shell variable in the script, instead of interpolating it inline.

## 4. Fork pull requests and privileged triggers
- Runs from a contributor's fork PR can require manual approval from a maintainer with write access; set the
  requirement at repository, organisation or enterprise level (see the fork-approval and organisation
  Actions settings pages). Runs awaiting approval for more than 30 days expire and are marked failed.
- Avoid `pull_request_target` unless needed; for privilege separation `workflow_run` is the better trigger.
  Do not explicitly check out untrusted code (fork PR code or repositories you do not control) in workflows
  using these triggers, and treat artifacts uploaded by other workflows with caution.

## 5. Runners
GitHub-hosted runners are ephemeral clean VMs. Self-hosted runners have no such guarantee and can be
persistently compromised by untrusted workflow code, so think about what sensitive material sits on the machine.
Automatically destroying a runner after each job is not a full fix, because there is no guarantee a runner
runs only one job and secrets passed as command-line arguments can be seen by another job on the same runner.
Use just-in-time runners created through the REST API (at most one job, then removed) with a clean environment.

## 6. Detect and respond
Rotate every secret the compromised action's job could read, and review workflow runs in the incident
window. Third-party tools (pinact, zizmor, harden-runner) are linked in the sources; read their own
documentation before relying on them.

## Verify
- [ ] No `uses:` references a tag or branch from an author you do not trust.
- [ ] No `pull_request_target` or `workflow_run` workflow checks out untrusted code.
- [ ] Fork approval is configured; workflow changes need CODEOWNERS review.

## Checked
2026-11-09. Confirmed against the GitHub docs "Secure use reference" page (raw source of the cited hardening guide) and the "Approving workflow runs from forks" page: third-party action risk, SHA pinning rationale, tag trust and Verified creator, lockfile note, auditing, reusable workflows, CODEOWNERS, CodeQL and Scorecards, Dependabot updates, intermediate environment variable fix, `pull_request_target` and `workflow_run` guidance, self-hosted and JIT runners, the 30-day approval expiry.
Removed as not confirmed on those pages: the tj-actions incident details, pinact/ratchet/zizmor/actionlint capabilities and commands, example SHA, allowlist menu paths, default token settings and "permissions resets others to none", "Require approval for all outside collaborators" default claims, cache and artifact poisoning rules, harden-runner egress settings, the `gh api` incident queries and the audit-log filter.
Method: documentation only; no commands were run.
