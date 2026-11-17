---
id: computing-software.cybersecurity-defensive.keycloak.kcadm-realm-key-rotation
name: kcadm-realm-key-rotation
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, kcadm, key-rotation, components, rsa-generated]
level: practitioner
status: docs-checked
description: "Rotate Keycloak realm keys from the command line: add a higher-priority rsa-generated or java-keystore provider with kcadm, make the old one passive, delete it."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/admin-cli.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kcadm realm key rotation
Key providers are components, so kcadm can rotate keys without the console. Assumes an authenticated kcadm session and a target realm `demorealm`.

1. List current keys: `kcadm.sh get keys -r demorealm`.
2. Get the realm id (used as `parentId`): `kcadm.sh get realms/demorealm --fields id --format csv --noquotes`.
3. Add a provider with a higher priority than the existing providers shown in step 1:
```
kcadm.sh create components -r demorealm -s name=rsa-generated -s providerId=rsa-generated -s providerType=org.keycloak.keys.KeyProvider -s parentId=<realm-id> -s 'config.priority=["101"]' -s 'config.enabled=["true"]' -s 'config.active=["true"]' -s 'config.keySize=["2048"]'
```
4. Run `kcadm.sh get keys -r demorealm` again; the new key is now the active key.

Java Keystore: create a component the same way with `providerId=java-keystore` and `config.priority`, `config.enabled`, `config.active`, `config.keystore`, `config.keystorePassword`, `config.keyPassword` and `config.keyAlias` (each value a JSON array of one string); change them to match your keystore.

Make the old key passive or disable it: identify the key with `get keys`, use its `providerId` in the endpoint `components/PROVIDER_ID`, then
```
kcadm.sh update components/PROVIDER_ID -r demorealm -s 'config.active=["false"]'
```
Set `config.enabled=["false"]` to disable it, or `config.priority=["110"]`-style values to change priority.

Delete an old key: ensure it is inactive and disabled first, so tokens held by applications and users do not fail, then `kcadm.sh delete components/PROVIDER_ID -r demorealm`.

See realm-signing-keys-and-rotation for the console procedure and the rotation timing the docs suggest.

## Checked
2026-11-03. Confirmed against server_admin/topics/admin-cli.adoc (Generating new realm keys, Java Key Store, passive/disable, deleting an old key). Changed the priority example to the page's 101 and the name to rsa-generated; removed the unsourced gotchas and the JWKS/ACTIVE Verify step.
Method: documentation only; no commands were run.
