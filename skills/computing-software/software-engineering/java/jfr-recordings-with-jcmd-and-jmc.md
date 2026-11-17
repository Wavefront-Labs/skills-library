---
id: computing-software.software-engineering.java.jfr-recordings-with-jcmd-and-jmc
name: jfr-recordings-with-jcmd-and-jmc
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-diagnostics, jfr-recording, flight-recorder, jcmd-jfr, jdk-mission-control, continuous-profiling, jfr-print]
level: practitioner
status: docs-checked
description: "Record, dump and read JDK Flight Recorder data with -XX:StartFlightRecording, jcmd JFR.*, the jfr tool and JDK Mission Control, with the documented options and defaults."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html", "https://openjdk.org/projects/jmc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JFR recordings

Documented against the JDK 21 manual pages for `java`, `jcmd` and `jfr`.

## Start
```bash
# at launch: keep up to 1 GB / 6 h of disk data, dump on JVM exit
java -XX:StartFlightRecording=filename=app.jfr,maxsize=1g,maxage=6h,dumponexit=true,settings=profile -jar app.jar
# on a running JVM
jcmd <pid> JFR.start name=r1 settings=profile duration=120s filename=r1.jfr
jcmd <pid> JFR.dump name=r1 filename=now.jfr     # write data while the recording keeps running
jcmd <pid> JFR.check
jcmd <pid> JFR.stop name=r1 filename=final.jfr   # without a filename the data is discarded
```
Facts from the manual pages:
- `-XX:StartFlightRecording` is equivalent to the `JFR.start` diagnostic command.
- `settings`: `default.jfc` (default) collects a predefined set with low overhead and "can be used with recordings that run continuously"; `profile.jfc` gives more data with more overhead, for short periods. Both live in `JAVA_HOME/lib/jfr`.
- `maxage` and `maxsize` apply only when `disk=true` (the default); default for both is unlimited (`0s` / `0`). `maxsize` must not be less than `maxchunksize` (set with `JFR.configure`, 12M default).
- `dumponexit` is off by default; with no `filename` the file is written to the process's start directory with a generated name containing PID, recording ID and timestamp. `%p` and `%t` in a filename expand to PID and timestamp.
- `duration` 0 means no limit. `JFR.dump` accepts `begin`/`end` times (local time, or relative such as `-15m`), `name`, `maxage`, `maxsize`; without `name` it dumps all recordings.
- `path-to-gc-roots` (the `java` option; spelled `path-to-gc-root` in `jcmd`) defaults to false: it is time-consuming, so enable it only for a suspected memory leak. With `settings=profile` the allocation stack of the potentially leaking object is included.
- `JFR.configure` sets repository path, `stackdepth` (default 64), `memorysize` (default 10M) and similar; several values cannot change once JFR is initialised.

## Analyse with the jfr tool
```bash
jfr summary app.jfr                                # event counts and sizes
jfr print --categories GC --events CPULoad app.jfr # union of both filters
jfr print --json --stack-depth 20 app.jfr          # --xml also; default stack depth 5
jfr view types app.jfr                             # event types; also: jfr view all-views app.jfr
jfr scrub --exclude-events 'jdk.Socket*' app.jfr clean.jfr
```
- `jfr print` filters take comma-separated names, categories or quoted glob patterns; no filter prints everything.
- `jfr view <view|event-type> file` aggregates; `jfr --help view` lists the available views.
- `jfr scrub` removes sensitive contents or reduces size; with no output file it writes `<input>-scrubbed`.
- `jfr assemble <repository> <file>` rebuilds a recording from chunk files, for example after a JVM crash (unfinished `.part` chunks are excluded); `jfr disassemble` splits one (default 5 chunks per file).

JDK Mission Control (JMC) is a separate OpenJDK project (sponsored by the HotSpot Group, GPLv2) for opening `.jfr` files; get releases from the project's wiki.

## Gotchas
- Recordings can hold sensitive data: use `jfr scrub` before sharing a file.
- In containers write to a volume that survives the pod, and use `dumponexit`.
- The default repository for in-flight data is the OS temp directory (`JFR.configure repositorypath`).

## Verify
Run a recording, then `jfr summary` shows non-zero event counts for the event types you enabled.

## Checked
Confirmed on the JDK 21 manual pages (`java`, `jcmd`, `jfr`) and the JMC project page: the options, defaults, subcommands and syntax above.
Removed: overhead percentages (1% / 2%), JDK-version availability, sampling intervals, the list of event names and what to inspect in JMC, the custom-event Java snippet and the sampling-limitation note (not on the cited pages; the JFR API page returned only a stub).
Method: docs-only read of cited pages, 2026-11-08
