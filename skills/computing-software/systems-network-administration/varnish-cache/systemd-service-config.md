---
id: computing-software.systems-network-administration.varnish-cache.systemd-service-config
name: systemd-service-config
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [systemd, override-conf, reload-vs-restart, execstart]
level: practitioner
status: docs-checked
description: "Manage the Varnish systemd service: enable and start, change varnishd flags with an override or full replacement unit, daemon-reload, and reload versus restart."
sources:
  - https://www.varnish.org/docs/tutorials/configuring-varnish-systemd-services/
  - https://www.varnish.org/docs/tutorials/troubleshooting-varnish/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# systemd service config

Newer Varnish Software packages keep startup parameters in the systemd `.service` file, not in external files.

```bash
sudo systemctl status varnish
sudo systemctl enable varnish --now      # enable and start; enable alone does not start
sudo systemctl disable varnish --now     # disable and stop; disable alone does not stop
```

`ExecStart` in the `[Service]` section holds the varnishd command line, so all startup flags go there. Editing the packaged unit directly is discouraged (changes can be lost, or upstream changes not applied). Two recommended ways:

```bash
sudo systemctl edit varnish.service        # override file
sudo systemctl edit --full varnish.service # full replacement unit
```

An override must clear the setting first or systemd complains:

```ini
[Service]
ExecStart=
ExecStart=/usr/sbin/varnishd \
          -a :80 \
          -f /etc/varnish/default.vcl \
          -P %t/%N/varnishd.pid \
          -p feature=+http2 \
          -s malloc,256m \
          -p first_byte_timeout=600
```

Afterwards `systemctl status` shows a `Drop-In: /etc/systemd/system/varnish.service.d` with `override.conf`. With `--full`, the file `/etc/systemd/system/varnish.service` becomes the active unit and nothing needs unsetting first. Some older systemctl versions lack `edit`.

Manual equivalents: create the drop-in `/etc/systemd/system/varnish.service.d/override.conf`, or a replacement `/etc/systemd/system/varnish.service`. Then run `sudo systemctl daemon-reload` after every manual change. A replacement blocks upstream changes, often desirable under configuration management. `sudo systemd-delta` lists local overrides ([EXTENDED] for drop-ins, [OVERRIDDEN] for replacements).

Reload versus restart (troubleshooting tutorial):

- `systemctl reload varnish` calls the varnishreload script, gracefully adds a new VCL and discards older ones; no effect on the main or child processes.
- `systemctl restart varnish` kills varnishd and starts it again; runtime parameters not persisted in the service file are reset. The tutorial calls restarting a last-resort habit that skips root-cause inspection.

## Checked

Method: 2026-11-08 docs-only read of the systemd tutorial and the restart/reload section of the troubleshooting tutorial. Removed the earlier claim that restart loses the cache (not stated) and the "Verify" step wording; the Drop-In status output is shown on the page.
