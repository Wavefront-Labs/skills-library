---
id: computing-software.collaboration-platform-administration.zulip.install-zulip-server
name: install-zulip-server
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-install, installer, certbot, realm-creation-link]
level: intro
status: docs-checked
description: "Install a production Zulip server from the release tarball with the installer script, Certbot and push notification registration, then create the first organization."
sources: ["https://zulip.readthedocs.io/en/latest/production/install.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing a Zulip server

Start with a fresh Ubuntu or Debian host that meets the requirements.

1. Download and unpack the latest release tarball from the download server into a temporary directory (`curl -fLO` then `tar -xf`). The install page links to the project's published sha256sums for verifying the download.
2. Become root and run the installer from the unpacked directory:

```
./zulip-server-*/scripts/setup/install --push-notifications --certbot \
    --email=YOUR_EMAIL --hostname=YOUR_HOSTNAME
```

3. When it finishes it prints a one-time organization creation link. Open it, create the organization and your administrator account.

Common flags:

- `--email` is a real contact address for the maintainers; users see it in automated mail and error pages. `ZULIP_ADMINISTRATOR` later sets a display name.
- `--hostname` becomes `EXTERNAL_HOST`; use Punycode for non-ASCII domains.
- `--certbot` obtains a certificate and installs a renewal cron job.
- `--self-signed-cert` is for testing, or for use behind a reverse proxy.
- `--push-notifications` registers with the Mobile Push Notification Service and prompts for the Terms of Service. Add `--agree-to-terms-of-service` for unattended runs, and `--no-submit-usage-statistics` to withhold aggregate statistics.

The installer is idempotent: fix the failure and rerun it. If you are importing data, stop after the install step and follow the import instructions. A new creation link can be made with `manage.py generate_realm_creation_link`.

Next, set up outgoing email.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/install.html (zulip.readthedocs.io, latest). Removed: the claim that checksums sit in a SHA256SUMS file next to the tarball (the page only links to published sha256sums).

Method: documentation only; no commands were run.
