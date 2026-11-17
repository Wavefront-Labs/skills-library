---
id: computing-software.cloud-infrastructure-engineering.ansible.inspecting-ee-contents-and-pinning-ansible-core
name: inspecting-ee-contents-and-pinning-ansible-core
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, execution-environments, ee-inspect, ee-ansible-core-pin, ansible-builder]
level: practitioner
status: docs-checked
description: "Inspect what an execution environment contains (collections, Python packages, core version) and pin ansible-core and ansible-runner versions in the EE definition."
sources: ["https://docs.ansible.com/projects/builder/en/latest/definition/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_content_navigator/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting EE contents and pinning core

## Inspect
```bash
ansible-navigator images --eei quay.io/acme/ee-platform:2.3   # inspect a specific image
ansible-navigator images                         # interactive: pick image, then :0 for details
podman run --rm quay.io/acme/ee-platform:2.3 ansible --version
podman run --rm quay.io/acme/ee-platform:2.3 ansible-galaxy collection list
podman run --rm quay.io/acme/ee-platform:2.3 pip freeze
podman inspect quay.io/acme/ee-platform:2.3 --format '{{ json .Config.Labels }}'
```
Store the output (collections list, pip freeze) as a build artifact so you can diff images between releases:
```bash
diff <(podman run --rm ee:2.2 ansible-galaxy collection list) <(podman run --rm ee:2.3 ansible-galaxy collection list)
```

## Pin core and runner (definition v3)
```yaml
version: 3
images:
  base_image:
    name: registry.access.redhat.com/ubi9/python-311:latest
dependencies:
  ansible_core:
    package_pip: ansible-core==2.16.12
  ansible_runner:
    package_pip: ansible-runner==2.4.0
  galaxy: requirements.yml
  python: requirements.txt
  system: bindep.txt
```
- With a base image that already contains core (ee-minimal, supported EE), omit `ansible_core` to keep the vendor-supported version, or override deliberately.
- Pin collection versions exactly in `requirements.yml` and Python packages in `requirements.txt` (or a constraints file via `python_interpreter`/build args) for reproducible images.
- Tag images with content versions (`ee-platform:2.3-core2.16`) rather than only `latest`.

## Gotchas
- `latest` base images drift: rebuilding the same definition next month yields different Python/OS packages. Pin base image digests for releases.
- A collection's `requirements.txt` may upgrade a package you pinned; check `pip freeze` after build.

## Verify
- [ ] `ansible --version` inside the image matches the pinned core.

## Checked

- 2026-10-31: `ansible-navigator images --eei <image>` confirmed in AAP 2.5 Using content navigator;
the execution environment definition v3 (`ansible_core`/`ansible_runner` with `package_pip:` such as
`ansible-core==2.14.4`, `galaxy`, `python`, `system`/bindep.txt, `additional_build_files`,
`additional_build_steps`) and the supported `ee-minimal`/`ee-supported` base images confirmed in the
ansible-builder definition page and the AAP RPM installation guide (ee_minimal_image/ee_supported_image).
- Removed: the `--details ansible_version,...` flag list and the `-m stdout` form (not re-verified in
  the current navigator docs); the interactive flow is kept as advice.
Method: documentation only; no commands were run.
