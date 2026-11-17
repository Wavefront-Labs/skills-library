---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-navigator-settings-file-container-engine-and-pull-policy
name: ansible-navigator-settings-file-container-engine-and-pull-policy
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-navigator, navigator-settings, ansible-navigator-yml, pull-policy, container-engine, execution-environments]
level: practitioner
status: docs-checked
description: "Configure ansible-navigator per project with ansible-navigator.yml: EE image, container engine, pull policy, volume mounts, environment passthrough, logging and artifact settings."
sources: ["ansible-navigator settings (https://github.com/ansible/ansible-navigator/blob/main/docs/settings.md)", "ansible-navigator FAQ (https://github.com/ansible/ansible-navigator/blob/main/docs/faq.md)", "ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-navigator settings file, container engine and pull policy

Search order for the settings file: `ANSIBLE_NAVIGATOR_CONFIG` env → `./ansible-navigator.<ext>`
(project dir, no leading dot) → `~/.ansible-navigator.<ext>` (home dir, leading dot). The first match is used. The file can be YAML (`.yml`/`.yaml`) or JSON (`.json`); two settings files in the same directory are an error.

```yaml
# ansible-navigator.yml
---
ansible-navigator:
  mode: stdout                         # or interactive
  execution-environment:
    enabled: true
    container-engine: podman           # auto | podman | docker | container
    image: registry.example.com/ee/platform:1.0.0
    pull:
      policy: missing                  # always | missing | never | tag
      arguments: ["--tls-verify=true"]
    environment-variables:
      pass: [AWS_PROFILE, AWS_REGION]
      set: {ANSIBLE_FORCE_COLOR: "1"}
    volume-mounts:
      - src: /tmp/directory
        dest: /tmp/directory
        options: Z                     # mount options, for example Z for SELinux relabelling
    container-options: ["--net=host"]
  ansible:
    config:
      path: ./ansible.cfg
    inventory:
      entries: [./inventories/prod]
  playbook-artifact:
    enable: true
    save-as: "artifacts/{playbook_name}-artifact-{time_stamp}.json"
  logging:
    level: warning
    file: artifacts/ansible-navigator.log
  editor:
    command: vim {filename}
```

## Pull policy
| Policy | Behaviour | Use |
|---|---|---|
| `always` | always pull the image | CI with moving tags (avoid moving tags) |
| `missing` | pull if not available locally | laptops with pinned tags |
| `never` | never pull | air-gapped, pre-loaded images |
| `tag` (default) | always pull if the tag is `latest`, otherwise pull if not available locally | general default |

Pin images by version tag; then `missing` avoids needless pulls.
Private registries: log in to the registry with the container engine first (`podman login` or `docker login`).

## Container engine
`auto` tries podman, then docker, then container. Navigator mounts the SSH agent socket (`SSH_AUTH_SOCK`) into the execution environment when `ssh-agent` is used, and also mounts the user's default-named SSH keys; keys with other names need `ssh-add` or an explicit volume mount. The navigator docs have a separate guide (`apple-container.md`) for differences when the engine is Apple Container.

## Checking effective settings
```bash
ansible-navigator settings --effective          # defaults, CLI, environment and settings file combined
ansible-navigator settings --sources            # source of each current entry
ansible-navigator settings --schema json        # draft-07 JSON Schema for the settings file
```

## Gotchas
- Run `settings --effective` after edits to confirm the file is read as intended.
- Host environment variables reach the EE only when listed under `environment-variables.pass` (or `--penv`); `--senv` sets one explicitly.
- Volume mounts can also be given on the command line (`--eev src:dest:options`) or in `ANSIBLE_NAVIGATOR_EXECUTION_ENVIRONMENT_VOLUME_MOUNTS` (entries separated by `;`).

## Verify
- [ ] `ansible-navigator settings --sources` shows the settings file as the source of `image`.
- [ ] A run with `--pp never` works offline once the image is present.

## Checked
Checked 2026-10-23 against the ansible-navigator repository on GitHub (docs/settings.md, docs/faq.md, navigator_configuration.py, data/settings-sample.template.yml): settings file search order and extensions, `container-engine` choices (auto, podman, docker, container) and the auto order, `pull.policy` choices and default `tag` with its meaning, `pull.arguments`, `volume-mounts` keys (src, dest, options), `environment-variables.pass/set`, `container-options`, the `settings` flags and SSH agent mounting. Removed the unconfirmed host registry auth path, the Docker-on-macOS note, the `<EE_RUNNER_HOME>` mount and the v1 format aside.
Method: documentation only; no commands were run.
