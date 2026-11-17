---
id: computing-software.cloud-infrastructure-engineering.fluentd.linux-capabilities-for-in-tail
name: linux-capabilities-for-in-tail
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, linux-capabilities, fluent-cap-ctl, capng-c, cap-dac-read-search, in-tail, non-root]
level: advanced
status: docs-checked
description: "Let non-root Fluentd read root-only log files using Linux capabilities: capng_c gem, fluent-cap-ctl on the Ruby binary, and Docker cap_add."
sources:
  - https://docs.fluentd.org/deployment/linux-capability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd Linux capabilities
Lets a non-root Fluentd (v1.12 or later) read files like `/var/log/syslog` (mode 640) via `in_tail`.

Prerequisites: `gcc`/`make`, `libcap-ng` and its dev package, `pkg-config`, Ruby with dev package.

1. Install the `capng_c` gem: add `gem 'capng_c'` to the Gemfile, or `fluent-gem install capng_c` (td-agent: `td-agent-gem install capng_c`). If it fails to link `libcap-ng`, check that `pkg-config` is installed.
2. `in_tail` handles `CAP_DAC_READ_SEARCH` and `CAP_DAC_OVERRIDE`. Attach one to the Ruby executable:
```
sudo fluent-cap-ctl --add dac_read_search [-f /path/to/bin/ruby]
sudo fluent-cap-ctl --add dac_override [-f /path/to/bin/ruby]
fluent-cap-ctl --get [-f /path/to/bin/ruby]
```
`--get` lists Effective, Inheritable and Permitted sets.
3. Run Fluentd as the ordinary user; `tail` reads the file without `Permission denied`. Make the `pos_file` directory writable by that user.

Docker: `CAP_DAC_READ_SEARCH` is not available by default. Add `--cap-add DAC_READ_SEARCH` to `docker run`, or in compose:
```
cap_add:
- DAC_READ_SEARCH
```

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/linux-capability and confirmed: prerequisites, capng_c gem, fluent-cap-ctl commands, Docker cap_add. Removed or reworded: nothing.

Method: documentation only; no commands were run.
