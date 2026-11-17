---
id: computing-software.systems-network-administration.headscale.logtail-privacy
name: logtail-privacy
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, logtail, no-logs-no-support, privacy, client-logging]
level: practitioner
status: docs-checked
description: "Stop Tailscale clients sending logs to Tailscale Inc: the logtail.enabled setting, the data-plane-audit-logs attribute trap, and client-side opt-outs."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding logs sent to Tailscale Inc

By default Headscale tells clients to disable log submission once they connect, controlled by:

```yaml
logtail:
  enabled: false
```

Enabling it makes the clients of your Headscale instance send logs to Tailscale Inc.

## Trap

Do not grant the node attribute `https://tailscale.com/cap/data-plane-audit-logs` while `logtail.enabled` is `false`. A client with log submission disabled treats that attribute as "the tailnet requires logging" and turns itself off, as `tailscale down` would, until the attribute is removed and `tailscale up` is run. A client started with `TS_NO_LOGS_NO_SUPPORT=true` or `--no-logs-no-support` reacts the same way, whatever `logtail.enabled` says.

## Client-side opt-out (independent of Headscale)

- Environment variable `TS_NO_LOGS_NO_SUPPORT=true`.
- `tailscaled` flag `--no-logs-no-support`.
- Mobile app: disable "Remote client logging" in settings.

## Checked

2026-11-04. Confirmed against the Headscale FAQ (avoiding logs to Tailscale Inc, attribute warning, client-side opt-outs) and config-example.yaml (`logtail.enabled` default false). Removed the Verify section, which was not on either page.

Method: documentation only; no commands were run.
