---
id: computing-software.software-engineering.csharp-dotnet.unit-tests-with-xunit-and-webapplicationfactory
name: unit-tests-with-xunit-and-webapplicationfactory
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-testing, xunit, webapplicationfactory, integration-testing, testcontainers, xunit-theory, dotnet-testing-practice]
level: practitioner
status: gated
description: "Test .NET code with xUnit: facts and theories, fixtures and collections, async lifetime, and in-memory API integration tests with WebApplicationFactory and Testcontainers."
sources:
  - https://xunit.net/docs/getting-started/v3/getting-started
  - https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests
  - https://dotnet.testcontainers.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# xUnit tests and WebApplicationFactory integration tests

**Goal:** fast unit tests plus realistic API tests that run the real pipeline in memory against real dependencies.

## 1. xUnit essentials
```csharp
public class PriceCalculatorTests
{
    [Fact]
    public void Applies_percentage_discount() =>
        Assert.Equal(90m, PriceCalculator.Apply(100m, Discount.Percent(10)));

    [Theory]
    [InlineData(0, 0)]
    [InlineData(100, 90)]
    public void Discount_table(decimal input, decimal expected) =>
        Assert.Equal(expected, PriceCalculator.Apply(input, Discount.Percent(10)));

    [Theory, MemberData(nameof(Cases))]
    public void Complex_cases(Order o, decimal expected) => Assert.Equal(expected, o.Total);
    public static TheoryData<Order, decimal> Cases => new() { { OrderWith(2, 5m), 10m } };
}
```
- A new class instance per test: constructor = setup, `IDisposable`/`IAsyncLifetime` = teardown.
- Shared expensive setup: `IClassFixture<T>` (per class) or `[Collection]` + `ICollectionFixture<T>` (across classes). Test collections also influence parallel execution (the exact rules: see the xunit.net parallelism docs) (gated: unconfirmed, source is paywalled or blocked).
- xUnit v3 test projects are stand-alone executables (`OutputType` Exe, runnable with `dotnet run`) and support Microsoft Testing Platform; the getting-started page names `xunit.v3.mtp-v2` as the core package. `TestContext.Current.CancellationToken` (used in the sample below) is not described on the getting-started page (gated: unconfirmed, source is paywalled or blocked).

## 2. WebApplicationFactory
The Testcontainers builder names in the sample (`PostgreSqlBuilder`, `GetConnectionString`) are unchecked (gated: unconfirmed, source is paywalled or blocked).
```csharp
public sealed class ApiFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _db = new PostgreSqlBuilder().WithImage("postgres:17").Build();

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDb>>();
            services.AddDbContext<AppDb>(o => o.UseNpgsql(_db.GetConnectionString()));
            services.AddSingleton<IClock>(new FakeClock(DateTimeOffset.Parse("2026-01-01Z")));
        });
    }
    public async ValueTask InitializeAsync() { await _db.StartAsync(); /* migrate */ }
    public new async ValueTask DisposeAsync() { await _db.DisposeAsync(); await base.DisposeAsync(); }
}

public class OrdersApiTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    [Fact]
    public async Task Create_returns_201()
    {
        var client = factory.CreateClient();
        var res = await client.PostAsJsonAsync("/orders", new { sku = "A1", qty = 2 }, TestContext.Current.CancellationToken);
        Assert.Equal(HttpStatusCode.Created, res.StatusCode);
    }
}
```
Minimal APIs: the docs use `WebApplicationFactory<Program>` where `TEntryPoint` is the SUT's entry point class, usually `Program.cs`; making `Program` accessible with `public partial class Program;` is the usual approach (that line is not on the fetched page) (gated: unconfirmed, source is paywalled or blocked).

## 3. Auth in integration tests
Register a test authentication handler in `ConfigureTestServices` (the docs mock an `AuthenticationHandler<TOptions>` returning `AuthenticateResult.Success`, with the scheme matching what the app expects), and choose claims per test via headers (gated: unconfirmed, source is paywalled or blocked), rather than disabling authorization.

## Gotchas
- `async void` tests are not awaited properly; return `Task`/`ValueTask`.
- Static state and shared databases across parallel classes cause flakiness; isolate data per test (unique IDs, transactions rolled back, or Respawn to reset).
- The Microsoft integration-testing docs say the EF Core in-memory provider suits only limited, basic testing and recommend the SQLite provider for in-memory testing; a real database via Testcontainers is closer to production.
- Ordering: with the minimal hosting model, the test app's `ConfigureServices` callback runs after the app's `Program.cs`; for the older Web Host model, `ConfigureServices` runs before `Startup.ConfigureServices` and `ConfigureTestServices` runs after. Use `ConfigureTestServices` for overrides so they win in both models.

## Verify
- `dotnet test` runs unit and integration tests in CI (Docker available), and a deliberately broken middleware order fails an integration test.

## Checked

2026-11-02. Checked against Microsoft Learn (ASP.NET Core integration tests), xunit.net shared-context and v3 getting-started pages. Confirmed: WebApplicationFactory<TEntryPoint> creating a TestServer, IClassFixture/collection fixture/IAsyncLifetime exist, new test class instance per test, ConfigureTestServices for overriding and auth handler mocking, SQLite recommended over in-memory provider, v3 projects are executables with Microsoft Testing Platform support. Fixed: unsupported parallelism statement, v3 package name, ConfigureServices ordering. Gated: public partial Program, TestContext cancellation token, header-based claims. Testcontainers (dotnet.testcontainers.org) was not fetched, so its API names in the sample are unchecked.

Method: documentation only; no commands were run.
