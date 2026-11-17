---
id: computing-software.collaboration-platform-administration.nextcloud.two-factor-provider-cleanup-and-disable
name: two-factor-provider-cleanup-and-disable
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [twofactorauth-cleanup, twofactorauth-disable, occ, lost-second-factor, providers]
level: advanced
status: draft
description: "Recover a user who lost their second factor with occ twofactorauth:disable, and clear stale provider records with twofactorauth:cleanup."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/two_factor-auth.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: fix 2FA problems without database edits.

Case 1, a user lost or forgot their second factor. Disable that provider for the user:

```
sudo -E -u www-data php occ twofactorauth:disable <uid> <provider_id>
```

Afterwards the user can enable the provider again in their personal settings.

Case 2, a provider app was removed or disabled. Nextcloud keeps a record of each user's enabled providers. If a provider is merely removed or disabled, Nextcloud still treats it as active for the user at login and shows a warning that at least one enabled two-factor method could not be loaded.

Clean up the stored associations:

```
sudo -E -u www-data php occ twofactorauth:cleanup <provider_id>
```

Warning from the docs: this is irreversible. Run it only for providers you do not intend to enable again, because each user would have to set the provider up again from scratch.

Working order for the second case:
1. Decide whether the provider is gone for good.
2. If yes, run cleanup with the provider id.
3. If you only turned it off temporarily, re-enable the app instead.


Check: the user logs in without the unloadable-provider warning.
