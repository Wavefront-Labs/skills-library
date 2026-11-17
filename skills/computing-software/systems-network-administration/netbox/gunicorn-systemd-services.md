---
id: computing-software.systems-network-administration.netbox.gunicorn-systemd-services
name: gunicorn-systemd-services
category: computing-software
field: systems-network-administration
product: netbox
tags: [gunicorn, systemd, netbox-rq]
level: practitioner
status: docs-checked
description: "Copy the shipped gunicorn config and service files and start the web and worker services."
sources: ["https://netboxlabs.com/docs/netbox/installation/4a-gunicorn/", "https://netboxlabs.com/docs/netbox/installation/upgrading/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gunicorn and systemd

Goal: run the WSGI app and the background worker as services.

NetBox runs as a WSGI application behind an HTTP server. gunicorn is installed with NetBox and uWSGI is an alternative.

**Steps**
```
sudo cp /opt/netbox/contrib/gunicorn.py /opt/netbox/gunicorn.py
sudo cp -v /opt/netbox/contrib/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now netbox netbox-rq
systemctl status netbox.service
```

- The gunicorn config is copied rather than referenced so local changes survive upgrades. Edit it to change the bound IP address and port or performance settings.
- `netbox.service` runs the web app; `netbox-rq.service` runs the background worker that processes queued jobs.
- The stock service files assume the user and group are both named `netbox`; edit them if yours differ.

During upgrades, copy `gunicorn.py` from the old release to the new one if you used the original guide.

**Checklist**

1. gunicorn.py copied.
2. Both services enabled.
3. User and group names match.
4. Status shows active.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Gunicorn installation page and the Upgrading page (gunicorn.py copy step), both read in full.
