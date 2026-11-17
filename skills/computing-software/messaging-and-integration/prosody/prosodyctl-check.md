---
id: computing-software.messaging-and-integration.prosody.prosodyctl-check
name: prosodyctl-check
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, prosodyctl, diagnostics, dns, certificates, connectivity]
level: practitioner
status: docs-checked
description: "prosodyctl check subcommands for Prosody: config, features, dns, certs, disabled, turn and connectivity, and what each one verifies."
sources:
  - https://prosody.im/doc/prosodyctl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prosodyctl check

Self-checks for a Prosody setup:

- `prosodyctl check config`: sanity checks on the configuration file.
- `prosodyctl check features`: finds missing or unconfigured features.
- `prosodyctl check dns`: compares DNS records with configured domains and ports.
- `prosodyctl check certs`: verifies certificates are valid and not expired.
- `prosodyctl check disabled`: lists disabled VirtualHosts and Components excluded from checks.
- `prosodyctl check turn [--ping=stun.server.example]`: tests the `mod_turn_external` setup, optionally pinging a STUN server.
- `prosodyctl check connectivity`: tests external reachability via the third-party service observe.jabber.network.

Run `check config` after every config edit and `check dns` plus `check certs` after moving a domain or renewing certificates. Use `--config /path/to/config.cfg.lua` to check a non-default file.

Verify: each subcommand finishes and prints no warnings for a healthy host.

## Checked

2026-11-04. Read the prosodyctl page: all seven check subcommands, the --ping option of check turn, and the observe.jabber.network connectivity probe match. Nothing removed.

Method: documentation only; no commands were run.
