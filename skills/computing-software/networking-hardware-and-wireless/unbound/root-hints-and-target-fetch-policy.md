---
id: computing-software.networking-hardware-and-wireless.unbound.root-hints-and-target-fetch-policy
name: root-hints-and-target-fetch-policy
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, root-hints, target-fetch-policy, iterator, nameserver-targets]
level: advanced
status: draft
description: "Override Unbound built-in root hints and set how aggressively it fetches nameserver target addresses with target-fetch-policy."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# root hints and target fetch policy
`root-hints` is a filename, default `""`, which uses the built-in hints for class IN. A file must be in zone-file format and contain only root server names and addresses.

`target-fetch-policy` is a quoted list of numbers, default `"3 2 1 0 0"`. Each position is a dependency depth and sets how many nameserver target addresses are fetched opportunistically: `-1` fetches all, `0` fetches on demand only, a positive number fetches that many. All zeros approximates BIND 9 behaviour; all `-1` is said to approximate BIND 8.

`unbound-control list_stubs` includes the root hints in use. In `unbound-anchor`, `-r <root.hints>` supplies a hints file to bootstrap resolution.
