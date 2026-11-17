---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-initial-setup-and-setup-token
name: portainer-initial-setup-and-setup-token
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [setup, setup-token, admin-user, license, environment-wizard]
level: practitioner
status: docs-checked
description: "Complete first-time Portainer setup: the admin user, the setup token from the server logs, the license key step and the environment wizard."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/install/server/setup.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/installing/setup-token.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After the Server container starts, open its URL to reach initial setup. The first user is an administrator; the username defaults to `admin` and the password must be at least 12 characters and meet the listed requirements.

New instances require a setup token. Find it in the Server logs on the `setup_token=` line:

- `docker logs <container>`
- `podman logs <container>`
- `kubectl logs <pod_name>`

Startup flags: `--setup-token <value>` supplies your own token, `--no-setup-token` disables the requirement (only on a network you fully control and trust), and `--admin-password` or `--admin-password-file` pre-set the admin password with no token needed. The token is one-time use and the user must be created within 5 minutes. Tokens are required from Portainer 2.43 / 2.39.4.

Business Edition then asks for a license key (from signing up or from the free trial). A "Don't have a license?" link is offered if you have no key. Paste the key and click Submit.

Once the admin exists, the Environment Wizard launches. Installation auto-detects the local environment and sets it up. Click Add Environments to connect more, or Get Started to begin using Portainer.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Corrected the license link description; added the documented token flags and limits.

Method: documentation only; no commands were run.
