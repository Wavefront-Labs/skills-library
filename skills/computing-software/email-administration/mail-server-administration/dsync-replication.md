---
id: computing-software.email-administration.mail-server-administration.dsync-replication
name: dsync-replication
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dsync-replication, dovecot-replication, dsync, replicator]
level: advanced
status: docs-checked
description: "Set up Dovecot dsync-based two-way replication between two servers with the replicator plugin."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/replication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dsync replication

**Goal:** a warm standby mailstore.
## Steps
1. Enable `mail_plugins = $mail_plugins notify replication`, start the replicator (`service replicator { process_min_avail = 1 }`) and give mail processes access to the `aggregator` listeners `replication-notify-fifo` and `replication-notify`. Expose `unix_listener replicator-doveadm` for the `doveadm replicator` commands.
2. Add a `service doveadm` `inet_listener` port and the same `doveadm_password` on both servers, then `plugin { mail_replica = tcp:mail2.example.com }`. For TLS use `tcps:`, set `ssl = yes` on the listener, and make the peer certificate verifiable through `ssl_client_ca_dir` or `ssl_client_ca_file`.
3. Make `doveadm user '*'` list all users; replicator needs the list.
4. Restart; check `doveadm replicator status` and `doveadm replicator status '*'`.
## Failure modes
- Not replicated: `doveadm purge`, `doveadm force-resync`, `doveadm quota recalc` and similar fixes (run them on both nodes). Replicas must not share a quota database and must have different hostnames.
- Shared-folder replication can create many duplicate mails; replication pairs only, so no director.
- Syntax here is Dovecot 2.3.
## Verify
- `doveadm replicator status '*'` shows sync times; deliver on node A and fetch from node B.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Replication with dsync page (plugins, replicator and aggregator listeners, doveadm_password, tcp/tcps targets, SSL CA settings, `replicator status` commands, notes on purge, force-resync, quota and hostnames, shared-folder warning). Removed: `replication_password` (not a setting; the shared secret is `doveadm_password`), `doveadm replicator replicate -f` (not in the docs), the clock-skew claim, and the backup-substitute and deletions-replicate wording (not stated).

Method: documentation only; no commands were run.
