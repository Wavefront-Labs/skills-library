---
id: computing-software.networking-hardware-and-wireless.bind9.response-rate-limiting
name: response-rate-limiting
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rate-limit, rrl, responses-per-second]
level: advanced
status: docs-checked
description: "Configure BIND 9 response rate limiting: responses-per-second, window, slip, prefix lengths, exempt-clients and log-only."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# response rate limiting
`rate-limit` in `options` or `view` limits identical responses to a client network, which blunts reflection attacks on authoritative servers.

```
rate-limit {
    responses-per-second 10;
    exempt-clients { /* trusted addresses */ };
};
```

Rates: `responses-per-second`, `nodata-per-second`, `nxdomains-per-second`, `referrals-per-second`, `errors-per-second`, `all-per-second`.

Other options: `window` (default 15 seconds), `slip` (default 2, range 0-10; with 2, every other UDP request without a valid server cookie gets a small response; 0 sends none), `ipv4-prefix-length` (24), `ipv6-prefix-length` (56), `qps-scale`, `log-only`, `min-table-size`, `max-table-size`.

Start with `log-only yes` to see what would be limited.

## Checked

2026-11-04. Read the rate-limit block and each option entry in the Administrator Reference Manual (window, slip, prefix lengths, qps-scale, exempt-clients, table sizes, log-only); defaults and ranges confirmed. Nothing was removed.

Method: documentation only; no commands were run.
