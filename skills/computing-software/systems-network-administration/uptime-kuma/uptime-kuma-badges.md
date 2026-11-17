---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-badges
name: uptime-kuma-badges
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [status-badge, uptime-badge, api-badge, shields-badge, cert-exp, badge-styles, markdown-badge]
level: practitioner
status: docs-checked
description: "Embed Uptime Kuma SVG badges (status, uptime, ping, avg-response, cert-exp, response) for public monitors."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Badge", "https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma badges

Since 1.16.0, badges are SVGs generated locally for every monitor published on a status page. Endpoints under `<kuma-url>/api/badge/:monitorID/`:

- `status`
- `uptime[/:duration]`, `ping[/:duration]`, `avg-response[/:duration]`
- `cert-exp`
- `response`

Duration is in hours (`.../uptime/720?label=30&labelSuffix=d` shows 30 days). In v2 the duration accepts only `24`, `24h`, `30d`, `1y` forms, up to 720h, 1440m or 365d.

Options (query string):
- status: `upLabel` (default Up), `downLabel` (default Down), `upColor`, `downColor`.
- uptime/ping/avg-response/response: `labelPrefix`, `label`, `labelSuffix`, `prefix`, `suffix` (defaults: `%` for uptime, `ms` for the others), `color`, `labelColor`. Uptime colour follows the percentage unless you give a colour name or hex.
- cert-exp: the same plus `upColor`, `downColor`, `warnDays`, `downDays`.
- `style=flat` (default), `flat-square`, `plastic`, `for-the-badge`, `social`.

```
![status](https://kuma.example.com/api/badge/1/status?upLabel=online&downLabel=offline&style=flat-square)
```

A badge maker is built in: open a status page in edit mode, click the settings icon, then Open Badge Maker.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Badge page (endpoints, option names, defaults, styles, badge maker path, version 1.16.0) and Migration From v1 To v2 page (v2 duration limits). Removed: The 404 troubleshooting hint and the generic verify line.

Method: documentation only; no commands were run.
