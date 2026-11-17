---
id: computing-software.systems-network-administration.apache-tomcat.stuck-thread-detection-valve
name: stuck-thread-detection-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, stuckthreaddetectionvalve, stuck-threads, threshold, interruptthreadthreshold, hung-requests]
level: practitioner
status: docs-checked
description: "Detect hung Tomcat 10.1 requests with StuckThreadDetectionValve: threshold, interruptThreadThreshold, WARN stack traces and JMX stuckThreadIds/stuckThreadNames."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# StuckThreadDetectionValve

Class `org.apache.catalina.valves.StuckThreadDetectionValve`; add to Engine, Host or Context.

- `threshold`: seconds a request may run before it is flagged. Default 600; 0 disables detection. Keep it above the container `backgroundProcessorDelay`.
- `interruptThreadThreshold`: seconds before the thread is interrupted. Default -1 (never); if used it must be >= `threshold`. Interruption helps with blocked I/O or lock waits, not infinite loops.

Output: a WARN log entry with the thread's stack trace when a request becomes stuck. JMX attributes `stuckThreadIds` and `stuckThreadNames` list current offenders.

```xml
<Valve className="org.apache.catalina.valves.StuckThreadDetectionValve"
       threshold="120" interruptThreadThreshold="300"/>
```

Use it to find slow downstream calls before the thread pool (see `computing-software.systems-network-administration.apache-tomcat.http-connector-threads-and-connections`) is exhausted.

Verify: add a servlet that sleeps beyond the threshold; the WARN with its stack appears in the log.

## Checked

2026-11-04. Read the Stuck Thread Detection Valve section of the Tomcat 10.1 Valve page (config/valve.html): confirmed threshold default 600 and 0 disabling, the backgroundProcessorDelay note, interruptThreadThreshold default -1 and the >= threshold rule, WARN stack trace and the JMX stuckThreadIds/stuckThreadNames attributes. Removed the claim of a second WARN on completion, which the page does not state.

Method: documentation only; no commands were run.
