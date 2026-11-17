---
id: computing-software.cloud-infrastructure-engineering.ansible.building-pushing-registering-and-running-execution-environments
name: building-pushing-registering-and-running-execution-environments
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, execution-environments, ee-build, ee-push, build-context, controller-ee, ee-registration, ee-local-run, navigator-ee]
level: advanced
status: docs-checked
description: "Build an execution environment with ansible-builder, tag and push it to a registry, register it in automation controller, and run the same image locally with navigator or runner."
sources: ["ansible-builder usage (https://github.com/ansible/ansible-builder/blob/devel/docs/usage.rst)", "ansible-builder CLI source (https://github.com/ansible/ansible-builder/blob/devel/src/ansible_builder/cli.py)", "awx.awx.execution_environment module source (https://github.com/ansible/awx/blob/devel/awx_collection/plugins/modules/execution_environment.py)", "ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)", "ansible-runner execution environments (https://ansible.readthedocs.io/projects/runner/en/latest/execution_environments/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build, push, register and run execution environments

## Build
```bash
pip install ansible-builder
ansible-builder build \
  --file execution-environment.yml \
  --tag registry.example.com/ee/platform:2.3.0 \
  --container-runtime podman \
  --context ./context \
  -v 3
```
`ansible-builder create` only writes the build context (default directory `context`, with the Containerfile or Dockerfile) — use it in CI systems that build with their own tool. `--output-filename` picks the file name (default depends on `--container-runtime`):
```bash
ansible-builder create -f execution-environment.yml --output-filename Containerfile
buildah bud -f context/Containerfile -t registry.example.com/ee/platform:2.3.0 context
```

## Push
```bash
podman login registry.example.com
podman push registry.example.com/ee/platform:2.3.0
```
Treat version tags as immutable by convention (never re-push 2.3.0); use `latest` only for dev.

## Register in automation controller
```yaml
- awx.awx.credential:            # registry credential
    name: registry-example
    organization: Platform
    credential_type: Container Registry
    inputs: {}                   # registry host and login fields as defined by the Container Registry credential type

- awx.awx.execution_environment:
    name: platform-2.3.0
    image: registry.example.com/ee/platform:2.3.0
    pull: missing                # always | missing | never
    credential: registry-example
    organization: Platform
```
Then set it on job templates (`execution_environment: platform-2.3.0`). Update by registering a new EE version and switching templates (keep the old one for rollback).

## Run locally — same image as production
```bash
ansible-navigator run site.yml -i inventories/stage \
  --eei registry.example.com/ee/platform:2.3.0 --pp missing -m stdout
```
or with ansible-runner:
```bash
ansible-runner run ./runner-dir -p site.yml \
  --container-image registry.example.com/ee/platform:2.3.0 --process-isolation
```
`ansible-navigator exec` runs a command within an execution environment (see its `--exec-command` setting) with your navigator settings applied; use it to debug inside the image. `--pp` accepts `always`, `missing`, `never` or `tag` (default `tag`).

## Gotchas
- Build for the architecture of the nodes that will run the image.
- Keep images lean and use `pull: missing` with versioned tags to avoid repeated pulls.
- Attach the registry credential to the EE when the registry needs authentication.

## Verify
- [ ] A test job on the controller using the new EE shows the image tag in job details and `ansible --version` matches.
- [ ] Local navigator run with the same tag gives the same results as the controller job.

## Checked

Checked 2026-10-26 against ansible-builder devel (`docs/usage.rst`, `cli.py`), awx devel (`execution_environment.py` module, `credential.py`), ansible-navigator main (`navigator_configuration.py`) and ansible-runner docs. Confirmed: `-f/--file`, `-t/--tag`, `-c/--context`, `--build-arg`, `--container-runtime`, `-v`, `create` and `--output-filename`; `pull` choices always, missing, never (module default missing); the `Container Registry` credential type name; navigator `--eei`, `--pp`, `exec` subcommand and `-m stdout`; runner `--container-image` and `--process-isolation`. Removed unconfirmed digest, hub registry, organisation default EE, buildx platform and credential field claims.

Method: documentation only; no commands were run.
