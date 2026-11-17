---
id: computing-software.systems-network-administration.apache-guacamole.ssh-connection-auth
name: ssh-connection-auth
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, ssh, ssh-parameters, private-key, passphrase, host-key, ssh-known-hosts, server-alive-interval, command, locale, timezone]
level: practitioner
status: docs-checked
description: "Guacamole SSH connection parameters: network, password and private-key auth, host-key checking via ssh_known_hosts or host-key, keepalives, command, locale and timezone."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH connections

Network: `hostname` (required), `port` 22, `timeout` 10 s, `server-alive-interval` (default 0 = off, minimum 2).

Authentication:
- `username`, `password`: optional; Guacamole prompts for any missing.
- `private-key`: full OpenSSH-format key contents (`ssh-keygen` output), enabling public-key auth. `passphrase` unlocks it; prompted if needed.
- `public-key`: base64 public key for certificate-based auth; mismatched keys fail.
- SSH "NONE" method is supported, usually with only a username.

Host verification (without it any host is accepted):
- Put an OpenSSH `known_hosts` file at `GUACAMOLE_HOME/ssh_known_hosts`, or
- set `host-key` to one `known_hosts` entry for that host.
(RDP/VNC SFTP uses `sftp-host-key`.)

Session:
- `command`: run it instead of the default shell
- `locale`: sent as `LANG`; server must accept it
- `timezone`: IANA name sent as `TZ`; server must allow it

Pair with SFTP (apache-guacamole.sftp-file-transfer), recording (apache-guacamole.graphical-session-recording) and terminal appearance (apache-guacamole.clipboard-and-terminal-display).

Troubleshooting: terminal protocols need installed fonts, else syslog shows `Unable to get font "monospace"`.

Verify: connect, confirm no host-key warning when `host-key` is set, and `echo $LANG` matches `locale`.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole and guacamole-native: hostname, port 22, timeout 10 seconds, server-alive-interval default 0 and minimum 2, username and password prompting, private-key in OpenSSH format, passphrase prompting, public-key behaviour, the NONE method, host verification by ssh_known_hosts in GUACAMOLE_HOME or host-key (sftp-host-key for RDP and VNC), command, locale as LANG, timezone as TZ with IANA names, and the font requirement with its syslog message. No changes needed.

Method: documentation only; no commands were run.
