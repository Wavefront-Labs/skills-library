---
id: computing-software.systems-network-administration.pi-hole.manage-allow-deny-lists-cli
name: manage-allow-deny-lists-cli
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [allowlist-cli, denylist-cli, domainlist-table]
level: practitioner
status: docs-checked
description: "Add and remove exact and regex allowlist and denylist entries with the pihole command, including quiet mode and group scope."
sources: ["https://docs.pi-hole.net/guides/misc/allowlist-denylist/", "https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allowlist and denylist from the CLI

**Exact domains**

```bash
pihole allow domain1 [domain2 ...]
pihole deny domain1 [domain2 ...]
pihole allow remove domain1
pihole deny remove domain1
```

Parameters: any number of domains, `remove` to delete instead of add, and `-q` for quiet output (useful from scripts). Each domain is validated; invalid domains and IDNs are ignored.

**Regex and wildcard entries**

```bash
pihole --regex '^example.com$' '.*\.example2.net'
```

The related switches are `--wild`, `--allow-regex` and `--allow-wild`. Domains are validated except when using `--regex`.

**What happens.** The script adds or removes a row in the `domainlist` table of `/etc/pihole/gravity.db`, then reloads the DNS server.

**Group scope.** New entries belong to the Default group only. To apply an entry to other groups, assign groups under Group Management > Domains in the web interface.

**Checklist**

1. Run the add command.
2. Confirm the entry in the web interface or with `pihole -q -exact example.com`.
3. Check group assignment if only some clients should be affected.
4. See `pihole allow --help` and `pihole deny --help` for the full option list.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Allowlist and Denylist editing (guides/misc/allowlist-denylist); The pihole Command (main/pihole-command). Changed the query example to the form the pihole command page shows (`pihole -q -exact`).
Method: documentation only; no commands were run.
