---
id: computing-software.cloud-infrastructure-engineering.docker.compose-modules-in-testcontainers
name: compose-modules-in-testcontainers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers-compose, docker-compose-container, compose-module, integration-tests, wait-strategies, multi-service-tests]
level: practitioner
status: docs-checked
description: "Start whole Docker Compose stacks from integration tests with Testcontainers Compose modules in Java, Go, Python and Node: service access, waits, profiles and trade-offs."
sources:
  - https://java.testcontainers.org/modules/docker_compose/
  - https://golang.testcontainers.org/features/docker_compose/
  - https://testcontainers-python.readthedocs.io/en/latest/core/README.html
  - https://node.testcontainers.org/features/compose/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose modules in Testcontainers

When the system under test needs several collaborating services already described in a `compose.yaml`, Testcontainers can start that stack, wait for readiness, give tests the mapped ports and tear it down.

## Java (JUnit 5)
```java
@Testcontainers
class CheckoutIT {
  @Container
  static ComposeContainer env = new ComposeContainer(new File("src/test/resources/compose-test.yaml"))
      .withExposedService("api-1", 8080, Wait.forHttp("/health").forStatusCode(200))
      .withExposedService("db-1", 5432, Wait.forListeningPort())
      .withLocalCompose(true);               // use the local docker compose v2 CLI

  @Test void placesOrder() {
    String host = env.getServiceHost("api-1", 8080);
    int port = env.getServicePort("api-1", 8080);
    // call http://host:port/...
  }
}
```
`ComposeContainer` targets Compose V2 (the docs' examples address services as `redis-1`, `db-1`); `DockerComposeContainer` uses Compose V1, which Docker has deprecated. By default Testcontainers waits up to 60 seconds for each exposed service's first mapped port to listen; the `withExposedService` overloads that take a wait strategy set a per-service strategy. Local Compose mode (`withLocalCompose(true)`) uses a locally installed compose binary instead of the containerised one.

## Go
```go
stack, err := compose.NewDockerComposeWith(compose.WithStackFiles("compose-test.yaml"))
require.NoError(t, err)
t.Cleanup(func() { _ = stack.Down(context.Background(), compose.RemoveOrphans(true), compose.RemoveImagesLocal) })
err = stack.WaitForService("api", wait.ForHTTP("/health").WithPort("8080/tcp")).Up(ctx, compose.Wait(true))
api, _ := stack.ServiceContainer(ctx, "api")   // *testcontainers.DockerContainer
host, _ := api.Host(ctx)
port, _ := api.MappedPort(ctx, "8080/tcp")
```

## Python
```python
from testcontainers.compose import DockerCompose
with DockerCompose("tests", compose_file_name="compose-test.yaml", wait=True) as compose:
    host = compose.get_service_host("api", 8080)
    port = compose.get_service_port("api", 8080)
```

When using Ryuk with the Go Compose module, the Go docs advise raising `ryuk.connection.timeout` to at least 5 minutes and
`ryuk.reconnection.timeout` to at least 30 seconds, because starting every service can take longer.

## Node
Node's `withWaitStrategy` takes container names (not service names); with Compose V2 the first replica is usually `<service>-1`.
```ts
const env = await new DockerComposeEnvironment("tests", "compose-test.yaml")
  .withWaitStrategy("api-1", Wait.forHttp("/health", 8080))
  .up();
const api = env.getContainer("api-1");
const url = `http://${api.getHost()}:${api.getMappedPort(8080)}`;
await env.down();
```

## Writing the test compose file
- An exposed service port does not need to be published in the Compose file: Testcontainers proxies it through an ambassador container (documented for Java and .NET) and gives you the mapped address, so avoid fixed host ports.
- Add `healthcheck:` to services and `depends_on: { condition: service_healthy }`; Python's `DockerCompose(wait=True)` and Go's `compose.Wait(true)` wait for running or healthy state.
- Python's `DockerCompose` accepts `profiles=[...]`, `services=[...]`, several compose files and `env_file`; pin image tags.
- Test data: init SQL mounted into the DB container, or seed through the API in test setup.

## Trade-offs vs individual containers
| Compose module | Individual containers |
|---|---|
| reuses existing compose definitions | per-service builders and modules |
| whole stack per test suite | per-container lifecycle control |
Prefer individual module containers unless the stack is genuinely complex.

## Verify
- [ ] Suite starts the stack, waits for health and passes; no fixed host ports in the test compose file.
- [ ] Containers and networks removed after the run.

## Checked
Documentation release: testcontainers-java 2.0.5 (docs/modules/docker_compose and ComposeContainerTest source), testcontainers-go v0.44.0 (docs/features/docker_compose, configuration), testcontainers-python 4.15.0 (docs/features/docker_compose), testcontainers-node v12.2.1 (docs/features/compose) and testcontainers-dotnet 4.16.0 (docs/api/compose), checked 2026-10-26.
Confirmed: Java `ComposeContainer` (Compose V2), `withExposedService(name, port, strategy)`, `getServiceHost`, `getServicePort`, local Compose mode, `DockerComposeContainer` is V1 and deprecated, 60 s default wait; Go `compose.NewDockerComposeWith`, `WithStackFiles`, `WaitForService`, `Up` with `compose.Wait`, `Down` with `RemoveOrphans` and `RemoveImagesLocal`, `ServiceContainer`; Python `DockerCompose(context, compose_file_name=..., wait=...)`, `get_service_host`, `get_service_port`, profiles; Node `DockerComposeEnvironment(path, file)`, `withWaitStrategy` by container name (`<service>-1`), `getContainer`; ambassador container for unpublished ports.
Corrected: removed the `PortEndpoint` Go helper (not in the docs read) and the v1 `_1` naming claim; added the Ryuk timeout advice for the Go Compose module.
Removed as unsupported: the trade-off table's startup-speed, isolation and missing-helper claims.
Method: documentation only; no commands were run.
