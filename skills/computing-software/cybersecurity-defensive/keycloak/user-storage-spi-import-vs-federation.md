---
id: computing-software.cybersecurity-defensive.keycloak.user-storage-spi-import-vs-federation
name: user-storage-spi-import-vs-federation
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, user-storage-spi, import-strategy, user-cache, federation]
level: practitioner
status: docs-checked
description: "Choose between importing external users into Keycloak and federated storage in a custom User Storage SPI, and manage the user cache."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/user-storage/import.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# user storage spi import vs federation
Two strategies for a user storage provider:
- **Import**: create the user locally in Keycloak's built-in user database and copy attributes from the external store. Keycloak becomes a persistent user cache for the external store, so once a user is imported you no longer hit the external store, and you can migrate applications gradually, then unlink the imported users and retire the legacy store. Downsides: looking up a user for the first time needs multiple updates to the Keycloak database (a possible performance loss under load), and you must keep local and external storage in sync (the SPI has capability interfaces for synchronisation, which the docs say can quickly become painful and messy).
- **Federated storage** (no import): Keycloak stores only extra data as needed, which may never be used depending on the external store's capabilities.

To implement import: check whether the user has been imported; if so return the local user, otherwise create it locally (via `UserProvider.addUser`, do not set the id yourself) and import the data. Call `UserModel.setFederationLink()` with the provider's `ComponentModel` id; imported users are removed when the provider is removed. You can proxy the local user with `UserModelDelegate` to synchronise changes. If a local user is linked, your provider is still consulted for `CredentialInputValidator` and `CredentialInputUpdater`; returning false makes Keycloak try local storage.

Interfaces: `ImportedUserValidation.validate(realm, user)` is called whenever a linked local user is loaded and may return a proxied user, or `null` to remove the local user (for example when it no longer exists in the external store). `ImportSynchronization` handles local copies drifting from external storage, for example users removed externally. If your provider implements `UserRegistrationProvider`, `removeUser()` need not remove the local user; the runtime does that after calling it.

## Checked
2026-11-03. Confirmed against server_development/topics/user-storage/import.adoc. Removed (not on the page): the `UserCache` eviction API (`evict`, `clear`) and cluster-invalidation statements, the provider lifecycle sentence, the gotchas and the Verify step.
Method: documentation only; no commands were run.
