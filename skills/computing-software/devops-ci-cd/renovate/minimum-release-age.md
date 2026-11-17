---
id: computing-software.devops-ci-cd.renovate.minimum-release-age
name: minimum-release-age
category: computing-software
field: devops-ci-cd
product: renovate
tags: [minimum-release-age, cooldown, supply-chain, renovate]
level: advanced
status: docs-checked
description: "Delay update suggestions with minimumReleaseAge as a dependency cooldown against malicious releases."
sources:
  - https://docs.renovatebot.com/key-concepts/minimum-release-age/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`minimumReleaseAge` makes Renovate wait a set time after a version is published before it suggests that update. Its purpose is supply chain safety, not slowing fast-moving projects: for that, use a per-package `schedule`. Other tools call it a dependency cooldown.

```json
{
  "packageRules": [
    {
      "matchDatasources": ["npm"],
      "minimumReleaseAge": "14 days"
    }
  ]
}
```

With that rule a version stays unsuggested for 14 days, giving researchers and scanners time to catch malicious code. Renovate waits per version; it does not wait for a quiet period.

How it behaves:

- While the age is not reached, the branch carries a pending status check, replaced by a passing one afterwards.
- The registry or datasource must supply the release timestamp, so that a package maintainer cannot specify a different timestamp from when the package was actually published. The default `minimumReleaseAgeBehaviour` is `timestamp-required`.
- `minimumReleaseAgeBehaviour=timestamp-optional` lets updates without timestamps proceed, logging a warning that also shows on the dashboard; remap it with `logLevelRemap` if unwanted.
- If your package manager has its own minimum age setting, configure both. Renovate uses the larger value, and setting Renovate's to `null` does not disable the manager's.

`internalChecksFilter` defaults to `strict`, so no branch is created until the `renovate/stability-days` check passes; the docs recommend `strict` with `minimumReleaseAge`. With automerge, PRs are created immediately but automerged only after the age passes. Transitive dependencies introduced by lock file updates may not get the age check from Renovate.

## Checked

2026-11-03. Confirmed against the Renovate Minimum Release Age page (purpose, 14-day example, pending status, timestamps, package manager interaction, `internalChecksFilter`, transitive dependencies) and the configuration options page (`minimumReleaseAge`, `minimumReleaseAgeBehaviour`, per-version waiting). Removed the claim that a Docker created annotation is untrusted.

Method: documentation only; no commands were run.
