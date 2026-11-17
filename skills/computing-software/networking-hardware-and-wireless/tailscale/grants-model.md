---
id: computing-software.networking-hardware-and-wireless.tailscale.grants-model
name: grants-model
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [grants, ip-capabilities, app-capabilities]
level: advanced
status: docs-checked
description: "Use grants to combine network (ip) and application (app) permissions in one rule."
sources: ["https://tailscale.com/kb/1324", "https://tailscale.com/kb/1337"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grants

Goal: express access as source, destination and capabilities.

A grant needs `src`, `dst` and at least one of `ip` (network layer) or `app` (application layer).

```
{
  "grants": [
    {"src": ["group:dev"], "dst": ["tag:db"], "ip": ["tcp:5432"]},
    {"src": ["group:dev"], "dst": ["tag:db"],
     "app": {"tailscale.com/cap/tailsql": [{"<param>": "<value>"}]}}
  ]
}
```

**Fields**

- `src` and `dst` accept emails, `group:`, `tag:`, roles such as `autogroup:admin`, and for destinations also `autogroup:internet` and `svc:<name>` (Tailscale Services).
- `ip` lists network capabilities by protocol and port, for example `tcp:443` or `*`.
- `app` uses the key format `domainName/capabilityName`. The application defines its own capabilities and parameters; Tailscale treats the parameters as opaque JSON and only checks that it is valid JSON.
- Device posture checks apply only to the source of a grant, not the destination.
- Grants and legacy ACLs can coexist in the same policy file.
- Grants add routing awareness through `via`.

**Checklist**

1. Each grant has `ip` or `app`.
2. App capability names come from the application's own docs.
3. Posture only on `src`.

## Checked

2026-11-09. Confirmed against the Tailscale Grants page: src, dst, ip and app fields, selector types, app key format, opaque JSON parameters, posture on src only, coexistence with ACLs and via. The wildcard ip value was confirmed on the policy syntax page. Replaced the example application parameter, which no page documents, with a placeholder.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1324 (Grants), read in full, and kb/1337 (policy syntax), searched for ip and app examples.
