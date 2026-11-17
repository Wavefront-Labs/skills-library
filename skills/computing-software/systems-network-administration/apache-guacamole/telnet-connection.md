---
id: computing-software.systems-network-administration.apache-guacamole.telnet-connection
name: telnet-connection
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, telnet, telnet-parameters, username-regex, password-regex, login-success-regex, login-failure-regex, terminal]
level: practitioner
status: docs-checked
description: "Guacamole telnet parameters: hostname, port 23, timeout, username via NEW-ENVIRON, password auto-typing and login prompt regexes."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Telnet connections

Network: `hostname` (required), `port` 23, `timeout` 10 s.

Authentication (all optional):
- `username`: sent only if the server supports NEW-ENVIRON and reads `USER`.
- `password`: typed automatically when the password prompt is detected.
- `username-regex`, `password-regex`: override the built-in prompt detection; setting `password-regex` overrides the heuristic.
- `login-success-regex`: the terminal stays hidden until matching text arrives.
- `login-failure-regex`: matching text closes the connection with a login failure error.

Example connection: `protocol=telnet`, `hostname=localhost`, `port=23`.

Telnet is unencrypted: credentials cross the network in clear text. Prefer SSH (apache-guacamole.ssh-connection-auth) or keep telnet to isolated management networks.

Terminal display, clipboard and recording options are shared with SSH (apache-guacamole.clipboard-and-terminal-display, apache-guacamole.graphical-session-recording).

Verify: with `login-success-regex` set, the terminal appears only after the banner text matches.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Guacamole manual Configuring Guacamole page (about 130k characters): the whole Telnet section was read; other protocols were not. Confirmed: hostname, port 23 default, 10 second timeout, username via NEW-ENVIRON and USER, password typed when the prompt is detected, username-regex and password-regex overriding built-in defaults, login-success-regex hiding the terminal until a match, login-failure-regex closing with a login failure, the localhost example, and the warning that telnet is unencrypted and should only be used on trusted networks.
