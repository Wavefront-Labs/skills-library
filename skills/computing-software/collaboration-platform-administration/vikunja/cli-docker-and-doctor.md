---
id: computing-software.collaboration-platform-administration.vikunja.cli-docker-and-doctor
name: cli-docker-and-doctor
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, cli-docker-exec, doctor-command, testmail-command, version-command]
level: practitioner
status: docs-checked
description: "Run the Vikunja CLI inside Docker and use doctor, testmail, version and web to diagnose an installation, with exit codes and what doctor checks."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The binary's default command is `web`. All commands read the same config file as the server.

In Docker, run them in the container (`-it` for interactive prompts such as password entry):

```
docker exec -it <container> /app/vikunja/vikunja <subcommand>
alias vikunja-docker='docker exec <container> /app/vikunja/vikunja'
```

`vikunja doctor` runs diagnostics and exits 0 when all pass, 1 if any fail. It checks:
- System: version, Go version, OS/arch, running user, working directory
- Config: file path, public URL, JWT secret, CORS origins
- Database: connection and server version
- Files: storage path, writability, disk space (Unix only)
- If enabled: Redis ping, SMTP connection, LDAP bind, OIDC discovery per provider

It also detects user-namespace problems in rootless Docker and suggests fixes.

`vikunja testmail <address>` sends a test mail over the configured SMTP. `vikunja version` prints the semantic version, or version plus commit hash. `vikunja help [command]` gives details.

## Checked

2026-11-04: checked against the CLI page (docker section, doctor, testmail, version, help). Removed the "run it first on any broken install" advice.

Method: documentation only; no commands were run.
