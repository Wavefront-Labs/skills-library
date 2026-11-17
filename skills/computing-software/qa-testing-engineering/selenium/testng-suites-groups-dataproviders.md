---
id: computing-software.qa-testing-engineering.selenium.testng-suites-groups-dataproviders
name: testng-suites-groups-dataproviders
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, testng, selenium-framework, data-provider, testng-groups, parallel-execution, java]
level: practitioner
status: docs-checked
description: "Structure Java Selenium suites with TestNG: testng.xml suites, groups, DataProviders, parallel methods/classes with thread-safe drivers, listeners and retry analyzers."
sources:
  - https://testng.org/
  - https://github.com/testng-team/testng-team.github.io
  - https://www.selenium.dev/documentation/test_practices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TestNG for Selenium suites

**Goal:** organised, parallel, data-driven Java Selenium tests.

## testng.xml
```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Regression" parallel="methods" thread-count="4">
  <parameter name="browser" value="chrome"/>
  <test name="Checkout">
    <groups><run><include name="smoke"/><exclude name="wip"/></run></groups>
    <classes><class name="com.shop.tests.CheckoutTest"/></classes>
  </test>
</suite>
```
Maven: the TestNG documentation says TestNG is supported through the Surefire plugin (use a recent version) and points to the Surefire site for suite file and group options.

## Thread-safe driver
```java
public abstract class BaseTest {
  private static final ThreadLocal<WebDriver> DRIVER = new ThreadLocal<>();
  protected WebDriver driver() { return DRIVER.get(); }
  @Parameters("browser") @BeforeMethod(alwaysRun = true)
  public void setUp(@Optional("chrome") String browser) { DRIVER.set(DriverFactory.create(browser)); }
  @AfterMethod(alwaysRun = true)
  public void tearDown() { DRIVER.get().quit(); DRIVER.remove(); }
}
```

## DataProvider
```java
@DataProvider(name = "discounts", parallel = true)
public Object[][] discounts() { return new Object[][] { {"standard", 100.00, "5%"}, {"gold", 99.99, "0%"} }; }
@Test(dataProvider = "discounts", groups = "smoke")
public void appliesDiscount(String tier, double total, String expected) { ... }
```

## Listeners and retries
- `ITestListener.onTestFailure(ITestResult)` to take screenshots (`((TakesScreenshot) driver()).getScreenshotAs(OutputType.FILE)`).
- `IRetryAnalyzer` for limited retries; report retried tests as flaky, do not hide them.
- `dependsOnMethods` creates order coupling between tests; avoid it where possible.

## Gotchas
- Shared static `WebDriver` with `parallel="methods"`: tests drive each other's browsers. Use ThreadLocal.
- Setting `alwaysRun = true` on a before method runs it regardless of which groups it belongs to; on an after method it runs even if earlier methods failed or were skipped.

## Verify
Run with `thread-count=4`; no cross-test interference, each failure has its own screenshot.

## Checked

Checked 2026-10-25 against the TestNG documentation source (testng-team/testng-team.github.io, main branch asciidoc, pushed 2026-08-31; the old `doc` tree on the master branch is a 2023 snapshot and was not used). Confirmed: `<suite parallel="methods" thread-count=...>` with the documented parallel values, the DTD URL, `<groups><run><include/><exclude/>`, `<parameter>` with `@Parameters` and `@Optional`, `@DataProvider(parallel = true)` and its `Object[][]` return type, `IRetryAnalyzer`, `ITestListener.onTestFailure`, `alwaysRun` semantics, `dependsOnMethods`; Selenium's `TakesScreenshot.getScreenshotAs(OutputType.FILE)` was confirmed in the Selenium Java source. Removed: the Surefire `suiteXmlFiles` snippet and `-Dgroups` option, which the TestNG docs delegate to the Surefire site.

Method: documentation only; no commands were run.
