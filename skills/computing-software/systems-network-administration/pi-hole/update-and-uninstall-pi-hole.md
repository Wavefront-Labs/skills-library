---
id: computing-software.systems-network-administration.pi-hole.update-and-uninstall-pi-hole
name: update-and-uninstall-pi-hole
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-update, pihole-uninstall, release-notes]
level: intro
status: docs-checked
description: "Update a bare-metal Pi-hole with pihole -up after reading release notes, and remove it with pihole uninstall."
sources: ["https://docs.pi-hole.net/main/update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Update and uninstall Pi-hole

**Update a regular installation**

```bash
pihole -up
```

`pihole updatePihole` is the long form. The script asks GitHub whether Core, Web interface or FTL have updates, downloads changes with `git`, and then runs `basic-install.sh`.

Always read the release notes for every component before a major update such as v5 to v6:

The notes are in the respective repository for Core, FTL and Web.

The Pi-hole blog sometimes carries a post on notable changes.

**Docker installs** do not use `pihole -up`; replace the container with a newer image instead (see the Docker upgrade skill).

**Uninstall**

```bash
pihole uninstall
```

It gives the option to remove each dependency individually.

**Checklist**

1. Read release notes for Core, FTL and Web.
2. Run `pihole -up`.
3. Run `pihole version` (also `pihole -v`) to confirm installed versions.
4. Run `pihole status` to confirm DNS and blocking are running.

## Checked

2026-11-03. Read the Updating page (`pihole -up`, release-notes warning for v5 to v6, blog posts, Docker pointer) and The pihole Command page (update, version, uninstall, status). Removed the unverified GitHub release URLs and the advice on which packages to keep.

Method: documentation only; no commands were run.
