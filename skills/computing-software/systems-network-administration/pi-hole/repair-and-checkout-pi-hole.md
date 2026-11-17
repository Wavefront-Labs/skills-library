---
id: computing-software.systems-network-administration.pi-hole.repair-and-checkout-pi-hole
name: repair-and-checkout-pi-hole
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-repair, pihole-checkout, branch-testing]
level: advanced
status: docs-checked
description: "Repair a broken Pi-hole install while keeping settings, or switch components to another GitHub branch for testing."
sources: ["https://docs.pi-hole.net/main/pihole-command/", "https://docs.pi-hole.net/main/post-install/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repair and checkout

**Repair**

```bash
pihole repair    # or: pihole -r
```

This runs `basic-install.sh` with the Repair option. Existing settings are retained and scripts or dependencies are repaired as necessary. The rest of the installer then runs as normal.

Repair needs a working internet connection. If the host uses Pi-hole as its only DNS resolver and Pi-hole is down, repair can fail; temporarily give the host another resolver.

**Checkout**

```bash
pihole checkout dev
pihole checkout core branchName
```

`pihole checkout` switches Pi-hole subsystems (core, web, FTL) to a different GitHub branch and repository. Developers sometimes ask users to do this to test a fix. See `pihole checkout --help`.

**Checklist**

1. Try `pihole debug` first to see what is wrong.
2. Run `pihole repair`.
3. Use `pihole checkout` only when a developer asks, and return to the stock branch afterwards.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: The pihole Command (main/pihole-command); Post-Install (main/post-install). Removed the Docker paragraph (disabled commands and `build.sh` flags), which is not on the cited pages.
Method: documentation only; no commands were run.
