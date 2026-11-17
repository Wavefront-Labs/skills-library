---
id: computing-software.systems-network-administration.varnish-cache.backend-health-probes
name: backend-health-probes
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [health-probe, probe-window-threshold, backend-list, set-health]
level: practitioner
status: docs-checked
description: "Configure backend health probes (url, request, interval, timeout, window, threshold, initial) and inspect or override health with backend.list and backend.set_health."
sources:
  - https://www.varnish.org/docs/reference/vcl-probe/
  - https://www.varnish.org/docs/reference/varnish-cli/
  - https://www.varnish.org/docs/users-guide/vcl-backends/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# backend health probes

Per backend, shared by name, or as `probe default { ... }`:

```vcl
probe light {
    .url = "/health";
    .timeout = 2s;
    .interval = 5s;
    .window = 8;
    .threshold = 3;
    .initial = 2;
}
backend foo { .host = "192.0.2.10"; .probe = light; }
```

Defaults: `.url` `/`, `.expected_response` 200, `.timeout` 2s, `.interval` 5s, `.window` 8, `.threshold` 3, `.initial` one less than threshold (so a backend is sick until its first good probe returns), `.expect_close` true. `.request` sends a full HTTP/1.1 request and must include `Connection: close`.

A 64-stage shift register records recent results; the backend is healthy when at least `.threshold` of the last `.window` probes were good.

CLI:

```bash
varnishadm backend.list -p
varnishadm backend.set_health boot.foo sick     # healthy | sick | auto
```

Probes run for all loaded VCLs and identical probes are coalesced, so discard old VCLs.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the unsupported 503 claim and added the vcl-backends source for probe coalescing.

Method: documentation only; no commands were run.
