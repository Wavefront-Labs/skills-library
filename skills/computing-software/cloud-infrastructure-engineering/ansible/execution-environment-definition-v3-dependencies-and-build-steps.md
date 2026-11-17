---
id: computing-software.cloud-infrastructure-engineering.ansible.execution-environment-definition-v3-dependencies-and-build-steps
name: execution-environment-definition-v3-dependencies-and-build-steps
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, execution-environments, execution-environment-yml, ee-definition, bindep, ee-dependencies, ee-minimal, base-image, additional-build-steps, prepend-append, ansible-builder]
level: advanced
status: docs-checked
description: "Write an ansible-builder version 3 execution-environment.yml: base image choice, Galaxy, Python and bindep system dependencies, and additional_build_steps for certs and proxies."
sources: ["ansible-builder execution environment definition (https://github.com/ansible/ansible-builder/blob/devel/docs/definition.rst)", "ansible-builder collection-level dependencies (https://github.com/ansible/ansible-builder/blob/devel/docs/collection_metadata.rst)", "ansible-builder passing secrets (https://github.com/ansible/ansible-builder/blob/devel/docs/scenario_guides/scenario_secret_passing.rst)", "ansible-builder schema source (https://github.com/ansible/ansible-builder/blob/devel/src/ansible_builder/ee_schema.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# execution-environment.yml (version 3)

```yaml
---
version: 3

images:
  base_image:
    name: docker.io/redhat/ubi9:latest        # must be an RPM-based image (dnf or microdnf)

dependencies:
  ansible_core:
    package_pip: ansible-core==2.18.*     # any format pip accepts; omit if the base image already ships ansible-core
  ansible_runner:
    package_pip: ansible-runner
  python_interpreter:
    package_system: python3.11            # installed with the package manager
    python_path: /usr/bin/python3.11
  galaxy: requirements.yml                # collections/roles
  python: requirements.txt                # extra pip packages
  system: bindep.txt                      # OS packages
  exclude:                                # needs ansible-builder 3.1 or newer
    python: [docker]                      # drop a collection's declared dep you don't need
    system: [python3-Cython]

options:
  package_manager_path: /usr/bin/microdnf # default is /usr/bin/dnf; only RPM-based managers are supported
  tags: [registry.example.com/ee/network:1.4.0]

additional_build_files:
  - src: files/ca-bundle.crt
    dest: certs
  - src: files/ansible.cfg
    dest: configs

additional_build_steps:
  prepend_base:
    - COPY _build/certs/ca-bundle.crt /etc/pki/ca-trust/source/anchors/corp-ca.crt
    - RUN update-ca-trust
  prepend_galaxy:
    - COPY _build/configs/ansible.cfg /etc/ansible/ansible.cfg   # galaxy server config
  append_final:
    - RUN rm -rf /root/.cache && ansible-galaxy collection list
```

## Dependencies
- `galaxy`: standard requirements.yml (`collections:` with pinned versions, `roles:`).
- `python`: a requirements file or an inline list (PEP 508 syntax) — pin versions; collection-declared dependencies (`meta/execution-environment.yml`, or `requirements.txt` and `bindep.txt` in the collection root) are collected automatically.
- `system`: bindep format, a file or an inline list, one package per line with platform selectors:
```
gcc [compile platform:rpm]
libxml2-devel [compile platform:rpm]
openssh-clients [platform:rpm]
sshpass [platform:rpm]
```
Entries with the `compile` profile are needed to build other requirements but are not installed in the final image; only entries with no profile are installed there.

## Base images
Ansible Builder requires RPM-based base images (dnf package management); the documentation lists ubi9, Rocky Linux 9, CentOS Stream 9 and Fedora as examples, and says Debian, Ubuntu and Alpine images are not supported. Add `ansible-core` and `ansible-runner` through `dependencies` and list collections explicitly for reproducibility.

## Build-step hooks
`prepend_base`, `append_base`, `prepend_galaxy`, `append_galaxy`, `prepend_builder`,
`append_builder`, `prepend_final`, `append_final` — raw Containerfile lines at each stage.
Typical: corporate CA, proxy `ENV`, galaxy server config, cleanup. Do not use `USER` directives in build steps; use `options.user` instead.

## Gotchas
- If the file does not say `version: 3`, Ansible Builder 3.x assumes an older schema, so state it explicitly.
- `package_manager_path` must match the base image (`/usr/bin/dnf` or `/usr/bin/microdnf`).
- For tokens needed at build time, use build secrets: pass `--extra-build-cli-args="--secret id=mytoken,src=my_secret_file.txt"` and a `RUN --mount=type=secret,id=mytoken ...` step in `additional_build_steps`.
- Unpinned `requirements.txt` makes rebuilds non-reproducible.

## Verify
- [ ] `ansible-builder create` completes without schema errors and writes the build context (default directory `context`).
- [ ] A container run of `ansible-galaxy collection list` and `pip freeze` inside the built image shows the pinned versions.

## Checked

Checked 2026-10-26 against ansible-builder devel (`docs/definition.rst`, `collection_metadata.rst`, secret passing guide, `ee_schema.py`). Confirmed the v3 sections, `images.base_image.name`, `dependencies` keys (`ansible_core`, `ansible_runner`, `python_interpreter`, `galaxy`, `python`, `system`, `exclude` from 3.1), `options.package_manager_path` (default `/usr/bin/dnf`, RPM only), `options.tags`, build step hook names, additional build files, RPM-only base images and the build-secret pattern. Removed Red Hat and community image names and the build-argument token example, which no public documentation covers.

Method: documentation only; no commands were run.
