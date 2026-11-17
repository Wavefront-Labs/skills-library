---
id: computing-software.cloud-infrastructure-engineering.docker.npm-and-jvm-signal-handling-in-containers
name: npm-and-jvm-signal-handling-in-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, graceful-shutdown, signal-handling, npm-start-signals, jvm-sigterm, node-image, java-image, pid1]
level: practitioner
description: "Fix slow or unclean shutdowns from CMD npm start, yarn and shell wrappers, and make JVM, Spring Boot and Node apps drain on SIGTERM inside Docker."
sources: ["https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md", "https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html", "https://docs.docker.com/reference/cli/docker/container/stop/", "https://docs.docker.com/reference/dockerfile/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# npm and JVM signal quirks in containers

## How docker stop works
`docker stop` sends the container's main process SIGTERM (or the image's `STOPSIGNAL` /
`--stop-signal`), then SIGKILL after a grace period. `-t` / `--timeout` sets the seconds to wait; if
the container has no configured default, the daemon decides, which is 10 seconds for Linux
containers and 30 seconds for Windows containers. Set the per-container default with `--stop-timeout`
at create time.

## Node: don't start through npm
The docker-node best-practices page says baking the command into the image, rather than using
the `package.json` start script, reduces the number of processes and makes SIGTERM and SIGINT reach
the Node.js process instead of npm swallowing them:
```dockerfile
CMD ["node", "index.js"]
```
It also says Node.js was not designed to run as PID 1: as PID 1 it will not respond to SIGINT
(Ctrl-C) and similar signals by default. Use `docker run --init` (Docker 1.13 or later) to wrap the
process in a lightweight init, or include Tini in the Dockerfile. If you run as PID 1 anyway,
handle the signal in code:
```js
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));       // stop accepting, finish in-flight
  setTimeout(() => process.exit(1), 9000).unref();
});
```

## Shell form hides signals
The Dockerfile reference: shell-form `ENTRYPOINT` starts your program as a subcommand of
`/bin/sh -c`, which does not pass signals, so the executable is not PID 1 and never receives the
SIGTERM from `docker stop`. Use the exec form, or start the program with `exec` in a wrapper
script (for example `exec java $JAVA_OPTS -jar app.jar`).
```dockerfile
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

## Spring Boot
Graceful shutdown is enabled by default for Jetty, Reactor Netty and Tomcat; it happens while the
application context closes, with a grace period for in-flight requests and no new ones accepted
(`server.shutdown=immediate` disables it). Set the grace period with
`spring.lifecycle.timeout-per-shutdown-phase=20s`, and keep the container stop timeout longer than
it (`docker stop -t` / `--stop-timeout`, or your orchestrator's equivalent).

## Choosing STOPSIGNAL
If a server drains on a signal other than SIGTERM, set `STOPSIGNAL <signal>` in the Dockerfile or
pass `--stop-signal`; check the server's own documentation for which signal means graceful stop.

## Verify
```sh
docker exec app ps -o pid,comm     # PID 1 is node/java, not npm/sh
time docker stop app               # well under the stop timeout
docker logs app                    # shutdown hook / drain messages present
```

## Checked
Checked 2026-10-28 against Docker Docs (`docker container stop`; Dockerfile reference on shell-form
ENTRYPOINT), docker-node Best Practices (PID 1, `--init`, Tini, `CMD ["node","index.js"]`) and the
Spring Boot graceful shutdown page (default-on, timeout property, `server.shutdown=immediate`).
Corrected: `server.shutdown=graceful` is already the default. Removed as unconfirmed: npm's
signal forwarding behaviour across versions, JVM SIGTERM handler and `ExitOnOutOfMemoryError`
remarks, Python and gunicorn behaviour, nginx, php-fpm and Apache stop signals, Compose
`stop_grace_period`, and exit codes 143 and 137.
Method: documentation only; no commands were run.
