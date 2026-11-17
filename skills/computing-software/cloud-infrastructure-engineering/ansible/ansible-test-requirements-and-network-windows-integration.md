---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-test-requirements-and-network-windows-integration
name: ansible-test-requirements-and-network-windows-integration
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-test, ansible-test-requirements, network-integration, windows-integration]
level: advanced
status: docs-checked
description: "Declare per-test Python requirements for ansible-test sanity, units and integration, and run network-integration and windows-integration against real devices with inventories."
sources: ["Ansible developer guide, integration tests (https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html)", "Ansible developer guide, unit tests (https://docs.ansible.com/ansible/latest/dev_guide/testing_units.html)", "Ansible developer guide, testing running locally (https://docs.ansible.com/ansible/latest/dev_guide/testing_running_locally.html)", "ansible-test source (https://github.com/ansible/ansible/tree/devel/test/lib/ansible_test)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible-test requirements and network/windows integration

## Requirements
```
tests/
  unit/requirements.txt           # Python requirements for unit tests
  integration/targets/<target>/   # integration targets
```
`ansible-test <command> --requirements` installs a command's additional requirements. When the environment is managed by ansible-test (`--docker`, `--venv`) the option is usually unnecessary. The ansible-core repository keeps its own unit test requirements in `test/units/requirements.txt`, ansible-test's own in `test/lib/ansible_test/_data/requirements/units.txt`, and shared constraints in `test/lib/ansible_test/_data/requirements/constraints.txt`.
```bash
ansible-test units --docker default -v
ansible-test units --python 3.12 --requirements apache2_module   # outside a managed environment
```

## network-integration
`network-integration` runs targets against network devices described by an inventory you supply:
```bash
ansible-test network-integration --inventory <inventory file> <target>
```
- The inventory must define the connection details for each device (host, user, credentials, `ansible_network_os` and `ansible_connection` for the platform under test); keep it out of version control because it holds credentials.
- `--testcase` limits a target to a named test case.
- `--docker-privileged` applies to `integration`, not to `network-integration` or `windows-integration`.

## windows-integration
The Windows tests exercise the `winrm` connection plugin and Windows modules against a real Windows Server that you provide. Enable PowerShell Remoting on the host (`Enable-PSRemoting -Force`), copy `inventory.winrm.template` to `inventory.winrm`, edit it, then run:
```bash
ansible-test windows-integration --inventory inventory.winrm -v shippable/
```
Running the tests can change the Windows host, so never point them at a production system. Targets use the same `aliases` mechanism as POSIX integration tests, with group aliases such as `shippable/windows/group2` and skip aliases such as `skip/windows/2022`.

## Gotchas
- Keep device and host inventories out of git; write them from CI secrets.
- A controller in `--docker` still needs network reachability to the devices.
- Make targets restore device or host state so reruns start clean.

## Verify
- [ ] `ansible-test integration --list-targets` shows the expected targets.

## Checked
Checked 2026-10-23 against the Ansible developer guide source (testing_integration.rst, testing_units.rst, testing_running_locally.rst, sanity/integration-aliases.rst) and the ansible-test CLI source on GitHub (latest ansible-core release v2.21.5): the `--requirements` behaviour, the requirements file locations, the `network-integration` and `windows-integration` commands with `--inventory`, `--testcase`, `--list-targets`, the Windows setup steps and `inventory.winrm.template`, `--docker-privileged` scope and the Windows aliases. Removed the unconfirmed example device IPs and credentials, `tests/cli/*.yaml` layout, `network/ios` alias, `tests/requirements.yml` and sanity/constraints file claims.
Method: documentation only; no commands were run.
