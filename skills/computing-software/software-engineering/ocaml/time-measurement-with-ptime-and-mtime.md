---
id: computing-software.software-engineering.ocaml.time-measurement-with-ptime-and-mtime
name: time-measurement-with-ptime-and-mtime
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, time-ptime-mtime, ocaml-time, ptime, mtime, monotonic-clock, unix-gettimeofday]
level: practitioner
status: docs-checked
description: "Read wall-clock time with Ptime and measure durations with the monotonic Mtime_clock counter, never by subtracting wall-clock timestamps."
sources: ["https://erratique.ch/software/ptime", "https://erratique.ch/software/ptime/doc/Ptime/", "https://erratique.ch/software/mtime/doc/Mtime_clock/", "https://erratique.ch/software/logs/doc/Logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time

```ocaml
(* Mtime_clock: monotonic durations *)
let c = Mtime_clock.counter ()
let () = do_work ()
let elapsed_us = Mtime.Span.to_us (Mtime_clock.count c)

(* Ptime: POSIX timestamps, RFC 3339 *)
let s = Ptime.to_rfc3339 ~tz_offset_s:0 t    (* t : Ptime.t *)
let r = Ptime.of_rfc3339 "2026-11-08T10:00:00Z"
```

## Notes
- Ptime POSIX timestamps are always on the UTC timeline, with picosecond precision in the range `Ptime.min` to `Ptime.max`. The separate Ptime_clock library gives access to the system POSIX clock and current time zone offset.
- Platform POSIX timestamps are not monotonic: they follow OS time adjustments and can go back. For spans within one program run use a monotonic source such as Mtime. The Ptime docs also warn against using `Ptime.diff` / `add_span` for wall-clock durations or calendar arithmetic.
- `Mtime_clock.counter ()` starts a counter; `Mtime_clock.count c` is the span elapsed since it was created. `Mtime_clock.elapsed ()` is the span since program start and `now ()` has no meaningful absolute value.
- `Mtime_clock` functions `elapsed`, `now`, `counter` raise `Sys_error` if the time cannot be determined; catch it at top level, log and abort.
- Linux uses `clock_gettime` with `CLOCK_BOOTTIME`, so sleep time is counted; other POSIX platforms use `CLOCK_MONOTONIC`.
- `Ptime.of_float_s` is compatible with the result of `Unix.gettimeofday`, but floats do not round-trip exactly (see the Ptime warning).
- `Ptime.of_rfc3339` returns a result `(t, tz_offset option, bytes_read)`; with the default `~strict:false` it also accepts lowercase `t`/`z`, space separators and `hhmm`/`hh` offsets. `Ptime.to_rfc3339 ?frac_s ?tz_offset_s t` renders exactly `frac_s` fractional digits (0-12).
- POSIX time does not count leap seconds, and Ptime is not a calendar library and has no time zone database (offsets only).

## Self-check
- [ ] Durations come from `Mtime_clock.count`, not from subtracting two wall-clock timestamps.

## Checked
Date: 2026-11-08. Confirmed against the Ptime and Mtime_clock API pages and the Ptime landing page on erratique.ch (Ptime module, Notes and limitations, Platform support, Error handling) and the Logs page (use of `Mtime.Span.to_us`). Removed unconfirmed claims: library findlib names, `Ptime_clock.now`, `Mtime.Span.to_float_ns`, `Sys.time` semantics, microsecond precision of `gettimeofday`, timedesc/tzdb recommendations, Eio and Lwt time helpers.
Method: documentation only; no commands were run.
