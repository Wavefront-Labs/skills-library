---
id: computing-software.networking-hardware-and-wireless.arista-eos.extensions-swix
name: extensions-swix
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, extensions, swix, eos-extension, install-extension]
level: practitioner
status: draft
description: "Install, list and persist EOS extensions such as agents and tools using .swix files."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EOS extensions (.swix)
Goal: add supported packages to EOS.

```
switch# copy http://192.0.2.70/ext/tool-1.0.swix extension:
switch# extension tool-1.0.swix
switch# copy installed-extensions boot-extensions
switch# show extensions
switch# show boot-extensions
```

- `extension` installs for the current boot; `copy installed-extensions boot-extensions` persists it across reloads.
- `no extension <file>` and `delete extension:<file>` remove one.
- `show extensions` lists status (`A` available, `I` installed, `F` forced).

Gotcha: forgetting to copy to `boot-extensions` means the extension disappears after a reload and any dependent automation breaks. Check compatibility with the EOS version first.

Operational tip: record installed extensions and versions in your inventory and compare them after upgrades, since an EOS upgrade may need new extension builds. Remove unused extensions to reduce attack surface. Keep a copy of every approved .swix on an internal server with checksums so rebuilds do not depend on external downloads.

## Verify
- After a reload `show extensions` still lists the extension as installed.
