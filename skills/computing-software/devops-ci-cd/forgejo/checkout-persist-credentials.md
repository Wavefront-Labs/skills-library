---
id: computing-software.devops-ci-cd.forgejo.checkout-persist-credentials
name: checkout-persist-credentials
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [persist-credentials, actions-checkout, git-credentials, extraheader]
level: practitioner
status: docs-checked
description: "Stop actions/checkout credentials overriding your own API key when a workflow touches other repositories."
sources:
  - https://forgejo.org/docs/latest/user/actions/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Normally `actions/checkout` creates git credentials on the fly and writes them to the git config, for example an entry like `http.https://codeberg.org/.extraheader=AUTHORIZATION: basic ***`. For standard cases that is what you want.

The problem appears when a workflow must interact with other repositories, such as private ones, often with tools like renovate, using a different credential such as a scoped API key. Your credentials may be set correctly, yet the auto-generated key in the git config is still preferred, so operations against the other repositories fail.

The fix is to disable credential persistence in the checkout step:

```
- uses: https://code.forgejo.org/actions/checkout@v7
  with:
    persist-credentials: false
```

Note the docs use the full URL form of the action. The automatic workflow token itself is documented under basic concepts, with `FORGEJO_TOKEN` and the `GITHUB_TOKEN` aliases.

The page's typical case is a workflow that touches other private repositories, usually with renovate or similar tools, using an API key of a specific scope. If the logs shown in the web interface are incomplete, also look at the logs of the Forgejo Runner itself.

## Checked

2026-11-04. Confirmed against the Forgejo Actions Troubleshooting page (Forgejo Runner logs and Non-Standard Git Credentials sections) and the Basic concepts page for the token aliases. Nothing removed.

Method: documentation only; no commands were run.
