---
id: computing-software.collaboration-platform-administration.matrix-synapse.upgrading-and-rolling-back-synapse
name: upgrading-and-rolling-back-synapse
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, upgrade, rollback, pip, poetry, synctl, schema-versions, background-updates, server-version]
level: practitioner
status: docs-checked
description: "Upgrade Synapse by install method (packages, pip, source, poetry), verify with server_version, read upgrade notes between releases, and understand rollback limits."
sources:
  - https://element-hq.github.io/synapse/latest/upgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before upgrading, read the special steps listed in the upgrade notes for every version between yours and the target. Confirm your Python and PostgreSQL versions are still supported: Synapse follows upstream lifecycles and drops versions that are no longer maintained (for example, v1.143.0 dropped PostgreSQL 13 and requires 14+).

**By install method**
- Prebuilt packages: use the normal package upgrade process.
- pip: `pip install --upgrade matrix-synapse`.
- Source: fetch new code (`git pull`), activate the virtualenv, then `pip install --upgrade .`, including extras such as `".[postgres,oidc]"`. With poetry, run `poetry install`, adding `--extras postgres --extras oidc` or `--extras all`.
- Restart with `synctl restart`.

**Verify** with `curl http://localhost:8008/_synapse/admin/v1/server_version`, adjusting the port to your listener.

**Rolling back is not guaranteed** because of schema changes between releases. Generally schemas are compatible across several versions, but once a version has run you may not be able to go back automatically. The upgrade page carries a table of version ranges and the earliest version each can roll back to (for instance v1.58.0 to v1.61.1 can go back to v1.57.0, but from v1.62.0 only to v1.61.0). Undo what the upgrade did: `pip install matrix-synapse==<older>`, or install the older Debian package with `dpkg -i`.

**From a very old version.** Read every upgrade note in between, but you need not install each release. The docs recommend stepping through each incompatible database schema version, which keeps the most rollback options. Synapse will not start until migrations finish, and background updates from each upgrade should complete before the next, so they do not stack up; watch them with the background updates admin API status endpoint.

Recent notes show the kind of config break to expect: the v1.163.0 notes say Synapse refuses to start when `limit_profile_requests_to_users_who_share_rooms` is set without `require_auth_for_profile_requests`.

## Checked

2026-11-04. Confirmed against the Synapse Upgrading page: install-method steps, poetry extras, synctl restart, server_version check, rollback table example, dpkg and pip rollback, very-old-version advice, background updates, v1.163.0 note. Replaced an unconfirmed v1.164.0 Python claim with the v1.143.0 PostgreSQL note.
Method: documentation only; no commands were run.
