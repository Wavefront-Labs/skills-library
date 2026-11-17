---
id: computing-software.systems-network-administration.nagios-core.monitor-public-services
name: monitor-public-services
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, monitor-http, monitor-ftp, monitor-ssh, monitor-smtp, check-http, check-ftp, check-ssh, check-smtp, public-services]
level: intro
status: docs-checked
description: "Monitor public network services in Nagios Core with check_http, check_ftp, check_ssh and check_smtp: basic service objects and flags passed after ! (URI, string, port, timeout)."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/monitoring-publicservices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring public services

Define a host, then a service per check. Sample commands live in `commands.cfg`; each passes `$HOSTADDRESS$` and takes extra flags through `$ARG1$`.

| Plugin | Flags shown |
|---|---|
| `check_http` | `-I` address, `-u` URI, `-t` timeout (s), `-s` expected string |
| `check_ftp` | `-p` port, `-t` timeout, `-e` expected text |
| `check_ssh` | `-t` timeout, `-r` expected version |
| `check_smtp` | `-t` timeout, `-e` expected text |

## Basic
Attach a service with only the command name; default timeout is 10 seconds.
```
define service {
    use                  generic-service
    host_name            www1
    service_description  HTTP
    check_command        check_http
}
```

## With arguments
```
check_command  check_http!-u /download/index.php -t 5 -s "latest-version.tar.gz"
```
POP3, IMAP and similar follow the same pattern with an expected-string flag.

Run any plugin with `--help` for all options. Verify config before restart (`computing-software.systems-network-administration.nagios-core.verify-configuration`).

## Checked

2026-11-04. Confirmed on the Monitoring Publicly Available Services page: the commands.cfg definitions passing $HOSTADDRESS$ and $ARG1$, check_http flags -I -u -t -s, check_ftp -p -t -e, check_ssh -t -r, check_smtp -t -e, the 10 second default, the POP and IMAP pattern, and --help for every plugin. Corrected the example search string to the one the page uses.

Method: documentation only; no commands were run.
