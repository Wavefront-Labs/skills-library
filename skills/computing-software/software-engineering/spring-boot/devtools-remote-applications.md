---
id: computing-software.software-engineering.spring-boot.devtools-remote-applications
name: devtools-remote-applications
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, devtools, remote, remotespringapplication, remote-secret, includeoptional]
level: practitioner
status: docs-checked
description: "Enable devtools remote update: include devtools in the repackaged archive, set spring.devtools.remote.secret, run RemoteSpringApplication and tune the quiet period."
sources:
  - https://docs.spring.io/spring-boot/reference/using/devtools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remote support is opt-in because it is a security risk. Use it only on a trusted network or secured with SSL; never enable it on a production deployment.

1. Include devtools in the repackaged archive (Maven; optional dependencies are excluded by default, hence `includeOptional`):
```xml
<plugin>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-maven-plugin</artifactId>
	<configuration>
		<includeOptional>true</includeOptional>
		<excludeDevtools>false</excludeDevtools>
	</configuration>
</plugin>
```
For the Gradle plugin, configure the task's classpath to include the `developmentOnly` configuration.
2. Set `spring.devtools.remote.secret` to a unique, strong value. The server endpoint is enabled automatically once the secret is set; the client must be launched manually. Not supported for Spring WebFlux.

Client: run `org.springframework.boot.devtools.RemoteSpringApplication` from your IDE with the same classpath as the remote project; its single required argument is the remote URL (for example `https://myapp.cfapps.io`). Because it shares the classpath it reads `spring.devtools.remote.secret` from the application properties and sends it for authentication. Use `https://`. For a proxy set `spring.devtools.remote.proxy.host` and `spring.devtools.remote.proxy.port`.

Remote update: the client monitors the classpath like local restart, pushes updated resources and triggers a restart if required. Files are only monitored while the client runs; changes made before starting it are not pushed. On a slow environment the quiet period may split changes into batches; the server restarts after the first batch, and the next upload fails with a warning in the `RemoteSpringApplication` log and a retry, possibly leaving inconsistent code. Increase `spring.devtools.restart.poll-interval` and `spring.devtools.restart.quiet-period`.

## Checked

2026-11-07

Read devtools.adoc (docs-repo source of the cited Developer Tools page) in full (448 lines), using Remote Applications, Running the Remote Client Application, Remote Update and the packaging TIP near the top. The embedded client output (remote-spring-application.txt) was not opened.
Confirmed: opt-in and security risk, trusted network or SSL, never on production; includeOptional true and excludeDevtools false in spring-boot-maven-plugin and the optional-dependencies NOTE; Gradle developmentOnly classpath TIP; spring.devtools.remote.secret unique and strong; server side automatic once the secret is set, client launched manually; not supported for Spring WebFlux; RemoteSpringApplication with the same classpath, single remote URL argument, https://myapp.cfapps.io example; secret read from application properties; https advice; proxy host and port properties; remote update behaviour, batch-splitting failure mode and the poll-interval / quiet-period fix; files monitored only while the client runs.
Nothing trimmed.

Method: documentation only; no commands were run.
