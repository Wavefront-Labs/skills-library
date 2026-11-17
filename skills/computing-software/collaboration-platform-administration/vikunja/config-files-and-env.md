---
id: computing-software.collaboration-platform-administration.vikunja.config-files-and-env
name: config-files-and-env
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, config-yml, env-var-mapping, config-search-path, config-formats]
level: intro
status: docs-checked
description: "How Vikunja finds and merges configuration: config file formats and search locations, the VIKUNJA_ environment variable mapping and precedence."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure through a `config.yml` or environment variables. If both set the same option, the environment variable wins.

Nested keys map to `VIKUNJA_` plus the path in upper case: `first.child: true` equals `VIKUNJA_FIRST_CHILD=true`.

Formats: toml, yaml, hcl, ini, json, envfile, env variables and Java Properties files; yaml or toml recommended. A sample `config.yml.sample` is published at dl.vikunja.io.

Search order for the config file:
- `service.rootpath` (default: current working directory, falling back to the binary's directory if the working directory cannot be determined)
- `/etc/vikunja`
- `~/.config/vikunja`
- the current working directory

`service.rootpath` is only used to find the first config file; a new `rootpath` inside that file is not used for further lookup.

`--config <file>` pins one config file and skips the search path; if the file cannot be read Vikunja exits with an error.

Common tasks: `service.enablelinksharing: false` disables public links, `service.enableregistration: false` disables sign-up, `auth.openid.enabled: true` enables OIDC, `mailer.*` sets SMTP, `ratelimit.*` rate limiting.

With Docker Compose, mount the file at `/etc/vikunja/config.yml`. The official image presets `VIKUNJA_SERVICE_ROOTPATH=/app/vikunja/` and `VIKUNJA_DATABASE_PATH=/db/vikunja.db` as environment variables, so setting `service.rootpath` or `database.path` in the mounted file has no effect; change the host side of the bind mount instead.

## Checked

2026-11-04: checked against the config page (precedence, mapping, formats, search order, `--config`, Docker Compose note, common tasks table). Removed `service.defaultlanguage`: the page's table lists it but config-raw.json has the setting as `defaultsettings.language`, so it was not kept.

Method: documentation only; no commands were run.
