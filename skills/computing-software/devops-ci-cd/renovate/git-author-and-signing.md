---
id: computing-software.devops-ci-cd.renovate.git-author-and-signing
name: git-author-and-signing
category: computing-software
field: devops-ci-cd
product: renovate
tags: [git-author, git-private-key, signed-commits, renovate]
level: advanced
status: docs-checked
description: "Set the commit author, sign commits with gitPrivateKey and skip hooks using gitAuthor and related options."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate commits as an author you can configure.

- `gitAuthor` sets the commit author. It must conform to RFC5322; include a name followed by an email address, for example `Development Bot <dev-bot@example.com>`. The docs do not recommend customising it: when unset, Renovate discovers its account's Git author from its platform credentials.
- `gitIgnoredAuthors` lists commit author emails Renovate ignores when deciding whether a PR was modified. Entries can be exact RFC5322 strings, globs or regexes.
- `gitPrivateKey` (global) is a private PGP or SSH key for signing commits. For PGP use an armored key with newlines replaced by `\n`. It cannot be passphrase protected in a headless environment. `gitPrivateKeyPassphrase` is supported for SSH keys only; for a GPG key it is ignored with a warning.
- `gitNoVerify` (global) lists which Git commands run with `--no-verify`: `commit`, `push`, or both (the default).
- `gitTimeout` (global) is a number of milliseconds to wait after the last received output before sending SIGINT to a hung Git process (default 0).
- `gitUrl` (global) overrides Git remote resolution: `default` (platform HTTPS URLs), `ssh` or `endpoint`.

```json
{
  "gitAuthor": "Renovate Bot <bot@example.com>",
  "gitPrivateKey": "-----BEGIN PGP PRIVATE KEY BLOCK-----...",
  "platformCommit": "enabled"
}
```

`platformCommit` (values `auto`, `disabled`, `enabled`) applies only when you run Renovate as a GitHub App, not with a personal access token. When enabled, Renovate creates commits through GitHub's API, so GitHub's commit signing for bots applies, and GitHub sets the author so Renovate's `gitAuthor` is ignored. Otherwise sign with `gitPrivateKey`.

Before the first commit in a repository, Renovate loads `gitPrivateKey` lazily: it runs `gpg import` for PGP and sets `user.signingkey`, `commit.gpgsign` and `gpg.format` locally in the cloned repo, not globally.

By default Renovate treats a PR as modified when another Git author adds to the branch, and then makes no further commits. If other bots commit on top of Renovate PRs, add their emails to `gitIgnoredAuthors`.

## Checked

2026-11-09: read the gitNoVerify, gitPrivateKey, gitPrivateKeyPassphrase, gitTimeout and gitUrl sections of https://docs.renovatebot.com/self-hosted-configuration/ and gitAuthor, gitIgnoredAuthors and platformCommit in https://docs.renovatebot.com/configuration-options/. Corrected the gitAuthor default and advice, the gitPrivateKey key types and passphrase support, and gitNoVerify values.

Method: documentation only; no commands were run.
