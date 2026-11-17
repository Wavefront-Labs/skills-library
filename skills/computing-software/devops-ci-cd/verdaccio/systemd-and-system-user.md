---
id: computing-software.devops-ci-cd.verdaccio.systemd-and-system-user
name: systemd-and-system-user
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [systemd, system-user, linux-service, verdaccio-service, systemctl, forever, crontab-reboot]
level: practitioner
status: docs-checked
description: "Run Verdaccio on Linux as a dedicated system user under systemd using the shipped unit, or with forever and a cron @reboot entry."
sources:
  - https://verdaccio.org/docs/server-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a service user:
```
sudo adduser --system --gecos 'Verdaccio NPM mirror' --group --home /var/lib/verdaccio verdaccio
# without adduser:
sudo useradd --system --comment 'Verdaccio NPM mirror' --create-home --home-dir /var/lib/verdaccio --shell /sbin/nologin verdaccio
sudo su -s /bin/bash verdaccio
```
Run Verdaccio once as that user to generate the config. To accept external connections set `listen: 0.0.0.0:4873`.

systemd: the install ships a unit.
```
sudo cp /usr/lib/node_modules/verdaccio/systemd/verdaccio.service /lib/systemd/system/ && sudo systemctl daemon-reload
```
The unit assumes config in `/etc/verdaccio/config.yaml` and data in `/var/lib/verdaccio`; move your files or edit the unit.

Alternative with forever:
```
sudo npm install -g forever
forever start `which verdaccio`
crontab -e    # @reboot /usr/bin/forever start /usr/lib/node_modules/verdaccio/bin/verdaccio
```
Locations vary; use `which forever` and `which verdaccio`.

For Apache or nginx in front, see the reverse proxy skills.

## Checked

2026-11-04. Confirmed against the Verdaccio Server Configuration page (user creation commands, listen 0.0.0.0:4873, shipped systemd unit and its assumed paths, forever and crontab @reboot). Removed: the instruction to enable and start with systemctl and the closing verify commands, which the page does not give.
Method: documentation only; no commands were run.
