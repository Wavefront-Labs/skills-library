---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-status-pages-and-custom-domains
name: uptime-kuma-status-pages-and-custom-domains
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [status-page, custom-domain, x-forwarded-host, slug, public-status, iframe, clickjacking]
level: practitioner
status: docs-checked
description: "Publish Uptime Kuma status pages, map them to custom domains, and understand the 5-minute cache and the default slug."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Status-Page"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Status pages

Status pages are for public users. Facts to design around:
- Results are cached for 5 minutes and the page refreshes every 5 minutes, so it is less responsive than the dashboard.
- `default` is a reserved slug: `http://example.com/status` points to `http://example.com/status/default`.
- Multiple status pages are supported since 1.13.0.

Domain names per status page (since 1.14.0):
1. Without a reverse proxy, expose Uptime Kuma on port 80. With one, add the domain in the proxy and point it at Uptime Kuma; for nginx or Apache you must forward `X-Forwarded-Host` or `Host`, otherwise Uptime Kuma cannot know the current domain.
2. Add an A or CNAME DNS record for the domain.
3. Add the domain in the status page settings sidebar.

Subdirectory or custom HTML is not supported natively; the wiki workaround is an HTML page embedding Uptime Kuma in a 100% width and height iframe. That requires `UPTIME_KUMA_DISABLE_FRAME_SAMEORIGIN=true`, which turns off the anti-framing protection and makes you vulnerable to clickjacking, so only use it where that risk is acceptable.

Monitors on a published status page also get public badges (see uptime-kuma-badges) and show maintenance banners (see uptime-kuma-maintenance-windows).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Status Page page (5 minute cache and refresh, default slug, 1.13.0, 1.14.0, domain steps, iframe workaround and clickjacking caution). Removed: The generic verify line.

Method: documentation only; no commands were run.
