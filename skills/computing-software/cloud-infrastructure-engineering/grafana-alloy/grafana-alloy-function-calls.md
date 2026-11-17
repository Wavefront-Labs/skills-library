---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-function-calls
name: grafana-alloy-function-calls
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [function-calls, stdlib, sysenv, encodingfrom-json, stringformat, arrayconcat]
level: practitioner
status: docs-checked
description: "Use Alloy standard library function calls in expressions: sys.env, encoding.from_json and from_yaml, string.format, string.join and array.concat."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/expressions/function_calls.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Function calls in expressions

Functions take zero or more arguments and return one value. Arguments are evaluated left to right, type checked, then the function runs. If a function fails, evaluation stops with an error (fail fast). You cannot define your own functions in config; they come from the standard library or from component exports.

Standard library namespaces: `sys` (environment), `encoding` (JSON/YAML), `string`, `array`, `convert`.

```alloy
log_level    = sys.env("LOG_LEVEL")
data_dir     = sys.env("DATA_PATH") + "/metrics"
config_data  = encoding.from_json(local.file.config.content)
metrics_conf = encoding.from_yaml(local.file.metrics.content)
full_address = config_data["host"] + ":" + string.format("%d", config_data["port"])
job_name     = string.format("%s-%s", config_data["service"]["name"], sys.env("ENVIRONMENT"))
log_file     = string.join(["/var/log", "app", "app.log"], "/")
all_targets  = array.concat(
  discovery.kubernetes.services.targets,
  discovery.file.local.targets,
  [{ "__address__" = "localhost:9090" }]
)
```

Components may export functions, called through the component reference, for example `validator.config.is_valid(processed_targets)`. They behave like stdlib functions and can be combined with operators such as `&&` and `==`.

## Checked

2026-11-08. Read the Function calls page in full. Confirmed: argument evaluation order and type checking, fail-fast behaviour, no user-defined functions, the two function sources, the five standard library categories, the common example expressions, and component-exported functions combined with operators.

Method: documentation only; no commands were run.
