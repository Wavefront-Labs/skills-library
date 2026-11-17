---
id: computing-software.collaboration-platform-administration.vikunja.config-secrets-from-files
name: config-secrets-from-files
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, file-suffix-env, docker-secrets, load-credential, secret-file-path]
level: practitioner
status: docs-checked
description: "Load Vikunja secrets such as database and SMTP passwords from files with the file child key or the _FILE environment suffix, including env var expansion."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any config value can be read from a file. In `config.yml`, add the child key `file`:

```
database:
  password:
    file: /path/to/password
```

With environment variables, add the `_FILE` suffix: `VIKUNJA_DATABASE_PASSWORD_FILE=/path/to/password`.

Rules:
- Files are evaluated after other values, so a file value overrides any previously set value.
- If the file is not accessible, Vikunja fails to start.

From version 2.3.0 the path supports environment variable expansion, handy with systemd `LoadCredential`:

```
mailer:
  password:
    file: $CREDENTIALS_DIRECTORY/smtp.secret
```

Every environment variable of the Vikunja process is expanded in these paths. Make sure untrusted users cannot set variables in the process environment, or Vikunja might read unintended files.

## Checked

2026-11-04: checked against the config page, section "Reading config values from files" and its env-var expansion subsection. Removed the list of "good candidates", which the page does not give (it shows `database.password` and `mailer.password` only).

Method: documentation only; no commands were run.
