---
id: computing-software.cybersecurity-defensive.application-security.openssf-scorecard-assessment
name: openssf-scorecard-assessment
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [supply-chain-security, openssf-scorecard, scorecard-action, open-source-risk, branch-protection, dependency-evaluation]
level: practitioner
status: docs-checked
description: "Run OpenSSF Scorecard on your repos and on dependencies you adopt, interpret each check, and fix low scores like branch protection, token permissions and pinning."
sources: ["https://github.com/ossf/scorecard/blob/main/README.md", "https://github.com/ossf/scorecard/blob/main/docs/checks.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSF Scorecard assessment

**Goal:** a measurable security-hygiene score for your own repositories, and a quick risk signal for open-source packages before adoption.

## Run it
- CLI: `scorecard --repo=github.com/org/repo`; authenticate with a token in `GITHUB_AUTH_TOKEN` (GitHub rate-limits unauthenticated calls); `--format=json` for automation; `--checks=Code-Review,Branch-Protection` to run a subset.
- GitHub Action `ossf/scorecard-action` (the README's easiest route for repos you own); alerts appear in the repository Security tab. `publish_results: true` makes results available on the REST API and enables the badge.
- Existing results for public projects come from the Scorecard REST API (see the README for the current host).

## Key checks and fixes
| Check | Fix |
|---|---|
| Branch-Protection | Block force pushes and branch deletion, require at least one reviewer, a passing status check, then two reviewers and code owner review (tiered scoring) |
| Code-Review | Recent changes approved by someone other than the committer; bot reviews do not count |
| Token-Permissions | Top-level workflow permissions read-only; declare write permissions per job |
| Pinned-Dependencies | Pin by hash: Docker images, GitHub Actions to full commit SHA, lock files for applications |
| Dangerous-Workflow | No `pull_request_target` or `workflow_run` with an explicit PR checkout; no untrusted context values (e.g. issue titles) in inline scripts |
| Maintained / Vulnerabilities | Recent commit activity; Vulnerabilities uses OSV for open unfixed issues |
| SAST, Fuzzing, Signed-Releases, Security-Policy | CodeQL or SonarCloud; OSS-Fuzz or ClusterFuzzLite; signature files on release assets; a SECURITY.md with contact and disclosure terms |

## Using scores for dependencies
The README defines each check as 0 to 10 and the aggregate as a risk-weighted average, and warns that aggregates hide which behaviours are missing. Read per-check results, not just the total; the README sets no pass/fail threshold, so choose your own and record it.

## Gotchas
- Several Branch-Protection settings need an admin token; without one the administrator requirements are treated as met, so scores can mislead.
- Maintained only applies to projects older than 90 days.

## Verify
- [ ] Scheduled Scorecard runs on all owned public repos.
- [ ] Dependency intake process records a Scorecard result.

## Checked
2026-11-01. Confirmed in the ossf/scorecard README (CLI `--repo`, token env var, `--format`, `--checks`, scorecard-action, `publish_results`, score range and weighted aggregate) and docs/checks.md (all check behaviours above, admin-token note, 90-day Maintained rule). Removed: SARIF upload, deps.dev, api.securityscorecards.dev host, `read-all`, rulesets, example threshold, SBOM-free guesses; none are stated on the pages read.
Method: documentation only; no commands were run.
