---
id: computing-software.cybersecurity-defensive.cosign.env-variables
name: env-variables
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, env, show-sensitive-values, cosign-password, environment-variables]
level: practitioner
status: docs-checked
description: "List cosign's environment variables with cosign env, show descriptions or sensitive values, and the variables named across the docs."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_env.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_pkcs11-tool_list-keys-uris.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign env

"Prints Cosign environment variables."

```
cosign env
cosign env --show-descriptions
cosign env --show-descriptions --show-sensitive-values
```

`--show-descriptions` defaults to true. `--show-sensitive-values` shows values of sensitive environment variables.

Variables mentioned in these docs:
- `COSIGN_PASSWORD`: private key password (generate-key-pair, import-key-pair).
- `COSIGN_REPOSITORY`: store signatures in another repository (see cosign-repository-env).
- `COSIGN_DOCKER_MEDIA_TYPES=1`: legacy media types (see docker-media-types-legacy).
- `COSIGN_PKCS11_PIN`: PKCS11 PIN when `--pin` is empty.
- `env://[ENV_VAR]` as a key reference.

The authoritative list for your version is the output of `cosign env --show-descriptions`; use it instead of memory.


## Checked

2026-11-04. Confirmed on the cosign env reference page (description, the three examples, flag text and `--show-descriptions` default true), the pkcs11-tool list-keys-uris page (COSIGN_PKCS11_PIN when `--pin` is empty), the generate-key-pair and import-key-pair pages (COSIGN_PASSWORD), the README (COSIGN_REPOSITORY, COSIGN_DOCKER_MEDIA_TYPES) and the verify page (`env://`). Removed: the CI masking advice and the log-avoidance remark.

Method: documentation only; no commands were run.
