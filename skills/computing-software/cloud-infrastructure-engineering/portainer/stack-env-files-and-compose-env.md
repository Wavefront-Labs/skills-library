---
id: computing-software.cloud-infrastructure-engineering.portainer.stack-env-files-and-compose-env
name: stack-env-files-and-compose-env
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [env-vars, stack-env, compose, swarm]
level: practitioner
status: docs-checked
description: "Distinguish a Compose .env file from Portainer's stack.env and how each supplies environment variables to a stack."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/stacks-deployments-and-updates/environment-variable-management-in-docker-.env-vs.-stack.env.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page contrasts two mechanisms.

A `.env` file belongs to Docker Compose on standalone deployments. It supports variable substitution inside the Compose file, so `image: nginx:${VERSION}` takes `VERSION` from `.env`. It is handy for changing ports and image versions without editing the Compose file itself, suits local development, and is detected automatically by Compose commands such as `docker-compose up`.

A `stack.env` file is used on Docker Swarm for orchestrated, multi-host deployments. It is only used to set environment variables under the `environment` field of your stack configuration. Unlike `.env`, it does not support variable substitution for other settings such as port numbers or image versions, and it cannot dynamically replace placeholders in the configuration file.

Because of that, the page suggests webhooks or the Portainer UI for dynamic updates on Swarm; a stack webhook URL can carry a variable, for example `?FRESHRSS_TAG=latest`.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed the writer's closing advice; added the documented webhook example.

Method: documentation only; no commands were run.
