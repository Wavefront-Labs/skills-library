---
id: computing-software.devops-ci-cd.renovate.security-model-self-hosted
name: security-model-self-hosted
category: computing-software
field: devops-ci-cd
product: renovate
tags: [security, trust-repository-developers, least-privilege, renovate]
level: advanced
status: docs-checked
description: "Security guidance for running Renovate yourself: who you trust, what code can run, logging and least privilege."
sources:
  - https://docs.renovatebot.com/security-and-permissions/
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Running Renovate self-hosted means decisions about trust. The docs cover trusting repository developers: a developer who can change repository config can influence what the bot reads and, if you allow it, what it executes.

Risks they describe:

- Access to information: the update process runs with the same user privileges as the Renovate process, so it can reach the same information and resources.
- Execution of code from an insider: `postUpgradeTasks` scripts, repository wrappers such as `gradlew` (with `allowedUnsafeExecutions=["gradleWrapper"]`), `mise` and `pixi` (also via `allowedUnsafeExecutions`). The project does not issue CVEs for such insider attacks other than in exceptional circumstances.
- Execution of code from an outsider (not an exhaustive list): Gradle updates evaluate the build script, `postUpgradeTasks` that use an updated dependency, and package manager scripts (`npm install`, `composer install`, lock file maintenance) when `allowScripts=true` is combined with `ignoreScripts=false`.
- Sensitive information ending up in centralized logs, for example from `customEnvVariables`.

Recommendations from the docs:

- Vet repositories before integrating them: ownership, contribution history, open issues and pull requests.
- Run Renovate with least privilege.
- Review `postUpgradeTasks` regularly and restrict them to an `allowedCommands` allowlist (an empty list runs no tasks). An allowlisted command such as `make lint-fix` can still run other commands, including `npm install --foreground-scripts`, which bypasses `allowScripts`.
- `allowShellExecutorForPostUpgradeCommands=true` lets commands use shell semantics, so they can call other commands unless `allowedCommands` restricts them.
- Use security tools such as code scanning on the Renovate config and managed repositories.
- Reference sensitive `customEnvVariables` with the secrets syntax `{{ secrets.VAR_NAME }}`. Renovate passes only a limited set of environment variables to package managers; `exposeAllEnv=true` exposes all of them, so use it only for repositories you have reviewed and trust, or hand-pick variables with `customEnvVariables`.
- Treat logs as sensitive (encryption, access controls, secure storage) and review or redact them.
- Apply Renovate updates and watch its security advisories; report vulnerabilities through GitHub Security Advisories.

The Mend Renovate App's privacy and permission tables are on the same page; self-hosted Renovate does not phone home except when Merge Confidence badges are requested.

## Checked

2026-11-08: read the whole Security and Permissions page (raw source of docs.renovatebot.com/security-and-permissions) plus the `allowedCommands`, `allowScripts`, `allowShellExecutorForPostUpgradeCommands` and `exposeAllEnv` sections of the self-hosted configuration page (partial read of that page; the `allowScripts` section there is empty). Confirmed the trust model, insider and outsider code execution cases, the recommendations, an empty `allowedCommands` running no tasks, and `exposeAllEnv` behaviour. Removed the claim that package manager scripts are disabled by default (not confirmed), the example config block and the unsourced isolated-container advice.
Method: documentation only; no commands were run.
