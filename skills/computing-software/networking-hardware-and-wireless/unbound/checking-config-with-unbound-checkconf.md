---
id: computing-software.networking-hardware-and-wireless.unbound.checking-config-with-unbound-checkconf
name: checking-config-with-unbound-checkconf
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-checkconf, validation, config-check, exit-codes]
level: intro
status: docs-checked
description: "Validate an Unbound config with unbound-checkconf before starting or reloading, and read single option values from it."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-checkconf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# checking config with unbound-checkconf
`unbound-checkconf [-ahf] [-o option] [cfgfile]` checks the syntax and other errors of an Unbound configuration file. If no file is given it checks the config file at the default location, which depends on how Unbound was installed.

Options:
- `-a` also reads the zone files of auth-zones and RPZ and checks their syntax.
- `-q` suppresses output on success.
- `-o <option>` prints that option's value to stdout after checking; a disabled option (`""`) prints an empty line.
- `-f` prints the full pathname with chroot applied; use it with `-o`.
- `-h` shows version and help.

Exit code 0 means the file is correct, 1 means an error was found.

The getting-started guide advises running it to find configuration errors before starting the server, then starting in debug mode with `unbound -d -vv -c unbound.conf` and dropping `-d` and `-v` once it works.

## Checked

2026-11-08. Read the unbound-checkconf manual page source in full and the getting-started configuration page in full. Added the -a option and replaced a hard-coded default config path with the install-dependent default.

Method: documentation only; no commands were run.
