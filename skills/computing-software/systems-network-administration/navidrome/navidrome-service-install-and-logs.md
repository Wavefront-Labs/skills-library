---
id: computing-software.systems-network-administration.navidrome.navidrome-service-install-and-logs
name: navidrome-service-install-and-logs
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, systemd, service-install, launchd, windows-service, journalctl, logs, sysconfig]
level: practitioner
status: docs-checked
description: "Install Navidrome as an OS service with navidrome service install and find its logs on Linux, Docker, FreeBSD and Windows installers."
sources: ["https://www.navidrome.org/docs/usage/admin/cli/service/", "https://www.navidrome.org/docs/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome as a service, and logs

`navidrome service` (alias `svc`) manages the OS service: systemd on most Linux, launchd on macOS, Service Control Manager on Windows. Subcommands: `install`, `uninstall`, `start`, `stop` (10 seconds to shut down cleanly), `status`, `execute` (foreground, as the service manager runs it).

```bash
sudo navidrome service install --user navidrome --configfile /etc/navidrome/navidrome.toml
sudo navidrome svc install --working-directory /var/lib/navidrome
```
- Install prints the working directory, music folder, data folder and log location first, and usually needs root.
- Without `--configfile` the service looks for `navidrome.toml` in its working directory (default: folder of the binary).
- The manager restarts it on failure. Logs go to the data folder unless `LogFile` is set.
- On Linux the systemd unit also reads environment variables from `/etc/sysconfig/navidrome` if present.
- `uninstall` leaves music and data untouched.

Where logs are (Navidrome writes only to stdout, following the Twelve-Factor approach):
- systemd: `journalctl -u navidrome.service`
- Docker: `docker logs navidrome` or `docker compose logs`
- FreeBSD: `/var/log/debug.log` by default
- Windows MSI installer: `navidrome.log` under the ProgramData Navidrome folder (follows `DataFolder`); with Shawl, `shawl_for_navidrome_*.log` beside the executable; NSSM uses the `AppStdout` attribute; WinSW logs next to its config.

Raise detail with `LogLevel=debug` (or `trace`).

## Checked

2026-11-04. Confirmed against the Navidrome `service` CLI page and the FAQ (Where are the logs?): service managers, subcommands, install flags, config file lookup, `/etc/sysconfig/navidrome`, 10 second stop, log locations per platform. Removed the advice about `EnableLogRedacting`, which neither page links to log sharing.

Method: documentation only; no commands were run.
