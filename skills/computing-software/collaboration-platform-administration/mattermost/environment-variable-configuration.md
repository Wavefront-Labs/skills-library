---
id: computing-software.collaboration-platform-administration.mattermost.environment-variable-configuration
name: environment-variable-configuration
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [environment-variables, config-json, mm-prefix, custom-defaults]
level: practitioner
status: docs-checked
description: "Override Mattermost config.json settings with MM_ environment variables, MM_LICENSE and MM_CUSTOM_DEFAULTS_PATH, and know the System Console side effects."
sources: ["https://docs.mattermost.com/administration-guide/configure/environment-variables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring Mattermost with environment variables

Environment variables override config.json. If a setting needs a restart when changed in the file, the same applies to its variable. To derive a name, take the config.json path, such as ServiceSettings.SiteURL, prefix MM_, uppercase it and replace dots with underscores: MM_SERVICESETTINGS_SITEURL, set with export MM_SERVICESETTINGS_SITEURL="http://example.com".

Notes from the docs:
- Under systemd-style init files, use Environment=<> or EnvironmentFile=<path> (a file listing the variables).
- From v7.5, MM_PLUGINSETTINGS_PLUGINS and MM_PLUGINSETTINGS_PLUGINSTATES accept JSON, useful in Helm values, provided all plugins are configured at once.
- A setting controlled by an environment variable cannot be changed in the System Console. If you save other changes in the console, the variable's value is written back into config.json.
- Settings absent from both file and environment use documented defaults.
- Variables set in the active shell take effect when migrating configuration into a database. Read-replica and search-replica connection strings must be URL encoded, or special characters may end the string early.

License override: start the server with MM_LICENSE set to the contents of a license file. It overrides licenses in the database or file without replacing them. An invalid value starts the server without a license. In a High Availability cluster it only affects that app server.

Custom defaults: create a JSON file such as custom.json and start with MM_CUSTOM_DEFAULTS_PATH=custom.json. Values apply only where the current configuration has no value already.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/configure/environment-variables. Nothing removed.

Method: documentation only; no commands were run.
