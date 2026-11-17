---
id: computing-software.software-engineering.csharp-dotnet.mocking-with-nsubstitute-and-moq
name: mocking-with-nsubstitute-and-moq
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, nsubstitute, moq, test-doubles, fakes, dotnet-testing, unit-testing]
level: practitioner
status: gated
description: "Use test doubles well in .NET: NSubstitute and Moq syntax for stubs and verification, argument matchers, async returns, when hand-written fakes beat mocks, and what not to mock."
sources: ["https://nsubstitute.github.io/help/getting-started/", "https://github.com/devlooped/moq/wiki/Quickstart", "https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocking with NSubstitute and Moq

**Goal:** isolate the unit under test from slow or nondeterministic collaborators
without writing brittle, implementation-coupled tests.

## NSubstitute
```csharp
var repo = Substitute.For<IOrderRepository>();
repo.GetAsync(42, Arg.Any<CancellationToken>()).Returns(new Order(42, OrderStatus.Open));
repo.GetAsync(Arg.Is<int>(id => id < 0), Arg.Any<CancellationToken>())
    .Returns<Order?>(_ => throw new ArgumentOutOfRangeException());

var sut = new OrderService(repo, Substitute.For<IEmailSender>());
await sut.CloseAsync(42, default);

await repo.Received(1).SaveAsync(Arg.Is<Order>(o => o.Status == OrderStatus.Closed), Arg.Any<CancellationToken>());
await repo.DidNotReceive().DeleteAsync(Arg.Any<int>(), Arg.Any<CancellationToken>());
```
Async methods returning `Task<T>` can use `.Returns(value)` directly (not on the fetched getting-started or return-value pages) (gated: unconfirmed, source is paywalled or blocked). NSubstitute documents an analysers page for catching misuse such as substituting non-virtual members (package name: gated: unconfirmed, source is paywalled or blocked).

## Moq equivalent
```csharp
var repo = new Mock<IOrderRepository>(MockBehavior.Loose);   // Loose is the default: unset calls return default values
repo.Setup(r => r.GetAsync(42, It.IsAny<CancellationToken>())).ReturnsAsync(new Order(42, OrderStatus.Open));
var sut = new OrderService(repo.Object, Mock.Of<IEmailSender>());
await sut.CloseAsync(42, default);
repo.Verify(r => r.SaveAsync(It.Is<Order>(o => o.Status == OrderStatus.Closed), It.IsAny<CancellationToken>()), Times.Once);   // Verify/Times API: the Quickstart shows Times.Never() and Times.AtLeastOnce(); Times.Once is not on that page (gated: unconfirmed, source is paywalled or blocked)
```
NSubstitute "will only work properly with interfaces, or with class members that are overridable from the test assembly", and warns that real code can run when you substitute classes with non-virtual members; Moq likewise sets up a mock's overridable methods. Check your organisation's policy on package versions before upgrading either library.

## What to mock
- Mock at architectural boundaries you own: repositories, gateways, clocks (`TimeProvider`),
  message publishers.
- Don't mock types you don't own (HttpClient, DbContext, ILogger internals): wrap them, or use
  real infrastructure (Testcontainers, WireMock.Net, `FakeLogger`; these tools were not checked) (gated: unconfirmed, source is paywalled or blocked).
- Don't mock value objects or the class under test.

## Stubs vs verification
Prefer asserting on outcomes (return values, state) and stub inputs. Use `Received`/`Verify` only
for meaningful side effects (email sent, message published). Verifying every call couples tests
to implementation and breaks on harmless refactors.

## Hand-written fakes
```csharp
sealed class InMemoryOrderRepository : IOrderRepository
{
    private readonly Dictionary<int, Order> _orders = new();
    public Task<Order?> GetAsync(int id, CancellationToken ct) => Task.FromResult(_orders.GetValueOrDefault(id));
    public Task SaveAsync(Order o, CancellationToken ct) { _orders[o.Id] = o; return Task.CompletedTask; }
    ...
}
```
Reusable across many tests, readable, and behave consistently - often better than repeating
mock setups.

## Verify
- [ ] Tests assert behaviour/outcomes; `Received`/`Verify` limited to important side effects.
- [ ] No mocks of third-party concrete types; boundaries wrapped by owned interfaces.

## Checked

2026-11-02. Checked against the NSubstitute getting-started and set-return-value pages and the Moq Quickstart wiki. Confirmed: Substitute.For<T>, Returns, Arg.Any/Arg.Is matching, Received check, interface/overridable-member restriction, Moq default Loose behaviour, `.Object`, `It.IsAny`/`It.Is`, `Mock.Of`, ReturnsAsync helpers. Removed: the SponsorLink claim about Moq 4.20.0. Gated: Task<T> Returns shorthand, analyser package name, `Times.Once`, the Testcontainers/WireMock.Net/FakeLogger suggestions, DidNotReceive.

Method: documentation only; no commands were run.
