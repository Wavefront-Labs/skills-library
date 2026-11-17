---
id: computing-software.cloud-infrastructure-engineering.docker.testcontainers-for-go
name: testcontainers-for-go
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers, testcontainers-go, go-testing, testmain, postgres-module, wait-strategy, snapshot-restore, integration-tests]
level: practitioner
status: docs-checked
description: "Write Go integration tests with testcontainers-go: modules vs GenericContainer, wait strategies, cleanup with t.Cleanup, sharing containers in TestMain, snapshots, and go test -p."
sources: ["https://golang.testcontainers.org/quickstart/", "https://golang.testcontainers.org/features/creating_container/", "https://golang.testcontainers.org/features/wait/introduction/", "https://golang.testcontainers.org/modules/postgres/", "https://golang.testcontainers.org/features/garbage_collector/", "https://golang.testcontainers.org/features/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testcontainers for Go

```bash
go get github.com/testcontainers/testcontainers-go
go get github.com/testcontainers/testcontainers-go/modules/postgres
```

## Module container (Postgres)
```go
func TestRepo(t *testing.T) {
    ctx := context.Background()
    pg, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("app"),
        postgres.WithUsername("app"),
        postgres.WithPassword("secret"),
        postgres.WithInitScripts("testdata/schema.sql"),
        postgres.BasicWaitStrategies(),          // the module sets no default wait strategy: set one
    )
    testcontainers.CleanupContainer(t, pg)       // terminates at test end, even on failure
    require.NoError(t, err)

    dsn, err := pg.ConnectionString(ctx, "sslmode=disable")
    require.NoError(t, err)
    db, err := sql.Open("pgx", dsn)
    // ...
}
```
Call `CleanupContainer` **before** checking `err`: a container that started but failed its
wait strategy still needs terminating.

## Any image: GenericContainer
```go
req := testcontainers.ContainerRequest{
    Image:        "redis:7-alpine",
    ExposedPorts: []string{"6379/tcp"},
    WaitingFor:   wait.ForListeningPort("6379/tcp").WithStartupTimeout(30 * time.Second),
}
redisC, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
    ContainerRequest: req, Started: true,
})
testcontainers.CleanupContainer(t, redisC)
require.NoError(t, err)
host, _ := redisC.Host(ctx)
port, _ := redisC.MappedPort(ctx, "6379/tcp")
```
The docs now recommend `testcontainers.Run` over `GenericContainer` (the old way):
```go
redisC, err := testcontainers.Run(ctx, "redis:7-alpine",
    testcontainers.WithExposedPorts("6379/tcp"),
    testcontainers.WithWaitStrategy(wait.ForListeningPort("6379/tcp").WithStartupTimeout(30*time.Second)),
)
testcontainers.CleanupContainer(t, redisC)
require.NoError(t, err)
```
Wait strategies include `wait.ForLog`, `wait.ForHTTP`, `wait.ForSQL`, `wait.ForListeningPort`
and `wait.ForAll(...)`. Never `time.Sleep`.

## Share one container per package
```go
var dsn string

func TestMain(m *testing.M) {
    ctx := context.Background()
    pg, err := postgres.Run(ctx, "postgres:16-alpine", postgres.BasicWaitStrategies())
    if err != nil { log.Fatal(err) }
    dsn, _ = pg.ConnectionString(ctx, "sslmode=disable")
    code := m.Run()
    _ = testcontainers.TerminateContainer(pg)
    os.Exit(code)
}
```
Reset state between tests with the Postgres module's snapshots:
```go
_ = pg.Snapshot(ctx)                 // after migrations, once
t.Cleanup(func() { _ = pg.Restore(ctx) })
```
Do not use the `postgres` system database as the container's database name with snapshots: the logic
drops the connected database and runs commands through the system database. `postgres.WithSQLDriver("name")` selects
the driver Snapshot and Restore use.

## Concurrency
`go test ./...` runs packages in parallel (`-p` sets the number of packages tested at once); each package with a `TestMain`
starts its own containers. On small CI runners lower `-p` or share via a single
integration package. Gate slow tests with a build tag (`//go:build integration`) and
`go test -tags integration ./...`.

## Environment
- Docker host detection order in the docs: `tc.host` in `~/.testcontainers.properties`, then `DOCKER_HOST`,
  then the default socket, then `docker.host` in the properties file, then rootless socket locations.
- Ryuk removes the test session's containers, networks and volumes even if you do not call Terminate; disable it with
  `TESTCONTAINERS_RYUK_DISABLED=true` (or `ryuk.disabled=true`) only where something else cleans up. Ryuk needs
  privileged mode in some environments (`TESTCONTAINERS_RYUK_CONTAINER_PRIVILEGED`).
- Properties map to environment variables with a `TESTCONTAINERS_` prefix (`ryuk.disabled` becomes `TESTCONTAINERS_RYUK_DISABLED`).

## Verify
```bash
go test -tags integration -run TestRepo -v ./internal/repo/
docker ps -a --filter label=org.testcontainers=true   # empty after the run
```

## Checked
Documentation release: testcontainers-go v0.44.0 docs (features/creating_container, wait/introduction, garbage_collector, configuration, modules/postgres) and module source (modules/postgres), main as of 2026-10-25, checked 2026-10-26.
Confirmed: `postgres.Run(ctx, img, opts...)`, `WithDatabase`, `WithUsername`, `WithPassword`, `WithInitScripts`, `BasicWaitStrategies`, `ConnectionString`, `Snapshot`, `Restore`, `WithSQLDriver`; `testcontainers.Run` with `WithExposedPorts` and `WithWaitStrategy` (recommended over `GenericContainer`); `CleanupContainer` and `TerminateContainer`; `container.Host` and `MappedPort`; wait strategies; Ryuk behaviour and environment variables; Docker host detection order; `TESTCONTAINERS_` property mapping.
Corrected: `testcontainers.Run` is the recommended API, not merely newer; Postgres has no default wait strategy; Docker host detection order differs from the original text; snapshot caveat is about the `postgres` system database.
Removed as unsupported: the `Endpoint` helper, `WithLogger`, `ForHTTP(...).WithPort` form, "waits for the ready log twice", the "template database" description and the `-p = GOMAXPROCS` statement.
Method: documentation only; no commands were run.
