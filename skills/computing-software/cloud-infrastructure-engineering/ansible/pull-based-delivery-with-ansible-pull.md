---
id: computing-software.cloud-infrastructure-engineering.ansible.pull-based-delivery-with-ansible-pull
name: pull-based-delivery-with-ansible-pull
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, gitops, pull-based, ansible-pull-gitops, ansible-pull, systemd-timers, self-configuring-hosts, autoscaling, cloud-init]
level: advanced
status: docs-checked
description: "Run GitOps-style pull delivery with ansible-pull: each host checks out the repo on a timer and applies its own config, with host-specific playbooks, splay, secrets and reporting."
sources: ["https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/pull.py", "https://docs.ansible.com/ansible/latest/cli/ansible-pull.html", "https://github.com/systemd/systemd/blob/main/man/systemd.timer.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pull-based delivery with ansible-pull

Goal: hosts converge themselves from git — no central SSH push, works for autoscaled instances,
laptops, edge sites behind NAT — and git is the single source of truth.

## How ansible-pull works
`ansible-pull -U <repo>` clones/updates the repo into a local dir (default `<ANSIBLE_HOME>/pull/<fqdn>`, override with `-d`), then runs a playbook against
`localhost`. Playbook choice, if not given: `<fqdn>.yml`, then `<hostname>.yml`, then `local.yml`. The clone is shallow unless `--full` is given.

## Repo layout
```
local.yml                 # entry point for every host
roles/...
group_vars/all.yml
```
`local.yml`:
```yaml
- hosts: localhost
  connection: local
  become: true
  vars_files: [group_vars/all.yml]
  roles:
    - base
  tasks:
    - name: Apply the role this host says it is
      ansible.builtin.include_role:
        name: "{{ ansible_local.role.name }}"      # include_role resolves at runtime, after facts
      when: ansible_local.role.name is defined
```
The host's role comes from a local fact (`/etc/ansible/facts.d/role.fact`, written at
provisioning by cloud-init from instance tags) — the host decides what it is.

## Schedule it (systemd timer, not cron)
```ini
# /etc/systemd/system/ansible-pull.service
[Service]
Type=oneshot
ExecStart=/usr/bin/ansible-pull -U https://git.example.com/infra/hosts.git -C main -d /var/lib/ansible-pull -o --accept-host-key -i localhost, local.yml
# /etc/systemd/system/ansible-pull.timer
[Timer]
OnBootSec=2min
OnUnitActiveSec=30min
RandomizedDelaySec=10min
[Install]
WantedBy=timers.target
```
- `-o` / `--only-if-changed`: run the playbook only when the repo changed (cheap no-op otherwise). Drop it if you want drift correction every interval.
- `RandomizedDelaySec` (or `ansible-pull -s <seconds>`, a random sleep of 0 to n seconds) spreads load on the git server.
- `-C` pins a branch/tag; promote by moving a tag (`prod`) instead of pushing to main.
- `--verify-commit` verifies the GPG signature of the checked-out commit and aborts if it fails; useful because every host executes repo content as root.

## Bootstrap (cloud-init)
```yaml
#cloud-config
packages: [git, ansible-core]
write_files:
  - {path: /etc/ansible/facts.d/role.fact, content: '{"name": "web"}'}
runcmd:
  - ansible-pull -U https://git.example.com/infra/hosts.git -C prod -i localhost, local.yml
  - systemctl enable --now ansible-pull.timer
```
(Install the timer units from the first pull run itself, so the repo owns them.)

## Secrets and reporting
- Vault-encrypted vars need `--vault-password-file` on every host — distribute via instance identity (fetch from a secret manager with the instance role), never bake into images.
- No central run log: ship `journalctl -u ansible-pull` to your log platform and alert on failed units (`systemctl is-failed ansible-pull.service`), or use a callback plugin that posts results.

## Gotchas
- Repo credentials on every host: use read-only deploy keys or tokens scoped to that repo.
- A broken commit breaks the fleet within one interval; keep a staging tag that canary hosts follow first.
- Collections must be installed on hosts: `ansible-galaxy collection install -r requirements.yml` as the first task or bake into the image.

## Verify
- [ ] `systemctl list-timers ansible-pull.timer` shows next run; `journalctl -u ansible-pull` shows recap with `failed=0`.
- [ ] A commit to the tracked tag reaches all hosts within interval + splay.

## Checked

Checked 2026-10-26 against the ansible-core `ansible-pull` CLI source (devel) and the systemd `systemd.timer` manual source (main). Confirmed: options `-U`, `-C`, `-d`, `-o` / `--only-if-changed`, `-s` / `--sleep` (random 0 to n seconds), `--accept-host-key`, `--verify-commit` (GPG), `--full`, `--purge`; playbook search order fqdn, hostname, `local.yml`; the default checkout directory under `ANSIBLE_HOME/pull/<hostname>`; timer options `OnBootSec`, `OnUnitActiveSec` and `RandomizedDelaySec`. Removed the invented `host_groups.yml` file.

Method: documentation only; no commands were run.
