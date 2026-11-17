---
id: computing-software.cybersecurity-defensive.keycloak.realm-signing-keys-and-rotation
name: realm-signing-keys-and-rotation
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, realm-keys, key-rotation, rsa-generated, priority]
level: practitioner
status: docs-checked
description: "Rotate Keycloak realm signing keys with no downtime: add a higher-priority provider, make the old one passive, delete it later; handle compromised keys."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/realms/keys.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# realm signing keys and rotation
A realm has one active key pair at a time plus any number of passive keys. The active pair creates new signatures; passive keys can verify earlier ones, so rotation needs no downtime. A key pair and self-signed certificate are generated when the realm is created.

A key pair can show status Active and still not be the realm's selected pair: the selected pair comes from the first key provider, sorted by priority, that can provide an active key pair.

Rotation (Admin Console, *Realm settings* > *Keys* tab > *Providers* tab):
1. *Add provider* and select `rsa-generated` (use `rsa` to upload an existing PEM private key and optional X509 certificate, `java-keystore` to load from a Java Keystore).
2. Enter a *Priority* higher than the existing active keys; the highest number becomes active. Creating the new keys with the same priority and making the previous keys passive also works.
3. Pick the AES Key size value and *Save*. Changing a provider's priority does not regenerate keys; editing the key size generates new ones.
4. Later make the old provider passive (open it, toggle *Active* Off, *Save*), and finally remove it. Toggling *Enabled* Off disables a provider.

After the new keys exist, new tokens and cookies are signed with them: the SSO cookie updates when the user authenticates and refreshed OIDC tokens get the new signature. The docs suggest creating new keys every three to six months and deleting old keys one to two months after the new ones. A user inactive across that gap must re-authenticate. Offline tokens also need refreshing before the old keys are removed.

Compromised keys: generate a new key pair first, then immediately remove the compromised pair (or delete its provider). Then in *Clients* > `security-admin-console` fill the Admin URL (Access settings), go to the *Advanced* tab, click *Set to now* in Revocation and *Push*. This makes clients reject existing tokens and fetch the new keys. REST and confidential clients must set Admin URL so Keycloak can send them the not-before push.

## Checked
2026-11-03. Confirmed against server_admin/topics/realms/keys.adoc. Removed: the "deleting too early invalidates tokens" gotcha as worded, and the JWKS Verify step (the page does not cover the certs endpoint). Added the passive/disable and compromised-key procedures from the page.
Method: documentation only; no commands were run.
