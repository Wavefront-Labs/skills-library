---
id: computing-software.messaging-and-integration.mosquitto.broker-command-line-options
name: broker-command-line-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-command-line, test-config, tls-keylog, daemon]
level: intro
status: docs-checked
description: "Start the mosquitto broker with -c, -d, -p, -v, -q and the version 2.1 options --test-config and --tls-keylog."
sources:
  - https://mosquitto.org/man/mosquitto-8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know the broker's command-line switches.

- `-c, --config-file`: load configuration from a file. Without it the broker listens on port 1883 bound to loopback with default values.
- `-d, --daemon`: run in the background as a daemon.
- `-p, --port`: listen on this port; up to 10 times. From 2.0 these listeners bind to loopback only, and if a config listener exists the `-p` options are ignored.
- `-v, --verbose`: equivalent to `log_type all`; overrides config logging options.
- `-q, --quiet` (2.1): disable all logging, equivalent to `log_type none`; overrides `--verbose`.
- `--test-config` (2.1): load the file given with `-c`, verify it is valid, and do not start the broker. Exit code 0 if valid, non-zero if no config file was given or the file is invalid.
- `--tls-keylog file` (2.1): log TLS connection information so tools such as tcpdump, wireshark and mqttshark can decrypt TLS traffic. In Wireshark set the (Pre)-Master-Secret log filename option. Debugging only, never production.

```
mosquitto -c /path/to/mosquitto.conf --test-config
```

Files named on the page: `/etc/mosquitto/mosquitto.conf`, `/var/lib/mosquitto/mosquitto.db`, and tcp-wrappers files `/etc/hosts.allow`, `/etc/hosts.deny` for host access control.

Environment: `MOSQUITTO_UNSAFE_ALLOW_SYMLINKS` allows loading sensitive files through symlinks.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
