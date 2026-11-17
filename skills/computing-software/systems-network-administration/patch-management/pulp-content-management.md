---
id: computing-software.systems-network-administration.patch-management.pulp-content-management
name: pulp-content-management
category: computing-software
field: systems-network-administration
product: patch-management
tags: [pulp, pulp-rpm, pulp-deb, repository-mirroring, patch-acquisition, patch-management]
level: practitioner
status: docs-checked
description: "Mirror and stage OS update content with Pulp 3: rpm/deb remotes, sync policies, repository versions, publications and distributions promoted per ring."
sources:
  - https://pulpproject.org/pulp_rpm/docs/user/tutorials/
  - https://pulpproject.org/pulp-cli/
  - https://pulpproject.org/pulpcore/docs/user/learn/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulp content management for patching

Pulp 3 gives you immutable **repository versions**, so "what dev got in October" is reproducible and promotable.

## Concepts
- **Remote**: upstream URL + sync settings. **Repository**: has numbered versions after each sync. **Publication**: metadata built from one version. **Distribution**: the URL clients use, pointing at a publication.
- Promotion = point the `prod` distribution at an older/newer publication; no copying.

## RPM example with pulp-cli
```sh
pip install pulp-cli[pygments] pulp-cli-deb
pulp config create --base-url https://pulp.example.com --username admin --password '...'
pulp rpm remote create --name el9-baseos --url https://cdn.example/rhel9/baseos/ --policy on_demand
pulp rpm repository create --name el9-baseos --remote el9-baseos --retain-repo-versions 10
pulp rpm repository sync --name el9-baseos
pulp rpm publication create --repository el9-baseos            # latest version
pulp rpm distribution create --name el9-baseos-dev  --base-path el9/dev/baseos  --publication <href>
pulp rpm distribution create --name el9-baseos-prod --base-path el9/prod/baseos --publication <older-href>
```
Clients: `baseurl=https://pulp.example.com/pulp/content/el9/prod/baseos/`.

## Promote after testing
```sh
pulp rpm publication list --repository el9-baseos      # find href for tested version
pulp rpm distribution update --name el9-baseos-prod --publication <tested-href>
```

## Deb
`pulp deb remote create --name jammy --url http://archive.ubuntu.com/ubuntu/ --distribution jammy-security --component main --architecture amd64`, then sync, publish (`pulp deb publication create --repository jammy --simple`), distribute.

## Policies
- `immediate` (the default) downloads everything at sync; `on_demand` and `streamed` download metadata at sync and fetch artifacts when a client asks (needs upstream reachable).
- Export does not work on repository versions synced with `on_demand` or `streamed`, so for air-gapped transfer use `immediate` plus `pulp export` / `pulp import`.

## Gotchas
- `--retain-repo-versions` deletes old versions; keep enough to cover your longest ring lag.
- Orphan cleanup (`pulp orphan cleanup`) frees disk only after versions are gone.
- Remotes accept client certificates (`--client-cert`) for upstreams that require them.

## Verify
Package versions on prod match the promoted publication, not latest upstream.

## Checked
2026-11-01. Confirmed against the pulp-cli source (option names: `--retain-repo-versions`, `--policy` choices, `--client-cert`, `--remote`, `--publication`, `--base-path`, `orphan cleanup`, `config create --base-url/--username/--password`), the pulp_deb guides (`--distribution`, `--component`, `--architecture`, `--simple`, `pulp-cli-deb` package) and the pulpcore on-demand-downloading and import-export guides (policy behaviour, default `immediate`, export limits). Removed: the Satellite/Katello claim, the RHEL entitlement note and the `dnf repoinfo` check.
Method: documentation only; no commands were run.
