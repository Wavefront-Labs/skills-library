---
id: computing-software.qa-testing-engineering.selenium.selenium-csharp-nunit
name: selenium-csharp-nunit
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [nunit, selenium-csharp, dotnet-selenium, webdriverwait-csharp]
level: practitioner
status: docs-checked
description: "Build Selenium tests in C# with NUnit: driver lifecycle with SetUp/TearDown, WebDriverWait, parallelizable fixtures, TestContext attachments and dotnet test filters."
sources:
  - https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
  - https://docs.nunit.org/articles/nunit/writing-tests/attributes/parallelizable.html
  - https://docs.nunit.org/articles/nunit/writing-tests/attributes/fixturelifecycle.html
  - https://docs.nunit.org/articles/nunit/writing-tests/TestContext.html
  - https://github.com/spekt/junit.testlogger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selenium with NUnit in C#

```bash
dotnet new nunit -n E2E && cd E2E
dotnet add package Selenium.WebDriver
dotnet add package Selenium.Support    # SelectElement and other support classes
```

```csharp
[TestFixture, Parallelizable(ParallelScope.Self)]
public class CheckoutTests
{
    private IWebDriver _driver = null!;

    [SetUp] public void SetUp()
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless=new");
        _driver = new ChromeDriver(options);    // Selenium Manager finds chromedriver
    }

    [Test] public void AddsItemToCart()
    {
        _driver.Navigate().GoToUrl("https://shop.test");
        _driver.FindElement(By.CssSelector("[data-test=add]")).Click();
        var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(10));
        var count = wait.Until(d => d.FindElement(By.CssSelector("[data-test=cart-count]")));
        Assert.That(count.Text, Is.EqualTo("1"));
    }

    [TearDown] public void TearDown()
    {
        if (TestContext.CurrentContext.Result.Outcome.Status == NUnit.Framework.Interfaces.TestStatus.Failed)
        {
            var path = Path.Combine(TestContext.CurrentContext.WorkDirectory, $"{TestContext.CurrentContext.Test.Name}.png");
            ((ITakesScreenshot)_driver).GetScreenshot().SaveAsFile(path);
            TestContext.AddTestAttachment(path);
        }
        _driver.Quit();
        _driver.Dispose();
    }
}
```

## Parallelism
`[assembly: LevelOfParallelism(4)]` and `[Parallelizable(ParallelScope.Fixtures)]` or `Self` (the default scope). A driver stored in a fixture field is shared by every test of that fixture, which is unsafe with `ParallelScope.Children`; `[FixtureLifeCycle(LifeCycle.InstancePerTestCase)]` creates a new fixture instance per test, so instance fields are not shared.

## Running
`dotnet test --filter "TestCategory=Smoke"` with `[Category("Smoke")]` (the NUnit docs also show `dotnet test -- NUnit.Where="cat == Smoke"`); `--logger "trx;logfilename=results.trx"` writes a TRX file, and the JunitXml.TestLogger package adds `--logger:junit` for CI.

## Gotchas
- `WebDriverWait` ignores `NotFoundException` by default only; add `wait.IgnoreExceptionTypes(typeof(StaleElementReferenceException))` as needed.
- Always `Quit()` (not `Close()`) to end the driver process.

## Verify
`dotnet test` in CI produces TRX/JUnit results with screenshot attachments for failures.

## Checked

Checked 2026-10-25 against the Selenium documentation source and .NET source (SeleniumHQ/selenium trunk), the NUnit docs source (nunit/docs, pushed 2026-10-24), the dotnet/docs `dotnet test` page and the JunitXml.TestLogger README. Confirmed: Selenium.WebDriver and Selenium.Support packages (4.51.0 in the docs examples), `dotnet new NUnit`, `ChromeOptions.AddArgument`, `ITakesScreenshot.GetScreenshot().SaveAsFile`, `WebDriverWait` ignoring `NotFoundException` by default and `IgnoreExceptionTypes`, `ParallelScope` values and default `Self`, `LevelOfParallelism`, `FixtureLifeCycle(LifeCycle.InstancePerTestCase)`, `TestContext.AddTestAttachment` (3.7+) and `WorkDirectory`, `--logger "trx;logfilename=..."`, `--logger:junit`. Corrected: the category filter is `TestCategory=` in the NUnit docs. Removed: the DotNetSeleniumExtras.WaitHelpers package (third party, not covered by the docs).

Method: documentation only; no commands were run.
