---
id: computing-software.software-engineering.spring-boot.application-availability-states
name: application-availability-states
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, liveness, readiness, applicationavailability, kubernetes-probes, availabilitychangeevent]
level: practitioner
status: docs-checked
description: "Liveness and readiness states in Spring Boot, when each becomes true, and how to read or change them with ApplicationAvailability and events."
sources:
  - https://docs.spring.io/spring-boot/reference/features/spring-application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spring Boot supports the "liveness" and "readiness" availability states for platforms such as Kubernetes probes. With Actuator they are exposed as health endpoint groups. In your own beans, inject `ApplicationAvailability`.

Liveness: whether internal state lets the app work or recover by itself. A broken Liveness state means the app cannot recover and the infrastructure should restart it. It should generally not be based on external checks such as health checks; otherwise a failing database, web API or cache would trigger massive restarts and cascading failures. The app is live as soon as the context has been refreshed.

Readiness: whether the app is ready to handle traffic. A failing Readiness state tells the platform not to route traffic for now, typically during startup while `CommandLineRunner` and `ApplicationRunner` components run, or whenever the app decides it is too busy. It is ready as soon as application and command-line runners have been called.

Startup tasks should run in `CommandLineRunner` or `ApplicationRunner` components rather than Spring lifecycle callbacks such as `@PostConstruct`.

Managing state: inject `ApplicationAvailability` and call its methods; more often, listen to state updates or publish them. The page shows exporting the Readiness state to a file so a Kubernetes exec probe can read it, and publishing a Liveness change when the app breaks and cannot recover (for example a local cache verifier). Events used: `AvailabilityChangeEvent` with `LivenessState` and `ReadinessState` values.

Kubernetes HTTP probes for liveness and readiness are provided through the Actuator health endpoint (see actuator-health-endpoint).

## Checked

2026-11-07

Read spring-application.adoc (docs-repo source of the cited SpringApplication page) in full, and the included MyReadinessStateExporter.java and MyLocalCacheVerifier.java examples. Sections used: Application Availability, Liveness State, Readiness State, Managing the Application Availability State.
Confirmed: liveness and readiness states exposed as health endpoint groups with Actuator; ApplicationAvailability injection; Liveness not based on external checks (database, Web API, external cache -> massive restarts and cascading failures); live once the context is refreshed; Readiness failing during CommandLineRunner/ApplicationRunner processing; ready once runners have been called; the @PostConstruct tip; the readiness exporter (ACCEPTING_TRAFFIC / REFUSING_TRAFFIC cases) and the cache verifier publishing LivenessState.BROKEN via AvailabilityChangeEvent.
Reworded: "such as the health endpoint" to "such as health checks", the page's own wording.

Method: documentation only; no commands were run.
