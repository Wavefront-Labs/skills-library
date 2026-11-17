---
id: computing-software.software-engineering.spring-boot.startup-tracking-and-virtual-threads
name: startup-tracking-and-virtual-threads
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, applicationstartup, bufferingapplicationstartup, flight-recorder, virtual-threads, spring-threads-virtual-enabled, keep-alive]
level: advanced
status: docs-checked
description: "Track startup with BufferingApplicationStartup or Flight Recorder, and enable virtual threads with spring.threads.virtual.enabled and spring.main.keep-alive."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Startup tracking: Spring Framework's `ApplicationStartup` records the startup sequence as `StartupStep` objects for profiling. Choose the implementation when setting up the `SpringApplication`.
- `FlightRecorderApplicationStartup` (from Spring Framework) adds Spring startup events to a Java Flight Recorder session, so you can correlate context lifecycle with allocations, GCs and class loading. Record with `java -XX:StartFlightRecording:filename=recording.jfr,duration=10s -jar demo.jar`.
- `BufferingApplicationStartup` (shipped with Boot) buffers steps for draining into an external metrics system; any component can ask for a bean of that type.
- Boot can expose the data as JSON through the actuator `startup` endpoint.

Virtual threads need Java 21 or later; Java 24 or later is strongly recommended. Enable with:
```yaml
spring:
  threads:
    virtual:
      enabled: true
```
Read the official Java virtual threads documentation first: applications can see lower throughput from pinned virtual threads, and that page explains detecting them with JDK Flight Recorder or `jcmd`.

With virtual threads enabled, properties that configure thread pools have no effect, because virtual threads run on a JVM-wide platform thread pool.

Gotcha: virtual threads are daemon threads, and a JVM exits when only daemon threads remain. A `@Scheduled` scheduler thread is virtual, so it will not keep the JVM alive; other technologies can be affected too. The page recommends setting `spring.main.keep-alive` to `true` so the JVM is kept alive even if all threads are virtual.

## Checked

2026-11-07. Read features/spring-application.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. Keep-alive sentence now attributes the recommendation to the page ('setting spring.main.keep-alive to true'). The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
