---
id: computing-software.cybersecurity-defensive.authentik.upgrade-authentik
name: upgrade-authentik
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, upgrade, release-notes, outposts, analyze, migration-inconsistency]
level: practitioner
status: docs-checked
description: "Upgrade authentik safely: back up first, never skip major versions, update outposts together, run compose or helm commands, then ANALYZE."
sources:
  - https://docs.goauthentik.io/install-config/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: move to a newer release without data loss. authentik does not support downgrading, so back up PostgreSQL first.

## Before
- Read the release notes for breaking changes and manual steps.
- Do not skip major versions: go to the latest `.x` of each `major.minor` before the next. From `2025.2.1`: latest `2025.2.x`, then latest `2025.4.x`, then latest `2025.6.x`.
- Server and all outposts must be on the same version; upgrade outposts at the same time.
- Air-gapped: mirror the target images first.
- Hourly update check creates the `update_available` event (rule `default-notify-update`); it is disabled by `AUTHENTIK_DISABLE_UPDATE_CHECK`.

## Commands
Docker Compose: download the new `compose.yml` (`wget -O compose.yml https://docs.goauthentik.io/compose.yml`), then
```shell
docker compose pull
docker compose up -d
```
Kubernetes:
```shell
helm repo update
helm upgrade --install authentik authentik/authentik -f values.yaml
```
AWS CloudFormation: create a changeset, use `https://authentik-cloudformation-templates.s3.amazonaws.com/authentik.ecs.VERSION.yaml` (VERSION may be `latest`).

## After
Check the version under **Dashboards > Overview**. If admin pages are slow, run `ANALYZE;` in the authentik database (safe while serving). If the version does not change, look for `migration inconsistency` in server logs; if present, restore the backup and upgrade through each higher version in sequence.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
