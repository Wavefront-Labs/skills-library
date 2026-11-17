---
id: computing-software.devops-ci-cd.renovate.changelog-fetching
name: changelog-fetching
category: computing-software
field: devops-ci-cd
product: renovate
tags: [changelogs, fetch-change-logs, release-notes, renovate]
level: intro
status: docs-checked
description: "How Renovate finds changelogs for PR bodies, and how to turn off or redirect changelog fetching."
sources:
  - https://docs.renovatebot.com/key-concepts/changelogs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate builds the changelog section of a PR in order:

1. Take a `sourceUrl` from the datasource response.
2. Otherwise check Renovate's internal `sourceUrl` data for the package.
3. Look the source URL up if it is on a supported platform such as GitHub.
4. Search for Releases metadata and common changelog filenames.
5. Keep only releases between the current and new versions.
6. Format and embed them in the PR body.

For private packages the algorithm is the same, but Renovate must be able to read the package, the registry must include the source URL, and Renovate must authenticate to the host that URL points to.

```json
{
  "fetchChangeLogs": "pr",
  "packageRules": [
    {
      "matchPackageNames": ["internal-lib"],
      "changelogUrl": "https://github.com/org/dummy"
    }
  ]
}
```

- `fetchChangeLogs` decides where to embed changelogs: `pr` (default), `branch` for the commit message too (not recommended due to size), or `off` if fetching causes problems.
- Override it per package with `packageRules`; later rules override earlier ones.
- `changelogUrl` does not fetch anything but adds a link to the PR body.
- Fetching changelogs from github.com needs a GitHub token. On GitHub Enterprise Server or any non-GitHub platform you must configure a github.com personal access token to fetch changelogs.

## Checked

2026-11-03. Confirmed against the Renovate changelogs key-concepts page (detection steps, private packages, `fetchChangeLogs`, `changelogUrl`, github.com token) and the configuration options page (`fetchChangeLogs` values and default, `packageRules.changelogUrl`). Removed: the `source-urls.json` file name, the invented `internal-lib` URL (replaced with the documented example) and the advice about large packages.

Method: documentation only; no commands were run.
