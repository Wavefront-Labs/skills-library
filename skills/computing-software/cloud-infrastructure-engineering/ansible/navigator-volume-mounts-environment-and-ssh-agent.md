---
id: computing-software.cloud-infrastructure-engineering.ansible.navigator-volume-mounts-environment-and-ssh-agent
name: navigator-volume-mounts-environment-and-ssh-agent
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-navigator, navigator-volume-mounts, navigator-env, navigator-ssh-agent]
level: practitioner
status: docs-checked
description: "Pass files, environment variables and SSH credentials into the execution environment with ansible-navigator volume-mounts, environment pass/set and SSH agent forwarding."
sources: ["ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)", "ansible-navigator settings schema (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/data/ansible-navigator.json)", "ansible-navigator FAQ (https://github.com/ansible/ansible-navigator/blob/main/docs/faq.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# navigator: mounts, environment and SSH agent

The EE container sees only the project directory (mounted automatically) and what you add. Below, `<EE_HOME>` is the runner user's home inside the image (print it with `ansible-navigator exec -- sh -c 'echo $HOME'`).

## ansible-navigator.yml
```yaml
ansible-navigator:
  execution-environment:
    image: quay.io/acme/ee-platform:2.3
    pull:
      policy: missing
    volume-mounts:
      - src: ~/.aws
        dest: <EE_HOME>/.aws
        options: ro,Z
      - src: /etc/pki/ca-trust/source/anchors
        dest: /etc/pki/ca-trust/source/anchors
        options: ro
    environment-variables:
      pass: [AWS_PROFILE, VAULT_ADDR, VAULT_TOKEN, http_proxy, https_proxy, no_proxy]
      set:
        ANSIBLE_FORCE_COLOR: "true"
    container-options:
      - "--net=host"
```
CLI equivalents: `--eev ~/.aws:<EE_HOME>/.aws:ro`, `--penv AWS_PROFILE`, `--senv KEY=value`, `--co --net=host`.

`Z` is shown as a mount option in the documented `--eev` example (`<host-dir>:<container-dir>:Z`); it is the container engine's SELinux relabel option.

## SSH credentials
- **ssh-agent** (recommended): navigator sets up `ssh-agent` use inside the EE by mounting the SSH authentication socket and setting `SSH_AUTH_SOCK`. Keys with default names (`id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `id_xmss`) are picked up; register others with `ssh-add ~/.ssh/automation_ed25519` before running.
- **Without ssh-agent**: navigator also mounts your SSH keys into the EE (in the default user's home and the `HOME` directory), but only default-named keys are used unless you set `ansible_ssh_private_key_file`. That path must be the location after mounting (for example `~/.ssh/key_name`, which resolves in both cases).
- For other files, add your own `--eev` mounts.

## Gotchas
- When `ansible_ssh_private_key_file` is used with an EE the path must reference the key's location after it is volume mounted into the EE; `~/.ssh/key_name` resolves to the user's home directory with or without an EE.
- The playbook directory is mounted automatically; files outside it (for example `/srv/certs`, or an `ansible.cfg` or collections directory elsewhere) must be added as volume mounts.

## Verify
```bash
ansible-navigator exec -- ls -la <EE_HOME>/.aws
```

## Checked

Checked 2026-10-26 against ansible-navigator main (`navigator_configuration.py`, settings schema, `docs/faq.md`). Confirmed: `execution-environment` keys `image`, `pull.policy` (always, missing, never, tag), `volume-mounts` (`src`, `dest`, `options`), `environment-variables` (`pass`, `set`), `container-options`; CLI `--eev`, `--penv`, `--senv`, `--co`, `--pp`; automatic ssh-agent socket mounting, default key names and key mounting behaviour; automatic mounting of the playbook directory. Removed unconfirmed SELinux failure, known_hosts and rootless podman claims.

Method: documentation only; no commands were run.
