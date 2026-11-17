---
id: computing-software.data-engineering.apache-nifi.encrypt-config-tool
name: encrypt-config-tool
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, toolkit, encrypt-config, secrets, nifi-properties, key-management]
level: advanced
status: docs-checked
description: "encrypt-config.sh flags for NiFi: input/output files, root key via -k or -p, migration with -m, protection schemes (AES_GCM default plus vault and cloud KMS) and Registry mode."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/toolkit-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# encrypt-config

`./bin/encrypt-config.sh`, NiFi mode flags:
- Files: `-n` nifi.properties in, `-o` out; `-l`/`-i` login-identity-providers.xml; `-a`/`-u` authorizers.xml; `-f`/`-g` flow.xml.gz; `-b` bootstrap.conf (holds the root key).
- Key: `-k` raw hex key, `-p` password, `-r` prompt for raw key; `-e`/`-w` old key/password.
- `-S` scheme (default `AES_GCM`), `-H` old scheme (default `AES_GCM`).
- `-m` migrate, `-x` re-encrypt flow.xml.gz only, `-s` props key for it, `-c` translate for the CLI, `-v` verbose.

Schemes: `AES_GCM`, `HASHICORP_VAULT_TRANSIT`, `HASHICORP_VAULT_KV`, `AWS_KMS`, `AWS_SECRETSMANAGER`, `AZURE_KEYVAULT_KEY`, `AZURE_KEYVAULT_SECRET`, `GCP_KMS`. Cipher is AES/GCM 256-bit with JCE unlimited policy, else 128-bit.

Registry mode: `--nifiRegistry` with `-r`/`-R`, `-a`/`-A`, `-i`/`-I`, `-b`/`-B`; `--decrypt` with `-r` prints decrypted content to stdout.

Verify: sensitive values in the output files carry the protected marker and NiFi starts.

## Checked

Checked against the NiFi Toolkit Guide, Encrypt-Config Tool section: the NiFi and Registry option lists, the eight protection scheme names, the AES/GCM 128 or 256-bit rule and the `.protected` / `encryption` markers all match the page. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08
