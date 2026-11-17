---
id: computing-software.data-engineering.apache-nifi.sensitive-properties-key
name: sensitive-properties-key
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, sensitive-properties, encryption, nifi-properties, cluster]
level: practitioner
status: docs-checked
description: "nifi.sensitive.props.key and nifi.sensitive.props.algorithm: minimum length 12, recommended Argon2 and PBKDF2 algorithms, auto-generation on new standalone installs."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive properties key

NiFi encrypts sensitive processor and service properties in the flow definition using:
- `nifi.sensitive.props.key`: the password the encryption key is derived from; the guide says the key-derivation algorithms require at least 12 characters. For new standalone installs of 1.14.0 or later NiFi generates a random value if it is empty, writes it to nifi.properties and logs a warning. Clustered installs need the same value on all nodes, and the guide says not to change it once sensitive properties are configured (use `bin/nifi.sh set-sensitive-properties-key` to change it).
- `nifi.sensitive.props.algorithm`: the guide lists `NIFI_ARGON2_AES_GCM_256` and `NIFI_PBKDF2_AES_GCM_256` as the strong methods (the 128-bit variants and the Bcrypt and Scrypt ones are deprecated); the nifi.properties table gives `NIFI_PBKDF2_AES_GCM_256` as the default. Change it with `bin/nifi.sh set-sensitive-properties-algorithm <algorithm>`.

The encrypt-config tool takes a new sensitive properties key with `-s`; in the guide's migration example `-x` tells it to process only the sensitive properties.

Verify: NiFi starts without a sensitive-key warning and processors with passwords stay valid after restart.

## Checked

Confirmed in the NiFi Administration Guide: Encrypted Passwords in Flows (algorithm list and deprecations), the 12 character requirement and the 1.14.0 auto-generation behaviour, the same-value-on-all-nodes note, the nifi.properties default algorithm, the set-sensitive-properties-key and set-sensitive-properties-algorithm commands, and the encrypt-config -s and -x flags. The earlier claims that -x re-encrypts flow.xml.gz only and that the guide states no default algorithm were corrected.

Method: docs-only read of cited pages, 2026-11-08
