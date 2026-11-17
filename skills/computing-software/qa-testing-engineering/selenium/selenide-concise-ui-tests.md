---
id: computing-software.qa-testing-engineering.selenium.selenide-concise-ui-tests
name: selenide-concise-ui-tests
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenide, java-ui-tests, selenide-conditions, automatic-waiting]
level: practitioner
status: docs-checked
description: "Write concise Java UI tests with Selenide: $ and $$ selectors, built-in waiting conditions, Configuration options, screenshots on failure and Selenoid/Grid remote."
sources:
  - https://selenide.org/documentation.html
  - https://github.com/selenide/selenide
  - https://selenide.org/javadoc/current/com/codeborne/selenide/Configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selenide concise UI tests

Selenide is a thin layer over WebDriver: auto driver lifecycle, implicit smart waiting on conditions, short syntax.

```java
import static com.codeborne.selenide.Selenide.*;
import static com.codeborne.selenide.Condition.*;
import static com.codeborne.selenide.CollectionCondition.*;

class SearchTest {
  @Test void search() {
    open("/search");
    $("#q").setValue("selenide").pressEnter();
    $$(".result").shouldHave(sizeGreaterThan(3));
    $(".result", 0).shouldHave(text("Selenide"));
    $(byText("Next")).shouldBe(visible, enabled).click();
    $("[data-test=toast]").shouldHave(exactText("Saved"), Duration.ofSeconds(10));
  }
}
```
`should*` conditions retry up to `Configuration.timeout` (default 4000 ms), so no explicit waits are needed.

## Configuration
```java
Configuration.baseUrl = "http://localhost:3000";
Configuration.browser = "firefox";
Configuration.headless = true;
Configuration.browserSize = "1440x900";
Configuration.timeout = 6000;
Configuration.remote = "http://grid:4444/wd/hub";    // remote WebDriver URL (default null: no Grid)
Configuration.reportsFolder = "build/reports/selenide";
```
The same options can be set in `selenide.properties` or as system properties such as `-Dselenide.browser=chrome` or `-Dselenide.timeout=10000`. Defaults include `browserSize` 1366x768 and `reportsFolder` build/reports/tests.

## Failure evidence
By default (`screenshots` and `savePageSource` are true) Selenide saves a screenshot and page source on failure. JUnit 5: `@ExtendWith(ScreenShooterExtension.class)` for all tests.

## Page objects
```java
public class LoginPage {
  private final SelenideElement email = $("#email");
  public void login(String u, String p) { email.setValue(u); $("#password").setValue(p).pressEnter(); }
}
```

## Gotchas
- Mixing raw `driver.findElement` with Selenide loses waiting; use `WebDriverRunner.getWebDriver()` only for gaps.
- `text(...)` asserts that the element's text contains the given text, ignoring case; `exactText` matches the whole text.

## Verify
A deliberately failing condition leaves a screenshot and page source in the reports folder and names the condition that timed out.

## Checked

Checked 2026-10-25 against the Selenide source (selenide/selenide main, pushed 2026-10-25): `Configuration` and `SelenideConfig` (timeout default 4000 ms, `baseUrl`, `browser`, `headless`, `browserSize` default 1366x768, `remote`, `reportsFolder` default build/reports/tests, `screenshots` and `savePageSource` defaults, `selenide.*` property prefix), `Condition.text` (case-insensitive contains) and `exactText`, `CollectionCondition.sizeGreaterThan`, `SelenideElement.shouldHave(condition, Duration)`, `pressEnter`, `$(selector, index)`, `ScreenShooterExtension` for JUnit 5. Removed as undocumented: the Selenoid mention, the per-thread driver and parallel remark, and the claim that error messages print screenshot paths.

Method: documentation only; no commands were run.
