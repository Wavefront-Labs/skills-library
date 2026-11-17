---
id: computing-software.software-engineering.deno.permissions-network
name: permissions-network
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-net, deny-net, hosts, wildcard, update-check]
level: practitioner
status: docs-checked
description: "Scoping --allow-net by host, port and wildcard subdomain, deny carve-outs, default module-loading hosts, and disabling the daily update check."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--allow-net[=<HOST>...]` (`-N`) covers HTTP requests, TCP/UDP sockets, listeners and DNS resolution. A host is a hostname or IP, optionally with a port. Subdomains are not included unless listed; use `*` as a subdomain wildcard.

```sh
deno run --allow-net=github.com,jsr.io script.ts
deno run --allow-net="*.example.com" script.ts
deno run --allow-net=example.com:80 script.ts
deno run --allow-net=1.1.1.1:443 script.ts
deno run --allow-net=[2606:4700:4700::1111] script.ts
```

Carve out exceptions:

```sh
deno run --allow-net --deny-net=github.com,jsr.io script.ts
```

Module loading is allowed without net permission from deno.land, jsr.io, esm.sh, raw.esm.sh, cdn.jsdelivr.net, raw.githubusercontent.com and gist.githubusercontent.com. Any npm package can be imported through `npm:` specifiers. Add more trusted registries with `--allow-import`.

Deno contacts `https://dl.deno.land/` at most once a day to check for CLI updates; disable with `DENO_NO_UPDATE_CHECK=1`.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md: --allow-net/-N syntax, wildcard and port examples, deny carve-out, default module hosts, npm: specifiers, daily dl.deno.land update check and DENO_NO_UPDATE_CHECK.

Method: documentation only; no commands were run.
