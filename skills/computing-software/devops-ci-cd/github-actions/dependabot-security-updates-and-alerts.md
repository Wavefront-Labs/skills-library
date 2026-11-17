---
id: computing-software.devops-ci-cd.github-actions.dependabot-security-updates-and-alerts
name: dependabot-security-updates-and-alerts
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, dependabot-security-updates, dependabot-alerts, github-advisory-database, auto-triage-rules, dependency-review, security-updates]
level: practitioner
status: docs-checked
description: "Run Dependabot alerts and security updates on GitHub: enable at org scale, how security PRs differ from version updates, grouped security updates, auto-triage rules and dismissal."
sources:
  - https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates
  - https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
  - https://docs.github.com/en/code-security/dependabot/dependabot-auto-triage-rules/about-dependabot-auto-triage-rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dependabot security updates and alerts

Three separate features:
- **Dependabot alerts**: the dependency graph matched against the GitHub Advisory Database; alerts in the Security tab.
- **Dependabot security updates**: automatic PRs that bump a vulnerable dependency to the minimum patched version.
- **Version updates**: scheduled PRs from `dependabot.yml` for staying current (separate skill).

## Enable
Enable the dependency graph, Dependabot alerts and Dependabot security updates per repository or organisation from the code security settings; follow the cited GitHub Docs pages for current steps.

## How security PRs behave
- When an alert is raised for a vulnerable dependency in the dependency graph, Dependabot tries to fix it with a PR that updates to the minimum patched version.
- A `dependabot.yml` file can customise Dependabot behaviour (schedules, pull request settings); check the docs for which options apply to security updates.
- Grouped security updates exist to reduce the number of PRs; see the docs for the configuration.

## Triage
- Auto-triage rules: GitHub presets are rules curated by GitHub (one dismisses low-impact alerts for development-scoped dependencies); custom rules can dismiss or snooze alerts.
- Check whether the vulnerable code is actually used before dismissing an alert, and record why.
- List and dismiss alerts in bulk through the REST API for Dependabot alerts (see the REST docs for parameters and dismissal reasons).

## Process
- Set remediation deadlines per severity and track them in security overview.
- Require the dependency review action on PRs (`actions/dependency-review-action`, option `fail-on-severity`) to stop new vulnerable dependencies entering.

## Verify
- [ ] Security overview shows alerts and security updates enabled on all active repos.
- [ ] Open critical/high alerts have a PR, a dismissal reason, or an owner and due date.

## Checked
2026-10-28. Confirmed against the fetched GitHub Docs pages (about Dependabot security updates, about Dependabot alerts, about auto-triage rules): alerts come from the Advisory Database and dependency graph changes; security updates target the minimum patched version; `dependabot.yml` can be added to customise behaviour; GitHub presets are GitHub-curated rules including dismissal of low-impact development-scoped alerts; auto-triage rules can dismiss or snooze; `fail-on-severity` exists on the dependency review action.
Removed (not confirmed): the `gh api` enable and triage commands and `dismissed_reason` values, menu paths, `open-pull-requests-limit` behaviour, the `groups` snippet, lockfile-only transitive fixes, reachability statement, severity SLA days, and the auto-merge recipe.

Method: documentation only; no commands were run.
