---
id: computing-software.devops-ci-cd.packer.github-api-token
name: github-api-token
category: computing-software
field: devops-ci-cd
product: packer
tags: [github-api-token, rate-limit, ci, packer-init, plugins-install, configure]
level: intro
status: docs-checked
description: "Set PACKER_GITHUB_API_TOKEN so packer init does not hit GitHub's unauthenticated rate limit in CI."
sources:
  - "https://developer.hashicorp.com/packer/docs/plugins/install-plugins/"
  - "https://developer.hashicorp.com/packer/docs/configure/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When `packer init` resolves plugins hosted on GitHub it queries the public GitHub API, which limits unauthenticated requests per hour from one IP address. Shared CI runners hit the limit easily.

Set `PACKER_GITHUB_API_TOKEN` to a GitHub token and Packer authenticates its requests, raising the limit:

```bash
export PACKER_GITHUB_API_TOKEN=<token>
packer init .
```

The plugin docs recommend setting a token whenever Packer runs on a continuous integration server, to avoid rate-limiting errors. The configuration reference describes the variable the same way.

Related approaches that avoid the API altogether:

- Host a mirror laid out like releases.hashicorp.com.
- For HashiCorp's own plugins on Packer 1.14.0 or later, the download comes from the HashiCorp release site.

## Checked
2026-11-03. Confirmed against the Install plugins page (GitHub API token section, mirror layout, Packer 1.14.0) and the Configure Packer page. Removed the plugin-cache bullet, token-scope advice and the error-message tip, none of which the pages state.
Method: documentation only; no commands were run.
