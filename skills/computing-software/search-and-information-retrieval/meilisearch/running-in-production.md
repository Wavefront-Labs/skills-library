---
id: computing-software.search-and-information-retrieval.meilisearch.running-in-production
name: running-in-production
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [production-deployment, systemd-service, reverse-proxy, meilisearch]
level: practitioner
status: docs-checked
description: "Deploy self-hosted Meilisearch on Linux: installer, dedicated user, meilisearch.toml with production env and master key, systemd unit, Nginx proxy and certbot HTTPS."
sources: ["https://www.meilisearch.com/docs/resources/self_hosting/deployment/running_production"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Meilisearch in production

The tutorial uses a Debian 12 droplet; any Linux works. Meilisearch Cloud is the recommended production route.

1. Install: `apt update`, `apt install curl -y`, then `curl -L https://install.meilisearch.com | sh` and `mv ./meilisearch /usr/local/bin/`.
2. Dedicated user: `useradd -d /var/lib/meilisearch -s /bin/false -m -r meilisearch` and `chown meilisearch:meilisearch /usr/local/bin/meilisearch`, to avoid running as root.
3. Directories and config: create `/var/lib/meilisearch/data`, `dumps`, `snapshots`, chown them to the user, `chmod 750 /var/lib/meilisearch`. Download the default `config.toml` to `/etc/meilisearch.toml` and set `env = "production"`, `master_key = "<MASTER_KEY>"` (a 16-byte string, kept secret), `db_path`, `dump_dir`, `snapshot_dir`.
4. systemd unit `/etc/systemd/system/meilisearch.service`: `Type=simple`, `WorkingDirectory=/var/lib/meilisearch`, `ExecStart=/usr/local/bin/meilisearch --config-file-path /etc/meilisearch.toml`, `User` and `Group` meilisearch, `Restart=on-failure`, `WantedBy=multi-user.target`. Then `systemctl enable meilisearch`, `systemctl start meilisearch`, `systemctl status meilisearch`.
5. Public access (skip if only a same-machine app calls it): install Nginx, remove the default site, add a server block with `proxy_pass http://localhost:7700;`, reload and restart nginx.
6. HTTPS: install `certbot python3-certbot-nginx`, run `certbot --nginx`, choose redirect, verify renewal with `certbot renew --dry-run` (certificates last 90 days; renewal is scheduled).

## Checked

2026-11-03. Confirmed claim by claim against the Running Meilisearch in production tutorial on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: the unsupported 'or longer' master key length (the page says a 16-byte string).

Method: documentation only; no commands were run.
