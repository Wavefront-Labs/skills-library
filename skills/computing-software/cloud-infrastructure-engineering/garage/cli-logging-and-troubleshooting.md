---
id: computing-software.cloud-infrastructure-engineering.garage.cli-logging-and-troubleshooting
name: cli-logging-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [rust-log, log-level, troubleshooting, garage-cli]
level: intro
status: docs-checked
description: "Raise Garage log verbosity with RUST_LOG and check the permissions and paths that most often break the first start."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
  - https://garagehq.deuxfleurs.fr/documentation/operations/debugging/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Quick Start troubleshooting section lists the usual first-run problems. Make sure the configuration file, `metadata_dir` and `data_dir` are readable by the user running the server, or by the Docker user. When you run the `garage` CLI, it needs the right path to the configuration file and read access to the metadata directory, because it reads connection parameters from there.

Verbosity is controlled by the `RUST_LOG` environment variable. Levels from least to most verbose are `error`, `warn`, `info`, `debug` and `trace`. Examples from the guide:

- `RUST_LOG=garage=info garage server` is the default, recommended for most cases.
- `RUST_LOG=garage=debug garage server` helps work out why S3 API calls are failing.
- `RUST_LOG=garage=trace garage server` is the most detailed.

The Docker debugging page adds that a container started from the official image has no shell, so inspect it with `docker logs garage`, set `RUST_LOG=garage=debug` when starting the container, and run subcommands directly with `docker exec garage /garage status`. The configuration reference separately describes `GARAGE_LOG_TO_SYSLOG`, `GARAGE_LOG_TO_JOURNALD`, `GARAGE_LOG_FORMAT` and `NO_COLOR`.

## Checked

2026-11-04. Read the Quick Start troubleshooting section, the Docker debugging page and the environment variable list of the Configuration page. Confirmed the permission advice, the five log levels and default, the three RUST_LOG examples, the no-shell image note, the docker commands and the four logging variables. Nothing removed.
Method: documentation only; no commands were run.
