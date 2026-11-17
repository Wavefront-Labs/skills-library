---
id: computing-software.networking-hardware-and-wireless.unbound.unbound-host-lookup-tool
name: unbound-host-lookup-tool
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-host, dnssec-lookup, libunbound, trust-anchor-testing]
level: intro
status: docs-checked
description: "Run validating lookups with unbound-host: type and class, trust anchors from DS, DNSKEY or files, config files, forwarders and exit codes."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-host.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-host lookup tool
`unbound-host [options] hostname`. Passing an IP address does a reverse lookup. By default it reads no configuration file and tries to reach the internet root servers. Its default lookup is IPv4, IPv6 and mail handler records (PTR for reverse).

Options:
- `-v` adds secure, insecure or bogus to each line.
- `-d` debug to stderr; repeat for packet detail.
- `-t type`, `-c class` (default IN).
- `-D` enables DNSSEC validation using the root anchor at the default configured location (set at build or install time).
- `-y key` trust anchor as a DS or DNSKEY record.
- `-f keyfile` zone-file anchors, one per line; `-F namedkeyfile` reads only `trusted-key` entries from a BIND `named.conf`.
- `-C configfile` loads an unbound.conf; put it first so later options override.
- `-r` uses forwarders from `/etc/resolv.conf`; validation fails if they lack DNSSEC.
- `-4` / `-6` restrict IP version.

Examples: `unbound-host www.example.com`; `unbound-host -v -y "example.com DS ..." www.example.com`. The manual's example keys are fake, so validation reports a failure.

Exit code 0 means no error (data may still be unavailable); 1 means a fatal error.

## Checked

2026-11-08. Read the unbound-host manual page source in full. Replaced a hard-coded root.key path with the install-time default and added that no config file is read by default.

Method: documentation only; no commands were run.
