---
id: computing-software.data-science-and-analytics.apache-superset.pypi-install
name: pypi-install
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [pypi, pip-install, virtualenv, fab-create-admin, db-upgrade]
level: intro
status: docs-checked
description: "Install Superset from PyPI in a virtualenv: OS prerequisites, pip install, db upgrade, admin creation, init and starting the development server."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/pypi.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install Superset directly on a host.

1. Install OS packages: the `cryptography` library, used to encrypt stored connection passwords, has OS-level dependencies. The page lists an `apt-get` command for Debian and Ubuntu (tested on 20.04, 22.04 and 24.04), `yum` or `dnf` packages for Fedora and RHEL derivatives, and Xcode command line tools plus Homebrew packages for macOS. `libpq-dev` is only needed for PostgreSQL. See the pyproject.toml for the supported Python versions.
2. Create and activate a Python virtual environment (recommended): `python3 -m venv venv` then `. venv/bin/activate`, or pyenv-virtualenv.
3. Install:

```bash
pip install apache_superset
```

4. Define the mandatory configuration:

```bash
export SUPERSET_SECRET_KEY=YOUR-SECRET-KEY
export FLASK_APP=superset
```

For production use a strong key, for example from `openssl rand -base64 42`.

5. Initialise the metadata database and the app:

```bash
superset db upgrade
superset fab create-admin
superset load_examples
superset init
```

Use `admin` as the username to be able to load the examples. `load_examples` loads sample data and `init` creates default roles and permissions.

6. Start the development web server on port 8088 (`-p` binds another port):

```bash
superset run -p 8088 --with-threads --reload
```

`--debugger` enables Werkzeug's interactive console at `/console`: use it for local development only and never bind to `0.0.0.0` or expose the server with it enabled. Then browse to the host and port and log in with the admin account you created.

## Checked

2026-11-08. Confirmed against the PyPI install page (read in full). Removed: the `superset_config.py` and `SUPERSET_CONFIG_PATH` step (the page uses `SUPERSET_SECRET_KEY` and `FLASK_APP`), `--debugger` in the default run command (the page keeps it as a localhost-only option), and the unsourced advice on database drivers and production deployment.
Method: documentation only; no commands were run.
