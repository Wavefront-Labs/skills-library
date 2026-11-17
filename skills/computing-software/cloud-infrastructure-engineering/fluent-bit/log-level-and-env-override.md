---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.log-level-and-env-override
name: log-level-and-env-override
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, log-level, flb-log-level, debugging, environment-variable]
level: intro
status: docs-checked
description: "Raise Fluent Bit's own log verbosity for one run with FLB_LOG_LEVEL without editing the configuration."
sources: ["https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/service-section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Log level and FLB_LOG_LEVEL

The service key `log_level` sets the verbosity of Fluent Bit's own logs. Values: `off`, `error`, `warn`, `info`, `debug`, `trace`. They are cumulative, so `debug` includes error, warning and info. `trace` exists only if Fluent Bit was built with the `FLB_TRACE` option. Logs go to stderr unless `log_file` names an absolute path.

The same setting is available as the `FLB_LOG_LEVEL` environment variable, which accepts the same values, is not case-sensitive, and treats `warning` as an alias for `warn`. If both the variable and the key are set, the environment variable takes precedence and the configured value is ignored in version 5.1.2 and greater, which lets you raise verbosity for a single run:

```shell
FLB_LOG_LEVEL=debug fluent-bit --config fluent-bit.yaml
```

In versions 5.1.0 and 5.1.1, setting both fails at startup with `could not configure service property log_level`; 5.1.2 and greater applies the precedence above.

## Checked

2026-11-03. Confirmed on the Fluent Bit YAML Service section page (Log level): values, cumulative behaviour, FLB_TRACE, stderr and `log_file`, FLB_LOG_LEVEL case and `warning` alias, 5.1.2 precedence, 5.1.0 and 5.1.1 startup failure. Removed: unsourced advice and verification step.

Method: documentation only; no commands were run.
