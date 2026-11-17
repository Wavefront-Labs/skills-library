---
id: computing-software.cloud-infrastructure-engineering.docker.testcontainers-for-dotnet
name: testcontainers-for-dotnet
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, testcontainers-dotnet, testcontainers, xunit, integration-tests, iasynclifetime, dotnet-testing]
level: practitioner
status: docs-checked
description: "Write .NET integration tests with Testcontainers for .NET: modules for databases and brokers, xUnit lifetimes and fixtures, wait strategies, networking, and CI configuration."
sources:
  - https://dotnet.testcontainers.org/
  - https://dotnet.testcontainers.org/modules/
  - https://dotnet.testcontainers.org/test_frameworks/xunit_net/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testcontainers for .NET

## Install
```bash
dotnet add package Testcontainers.PostgreSql
dotnet add package Testcontainers.Redis
```
Modules exist for PostgreSQL, SQL Server (MsSql), MongoDB, Redis, RabbitMQ, Azurite, Elasticsearch and more (see the modules index); the generic `ContainerBuilder` covers anything else. Module builders and `ContainerBuilder` take the image in the constructor, for example `new PostgreSqlBuilder("postgres:16-alpine")` or `new ContainerBuilder("nginx:1.26.3-alpine3.20")`; `WithImage(...)` still replaces it.

## xUnit: container per test class
```csharp
public sealed class OrderRepositoryTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _pg = new PostgreSqlBuilder("postgres:16-alpine")
        .Build();

    public Task InitializeAsync() => _pg.StartAsync();
    public Task DisposeAsync() => _pg.DisposeAsync().AsTask();

    [Fact]
    public async Task Saves_and_loads_order()
    {
        await using var db = new ShopDbContext(new DbContextOptionsBuilder<ShopDbContext>()
            .UseNpgsql(_pg.GetConnectionString()).Options);
        await db.Database.MigrateAsync();
        db.Orders.Add(new Order { Id = 1, Total = 9.99m });
        await db.SaveChangesAsync();
        Assert.Equal(9.99m, (await db.Orders.FindAsync(1))!.Total);
    }
}
```
Share one container across classes with an `ICollectionFixture<T>` (xUnit collection) to cut startup time, and reset data between tests. The `Testcontainers.Xunit` (xUnit.net v2) and `Testcontainers.XunitV3` packages also provide `ContainerTest<,>` (a new container per test) and `ContainerFixture<,>` (shared, used with `IClassFixture<>`) base classes, plus `DbContainerTest` and `DbContainerFixture` for ADO.NET databases; always pin the image version.

## ASP.NET Core with WebApplicationFactory
```csharp
public class ApiFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _pg = new PostgreSqlBuilder("postgres:16-alpine").Build();
    protected override void ConfigureWebHost(IWebHostBuilder b) =>
        b.UseSetting("ConnectionStrings:Shop", _pg.GetConnectionString());
    public Task InitializeAsync() => _pg.StartAsync();
    public new Task DisposeAsync() => _pg.DisposeAsync().AsTask();
}
```

## Generic containers and waits
```csharp
var api = new ContainerBuilder("ghcr.io/org/stub-api:1.2")
    .WithPortBinding(8080, true)                                   // random host port
    .WithEnvironment("MODE", "test")
    .WithWaitStrategy(Wait.ForUnixContainer().UntilHttpRequestIsSucceeded(r => r.ForPort(8080).ForPath("/health")))
    .Build();
await api.StartAsync();
var url = $"http://{api.Hostname}:{api.GetMappedPublicPort(8080)}";
```
Use `Hostname` and mapped ports, never a fixed `localhost:8080`; with `WithPortBinding(8080, true)` the host port is assigned at random. The HTTP wait strategy also accepts `ForStatusCode(...)`; `UntilMessageIsLogged(...)` and `UntilInternalTcpPortIsAvailable(...)` are other strategies.

## Networks
```csharp
var net = new NetworkBuilder().Build();
var db = new PostgreSqlBuilder("postgres:16-alpine").WithNetwork(net).WithNetworkAliases("db").Build();
```
Containers on the same custom network talk via aliases without publishing ports; tests talk via mapped ports.

## CI
- CI only needs Docker (a local install is not mandatory; a remote Docker works). Microsoft-hosted agents and GitHub-hosted runners come with Docker pre-installed. Linux containers run on Windows, macOS and Linux hosts; native Windows containers only on Windows.
- Ryuk (resource reaper) removes the session's Docker resources after the tests finish, whether they pass or not. The docs say not to disable it where possible; `TESTCONTAINERS_RYUK_DISABLED=true` is for environments that clean up themselves (the docs use it for Bitbucket Pipelines, which does not support Ryuk).
- GitLab CI needs the `docker:dind` service with `DOCKER_HOST: tcp://docker:2375`.
- Pin image tags.

## Verify
- [ ] `dotnet test` passes locally and in CI with no leftover containers (`docker ps -a` empty after).
- [ ] Tests use mapped ports/hostname only.

## Checked
Documentation release: testcontainers-dotnet 4.16.0 docs (docs/index, api/create_docker_container, api/wait_strategies, api/create_docker_network, api/resource_reaper, cicd, test_frameworks/xunit_net, modules/postgres, examples/aspnet; main as of 2026-10-24), checked 2026-10-26.
Confirmed: `Testcontainers.PostgreSql` package and `new PostgreSqlBuilder("postgres:15.1")` form; `new ContainerBuilder("image")` constructor and `WithImage`; `WithPortBinding(port, true)`, `Hostname`, `GetMappedPublicPort`; `Wait.ForUnixContainer()` with `UntilHttpRequestIsSucceeded` (`ForPort`, `ForPath`, `ForStatusCode`), `UntilMessageIsLogged`, `UntilInternalTcpPortIsAvailable`; `NetworkBuilder`, `WithNetwork`, `WithNetworkAliases`; `WebApplicationFactory` with `ConfigureWebHost` and `UseSetting`; Testcontainers.Xunit and XunitV3 base classes; Ryuk behaviour and `TESTCONTAINERS_RYUK_DISABLED`; CI notes for Azure Pipelines, GitHub Actions and GitLab dind; OS support statement.
Corrected: builders take the image in the constructor in the current docs; removed MySQL, Kafka and LocalStack module names, `KafkaBuilder` example, Respawn, "pre-pull images in a cache step", and the claim that Windows runners only run Windows containers.
Method: documentation only; no commands were run.
