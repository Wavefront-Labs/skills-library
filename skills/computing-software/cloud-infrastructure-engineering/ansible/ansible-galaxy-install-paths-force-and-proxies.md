---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-galaxy-install-paths-force-and-proxies
name: ansible-galaxy-install-paths-force-and-proxies
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-galaxy, galaxy-install-path, galaxy-force, galaxy-proxy]
level: practitioner
status: docs-checked
description: "Control where ansible-galaxy installs content (-p, collections_path), when to use --force or --upgrade, and make installs work behind proxies and TLS inspection."
sources: ["ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)", "Installing collections (https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html)", "Ansible configuration settings (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "Galaxy server list (https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible-galaxy install paths, force and proxies

## Paths
```bash
ansible-galaxy collection install -r requirements.yml -p ./collections    # project-local
ansible-galaxy role install -r requirements.yml -p ./roles
```
- Collections install into `<path>/ansible_collections/<ns>/<name>`; `-p ./collections` and then `collections_path = ./collections` in ansible.cfg (warning if the path is not on the configured search path).
- Without `-p`, `collection install` uses the first path in the configured collections paths (by default `~/.ansible/collections`).

## Updating
| Flag | Effect |
|---|---|
| (none) | an already installed collection is skipped |
| `--upgrade` / `-U` | upgrade installed collections; also updates dependencies unless `--no-deps` is given |
| `--force` / `-f` | force overwriting an existing collection |
| `--force-with-deps` | force overwriting an existing collection and its dependencies |
| `--no-deps` / `-n` | do not install collections listed as dependencies (mutually exclusive with `--force-with-deps`) |
| `--pre` | include pre-release versions (ignored by default) |

## Certificates and timeouts
- `--ignore-certs` / `-c`, `[galaxy] ignore_certs = true` or `ANSIBLE_GALAXY_IGNORE` disables TLS verification: last resort and never in CI against public Galaxy.
- Per server: `[galaxy_server.hub] validate_certs = false` (defaults to true unless `--ignore-certs` or the global setting is on; prefer fixing trust over disabling it).
- `--timeout 120` for slow servers; the default is 60 seconds. Set it globally with `[galaxy] server_timeout` (`ANSIBLE_GALAXY_SERVER_TIMEOUT`) or per server with `timeout`.

## Gotchas
- A `-p` path that is not on the configured collections paths triggers a warning: the collection is not picked up in a run unless it is in a playbook-adjacent `collections` directory.

## Verify
```bash
ansible-galaxy collection list -p ./collections
```

## Checked

Checked 2026-10-26 against ansible-core devel (`lib/ansible/cli/galaxy.py`, `config/base.yml`), the collections guide and the Galaxy user guide. Confirmed: `-p/--collections-path` default is the first configured path (`~/.ansible/collections`) and the out-of-path warning; `-U/--upgrade`, `-f/--force`, `--force-with-deps`, `-n/--no-deps` (mutually exclusive with `--force-with-deps`), `--pre`; `-c/--ignore-certs`, `[galaxy] ignore_certs`, per-server `validate_certs` and `timeout`, default timeout 60 s. Removed unconfirmed proxy environment variable, CA bundle and git proxy advice.

Method: documentation only; no commands were run.
