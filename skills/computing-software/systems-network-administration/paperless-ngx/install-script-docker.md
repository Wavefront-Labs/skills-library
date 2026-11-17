---
id: computing-software.systems-network-administration.paperless-ngx.install-script-docker
name: install-script-docker
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, docker, install-script, docker-compose, superuser]
level: intro
status: docs-checked
description: "Install Paperless-ngx with the project's interactive script, which writes the compose files, starts the containers and creates the superuser."
sources:
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing with the Docker install script

The fastest route for a first install is the interactive script that automates the Docker Compose setup.

## Prerequisites
- Docker and Docker Compose installed.
- On macOS, GNU sed (it must work when invoked as `sed`) and wget.

## Run it
```bash
bash -c "$(curl --location --silent --show-error https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/install-paperless-ngx.sh)"
```
The script asks a few configuration questions, writes the required files, pulls the image, starts the containers and creates your superuser account from the credentials you supply.

## After it finishes
The web UI is normally at `http://127.0.0.1:8000` (adjust for the port you chose). Log in with the account you just created.

## Choosing a route
The docs recommend Docker for most users: it is faster to set up, easier to maintain and ships sensible defaults. Bare metal is for advanced setups and contributors, and community-hosted providers are listed in the project wiki.

## Good practice
A superuser sees every object and document. Create a separate normal account for daily use, or downgrade the superuser once setup is done.

## Checked
2026-11-04. Compared with the Quick Start, Overview and Installation Script sections of setup (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: script purpose and actions, prerequisites including macOS sed and wget, the command, URL after install, route recommendation, hosted providers wiki, superuser advice. Removed: closing paragraph about editing generated compose files and the cross-reference to a Docker Compose skill (not on the page).

Method: documentation only; no commands were run.
