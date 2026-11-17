---
id: computing-software.search-and-information-retrieval.typesense.server-configuration-parameters
name: server-configuration-parameters
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [server-configuration, config-file, environment-variables, typesense]
level: practitioner
status: docs-checked
description: "Configure typesense-server via --parameter=value flags, a config file, or TYPESENSE_ environment variables, with precedence rules."
sources: ["https://typesense.org/docs/30.2/api/server-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server configuration methods

Typesense accepts the same settings in three forms.

## Command line

`--parameter=value`. Required ones: `--api-key`, the bootstrap admin key allowing all operations (never expose it to browser JavaScript; create search-only or scoped keys with the key management API), and `--data-dir`, the directory where data is stored on disk. `--config` points to a configuration file that can hold all the other arguments.

## INI file

Pass the file with `--config`. The Linux DEB and RPM packages install it at `/etc/typesense/typesense-server.ini`. It uses a simple INI format, and any parameter from the command line table can be used there without the preceding `--`.

## Environment variables

Use capitals and underscores instead of hyphens, and prefix `TYPESENSE_`: for example `TYPESENSE_DATA_DIR` for `--data-dir`.

## Precedence

Command line arguments win, environment variables have the lowest priority.

On Typesense Cloud these server parameters are managed for you; to change one, email support with the use case.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Server Configuration (names, defaults, parameters and behaviours as stated in the skill). Removed: the sample INI section name and example values and the sample environment-variable command line, which the page does not show in readable form.

Method: documentation only; no commands were run.
