---
id: computing-software.cloud-infrastructure-engineering.ansible.ee-builds-registry-auth-and-build-failures
name: ee-builds-registry-auth-and-build-failures
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, execution-environments, registry-auth, ee-build-failures, ansible-builder]
level: practitioner
status: docs-checked
description: "Authenticate to registries for base image pulls and pushes, and troubleshoot ansible-builder failures: bindep, compiler, pip conflicts, galaxy auth and context issues."
sources: ["https://docs.ansible.com/projects/builder/en/latest/usage/", "https://docs.ansible.com/projects/builder/en/latest/definition/", "https://docs.podman.io/en/latest/markdown/podman-login.1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EE builds: registry auth and build failures

## Registry auth
```bash
podman login registry.redhat.io            # Red Hat base images (service account token)
podman login hub.corp.example.com          # private automation hub registry
ansible-builder build -t hub.corp.example.com/acme/ee-platform:2.3 -v 3
podman push hub.corp.example.com/acme/ee-platform:2.3
```
Credentials go to `${XDG_RUNTIME_DIR}/containers/auth.json`; in CI use `podman login --authfile` with secrets. Runtime pulls by controller use a Container Registry credential on the EE object; navigator uses the local podman/docker login.

## Galaxy auth during build
Private hub collections need a token inside the build:
```yaml
# execution-environment.yml (v3)
additional_build_files:
  - src: ansible.cfg          # contains [galaxy_server.*] urls, token via env
    dest: configs
additional_build_steps:
  prepend_galaxy:
    - ADD _build/configs/ansible.cfg /etc/ansible/ansible.cfg
    - ARG ANSIBLE_GALAXY_SERVER_PAH_TOKEN
```
`ansible-builder build --build-arg ANSIBLE_GALAXY_SERVER_PAH_TOKEN=$TOKEN` — use build args or secrets, never bake tokens into a layer you push.

## Common failures
| Error | Fix |
|---|---|
| `bindep` reports missing `gcc`/`python3-devel` | add to bindep.txt (system requirements), or use wheels |
| pip resolver conflict between collection requirements | add a constraints file, pin the conflicting package |
| `ERROR! ... 401 Unauthorized` in galaxy stage | token/URL in build ansible.cfg |
| `manifest unknown` pulling base image | wrong tag or not logged in |
| `No such file` for additional_build_files | path relative to the definition file |
| Image works locally, fails on controller | architecture (arm64 vs amd64) — build with `--platform` |
| Build very slow, re-downloads everything | keep the build context and use layer caching; avoid changing early steps |

Debug: `ansible-builder create` writes the build context (Containerfile) so you can read and run
steps manually with `podman build`.

## Verify
- [ ] `podman run --rm <image> ansible-galaxy collection list` shows the private collections.

## Checked

- 2026-10-31: `ansible-builder build`/`create` two-step model, `--build-arg` (vs build_arg_defaults),
  `--verbosity`, `-vvv`, `--galaxy-keyring`/`--galaxy-required-valid-signature-count`, `--container-policy`,
  the v3 definition keys (`additional_build_files`, `additional_build_steps`, `system: bindep.txt`,
  base image requirements) and the build-context output confirmed in the ansible-builder usage and
definition pages. `podman login --authfile` confirmed in the podman-login man page.
- Removed: the bindep `[compile]` profile tag (bindep format is documented; the profile claim was not).
Method: documentation only; no commands were run.
