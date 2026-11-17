---
id: computing-software.cloud-infrastructure-engineering.fluentd.command-line-options-and-tools
name: command-line-options-and-tools
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, command-line, fluent-cat, fluent-plugin-config-format, fluent-plugin-generate, dry-run]
level: practitioner
status: docs-checked
description: "Fluentd CLI: fluentd flags (-c, -d, --workers, -v/-q, -i, --no-supervisor), fluent-cat for test events, fluent-plugin-config-format and fluent-plugin-generate."
sources:
  - https://docs.fluentd.org/deployment/command-line-option
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd command line
`fluentd` options: `-s/--setup [DIR]` sample config, `-c/--config PATH` (default `/etc/fluent/fluent.conf`), `--dry-run`, `-p` plugin dir, `-I`, `-r`, `-d/--daemon PIDFILE`, `--no-supervisor`, `--workers NUM`, `--user`, `--group`, `--umask`, `-o/--log PATH`, `--log-rotate-age`, `--log-rotate-size`, `-i/--inline-config`, `--emit-error-log-interval`, `--suppress-repeated-stacktrace`, `--without-source`, `--with-source-only`, `--strict-config-value`, `-v`/`-vv` (debug/trace), `-q`/`-qq` (warn/error), `--suppress-config-dump`, `-g/--gemfile`, `-G`, `--conf-encoding`, `--disable-shared-socket`, `--enable-size-metrics`.

Notes from the page:
- `-g` starts with bundler-managed plugins; `--suppress-config-dump` hides secrets such as private keys from logs.
- `--without-source` is useful to flush buffers without new events.
- `-i` helps on platforms without persistent disks; `--no-supervisor` avoids a double supervisor with your own tool.

`fluent-cat <tag>` sends events to `in_forward` or `in_unix` (`-p` port default 24224, `-h` host default 127.0.0.1, `-u`/`-s` unix socket, `-f` format json|msgpack|none, `--message-key`, `--retry-limit`):
```
echo '{"message":"hello"}' | fluent-cat debug.log
```
`fluent-plugin-config-format [-f markdown|txt|json] [-c] [-t] <type> <name>` prints a plugin's parameters, e.g. `fluent-plugin-config-format output null`. `fluent-plugin-generate <type> <name>` scaffolds a plugin project.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/command-line-option and confirmed: fluentd flags, notes on -g, -i, --no-supervisor, fluent-cat options and defaults, fluent-plugin-config-format and fluent-plugin-generate usage. Removed or reworded: nothing.

Method: documentation only; no commands were run.
