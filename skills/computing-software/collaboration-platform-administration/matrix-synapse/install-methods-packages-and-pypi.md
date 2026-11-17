---
id: computing-software.collaboration-platform-administration.matrix-synapse.install-methods-packages-and-pypi
name: install-methods-packages-and-pypi
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, install, debian, ubuntu, docker, pypi, virtualenv, python, rhel, packages]
level: practitioner
status: docs-checked
description: "Pick a Synapse install route: Docker images, matrix.org Debian/Ubuntu apt repo, distro packages, or PyPI in a virtualenv, with prerequisites and Ubuntu and Windows cautions."
sources:
  - https://element-hq.github.io/synapse/latest/setup/installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prebuilt packages are recommended for most users. Official images are at `matrixdotorg/synapse` on Docker Hub and `ghcr.io/element-hq/synapse`, usable with the docker-compose file under `contrib/docker`.

For Debian and Ubuntu on amd64 the matrix.org repository at `packages.matrix.org/debian/` provides `matrix-synapse-py3`: install `lsb-release wget apt-transport-https`, download `matrix-org-archive-keyring.gpg` into `/usr/share/keyrings/`, add a `deb [signed-by=...]` line to `/etc/apt/sources.list.d/matrix-org.list`, then `apt update` and `apt install matrix-synapse-py3`. Adding `prerelease` to the sources line enables release candidates. The docs give the signing key fingerprint `AAF9AE843A7584B5A3E4CD2BCF45A512DE2DA058` for verification. The distro `matrix-synapse` package exists for Debian forky and sid only, and the default Ubuntu package is not recommended because it is old and has known security vulnerabilities.

Installing from PyPI needs a POSIX system, a supported Python 3 (the install page states the minimum and maximum), and at least 1GB of free RAM if you want to join large public rooms. On uncommon architectures without prebuilt wheels you need a recent Rust compiler. Install prerequisites first (a C compiler and Python headers; Debian needs `build-essential python3-dev libffi-dev python3-pip python3-setuptools sqlite3 libssl-dev virtualenv libjpeg-dev libxslt1-dev`), then:

```sh
mkdir -p ~/synapse
virtualenv -p python3 ~/synapse/env
source ~/synapse/env/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install matrix-synapse
```

Upgrade later with `pip install -U matrix-synapse`. On RHEL-family systems use the `venv` module with python3.11 or 3.12, since the default Pythons are EOL. A journald logging config that references `systemd.journal.JournalHandler` needs `systemd-python` installed separately. Native Windows is not supported; use WSL. If pip runs out of memory on a 512MB host, install the failing dependencies, such as `twisted`, one at a time.

## Checked

2026-11-04. Confirmed against the Synapse Installation Instructions page: image names, Matrix.org apt route and key fingerprint, prerelease channel, downstream Debian and Ubuntu notes, PyPI requirements and commands, RHEL venv note, systemd-python note, WSL note, 512MB pip memory note. Removed the specific Python version range (the page text did not match the skill).
Method: documentation only; no commands were run.
