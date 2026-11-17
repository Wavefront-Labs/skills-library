---
id: computing-software.systems-network-administration.immich.cli-install-and-login
name: cli-install-and-login
category: computing-software
field: systems-network-administration
product: immich
tags: [immich-cli, api-key, auth-yml, npm, docker]
level: practitioner
status: docs-checked
description: "Install the Immich CLI with npm or Docker, authenticate with an API key, and know where credentials are stored."
sources:
  - https://docs.immich.app/features/command-line-interface
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get the `immich` command line client installed and logged in.

Requirements: Node.js 22 or above and npm. If you cannot install Node, use the Docker image.

Install with npm:

```bash
npm i -g @immich/cli
```

If you previously installed the legacy CLI, remove it first:

```bash
npm uninstall -g immich
```

Docker alternative, which runs `immich` directly so you append arguments:

```bash
docker run -it -v "$(pwd)":/import:ro -e IMMICH_INSTANCE_URL=https://your-immich-instance/api -e IMMICH_API_KEY=your-api-key ghcr.io/immich-app/immich-cli:latest upload -a -c 5 --recursive directory/
```

Keep the key in a Docker env file instead of the command line if you prefer.

Create an API key in the web interface under user settings; you can restrict the key's permissions to limit its access.

Log in once:

```bash
immich login http://192.168.1.216:2283/api <api-key>
```

Credentials are written to `auth.yml` in the configuration directory, default `~/.config/immich/`. Change the directory with `-d` or the `IMMICH_CONFIG_DIR` variable. Protect that file, or run `immich logout` after use to remove stored credentials.

Global options: `-u, --url` (env `IMMICH_INSTANCE_URL`), `-k, --key` (env `IMMICH_API_KEY`). Other commands are `login`, `logout`, `server-info` and `upload`. The docs examples use a server URL ending in `/api`.

For a Google Photos takeout the docs recommend the community tool immich-go instead.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/command-line-interface in full: requirements, npm and Docker install, legacy CLI note, login, auth.yml location, global options, API key section.
Reworded: the `/api` URL suffix, now described as what the examples use; listed the `login` and `logout` commands.
Method: documentation only; no commands were run.
