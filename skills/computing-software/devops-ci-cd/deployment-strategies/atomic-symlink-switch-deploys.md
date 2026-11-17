---
id: computing-software.devops-ci-cd.deployment-strategies.atomic-symlink-switch-deploys
name: atomic-symlink-switch-deploys
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, atomic-symlink-deploy, deployment-automation, rollback]
level: practitioner
status: docs-checked
description: "Deploy to servers over SSH with release directories and an atomic symlink switch (Capistrano style): layout, ln -sfn, shared files, cleanup and instant rollback."
sources: ["https://capistranorb.com/documentation/getting-started/structure/", "https://man7.org/linux/man-pages/man2/rename.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomic symlink-switch deploys over SSH

## Layout
```
/srv/app/
  releases/20261018T101500Z-9a1b2c3/
  releases/20261017T160000Z-1d2e3f4/
  shared/{.env,storage,logs}
  current -> releases/20261018T101500Z-9a1b2c3
```

## Deploy steps
```bash
R=/srv/app/releases/$(date -u +%Y%m%dT%H%M%SZ)-$SHA
ssh $HOST "mkdir -p $R"
rsync -az --delete build/ $HOST:$R/
ssh $HOST "ln -sfn /srv/app/shared/.env $R/.env && ln -sfn /srv/app/shared/storage $R/storage"
ssh $HOST "cd $R && ./bin/migrate --check"
# switch: GNU ln -f replaces the link with no moment when it is missing
ssh $HOST "ln -sfn $R /srv/app/current"
ssh $HOST "sudo systemctl reload app"          # or php-fpm reload / opcache reset
ssh $HOST "ls -1dt /srv/app/releases/* | tail -n +6 | xargs -r rm -rf"   # keep 5
```
GNU `ln` documents that, without `--backup`, there is no brief moment when the destination does not exist when `-f` replaces it (an extension to POSIX). On other systems create the link under a temporary name and rename it over `current`: `rename(2)` atomically replaces an existing newpath so no process finds it missing.

## Rollback
Point `current` at the previous release with the same `ln -sfn` and reload. Seconds, no rebuild.

## Gotchas
- Processes resolve `current` at start; long-running ones keep the old path until reloaded. PHP
  opcache and some app servers cache realpaths: reset/reload explicitly.
- Shared state (uploads, sessions) must live in `shared/`, never inside a release.
- Database migrations are not rolled back by the symlink; keep them backward compatible.
- Capistrano implements this pattern: `releases/` timestamped folders, `shared/` for linked files, and a `current` symlink updated at the end of a successful deployment.

## Verify
- [ ] `readlink /srv/app/current` shows the new release; rollback to previous takes under a minute.

## Checked

2026-10-28. Confirmed: Capistrano structure page (releases, shared, current symlink updated at the end of a successful deployment); GNU coreutils ln manual (-f, -n/--no-dereference, no moment when the destination does not exist without --backup); rename(2) man page (atomic replacement of an existing newpath); rsync man page (--delete). Corrected: the skill said ln -sfn leaves a window with no current, which GNU ln documents as not the case. Removed: mv -T (not documented in the fetched mv page), Deployer and Ansible deploy_helper.

Method: documentation only; no commands were run.
