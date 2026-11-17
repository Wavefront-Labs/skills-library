---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-compromised-key-response
name: sealed-secrets-compromised-key-response
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, key-cutoff-time, compromised-key, secret-rotation, incident-response, early-renewal]
level: sme
status: docs-checked
description: "Respond to a leaked Sealed Secrets sealing key: force early renewal with --key-cutoff-time before rotating actual secret values and resealing them."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets compromised key response

If a sealing private key leaks, every SealedSecret encrypted with it must be considered compromised. Key renewal and re-encryption cannot undo that, especially if the old SealedSecret files sit in version control that you cannot erase. They are also no substitute for periodically rotating your real secret values.

Order of operations from the README:
1. Renew the sealing key immediately, before sealing any rotated secrets. Otherwise the new values are encrypted to the compromised key and the attacker gets them too.
2. Then neutralise the damage according to the secret's nature. For a database password: change it on the database, revoke the old one, and run `kubeseal` again to produce an updated SealedSecret.

Force early renewal by giving the controller a cutoff time, either the flag `--key-cutoff-time` or the environment variable `SEALED_SECRETS_KEY_CUTOFF_TIME`. The format is RFC1123, which `date -R` generates. A key is generated early when the current timestamp is passed as the cutoff.

The routine rule: periodically renew the sealing key and rotate the actual secrets. Either alone is moot, since an attacker with an old key could read new secrets sealed to it.

Labelling a key Secret as compromised (anything other than `active`) takes it out of the controller's active set, but only after a controller restart.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Secret Rotation, User secret rotation, Early key renewal, Manual key management, Details.
Confirmed: `--key-cutoff-time`, `SEALED_SECRETS_KEY_CUTOFF_TIME`, RFC1123 / `date -R`, order of operations, database password example, relabel needs restart.
Removed: nothing.
Method: documentation only; no commands were run.
