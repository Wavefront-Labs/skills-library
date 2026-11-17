---
id: computing-software.devops-ci-cd.dagger.services-bind-expose-lifecycle
name: services-bind-expose-lifecycle
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, services, service-binding, networking, testing, redis, lifecycle]
level: practitioner
status: docs-checked
description: "Return, bind, expose and start/stop service containers in Dagger Functions, including host services, interdependent hostnames, endpoints and persisted state."
sources: [https://docs.dagger.io/0.21/extending/services, https://docs.dagger.io/0.21/cookbook/services]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger services: bind, expose, start and stop

Goal: run long-lived containers (databases, HTTP servers, sidecars) from Dagger Functions and reach them from other functions or the host. Based on the Dagger 0.21 docs.

## Facts about service containers
- Each has a content-addressed hostname and optional exposed ports; they start just-in-time, are de-duplicated, are health checked before clients run, and stop when no longer needed.
- Services are de-duplicated only within one Dagger client session (regular containers dedupe engine-wide). For several instances of one service, attach something unique such as an instance ID.
- A service is cancelled after a 10 second grace period unless the explicit `Start`/`Stop` APIs are used.

## Return a service and bind it (Go)
```go
func (m *MyModule) HttpService() *dagger.Service {
	return dag.Container().
		From("python").
		WithWorkdir("/srv").
		WithNewFile("index.html", "Hello, world!").
		WithExposedPort(8080).
		AsService(dagger.ContainerAsServiceOpts{Args: []string{"python", "-m", "http.server", "8080"}})
}

func (m *MyModule) Get(ctx context.Context) (string, error) {
	return dag.Container().
		From("alpine").
		WithServiceBinding("www", m.HttpService()).
		WithExec([]string{"wget", "-O-", "http://www:8080"}).
		Stdout(ctx)
}
```
Call `dagger call get` (or `dagger -c get`); result `Hello, world!`. The binding alias works at the `/etc/hosts` level, not DNS.

## Expose to the host
`dagger call http-service up` maps each service port to the same host port (8080 here; `curl localhost:8080`). Remap with `up --ports 9000:8080`; `--random` binds ports randomly.

## Expose a host service to a function
Take a `*dagger.Service` argument and pass `tcp://<host>:<port>`: `dagger call user-list --svc=tcp://localhost:3306`. The service must already be listening on the host. The docs bind it as `db` in a `mariadb:10.11.2` container and run `mysql --host=db`.

## Interdependent services
Give services global hostnames with `WithHostname("svca")` and `WithHostname("svcb")` so each reaches the other without a binding (circular dependencies). Hostnames take the form `<host>.<module id>.<session id>.dagger.local`. Call `svcA.Start(ctx)` before defining B. Run with `dagger call services up --ports 8080:80`.

## Endpoints
Use when a client cannot resolve the alias, or a service must be reachable over plain HTTP:
```go
service, err := dag.Container().From("nginx").WithExposedPort(80).AsService().Start(ctx)
endpoint, err := service.Endpoint(ctx, dagger.ServiceEndpointOpts{Scheme: "http", Port: 80})
dag.HTTP(endpoint).Contents(ctx)
```

## Persist or control state
Two ways to avoid depending on the grace period:
1. Cache volume: mount `dag.CacheVolume("my-redis")` at `/data` on the Redis service (`AsService` with `UseEntrypoint: true`), run `set` then `save` through a `redis-cli` client container. `dagger call set --key=foo --value=123` then `dagger call get --key=foo` prints `123`.
2. Explicit lifecycle: `redisSrv, err := redisSrv.Start(ctx)` then `defer redisSrv.Stop(ctx)` (Python wraps this in an async context manager). Use when the app must flush on shutdown.

Better still, chain both client commands in one `WithExec` pipeline so the service stays up for both. The page warns that separate calls depending on the 10 s window are risky (CPU load, network latency).

## Test against a database
Create `mariadb:10.11.2` as a service with `MARIADB_USER`, `MARIADB_PASSWORD`, `MARIADB_DATABASE`, `MARIADB_ROOT_PASSWORD` and port 3306, bind it as `db` to a Drupal container, set `SIMPLETEST_DB=mysql://user:password@db/drupal`, then run phpunit. `dagger call test` prints the phpunit summary.

Related: cache-volumes-dependencies, secrets-handling-and-caching.

## Checked

2026-11-07

Read extending/modules/services.mdx (live slug /extending/services) and cookbook/services.mdx (live slug /cookbook/services) in full; both cited URLs match the live slugs. The cookbook page only imports partials, so I read the seven service partials (five while checking service-type-bindings plus _start-stop-service and _create-interdependent-services). I also read the Go snippets bind-services, create-interdependent-services, persist-service-state, start-stop-services, service-lifecycle-3, expose-host-services-to-dagger, use-endpoint and test-against-db-service, and the Python start-stop-services snippet; the service-lifecycle-1 and -2 snippets and the TypeScript, PHP and Java tabs were not opened. Confirmed the service container characteristics, de-duplication per client session, the 10 second grace period, the www binding and /etc/hosts remark, up and --ports and --random, host services via tcp://, interdependent hostnames and the hostname format, Start before defining B, endpoints, the Redis cache volume example, Start/defer Stop, the async context manager in Python, the chained WithExec advice, and the MariaDB/Drupal test. No corrections needed.

Method: documentation only; no commands were run.
