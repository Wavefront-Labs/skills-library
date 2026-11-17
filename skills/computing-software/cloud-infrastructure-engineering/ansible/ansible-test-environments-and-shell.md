---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-test-environments-and-shell
name: ansible-test-environments-and-shell
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-test, ansible-test-venv, ansible-test-remote, ansible-test-shell, docker-environment, integration-tests]
level: advanced
status: docs-checked
description: "Choose ansible-test execution environments (--docker, --venv, --remote, --controller/--target) and debug failing integration tests interactively with ansible-test shell."
sources: ["Ansible developer guide, testing running locally (https://docs.ansible.com/ansible/latest/dev_guide/testing_running_locally.html)", "Ansible developer guide, testing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html)", "Ansible developer guide, integration tests (https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html)", "ansible-test source and completion files (https://github.com/ansible/ansible/tree/devel/test/lib/ansible_test)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible-test environments and shell

Run from the collection root, which must end in `.../ansible_collections/<namespace>/<name>/`. Collections your collection depends on must sit in the same collection root, because ansible-test ignores your configured collection paths.

## Environments
| Option | Where tests run | Use |
|---|---|---|
| `--docker [image]` | container (Docker or Podman); no image argument means `default` | recommended for sanity, units and integration; `default` is recommended for all sanity and unit tests |
| `--docker <image>` | another listed container, for example `ubuntu2404` or an alias such as `fedora` | integration tests that need a particular distribution |
| `--venv` | virtual environment managed by ansible-test (requirements installed automatically) | when containers and remote VMs cannot be used |
| `--local` | the local environment | no isolation |
| `--remote <platform>` | cloud-hosted ephemeral VM | integration tests unsuitable for containers; needs an API key unless run under an approved Azure Pipelines organisation |
| `--controller` / `--target` | composite environment arguments, alternatives to `--docker`/`--remote`/`--venv` | split controller and target; see `ansible-test <command> --help` |

The list of containers and remote platforms depends on the ansible-test command and the ansible-core version; read it from `--help`. If both Docker and Podman are installed, Docker is used; set `ANSIBLE_TEST_PREFER_PODMAN` to any non-empty value to prefer Podman.
```bash
ansible-test sanity --docker default -v
ansible-test units --docker default -v --python 3.12
ansible-test integration --docker ubuntu2404 -v my_target
ansible-test integration --docker default --retry-on-error my_target   # re-run failures with higher verbosity
ansible-test env --show                    # show the environment on stdout
```
Python requirements for unit tests go in `tests/unit/requirements.txt`. `--requirements` installs a command's extra requirements; with an environment managed by ansible-test (`--docker`, `--venv`) it is usually unnecessary.

## Debugging with ansible-test shell
`ansible-test shell` opens an interactive shell in the selected environment:
```bash
ansible-test shell --docker ubuntu2404 -v
ansible-test shell --venv --python 3.12
```
The `--docker-terminate` option controls whether the container is terminated after the run (see `--help` for the modes), which lets you inspect a failed run with the container engine. `--debug` runs ansible commands in debug mode. Increase verbosity with `-v`/`-vvv`.

## Integration target layout
```
tests/integration/targets/my_target/
  aliases            # one group, plus optional requirement/skip aliases
  tasks/main.yml
  meta/main.yml      # role dependencies, for example setup_remote_tmp_dir
```
Every target needs an `aliases` file, one alias per line. Documented aliases include a group such as `shippable/posix/group1`, `destructive` (needs `--allow-destructive` outside containers and VMs), `needs/root`, `needs/ssh`, `skip/macos`, `retry/never` and `unsupported` (cannot run in CI). Role dependencies in `meta/main.yml` are discovered automatically.

## Gotchas
- Files ignored by git are ignored by ansible-test as well.
- Unit tests run with network isolation in containers.
- On SELinux hosts, Docker may need permissive mode; the docs suggest Podman instead. Some container hosts need cgroup setup that ansible-test reports with instructions.
- Environment variables on the host are not passed into `--docker` or `--remote` environments.

## Verify
- [ ] `ansible-test integration --docker <image> <target>` passes locally the same way as in CI.

## Checked
Checked 2026-10-23 against the Ansible developer guide source (testing_running_locally.rst, developing_collections_testing.rst, testing_integration.rst, sanity/integration-aliases.rst) and the ansible-test source on GitHub (cli/environments.py, completion/docker.txt, cli/commands; latest ansible-core release v2.21.5): environment options and the container default, Docker-over-Podman preference and `ANSIBLE_TEST_PREFER_PODMAN`, `--remote` API key requirement, `--controller`/`--target`, `--local`, `--retry-on-error`, `env --show`, `shell`, `--docker-terminate`, `--debug` meaning, and the documented aliases. Removed the unconfirmed container names `fedora40` and `rhel/9.4` (names change per release), `docker:default` composite syntax, in-container paths, the error-message quote and the `tests/output` and rootless-Podman claims.
Method: documentation only; no commands were run.
