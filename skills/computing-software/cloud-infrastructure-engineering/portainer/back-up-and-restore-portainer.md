---
id: computing-software.cloud-infrastructure-engineering.portainer.back-up-and-restore-portainer
name: back-up-and-restore-portainer
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [backup, restore, s3, portainer-db, stacks]
level: practitioner
status: docs-checked
description: "Know what a Portainer backup contains, how to store it locally or in S3, and why it does not include container data."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/getting-started/what-does-portainers-backup-include.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/general.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/stacks-deployments-and-updates/why-is-my-portainer-backup-so-large.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Portainer backup contains the Portainer database plus stack files deployed through Portainer. It does not include your environments' containers or their data; it exists to return Portainer's configuration to a known-good state.

The records include settings and version, license data, SSL certificates, snapshot metadata and S3 backup settings; API keys, users, roles, teams and memberships, endpoint authorizations and resource controls; environments, groups, tunnel server configuration and edge metadata; stack definitions, edge stack status and schedules, and stack webhooks; Edge groups, jobs, configurations and async commands; and policies with their enforcement configuration.

Take a backup under Settings, Back up Portainer. The archive is a tar.gz, optionally encrypted with a password. In Business Edition you can instead choose Store in S3, on demand or on a schedule. Restore is only possible on a fresh instance with an empty data volume: choose Restore Portainer from backup during setup, from a local file or by retrieving from S3.

Always back up before an upgrade: newer versions bump the database schema, so a newer database cannot be used with an older Portainer. If the backup is large, the usual cause is Git-deployed stacks: the cloned repository under `/data/compose/<stack-id>/` is included, and a repository used by several stacks is cloned once per stack. With relative path volumes the clone lives outside the data directory and is not backed up.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Added the Business Edition limit on S3, the restore-on-fresh-instance rule and the backup-size cause. Schema-bump claim confirmed on the rollback FAQ.

Method: documentation only; no commands were run.
