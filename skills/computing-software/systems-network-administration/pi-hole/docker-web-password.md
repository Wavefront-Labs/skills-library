---
id: computing-software.systems-network-administration.pi-hole.docker-web-password
name: docker-web-password
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-password, webpassword-file, docker-secrets]
level: practitioner
status: docs-checked
description: "Set, secure or clear the Pi-hole web interface password in Docker with an environment variable, .env file or Docker secret."
sources: ["https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Web password in Docker

Set the password with `FTLCONF_webserver_api_password`. If it is absent, and none was set earlier with `pihole setpassword` or `pihole-FTL --config webserver.api.password`, a random password is assigned at startup and printed to the log. Find it with:

```bash
docker logs pihole
```

and look for "random password".

**Options**

1. Directly in compose: `FTLCONF_webserver_api_password: 'correct horse battery staple'`
2. From the shell or an `.env` file kept beside the compose file:

```yaml
FTLCONF_webserver_api_password: ${ADMIN_PASSWORD}
```

3. From a Docker secret through `WEBPASSWORD_FILE`:

```yaml
environment:
  WEBPASSWORD_FILE: pihole_webpasswd
secrets:
  - pihole_webpasswd
```

with a top-level `secrets:` entry pointing at a file containing the password.

**Explicitly no password.** Set `FTLCONF_webserver_api_password: ''`. Using `pihole setpassword` to set an empty password does not persist across container restarts.

**Checklist**

1. Prefer a secret or `.env` file over a literal in a committed compose file.
2. Remember the variable makes the setting read-only in the web interface and CLI.
3. If you rely on a random password, read it from the first start's log.

## Checked

2026-11-03. Read the Docker Configuration page: `FTLCONF_webserver_api_password`, the random password behaviour and `docker logs pihole`, the compose, `.env` and `WEBPASSWORD_FILE` secret examples, the empty password note and the read-only rule for settings set through the environment. Removed the restart-after-change advice.

Method: documentation only; no commands were run.
