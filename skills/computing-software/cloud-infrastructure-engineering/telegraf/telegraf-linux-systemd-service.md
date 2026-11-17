---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-linux-systemd-service
name: telegraf-linux-systemd-service
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [systemd, service, reload, sighup, etc-default-telegraf]
level: practitioner
status: docs-checked
description: "Covers managing the Telegraf systemd unit installed by the deb and rpm packages: systemctl commands, SIGHUP reload, /etc/default/telegraf and journal logs."
sources: ["https://docs.influxdata.com/telegraf/v1/administer/run-as-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Telegraf under systemd

The `.deb` and `.rpm` packages install a `telegraf` systemd unit that runs Telegraf with `/etc/telegraf/telegraf.conf` and the `/etc/telegraf/telegraf.d` directory.

```bash
sudo systemctl start telegraf
sudo systemctl stop telegraf
sudo systemctl restart telegraf
sudo systemctl reload telegraf
sudo systemctl enable telegraf
sudo systemctl status telegraf
```

`reload` sends `SIGHUP`, making Telegraf reload its configuration files without restarting the process.

## Environment

The unit reads `/etc/default/telegraf`. Use it for variables referenced in config and to pass extra command-line options through `TELEGRAF_OPTS`.
## Logs

Under systemd Telegraf logs to the journal unless the agent `logfile` setting points elsewhere:

```bash
journalctl --unit telegraf
```

## macOS

With Homebrew use `brew services start telegraf` (also `restart`, `stop`, `info`). To manage the launch agent by hand, symlink the installed `.plist` into the user LaunchAgents folder and `launchctl load` it. Use `/opt/homebrew` paths on Apple Silicon and `/usr/local` on Intel.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 source for "Run Telegraf as a service" (Linux and macOS sections read; Windows section read but not used). A GODEBUG netdns claim was removed as unconfirmed.
