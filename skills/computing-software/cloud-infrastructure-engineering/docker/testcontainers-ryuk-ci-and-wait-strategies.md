---
id: computing-software.cloud-infrastructure-engineering.docker.testcontainers-ryuk-ci-and-wait-strategies
name: testcontainers-ryuk-ci-and-wait-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers, integration-tests, ryuk, container-reuse, testcontainers-ci, testcontainers-docker-host, wait-strategy, testcontainers-modules]
level: advanced
description: "Make Testcontainers reliable: wait strategies and modules instead of sleeps, Ryuk cleanup and reuse, and CI setups with socket mounts, DinD, remote hosts or Testcontainers Cloud."
sources: ["https://java.testcontainers.org/features/startup_and_waits/", "https://java.testcontainers.org/features/configuration/", "https://java.testcontainers.org/supported_docker_environment/continuous_integration/dind_patterns/", "https://java.testcontainers.org/supported_docker_environment/continuous_integration/gitlab_ci/", "https://java.testcontainers.org/features/reuse/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testcontainers: Ryuk, CI and wait strategies

## Wait strategies (never sleep)
Java examples (Go/Python/Node have equivalents: `wait.ForLog`, `wait_for_logs`, `Wait.forLogMessage`):
```java
new GenericContainer<>("redis:7")
    .withExposedPorts(6379)
    .waitingFor(Wait.forListeningPort());                     // default: port is open
new GenericContainer<>("app:dev")
    .withExposedPorts(8080)
    .waitingFor(Wait.forHttp("/ready").forStatusCode(200).withStartupTimeout(Duration.ofSeconds(90)));
new GenericContainer<>("kafka-ish")
    .waitingFor(Wait.forLogMessage(".*started.*\\n", 1));
new GenericContainer<>("svc").waitingFor(Wait.forHealthcheck());   // uses image HEALTHCHECK
```
By default Java waits up to 60 seconds for the container's first mapped port to listen (`withStartupTimeout()` changes it), and
a listening port is not always readiness. Prefer **modules**, which encode the waits for their service: Java `PostgreSQLContainer`, Go
`postgres.Run(ctx, ...)` (the Go Postgres module sets no default wait: add `postgres.BasicWaitStrategies()`), Python
`PostgresContainer`. Always use mapped ports (`getMappedPort`, `getHost`), never fixed ports.

## Ryuk
Ryuk (`testcontainers/ryuk`, the resource reaper) removes the test session's containers, networks and volumes after the
tests finish or the process dies, which prevents leaks after crashes.
- Ryuk must be started as a privileged container (in Java `ryuk.container.privileged` defaults to true; Go has
  `TESTCONTAINERS_RYUK_CONTAINER_PRIVILEGED`). If your environment cleans up containers itself and does not allow
  privileged containers, set the `TESTCONTAINERS_RYUK_DISABLED=true` environment variable; the Java docs note
  that cleanup then still happens at JVM shutdown unless the JVM is killed with `kill -9`. Disable it only where something else cleans up.
- Ryuk's image can be overridden (`ryuk.container.image` property in Java) for registries that mirror it.

## Reuse (local dev speed)
```java
new GenericContainer<>("redis:6-alpine").withExposedPorts(6379).withReuse(true);
```
Reuse is experimental. Enable it with `TESTCONTAINERS_REUSE_ENABLE=true` or `testcontainers.reuse.enable=true`
in `~/.testcontainers.properties` (not in a classpath properties file), start the container manually and do not call
`stop()`; the container configuration must be identical to be reused. The Java docs say reusable containers are not suited to CI.

## CI environments
| CI | Setup |
|---|---|
| GitHub Actions ubuntu runners | Docker present - works out of the box |
| GitLab with DinD service | the `docker:dind` service (with `--tls=false` in the Java example), `DOCKER_HOST=tcp://docker:2375` and `DOCKER_TLS_CERTDIR=""` |
| GitLab runner with a mounted Docker socket | mount `/var/run/docker.sock` and set `TESTCONTAINERS_HOST_OVERRIDE` to the Docker host's IP, otherwise a wrong address is used |
| Job running in a container (sibling containers) | mount the Docker socket and the source directory at the same path; Testcontainers detects it is in a container and uses the default gateway IP instead of localhost; on Docker Desktop set `TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal` |
| Remote Docker | `DOCKER_HOST=tcp://...`; Java also reads `docker.host` in `~/.testcontainers.properties` with the `EnvironmentAndSystemPropertyClientProviderStrategy` |
Other relevant variables: `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` (socket path used by Ryuk, Docker Compose and similar containers).

## Verify
Tests start without arbitrary sleeps; after a killed run, `docker ps -a --filter label=org.testcontainers=true`
shows no leftover containers once Ryuk has run.

## Checked
Documentation release: testcontainers-java 2.0.5 docs (features/startup_and_waits, features/configuration, features/reuse, supported_docker_environment/continuous_integration gitlab_ci and dind_patterns) and source (Wait.java, TestcontainersConfiguration.java), testcontainers-go v0.44.0 docs (configuration, garbage collector), checked 2026-10-26.
Confirmed: `Wait.forListeningPort`, `forHttp(path)`, `forLogMessage(regex, times)`, `forHealthcheck`; default 60 s wait for the first mapped port and `withStartupTimeout`; Ryuk privileged requirement, `TESTCONTAINERS_RYUK_DISABLED` and JVM-shutdown cleanup note; reuse prerequisites and CI warning; GitLab dind variables and socket-mount `TESTCONTAINERS_HOST_OVERRIDE`; sibling-container behaviour and `host.docker.internal` for Docker Desktop; `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE`; Java `docker.host` strategy.
Corrected: Ryuk is privileged rather than needing a socket-mount workaround, and the Java default already runs it privileged; the GitLab dind row no longer sets `TESTCONTAINERS_HOST_OVERRIDE`; reuse example uses `GenericContainer` as in the docs.
Removed as unsupported: the cleanup `docker rm` one-liner, SELinux remark, "Ryuk ignores it, matched by config hash", the single Docker host resolution order (Go and Java differ), `tc.host`, Testcontainers Cloud row and the 10 s Ryuk timing.
Method: documentation only; no commands were run.
