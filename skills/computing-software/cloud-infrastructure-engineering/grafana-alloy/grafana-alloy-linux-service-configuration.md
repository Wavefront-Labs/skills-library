---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-linux-service-configuration
name: grafana-alloy-linux-service-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [systemd, config-file, custom-args, etc-default-alloy, alloy-otel-mode, systemctl-reload]
level: intro
status: docs-checked
description: "Configure the Alloy Linux service: config file, reload, CONFIG_FILE and CUSTOM_ARGS in the environment file, exposing the UI, and the OTel engine mode."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/configure/linux.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring the Alloy Linux service

Edit the default config at `/etc/alloy/config.alloy`, then reload:

```shell
sudo systemctl reload alloy
```

## Use a different config file
Edit the service environment file: `/etc/default/alloy` on Debian or Ubuntu, `/etc/sysconfig/alloy` on RHEL, Fedora, SUSE or openSUSE. Set `CONFIG_FILE` to the new path and run `sudo systemctl restart alloy`.

## Extra flags
The service runs the `run` command with `--storage.path=/var/lib/alloy/data`. Add more flags through `CUSTOM_ARGS` in the same environment file and restart the service.

## Expose the UI
By default the HTTP server listens locally only, so other machines cannot reach the debugging UI. Append to `CUSTOM_ARGS`:

```shell
--server.http.listen-addr=0.0.0.0:12345
```
Use an IP that other machines can reach, or `0.0.0.0` for all interfaces.

## OTel engine
The service runs the default engine unless `ALLOY_OTEL_MODE` is enabled in the environment file. `CONFIG_FILE` and `CUSTOM_ARGS` apply only to the default engine; the OTel engine reads `OTEL_CONFIG_FILE` and `OTEL_CUSTOM_ARGS` instead.

## Checked

2026-11-04. Confirmed against the Configure Alloy on Linux page (configure/linux.md): config path, environment files, CONFIG_FILE, CUSTOM_ARGS, default storage flag, listen-addr, OTel engine variables. No claims changed.

Method: documentation only; no commands were run.
