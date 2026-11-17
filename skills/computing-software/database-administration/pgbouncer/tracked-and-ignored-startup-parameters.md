---
id: computing-software.database-administration.pgbouncer.tracked-and-ignored-startup-parameters
name: tracked-and-ignored-startup-parameters
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, track-extra-parameters, ignore-startup-parameters, startup-parameters, search-path]
level: sme
status: docs-checked
description: "track_extra_parameters and ignore_startup_parameters: which session parameters PgBouncer keeps per client and how to handle unknown startup parameters."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop session parameters leaking between clients and avoid startup parameter errors.

PgBouncer tracks, by default, parameters that Postgres reports and clients can change: application_name, client_encoding, DateStyle, default_transaction_read_only, IntervalStyle, scram_iterations (PostgreSQL 16+), search_path (PostgreSQL 18+), session_authorization, standard_conforming_strings, TimeZone. They are cached per client and restored on the server when the client becomes active.

`track_extra_parameters` (default empty): comma-separated extra parameters, for example `some_extension.setting, other_extension.setting`. Only parameters Postgres reports to clients can be fully tracked. For a tracked parameter Postgres does not report (such as search_path before Postgres 18), PgBouncer knows only the startup-packet (or `options`) value; later SET changes are not tracked and leak to other clients on the shared server connection unless `server_reset_query_always` is used. `options` itself cannot be listed, only parameters contained in it. Citus 12.0+ makes Postgres report search_path.

`ignore_startup_parameters` (default empty): by default only trackable parameters are accepted in startup packets; others raise an error. List names to ignore, for example `options,extra_float_digits`. Listing `options` ignores unknown parameters inside options. Explicitly listed parameters are ignored even if otherwise tracked, which lets you opt out of tracking search_path on older Postgres; including options does not ignore tracked parameters inside options.

`application_name_add_host` (default 0) appends client host address and port to application_name at connection start only; a later SET is not modified.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
