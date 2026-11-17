---
id: computing-software.cybersecurity-defensive.cosign.registry-login
name: registry-login
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, login, password-stdin, registry-credentials]
level: intro
status: docs-checked
description: "Authenticate to a registry with cosign login, keeping the password off the command line using --password-stdin."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_login.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign login

```
cosign login [OPTIONS] [SERVER]
cosign login reg.example.com -u USER --password-stdin < /path/to/password-file
```

Flags: `-u, --username`, `-p, --password`, `--password-stdin` ("Take the password from stdin").

The docs example passes `-p` on the command line; `--password-stdin` takes the password from stdin instead:

```
echo "$REGISTRY_TOKEN" | cosign login reg.example.com -u USER --password-stdin
```

Alternatives: explicit `--registry-username/--registry-password/--registry-token` per command (see registry-auth-flags) or `--k8s-keychain` in clusters (see k8s-keychain).

## Checked

2026-11-04. Confirmed on the cosign login reference page: usage line, `-u`, `-p`, `--password-stdin` text and the example with `-p`. Removed: the shell-history rationale, the claim that later commands use the stored credential via the default keychain and the read-only credential note (none on the page).

Method: documentation only; no commands were run.
