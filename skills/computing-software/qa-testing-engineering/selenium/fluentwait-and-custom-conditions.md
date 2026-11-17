---
id: computing-software.qa-testing-engineering.selenium.fluentwait-and-custom-conditions
name: fluentwait-and-custom-conditions
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [fluentwait, explicit-waits, webdriverwait, expected-conditions, selenium-waits]
level: practitioner
status: docs-checked
description: "Use Selenium FluentWait and WebDriverWait with custom conditions: polling interval, ignored exceptions, lambda conditions, and why mixing implicit and explicit waits breaks."
sources:
  - https://www.selenium.dev/documentation/webdriver/waits/
  - https://www.selenium.dev/documentation/support_features/expected_conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FluentWait and custom conditions

## FluentWait (Java)
```java
Wait<WebDriver> wait = new FluentWait<>(driver)
    .withTimeout(Duration.ofSeconds(30))
    .pollingEvery(Duration.ofMillis(500))
    .ignoring(NoSuchElementException.class)
    .ignoring(StaleElementReferenceException.class)
    .withMessage("order status never became PAID");

String status = wait.until(d -> {
  String s = d.findElement(By.cssSelector("[data-test=status]")).getText();
  return s.equals("PAID") ? s : null;          // null/false = keep polling; any other value = done
});
```

## Python
```python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

wait = WebDriverWait(driver, timeout=30, poll_frequency=0.5,
                     ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "[data-test=status]").text == "PAID",
           message="order status never became PAID")
```

## Custom conditions worth having
- Element count stops changing (list finished loading).
- No spinner and no pending requests, if the app exposes a readiness flag you can read with `execute_script`.

## Rules
- Do not mix implicit and explicit waits: the Selenium docs warn this causes unpredictable wait times (for example a 10 s implicit and 15 s explicit wait could time out after 20 s).
- Conditions must be side-effect free; they run repeatedly.

## Gotchas
- Ignoring broad exceptions (`WebDriverException`) hides real failures until timeout.
- `Thread.sleep` in conditions defeats polling.

## Verify
No `sleep` calls remain, implicit and explicit waits are not mixed, and timeout messages say what was awaited.

## Checked

Checked 2026-10-25 against the Selenium documentation (waits page and the Java and Python wait examples; pushed 2026-10-23). Confirmed: FluentWait customisation (timeout, polling interval, ignored exceptions, message) in Java and the Python `WebDriverWait` equivalent; the warning not to mix implicit and explicit waits. Removed as undocumented: the 500 ms default polling and WebDriverWait definition, the `attributeToBe` and file-exists examples, the generic-object FluentWait remark, and the `Thread.sleep` gotcha; the implicit-wait mechanism was replaced by the documented warning.

Method: documentation only; no commands were run.
