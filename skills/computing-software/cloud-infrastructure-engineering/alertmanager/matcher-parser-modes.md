---
id: computing-software.cloud-infrastructure-engineering.alertmanager.matcher-parser-modes
name: matcher-parser-modes
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, utf8-strict-mode, classic-mode, fallback-mode, feature-flags]
level: sme
status: docs-checked
description: "Alertmanager 0.27+ matcher parser modes: fallback (default), UTF-8 strict and classic, with enabling flags and the amtool migration check."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Matcher parser modes

Alertmanager 0.27 and later has a new matcher parser with some backwards-incompatible changes. During the transition period there are three server modes.

Fallback mode (default): configurations are parsed first as UTF-8 matchers; if incompatible, they are parsed as classic matchers and a warning is logged. Routes, silences and inhibition rules behave as before. A warning of `Matchers input has disagreement` means a matcher is valid in both parsers but parses differently; review each case individually.

UTF-8 strict mode disables classic matchers:

```
alertmanager --config.file=config.yml --enable-feature="utf8-strict-mode"
```

Recommended for new installations, and for existing ones once all incompatible-matcher warnings are resolved. Alertmanager will not start until warnings are fixed. It becomes the default at the end of the transition period.

Classic mode equals Alertmanager 0.26.0 and older:

```
alertmanager --config.file=config.yml --enable-feature="classic-mode"
```

Use it if you suspect an issue with the other modes, and open a GitHub issue.

Verification without a server: run `amtool check-config config.yml`. No warnings means the file is strict-mode compatible. Adding `--enable-feature="utf8-strict-mode"` makes an incompatible file fail, for example with `expected label value`.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the matcher parser modes. Removed: nothing.

Method: documentation only; no commands were run.
