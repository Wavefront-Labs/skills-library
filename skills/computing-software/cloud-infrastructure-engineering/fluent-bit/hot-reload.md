---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.hot-reload
name: hot-reload
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, hot-reload, sighup, reload-endpoint, configuration-reload]
level: practitioner
status: docs-checked
description: "Reload Fluent Bit configuration without a restart through the reload endpoint or SIGHUP."
sources: ["https://docs.fluentbit.io/manual/administration/hot-reload"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hot reload

Hot reloading works on Linux, macOS and Windows. Enable it in the configuration or with `-Y` / `--enable-hot-reload` on the command line:

```yaml
service:
  http_server: on
  http_listen: 0.0.0.0
  http_port: 2020
  hot_reload: on
```

After editing the file, reload by one of two routes.

**HTTP.** `PUT /api/v2/reload` or `POST /api/v2/reload`. With curl you must send an empty JSON body:

```shell
curl -X POST -d '{}' localhost:2020/api/v2/reload
```

`GET /api/v2/reload` returns the count of reloads so far, for example `{"hot_reload_count":3}`; it starts at `0`. Other methods return `405 Method Not Allowed`.

**Signal.** Send `SIGHUP` to the process. `SIGHUP` is not supported on Windows.

Relative paths for `parsers_file`, `plugins_file`, upstream files and `streams_file` resolve first against the process working directory, then against the directory holding the main configuration file. If the directory cannot be preserved, the reload halts with `[reload] copying configuration path failed. Reloading is halted` and the previous configuration keeps running. Before version 5.1.2 the reloaded configuration loses the main file's directory, so use absolute paths for referenced files on those versions.

Settings such as `security.fips_mode` cannot change by reload (see `computing-software.cloud-infrastructure-engineering.fluent-bit.fips-mode`).

Obtain the reload count with `GET /api/v2/reload`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Hot reload page and the Monitoring page (/api/v2/reload, 405 for other methods): enabling, endpoints, empty body for curl, hot_reload_count and its 0 start, SIGHUP not on Windows, relative path resolution and the halt message, 5.1.2 behaviour.

Method: documentation only; no commands were run.
