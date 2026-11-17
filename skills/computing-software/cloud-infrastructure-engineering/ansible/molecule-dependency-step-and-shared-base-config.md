---
id: computing-software.cloud-infrastructure-engineering.ansible.molecule-dependency-step-and-shared-base-config
name: molecule-dependency-step-and-shared-base-config
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, molecule, molecule-dependency, molecule-shared-config, molecule-base-config, scenarios, requirements-yml]
level: advanced
status: docs-checked
description: "Install role and collection dependencies in Molecule's dependency step, and share one base configuration across scenarios with --base-config or a .config/molecule/config.yml."
sources: ["Molecule configuration (https://github.com/ansible/molecule/blob/main/docs/configuration.md)", "Molecule CLI source: base config option (https://github.com/ansible/molecule/blob/main/src/molecule/shell.py)", "Molecule merge function (https://github.com/ansible/molecule/blob/main/src/molecule/util.py)", "Molecule collections guide (https://github.com/ansible/molecule/blob/main/docs/getting-started-collections.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Molecule: dependency step and shared base config

## The dependency step
Runs before `create` in `molecule test` (sequence: dependency, cleanup, destroy, syntax, create,
prepare, converge, idempotence, side_effect, verify, cleanup, destroy).
```yaml
# molecule/default/molecule.yml
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml    # roles + collections in one file
    role-file: requirements.yml
```
Galaxy is the default dependency manager. `role-file` defaults to `requirements.yml` and `requirements-file` defaults to `collections.yml`, both searched in the role directory (not the scenario directory). Point both options at one file with `roles:` and `collections:` keys to combine them. Options are passed to `ansible-galaxy install`.
`name: shell` with `command: ./scripts/deps.sh` for custom installs (the `options` key is ignored for `shell`; put flags in `command`). Skip the step when an EE/venv already has everything with `dependency: {enabled: false}`.

Run alone: `molecule dependency`.

## Shared base configuration
Several scenarios (default, ubuntu, rhel9, upgrade) usually share driver, platforms defaults,
provisioner and verifier. Put common settings in one file:
```yaml
# .config/molecule/config.yml   (found in the current VCS repository, else in your home directory; merged UNDER each scenario's molecule.yml)
dependency: {name: galaxy}
driver: {name: podman}
provisioner:
  name: ansible
  config_options:
    defaults: {callbacks_enabled: ansible.posix.profile_tasks, stdout_callback: yaml}
  inventory:
    group_vars:
      all: {app_env: test}
verifier: {name: ansible}
```
Then each scenario's `molecule.yml` contains only what differs (platforms, extra vars).
Collections use `extensions/molecule/config.yml` for the same purpose. Alternative explicit global option, placed before the subcommand: `molecule --base-config ci/base.yml test` (`-c`, repeatable; merged in order, then each scenario's `molecule.yml` on top).

Merge is a recursive dict merge (like Ansible's `combine(recursive=True)`); lists (like `platforms`) are **replaced**, not appended.

## Scenario layout
```
molecule/
  default/{molecule.yml, converge.yml, verify.yml}
  rhel9/{molecule.yml}           # converge.yml can be shared via provisioner.playbooks.converge: ../default/converge.yml
```
`molecule test --all` runs every scenario; `molecule list` shows them and instance state.

## Gotchas
- Since Molecule 6.0.0 dependencies are installed into the directory defined by the Ansible configuration (the default roles path under `ANSIBLE_HOME`); two versions of one dependency conflict there.
- Network access is needed for the galaxy step; for air-gapped CI pre-install and disable the step.
- The base config is merged silently — when a scenario behaves oddly, check it.

## Verify
- [ ] `molecule matrix test` shows `dependency` in the sequence; `molecule list` shows all scenarios with the same driver.

## Checked

Checked 2026-10-26 against Molecule main (`docs/configuration.md`, `shell.py` `--base-config` help, `util.merge_dicts`, `config.py`, collections guide). Confirmed: test sequence, Galaxy and shell dependency managers, `role-file` and `requirements-file` defaults and search directory, `enabled: False`, base config locations and the global `--base-config/-c` option, recursive merge with list replacement, `provisioner.playbooks.converge` pointing at another scenario, v6.0.0 dependency install location. Removed unconfirmed `force` option and the cache-path claim.

Method: documentation only; no commands were run.
