---
id: computing-software.software-engineering.ocaml.structured-logging-with-logs
name: structured-logging-with-logs
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, logs-library, ocaml-observability, log-sources, log-reporter, log-levels]
level: practitioner
status: docs-checked
description: "Create Logs sources per library, set levels and a reporter in the application only, and log lazily with msgf closures."
sources: ["https://erratique.ch/software/logs", "https://erratique.ch/software/logs/doc/Logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logs

```ocaml
let src = Logs.Src.create "myapp.db" ~doc:"database layer"
module Log = (val Logs.src_log src : Logs.LOG)
let query () = Log.debug (fun m -> m "running %s" "select"); Log.err (fun m -> m "failed: %s" "x")

(* application only *)
let main () =
  Logs.set_reporter (Logs_fmt.reporter ());
  Logs.set_level (Some Logs.Info);
  if Logs.err_count () > 0 then 1 else 0
```

## Notes
- Levels are `App`, `Error`, `Warning`, `Info`, `Debug`. A source with level `Some l` reports messages at level l or lower (more severe); `None` reports nothing.
- Libraries create or reuse a source, and never install reporters, set levels, log on the default source or log at `App` level; the application controls these.
- An application must set a reporter before logging, otherwise no messages are reported (the initial reporter is `nop_reporter`).
- Message formatting happens only when the message is reported: `Logs.err (fun m -> m "invalid kv (%a,%a)" pp_key k pp_val v)`.
- `Logs.err_count ()` and `Logs.warn_count ()` count messages at those levels across all sources, useful for exit status.
- `Logs.set_level ?all` also sets existing sources by default (`all` true); use `Logs.Src.set_level` for one source.
- Optional libraries: `Logs_fmt` (reporter on Fmt formatters), `Logs_cli` (command-line control, depends on Cmdliner), `Logs_lwt` (Lwt logging functions).
- Multi-threaded programs: reporter access needs mutual exclusion via `Logs.set_reporter_mutex`; with OCaml Threads, call `Logs_threaded.enable`.
- `Logs.format_reporter` is synchronous, so channel-backed formatters block until written, which may not suit Lwt.

## Self-check
- [ ] A library using Logs installs no reporter; the executable sets one before the first log call.

## Checked
Date: 2026-11-08. Confirmed against the Logs landing page and the Logs API page (reporting levels, sources, usage conventions, reporter setup, set_reporter_mutex, counts, synchronous note). Removed unconfirmed claims: findlib library names, the exact `-v`/`-q` flags of `Logs_cli`, and the claim that Logs is unsafe across domains (only the documented mutex hook is kept).
Method: documentation only; no commands were run.
