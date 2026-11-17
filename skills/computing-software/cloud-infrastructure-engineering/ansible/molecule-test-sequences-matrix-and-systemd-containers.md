---
id: computing-software.cloud-infrastructure-engineering.ansible.molecule-test-sequences-matrix-and-systemd-containers
name: molecule-test-sequences-matrix-and-systemd-containers
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, molecule, molecule-matrix, test-sequence, molecule-systemd, molecule-scenario]
level: advanced
status: docs-checked
description: "Customise Molecule test sequences, inspect them with molecule matrix, and run systemd-based services in Podman or Docker platforms with the right privileges."
sources: ["Molecule configuration, scenario sequences (https://github.com/ansible/molecule/blob/main/docs/configuration.md)", "Molecule command source (https://github.com/ansible/molecule/tree/main/src/molecule/command)", "Molecule systemd container guide (https://github.com/ansible/molecule/blob/main/docs/guides/systemd-container.md)", "molecule-plugins Podman driver (https://github.com/ansible-community/molecule-plugins/blob/main/src/molecule_plugins/podman/driver.py)", "molecule-plugins Docker driver (https://github.com/ansible-community/molecule-plugins/blob/main/src/molecule_plugins/docker/driver.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Molecule sequences, matrix and systemd containers

## Sequences
```yaml
# molecule/default/molecule.yml
scenario:
  test_sequence:
    - dependency
    - cleanup
    - destroy
    - syntax
    - create
    - prepare
    - converge
    - idempotence
    - side_effect
    - verify
    - cleanup
    - destroy
  converge_sequence: [dependency, create, prepare, converge]
  check_sequence: [dependency, cleanup, destroy, create, prepare, converge, check, destroy]
```
Drop steps you do not need (e.g. remove `side_effect`) or add `check` to `test_sequence` to also test check-mode safety.

## See what will run
```bash
molecule matrix test                      # per scenario, the actions 'molecule test' runs
molecule matrix converge --scenario-name upgrade
molecule test --all                        # every scenario
molecule test --destroy=never              # keep instances for debugging
```

## systemd in containers
Roles that manage services need PID 1 = systemd:
```yaml
platforms:
  - name: rhel9
    image: registry.access.redhat.com/ubi10/ubi-init:latest   # init image: ships systemd as PID 1
    command: /usr/sbin/init
    systemd: always            # podman driver: sets up tmpfs/cgroups for systemd
    pre_build_image: true
  - name: debian12
    image: registry.example.com/ci/debian12-systemd:latest   # your image with systemd
    command: /usr/sbin/init
    privileged: true           # grants the container elevated access to the host
    cgroupns_mode: host        # some systems (macOS) need this for systemd
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    tmpfs: ["/run", "/tmp"]
```
- Podman: `systemd: true|false|always`; the guide recommends `always` (with `true` and a command set, systemd mode is not enabled). Rootless Podman additionally needs the cgroup v2 hierarchy delegated to the user.
- `privileged` and `SYS_ADMIN` give the container elevated access to the host; use them only when a task needs them. systemd as PID 1 needs a cgroup v2 host.

## Gotchas
- Plain base images (`ubi`, not `ubi-init`) have no systemd, and a placeholder command such as `sleep` as PID 1 means systemd never starts: converge fails with "System has not been booted with systemd as init system (PID 1)".
- For tasks that need a full machine, use a VM-based driver (vagrant, ec2).

## Verify
```bash
molecule converge && molecule verify    # verify.yml asserts the unit is running via service_facts
```

## Checked

Checked 2026-10-26 against Molecule main (`docs/configuration.md` scenario sequences, `src/molecule/command/*`, systemd container guide) and the molecule-plugins Podman and Docker driver sources. Confirmed: `test_sequence`, `converge_sequence`, `check_sequence`, `molecule matrix`, `--all`, `--destroy`, Podman `systemd: true|false|always`, `command: /usr/sbin/init`, UBI init image, the systemd error text, cgroup v2 requirement, privileged caution. Removed `scenario.name`, third-party image, GitHub runner and `login` claims.

Method: documentation only; no commands were run.
