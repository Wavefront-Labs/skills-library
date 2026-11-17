---
id: computing-software.collaboration-platform-administration.mattermost.configuration-in-database
name: configuration-in-database
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [config-in-database, mm-config, mmctl-config-migrate, high-availability-config]
level: advanced
status: docs-checked
description: "Make the database the single source of truth for Mattermost configuration: MM_CONFIG, local mode, mmctl config migrate, systemd, verify and roll back."
sources: ["https://docs.mattermost.com/administration-guide/configure/configuration-in-your-database.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store configuration in the database

Self-hosted servers can read their active configuration from the database instead of config.json. Benefits: change settings from the System Console even in HA and read-only container setups, every HA node gets the same configuration (including new nodes), and SAML certificates and keys are deployed to all nodes automatically. The configuration database and the application database are separate concepts and can be different databases.

Steps (paths assume /opt/mattermost; in an HA cluster do each step on every node except the migrate command, which runs once):
1. Copy the master connection string from SqlSettings.DataSource or MM_SQLSETTINGS_DATASOURCE. It must start with postgres:// or mysql://; replace any \u0026 with &.
2. Create config/mattermost.environment containing MM_CONFIG='<connection string>' (escape single quotes), and make sure the mattermost user owns the directory.
3. Set EnableLocalMode to true in config.json and restart with sudo systemctl restart mattermost.
4. Migrate: ./bin/mmctl config migrate path/to/config.json "<connection string>" --local. Existing MM_* environment variables in the shell are merged in, and SAML certificates move into the database.
5. Add EnvironmentFile=/opt/mattermost/config/mattermost.environment above ExecStart in mattermost.service, then sudo systemctl daemon-reload and restart.
6. Verify with SELECT * FROM Configurations WHERE Active=true; exactly one row should return and its Value should match config.json.

Changes are recorded in the Configurations and ConfigurationFiles tables and ClusterSettings.ReadOnlyConfig is ignored. Do not hand-edit the active row; use the System Console or mmctl. Per-server settings go as separate lines in the environment file. Roll back by commenting out MM_CONFIG and restarting. Passing --disableconfigwatch without pointing at a file prevents the server starting.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/configure/configuration-in-your-database (steps, verification query, rollback). Fixed the connection-string escape to the documented \u0026 to & replacement.

Method: documentation only; no commands were run.
