---
id: computing-software.cloud-infrastructure-engineering.ansible.idempotency-and-testing-with-molecule
name: idempotency-and-testing-with-molecule
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, molecule, molecule-plugins, role-testing, idempotence, idempotency-test, converge, verify, prepare, side-effect, docker-driver, podman-driver, delegated-driver, testinfra, ansible-verifier, systemd-container, scenario, test-matrix, ci-testing, ansible-lint, tox-ansible, molecule-init, molecule-login, molecule-destroy]
level: advanced
status: docs-checked
description: "Test Ansible roles with Molecule: scenario files, the test sequence, Docker/Podman platforms that run systemd, idempotence step failures and how to fix them, verify.yml assertions, CI matrix."
sources: ["Molecule configuration (https://github.com/ansible/molecule/blob/main/docs/configuration.md)", "Molecule ansible-native configuration (https://github.com/ansible/molecule/blob/main/docs/ansible-native.md)", "Molecule systemd container guide (https://github.com/ansible/molecule/blob/main/docs/guides/systemd-container.md)", "molecule-plugins Docker driver (https://github.com/ansible-community/molecule-plugins/blob/main/src/molecule_plugins/docker/driver.py)", "Molecule command source (https://github.com/ansible/molecule/tree/main/src/molecule/command)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Idempotency and testing with Molecule — prove the second run changes nothing

**Goal:** every role has a scenario that builds a disposable host, converges the role,
proves a second converge reports zero changes, and asserts the service actually works —
locally in a minute and in CI across target distros. How to *write* idempotent tasks is
in `computing-software.cloud-infrastructure-engineering.ansible.idempotent-playbooks-and-roles`.

## 1. Install and scaffold
```bash
pip install molecule "molecule-plugins[docker]" ansible-core ansible-lint
cd roles/nginx && molecule init scenario default
```
`molecule init scenario [NAME]` takes only a scenario name (default `default`). The Docker, Podman, Vagrant and EC2 drivers live in the separate `molecule-plugins` package, installed with extras such as `molecule-plugins[docker]`. The latest Molecule release at the time of checking was v26.10.0 (October 2026); pin the version in `requirements-dev.txt` and read the changelog when upgrading. The driver, platforms, provisioner and verifier sections below are the pre ansible-native configuration style; newer Molecule also supports an ansible-native style (top-level `ansible:` section with inventory and playbooks, no driver).

## 2. Scenario files
```yaml
# molecule/default/molecule.yml
driver: { name: docker }
platforms:
  - name: debian12
    image: registry.example.com/ci/debian12-systemd:latest   # an image with systemd and Python
    command: "/usr/sbin/init"          # run the image's init as PID 1
    privileged: true
    cgroupns_mode: host
    volumes: ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
    pre_build_image: true
  - name: rocky9
    image: registry.example.com/ci/rockylinux9-systemd:latest
    command: "/usr/sbin/init"
    privileged: true
    cgroupns_mode: host
    volumes: ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
    pre_build_image: true
provisioner:
  name: ansible
  inventory:
    group_vars:
      all: { nginx_sites: [{ name: default, port: 8080 }] }
verifier: { name: ansible }
```
```yaml
# molecule/default/converge.yml
- name: Converge
  hosts: all
  become: true
  roles: [{ role: nginx }]
```
`prepare.yml` installs things the *real* hosts already have (e.g. `iproute2`) so the
role does not need to.

## 3. The sequence (`molecule test`)
dependency → cleanup → destroy → syntax → create → prepare → converge →
**idempotence** → side_effect → verify → cleanup → destroy.
Inner loop while developing:
```bash
molecule converge          # create if needed, apply role
molecule login --host debian12 # poke around
molecule verify
molecule idempotence
molecule test --destroy=never   # full run, keep containers for debugging
molecule destroy
```

## 4. Fixing idempotence failures
The idempotence step re-runs converge and fails listing every task that reported
`changed`. Common causes and fixes:
- `command`/`shell` without `creates:`/`removes:`/`changed_when:`.
- Templates rendering timestamps, unordered dicts or `ansible_date_time` → make output deterministic (`| dictsort`).
- `lineinfile` regexp not matching the inserted line.
- Package modules with `state: latest` in a fast-moving repo → use `present` in roles.
Never mark a task `changed_when: false` just to pass the test if it really changes state.

## 5. Verify behaviour, not files
```yaml
# molecule/default/verify.yml
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: Service is running
      ansible.builtin.service_facts:
    - ansible.builtin.assert:
        that: ansible_facts.services['nginx.service'].state == 'running'
    - name: Port answers
      ansible.builtin.uri: { url: "http://localhost:8080/", status_code: 200 }
    - name: Config passes syntax check
      ansible.builtin.command: nginx -t
      changed_when: false
```
Testinfra (`verifier: testinfra`, Python `test_*.py`) is an alternative when you prefer pytest.

## 6. CI
- Matrix over scenarios/distros; environment-variable substitution in `molecule.yml` (for example in `image:`) keeps one file. Avoid hard-coded credentials; use substitution.
- `molecule check` is a separate dry-run sequence (destroy, dependency, create, prepare, converge in check mode, destroy), useful for catching tasks that crash only in check mode.
- Run `ansible-lint` before Molecule; it is seconds versus minutes.

## Gotchas
- Containers are not VMs; for roles that need a full machine use a VM-based driver such as Vagrant (see the molecule-plugins documentation).
- Converge fails with "System has not been booted with systemd as init system (PID 1)" when the container runs a placeholder command instead of the image's init; set `command` to the init. systemd as PID 1 needs a cgroup v2 host, and on some systems (macOS) `cgroupns_mode: host` is required.
- With `pre_build_image: false` (the default) the Docker driver builds an image from `Dockerfile.j2` — slower; use `pre_build_image: true` with a ready image.
- If the image declares its own `CMD`, set `override_command: False`; otherwise Molecule runs the `command` value (default a sleep loop).

## Verify
- [ ] `molecule test` passes on every target distro from a clean checkout.
- [ ] The idempotence step reports zero changed tasks.
- [ ] `verify.yml` checks the service responds, not just that files exist.
- [ ] `molecule check` completes without errors.
- [ ] CI runs `ansible-lint` then the Molecule matrix on every role change.

## Checked

Checked 2026-10-26 against Molecule main (`docs/configuration.md`, `docs/ansible-native.md`, systemd container guide, `src/molecule/command/*`), the molecule-plugins Docker driver source and the latest Molecule release (v26.10.0, 2026-10-12). Confirmed: test sequence order, `init scenario [NAME]` syntax (no `--driver-name`), `--destroy` on `test`, `login --host`, idempotence behaviour, `check` as a dry-run sequence, Docker platform keys (`pre_build_image`, `privileged`, `cgroupns_mode`, `volumes`, `command`, `override_command`), the systemd error message and cgroup v2 requirement, Testinfra no longer the default verifier. Fixed the stale `--driver-name` flag, the misplaced `molecule check` advice and removed unconfirmed driver-split, image and rootless claims.

Method: documentation only; no commands were run.
