---
id: computing-software.qa-testing-engineering.playwright.playwright-java-and-dotnet
name: playwright-java-and-dotnet
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-java, playwright-dotnet, playwright-nunit, playwright-junit]
level: practitioner
status: docs-checked
description: "Write Playwright tests in Java (JUnit 5, Maven) and .NET (NUnit base classes): install browsers, assertions, runsettings, per-thread instances, tracing."
sources:
  - https://playwright.dev/java/docs/intro
  - https://playwright.dev/java/docs/junit
  - https://playwright.dev/java/docs/test-runners
  - https://playwright.dev/java/docs/browsers
  - https://playwright.dev/dotnet/docs/intro
  - https://playwright.dev/dotnet/docs/test-runners
  - https://playwright.dev/dotnet/docs/running-tests
  - https://playwright.dev/dotnet/docs/trace-viewer-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright for Java and .NET

In Java/.NET you use JUnit/NUnit (or MSTest, xUnit) for structure; Playwright supplies the browser API and assertions.

## Java
Install browsers (and OS dependencies) through the bundled CLI:
`mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install --with-deps"`.

```java
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

class CheckoutTest {
  static Playwright playwright;
  static Browser browser;
  BrowserContext context;
  Page page;

  @BeforeAll static void launch() {
    playwright = Playwright.create();
    browser = playwright.chromium().launch();
  }
  @BeforeEach void newContext() {
    context = browser.newContext();
    page = context.newPage();
  }
  @Test void addsToCart() {
    page.navigate("http://localhost:3000/shop");
    page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Add to cart")).click();
    assertThat(page.getByTestId("cart-count")).hasText("1");
  }
}
```
Create `Playwright` in `@BeforeAll` and a fresh `BrowserContext` per test in `@BeforeEach`. Playwright objects are not safe to share across threads without extra synchronization: for parallel JUnit, create one Playwright instance per thread and use it only on that thread.

## .NET
```bash
dotnet add package Microsoft.Playwright.NUnit
dotnet build && pwsh bin/Debug/net8.0/playwright.ps1 install --with-deps
```
```csharp
[Parallelizable(ParallelScope.Self)]
public class CartTests : PageTest {
  [Test] public async Task AddsToCart() {
    await Page.GotoAsync("http://localhost:3000/shop");
    await Page.GetByRole(AriaRole.Button, new() { Name = "Add to cart" }).ClickAsync();
    await Expect(Page.GetByTestId("cart-count")).ToHaveTextAsync("1");
  }
}
```
`PageTest` gives each test a fresh Page in its own BrowserContext. Override `ContextOptions()` to set context options per test file. Configure the browser with a `.runsettings` file (`<Playwright>` section with `<BrowserName>` and `<LaunchOptions>`), command-line parameters such as `Playwright.BrowserName=chromium`, or the `BROWSER` environment variable (`BROWSER=webkit dotnet test`).

## Tracing
Start tracing explicitly in setup (`Context.Tracing.StartAsync`) and stop it with a path in teardown (`Context.Tracing.StopAsync`); open the zip with `playwright.ps1 show-trace`.

## Gotchas
- Install the browsers in CI after restore/build.
- Forgetting `await` in C# produces flaky passes.

## Checked
2026-11-01. Confirmed from the Playwright docs source (docs/src: browsers, intro-csharp, test-runners-java, test-runners-csharp, junit-java, running-tests-csharp, trace-viewer-intro-csharp): Maven CLI install with `--with-deps`, `playwright.ps1 install`, `Microsoft.Playwright.NUnit` package, `PlaywrightAssertions.assertThat`, `@BeforeAll`/`@BeforeEach` pattern, per-thread Playwright instance advice, `PageTest` fresh context, `ContextOptions` override, `.runsettings` BrowserName/LaunchOptions, `BROWSER` env, `Parallelizable(ParallelScope.Self)`, `Context.Tracing.StartAsync/StopAsync`, `show-trace`. Removed: `@UsePlaywright`/`OptionsFactory` example, "test runner features are Node-only" and MSTest runsettings specifics, none of which those pages state.
Method: documentation only; no commands were run.
