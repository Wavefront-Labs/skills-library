---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-non-gui-cli
name: jmeter-non-gui-cli
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-cli, non-gui-mode, jmeter-command-line, jmeter-properties-override]
level: practitioner
status: docs-checked
description: "Run JMeter load tests in non-GUI mode with the right flags (-n -t -l -j -e -o -J -G -q -f), pass properties, set JVM heap and interpret exit behaviour in CI."
sources:
  - https://jmeter.apache.org/usermanual/get-started.html#non_gui
  - https://jmeter.apache.org/usermanual/get-started.html#override
  - https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-GUI CLI flags

GUI mode is for building and debugging; real load runs use CLI mode (GUI listeners and rendering consume CPU/memory).

```bash
HEAP="-Xms2g -Xmx2g" jmeter -n \
  -t plans/checkout.jmx \
  -l results/run.jtl \
  -j results/jmeter.log \
  -e -o results/dashboard \
  -Jthreads=200 -Jrampup=300 -Jduration=1800 -Jhost=staging.example.com \
  -q env/staging.properties \
  -f
```
| Flag | Meaning |
|---|---|
| `-n` | non-GUI |
| `-t` | test plan |
| `-l` | results file (JTL, CSV by default) |
| `-j` | JMeter log file |
| `-e -o <dir>` | generate HTML dashboard at end; the folder must not exist or be empty |
| `-f` | force delete existing results files and web report folder before the test |
| `-J name=value` | local JMeter property (read via `${__P(name,default)}`) |
| `-G name=value` / `-Gfile` | global property sent to remote servers |
| `-q file` | additional property file |
| `-D name=value` | Java system property |
| `-r` / `-R host1,host2` | remote run on servers in `remote_hosts` / on the listed servers (`-R` overrides `remote_hosts` without defining it) |
| `-X` | exit remote servers at end |
| `-g results.jtl -o dir` | generate dashboard from an existing JTL only |

In the plan, Thread Group fields use `${__P(threads,10)}` so the same JMX serves smoke and full runs.

## CI result checks
The manual documents flags and properties, not a pass/fail exit code for failed samples. Do not rely on the process exit status alone: judge the JTL (or the dashboard's `statistics.json`) with assertions and a post-run check against your thresholds.

## Gotchas
- `-o` folder must be empty or absent (use `-f`).
- Heap: set via the `HEAP` environment variable or `JVM_ARGS` in the `bin/jmeter` script; the default is `-Xms1g -Xmx1g -XX:MaxMetaspaceSize=256m`.
- A CSV Data Set relative file name is resolved against the path of the active test plan; in distributed runs the file must exist on each server relative to where it was started. Relative paths used by `-o` and some other settings are built from the JMeter working directory.

## Verify
`results/run.jtl` has rows, `results/dashboard/index.html` opens, and the log has no ERROR lines.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: -n -t -l -j -e -o -g -f -J -G -q -D -r -R -X semantics, `-o` folder rule, HEAP and JVM_ARGS defaults, CSV Data Set relative path rule. Removed the unconfirmed exit-code and Taurus claims.

Method: documentation only; no commands were run.
