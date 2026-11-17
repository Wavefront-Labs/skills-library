---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-mobile-push-notifications
name: vaultwarden-mobile-push-notifications
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, push-notifications, mobile, push-installation-id, bitwarden-eu, firebase, android, ios]
level: practitioner
status: docs-checked
description: "Enable Vaultwarden mobile push notifications through the Bitwarden relay: installation ID and key, US versus EU variables, client requirements and region switching."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Enabling-Mobile-Client-push-notification"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden mobile push

Get an installation ID and key by entering your email at bitwarden.com/host. Then set:

```
PUSH_ENABLED=true
PUSH_INSTALLATION_ID=<id>
PUSH_INSTALLATION_KEY=<key>
# EU registrations only:
PUSH_RELAY_URI=https://api.bitwarden.eu
PUSH_IDENTITY_URI=https://identity.bitwarden.eu
```

Requirements: Vaultwarden 1.29.0+. Recreate the container (`docker compose up -d vaultwarden`) and log out and back in on every client. Apps connected before v1.30.2 need their app data cleared or a reinstall to register a push token. Use apps from the official stores (App Store, Google Play) or Aurora Store; F-Droid and other alternative builds lack Firebase Messaging support. Do not block `firebaseinstallations.googleapis.com`.

Switching regions: deauthorize all sessions and clear app data on the mobile app, then repeat setup with the other region; alternatively run `UPDATE devices SET push_uuid = NULL;` on the database (update Vaultwarden first).

Test: rename a folder in the web vault and check that the mobile app reflects it within seconds.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Enabling-Mobile-Client-push-notification.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
