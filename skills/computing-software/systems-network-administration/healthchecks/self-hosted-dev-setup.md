---
id: computing-software.systems-network-administration.healthchecks.self-hosted-dev-setup
name: self-hosted-dev-setup
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, self-hosted, virtualenv-setup, createsuperuser, sendalerts-command]
level: practitioner
status: docs-checked
description: "Set up a self-hosted Healthchecks from source on a Debian-based system: virtualenv, migrations, superuser, dev server, sendalerts and the admin panel."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Healthchecks is open source (BSD 3-clause), built on Python, Django and PostgreSQL or MySQL.

Steps on a Debian-based OS:

```
sudo apt-get update
sudo apt-get install -y gcc python3-dev python3-venv
mkdir -p ~/webapps && cd ~/webapps
python3 -m venv hc-venv
source hc-venv/bin/activate
git clone https://github.com/healthchecks/healthchecks.git
pip install wheel
pip install -r healthchecks/requirements.txt
cd healthchecks
./manage.py migrate
./manage.py createsuperuser
./manage.py test
./manage.py runserver
```

By default data is stored in the SQLite file `hc.sqlite` in the project directory; the dev server listens on http://localhost:8000. In a second shell run `./manage.py sendalerts`: it polls for state changes continuously, and without it no alerts are sent. In production, make sure it survives server restarts.

Admin panel: `createsuperuser` (optionally with `--email` and `--password`), then Account dropdown, Site Administration. Tasks include deleting accounts, resetting passwords, raising per-user limits and inspecting tables.

Production: set `DEBUG = False`, configure `ALLOWED_HOSTS`, front with a reverse proxy, use gunicorn or uWSGI instead of `runserver`.

## Checked

2026-11-04. Confirmed against the Healthchecks self-hosted page and README: the Debian dependency and virtualenv steps, migrate, createsuperuser (with --email and --password), test, runserver, SQLite hc.sqlite default, sendalerts behaviour, admin panel path and tasks, and the production advice on DEBUG, ALLOWED_HOSTS, reverse proxy, gunicorn and uWSGI. Reworded the process-manager advice to match the page.

Method: documentation only; no commands were run.
