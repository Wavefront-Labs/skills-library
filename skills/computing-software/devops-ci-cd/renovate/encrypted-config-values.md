---
id: computing-software.devops-ci-cd.renovate.encrypted-config-values
name: encrypted-config-values
category: computing-software
field: devops-ci-cd
product: renovate
tags: [encrypted, private-key, pgp-encryption, renovate]
level: advanced
status: docs-checked
description: "Decrypt PGP-encrypted values in repository config with a self-hosted privateKey and publish a public key."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Repository config can carry secrets encrypted with PGP so the file is safe to commit. The Renovate administrator holds the private key and sets it in the global config; users encrypt with the public key.

Admin steps:

- Generate a PGP key pair: `gpg --full-generate-key`. Name and email do not matter, use a 4096-bit key, and do not configure a passphrase.
- Set `privateKey` (inline) or `privateKeyPath` (file path) in global config. `privateKeyOld` and `privateKeyPathOld` let you rotate keys by decrypting older values.
- Publish the public key, for example in a small HTML page like the one at app.renovatebot.com/encrypt, so users can encrypt values.

User side:

```json
{
  "hostRules": [
    {
      "matchHost": "registry.example.com",
      "encrypted": {
        "token": "<encrypted-value>"
      }
    }
  ]
}
```

The `encrypted` object appears in config; Renovate decrypts it at run time. Encrypted secrets must have at least an org/group scope (and optionally a repository scope): Renovate checks the scope against the current repository and warns and discards on a mismatch. The payload is JSON of the form `{"o": "<org>", "r": "<repo, optional>", "v": "<secret>"}` encrypted to the public key. When migrating from the legacy encryption to PGP, move the legacy key to `privateKeyOld` and put the PGP key in `privateKey`.

The `encryptedWarning` global option (advanced) is for admins who want to stop supporting encrypted config: when set to a string, Renovate logs that text as a warning where users see it, for example on the Dependency Dashboard, so they can migrate first.

## Checked

2026-11-09: read the privateKey, privateKeyOld, privateKeyPath, privateKeyPathOld and encryptedWarning sections of https://docs.renovatebot.com/self-hosted-configuration/ and the encrypted section of https://docs.renovatebot.com/configuration-options/. Corrected the `encryptedWarning` description; removed the advice on preferring environment based hostRules (not on the pages).

Method: documentation only; no commands were run.
