---
id: computing-software.networking-hardware-and-wireless.arista-eos.software-upgrade-swi
name: software-upgrade-swi
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, swi, eos-upgrade, boot-system, image]
level: practitioner
status: draft
description: "Upgrade EOS by copying a .swi to flash, selecting it with boot system and reloading, with verification and rollback."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EOS image upgrade (SWI)
Goal: upgrade safely.

```
switch# show version
switch# copy scp://admin@192.0.2.70/images/EOS-4.xx.xM.swi flash:
switch# verify /sha512 flash:EOS-4.xx.xM.swi
switch# configure
switch(config)# boot system flash:EOS-4.xx.xM.swi
switch(config)# end
switch# write memory
switch# reload
```

```
switch# show boot-config
switch# dir flash:
```

- Compare the SHA-512 with the value on the Arista software download page.
- Keep the previous image on flash for rollback (re-point `boot system`).
- MLAG pair upgrades: use Arista's recommended MLAG ISSU / staged process, confirm on your release, and upgrade one peer at a time.

Gotcha: not enough flash space makes the copy fail midway; `dir flash:` and delete old images first. Never upgrade both MLAG peers at once.

Operational tip: read the release notes for the target version, take a config backup first, and verify BGP, MLAG and EVPN neighbors after reload before touching the next device in the pair.

## Verify
- `show version` after reload shows the new version; `show boot-config` points at it.
