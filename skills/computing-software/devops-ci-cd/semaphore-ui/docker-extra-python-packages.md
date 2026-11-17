---
id: computing-software.devops-ci-cd.semaphore-ui.docker-extra-python-packages
name: docker-extra-python-packages
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [docker, python, requirements-txt, pip, ansible, semaphore-ui]
level: practitioner
status: docs-checked
description: "Install extra Python packages into the Semaphore server or runner container with requirements.txt or a custom image."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Add Python packages to the Semaphore container

Goal: give Ansible modules and Python apps the extra pip packages they need.

Mount a `requirements.txt` into the config directory (`SEMAPHORE_CONFIG_PATH`, default `/etc/semaphore`) of either `semaphoreui/semaphore` or `semaphoreui/runner`:

```yaml
services:
  semaphore:
    image: semaphoreui/semaphore:latest
    volumes:
      - ./requirements.txt:/etc/semaphore/requirements.txt:ro
```

Example file contents: `netaddr`, `pywinrm[kerberos]`, `hvac>=2.0`.

How it works: at start the container looks for `${SEMAPHORE_CONFIG_PATH}/requirements.txt` and runs `pip3 install --upgrade -r` on it. If the file is absent it logs `No additional python dependencies to install`.

Things to know:
- Packages install into the bundled Ansible virtual environment, not system Python.
- Installation repeats on every container start and needs network access; packages are not persisted.
- A failed install (typo, missing build dependency, no network) makes the container exit before Semaphore starts, so read the container logs.
- The image has no compiler, so packages needing compilation can fail; prefer wheels.

For many dependencies, system packages or offline use, build an image instead:

```dockerfile
FROM semaphoreui/semaphore:latest
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
```

The base image already sets `PATH` and `VIRTUAL_ENV` to the Ansible venv and the `semaphore` user, so no activation is needed. The same works with `semaphoreui/runner`.

Verify: `docker logs` shows pip installing, and `docker exec <c> pip3 show <package>` finds it.

## Checked

2026-11-04: checked against the Docker installation page. Every claim is stated there.

Method: documentation only; no commands were run.
