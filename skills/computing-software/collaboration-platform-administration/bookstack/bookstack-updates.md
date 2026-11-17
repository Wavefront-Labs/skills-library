---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-updates
name: bookstack-updates
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, update, upgrade, git-pull, composer, artisan-migrate, clear-cache, system-cli]
level: practitioner
status: docs-checked
description: "Update BookStack from the release branch with git pull, composer install and artisan migrate, optional download-vendor system CLI, and cache clearing."
sources: ["https://www.bookstackapp.com/docs/admin/updates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack updates

Back up the database and uploads first. Updating is done with Git from the BookStack root:

```
git pull origin release
composer install --no-dev
php artisan migrate
```

Beta alternative without Composer (needs v25.02.1 or later):

```
git pull origin release
./bookstack-system-cli download-vendor
php artisan migrate
```

Clearing caches afterwards is recommended:

```
php artisan cache:clear
php artisan config:clear
php artisan view:clear
```

Releases are listed on the project's Codeberg releases page and announced on the blog; check the Version Specific Instructions in the docs for the version you move to, because some releases need extra steps.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/updates/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: the claim to pull 'not the development branch', which the page does not state.
Method: documentation only; no commands were run.
