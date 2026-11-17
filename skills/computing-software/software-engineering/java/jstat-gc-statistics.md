---
id: computing-software.software-engineering.java.jstat-gc-statistics
name: jstat-gc-statistics
category: computing-software
field: software-engineering
product: java
tags: [java, jdk-diagnostics, jstat, jstat-gcutil, gc-statistics, jvm-monitoring, gc-frequency, metaspace-usage]
level: practitioner
status: docs-checked
description: "Watch live JVM heap and GC behaviour with jstat -gcutil/-gc/-gccause and a sampling interval, using the JDK 21 man page's options, columns and vmid syntax."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/jstat.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jstat GC statistics

The JDK 21 man page marks `jstat` "experimental and unsupported" and says all options are subject to change or removal. It displays performance statistics for an instrumented HotSpot VM.

## Synopsis
`jstat outputOptions [-t] [-h lines] vmid [interval [count]]`
- `interval`: sampling interval in `s` or `ms`; default unit is milliseconds; must be a positive integer.
- `count`: number of samples; default is infinity (until the JVM or jstat ends).
- `-h n`: print a column header every n rows; default 0 prints the header once.
- `-t`: first column `Timestamp`, seconds since the target JVM started.
- `-options` lists the stat options for your installation; `-help` shows help.

## Commands
```bash
jstat -gcutil <pid> 1000 30        # utilisation summary, every 1000 ms, 30 samples
jstat -gc <pid> 5s                 # capacities and usage in KB
jstat -gccause <pid> 1s            # gcutil columns plus LGCC and GCC (last and current GC cause)
jstat -gcnew <pid>
jstat -gcold <pid>                 # old generation and metaspace
jstat -class <pid>
jstat -compiler <pid>
jstat -options
```

## Columns (from the man page)
- `-gcutil`: S0, S1, E, O, M (percent of current capacity), CCS (compressed class space percent), YGC and FGC (counts of young and full GC events), YGCT, FGCT, GCT (times).
- `-gc`: S0C, S1C, S0U, S1U, EC, EU, OC, OU, MC, MU, CCSC, CCSU in KB, plus YGC, YGCT, FGC, FGCT, GCT.
- `-gcnew` adds TT (tenuring threshold), MTT and DSS (desired survivor size).
- The man page's example output shows a young collection moving eden contents to the old space and survivor changes; and a tenuring threshold dropping from 31 to 2 when survivors would exceed the desired survivor size.
- Other options: gccapacity, gcnewcapacity, gcoldcapacity, gcmetacapacity, printcompilation.

## vmid syntax
`[protocol:][//]lvmid[@hostname[:port][/servername]]`. The lvmid is typically the OS process id; `jps` finds it when the JVM is not in a separate docker instance. With a host name the default protocol is rmi, and the port defaults to the rmiregistry port 1099. The man page's remote example is `jstat -gcutil 40496@remote.domain 1000`, which uses the jstatd server on the remote host.

## Gotchas
- The man page says not to write scripts that parse jstat output, because the format may change.
- Column names are consistent across options; where two options show the same name the data source is the same.
- Counters are cumulative, so compare successive samples.

## Verify
Run `jstat -options` on your JDK, then sample `-gcutil` with an interval and confirm YGC and FGC increase as you expect under load.

## Checked
Confirmed against the JDK 21 `jstat` man page: synopsis, defaults, stat options and column definitions, vmid syntax, examples. Removed: G1/ZGC/Shenandoah-specific claims and the CGC/CGCT column, rules of thumb (pause thresholds), container and hsperfdata notes, `-XX:-UsePerfData`, and metaspace tuning advice, none of which the page states.
Method: docs-only read of cited pages, 2026-11-08
