---
id: computing-software.systems-network-administration.pi-hole.pihole-cli-group-access
name: pihole-cli-group-access
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-group, cli-authentication, cli-password]
level: practitioner
status: docs-checked
description: "Let a local user run pihole CLI commands without a password prompt by joining the pihole group, and understand cli_pw."
sources: ["https://docs.pi-hole.net/main/post-install/", "https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CLI authentication and the pihole group

In Pi-hole v6 the CLI talks to the same API as the web interface instead of editing databases directly. When an API password is set, CLI commands must authenticate too.

Members of the `pihole` group authenticate without typing the password. Add your user:

```bash
# Debian, Ubuntu, Raspberry Pi OS, Armbian, Fedora, CentOS
sudo usermod -aG pihole $USER

# Alpine
doas addgroup $USER pihole
```



**How it works.** The setting `webserver.api.cli_pw` (default `true`) makes FTL create a temporary CLI password. It is stored in clear in `/etc/pihole`, is valid only for the current session and is regenerated on each FTL restart. Sessions started with it can query data and manage lists, but cannot change the Pi-hole configuration or passwords.

**Disable the mechanism** if you do not want a password file on disk:

```bash
sudo pihole-FTL --config webserver.api.cli_pw false
```

CLI commands then have to authenticate with the password.

**Checklist**

1. Add the user to `pihole`.
2. Run a read command such as `pihole status`.
3. Use `pihole setpassword` to change the web password; it can be given as an argument or entered at a prompt to keep it off the screen.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Post-Install (main/post-install); FTL Configuration Reference (ftldns/configfile); The pihole Command (main/pihole-command). Removed the unconfirmed "open a new login session" step.
Method: documentation only; no commands were run.
