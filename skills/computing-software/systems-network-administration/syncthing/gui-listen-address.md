---
id: computing-software.systems-network-administration.syncthing.gui-listen-address
name: gui-listen-address
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, gui, listen-address, port-8384]
level: practitioner
status: docs-checked
description: "Change the Syncthing GUI listen address safely, including 0.0.0.0, Unix sockets, port limits and the authentication it needs."
sources: ["https://docs.syncthing.net/users/guilisten.html", "https://docs.syncthing.net/users/syncthing.html", "https://docs.syncthing.net/users/config.html", "https://docs.syncthing.net/users/firewall.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GUI listen address

## Default
The GUI and REST API share one TCP port, `127.0.0.1:8384`, reachable only from the same computer. If 8384 is taken at install time, a random port is chosen. The port is printed at start-up.

## Exposing it
Setting `0.0.0.0:8384` allows access from the network. You should then also set a username and a strong password and check the option to use HTTPS; otherwise you are potentially opening your installation to the world. Binding to a LAN address such as `192.168.0.123:8384` does not restrict access to the local network. Connections with that address as destination are accepted regardless of their origin; proper network configuration and a firewall are needed for filtering, which Syncthing cannot do reliably itself.

```xml
<gui enabled="true" tls="true">
  <address>0.0.0.0:8384</address>
</gui>
```
Relevant keys: `gui.user`, `gui.password` (a bcrypt hash), `gui.apikey`, `gui.insecureAdminAccess` (allows access from outside localhost without authorization; a warning is displayed on startup). `gui.user` is set to require authentication.

## Other forms
- Unix sockets are specified with an absolute path (for example `/run/syncthing/syncthing.socket`); with `--gui-address` use the URL form `unix:///run/syncthing/syncthing.socket` (`unixs` for TLS over a Unix socket). `unixSocketPermissions` overrides the default socket permissions.
- `--gui-address` overrides the setting for one run.

## Ports
Use the unprivileged range 1024 to 65535 and a port nothing else uses. The docs do not recommend ports below 1024: Syncthing needs the privilege to open them, should not in general run as a privileged user, and the port must be set in the advanced config editor or the configuration file. An unusable port means Syncthing cannot present its GUI and you must edit the configuration file by hand; changing the port on a remote installation is not recommended unless you have other access.

## Safer remote access
An SSH forward such as `ssh -L 9999:localhost:8384 machine` binds local port 9999 and forwards to port 8384 on the target machine; it still works when Syncthing listens on localhost only.

## Checked
2026-11-04. Read The GUI Listen Address, the config page (gui element: address formats, `tls`, `user`, `password` bcrypt, `apikey`, `insecureAdminAccess`, `unixSocketPermissions`), Command Line Operation (`--gui-address` schemes) and Firewall Setup (SSH tunnel). Port rules, random-port fallback, LAN-address warning and port-change risks are confirmed; wording tightened.
Method: documentation only; no commands were run.
