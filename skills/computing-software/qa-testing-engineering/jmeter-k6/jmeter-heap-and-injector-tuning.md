---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-heap-and-injector-tuning
name: jmeter-heap-and-injector-tuning
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, jmeter-tuning, jvm-heap, non-gui-mode, injector-tuning, jmeter-reporting, best-practices]
level: practitioner
status: docs-checked
description: "Tune JMeter for heavy load: non-GUI mode, heap sizing via JVM_ARGS, disabling heavy listeners, saving only needed result fields, and OS limits on the injector."
sources:
  - https://jmeter.apache.org/usermanual/best-practices.html
  - https://jmeter.apache.org/usermanual/get-started.html#non_gui
  - https://jmeter.apache.org/usermanual/generating-dashboard.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter heap and load-generator tuning

**Goal:** one injector produces as much accurate load as possible.

## Must-dos
- **Non-GUI mode** for load: `jmeter -n -t plan.jmx -l results.jtl -e -o report/`. GUI only for scripting and small debug runs.
- **No View Results Tree / Summary listeners** in load runs (disable or remove); they consume memory and CPU.
- **Heap**: `JVM_ARGS="-Xms4g -Xmx4g" jmeter -n ...` (or edit `HEAP` in `bin/jmeter`/`jmeter.bat`). Same min and max avoids resizing; leave RAM for the OS. The default is `HEAP="-Xms1g -Xmx1g -XX:MaxMetaspaceSize=256m"`.
- JMeter starts with G1 (`GC_ALGO`, default `-XX:+UseG1GC -XX:MaxGCPauseMillis=250 -XX:G1ReservePercent=20`); the `bin/jmeter` script has commented `VERBOSE_GC` examples for GC logging if timings look spiky.

## Result file settings (user.properties)
```
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.samplerData=false
jmeter.save.saveservice.response_data.on_error=false
```
Keep the fields the dashboard needs: the manual lists `bytes`, `label`, `latency`, `response_code`, `response_message`, `successful`, `thread_counts`, `thread_name`, `time`, `connect_time`, `assertion_results_failure_message` and a timestamp format that includes the time.

## Script efficiency
Use JSR223 with Groovy and compilation caching (not BeanShell), use as few assertions and listeners as possible, create large or randomised test data in a file read by CSV Data Set, avoid many near-identical samplers (loop one sampler with variables), and do not use functional mode.

## Capacity
The thread count one injector can run depends on hardware, script weight and server speed; an undersized thread count gives Coordinated Omission and misleading results. Calibrate threads per injector (`load-generator-saturation-checks`), and use several CLI instances or distributed mode for large loads. The JavaTest sampler needs no network and gives a rough maximum throughput of the platform. Delaying thread creation until a thread starts sampling allows a very large total number of threads if few are active at once.

## Gotchas
- Check `jmeter.log` for OutOfMemoryError; the `bin/jmeter` script already passes `-XX:+HeapDumpOnOutOfMemoryError`.
- Saving response data on error for a run with thousands of errors fills the disk.

## Verify
Injector CPU and heap after GC stay stable through the run; jmeter.log is free of OOM errors.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: CLI mode, no View Results Tree in load runs, `JVM_ARGS` and `HEAP` usage and defaults, G1 `GC_ALGO` default, CSV output, result-saving properties, JSR223 over BeanShell, capacity and Coordinated Omission advice. Removed unconfirmed OS tuning and thread-count figures.

Method: documentation only; no commands were run.
