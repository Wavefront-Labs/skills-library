---
id: computing-software.qa-testing-engineering.selenium.selenium-jupiter-junit5
name: selenium-jupiter-junit5
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium-jupiter, junit5, webdriver-injection, java-selenium]
level: practitioner
status: docs-checked
description: "Use Selenium-Jupiter (JUnit 5 extension) to inject WebDriver instances, run cross-browser templates, use Docker browsers and capture screenshots on failure in Java."
sources:
  - https://bonigarcia.dev/selenium-jupiter/
  - https://github.com/bonigarcia/selenium-jupiter
  - https://junit.org/junit5/docs/current/user-guide/#extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JUnit 5 with Selenium-Jupiter

## Dependency
```xml
<dependency><groupId>io.github.bonigarcia</groupId><artifactId>selenium-jupiter</artifactId><version>${sj.version}</version><scope>test</scope></dependency>
```

## Injection
```java
@ExtendWith(SeleniumJupiter.class)
class LoginTest {
  @Test void loginChrome(ChromeDriver driver) {
    driver.get("https://app.test/login");
    driver.findElement(By.id("email")).sendKeys("a@b.test");
  }
  @Test void loginHeadless(@Arguments("--headless=new") ChromeDriver driver) { ... }
  @Test void loginInDocker(@DockerBrowser(type = CHROME, version = "beta") WebDriver driver) { ... }
}
```
By default the extension creates drivers before each test and disposes them after each test; the class-level `@SingleSession` annotation shares one driver across the class. Docker browsers need Docker Engine on the machine running the tests.

## Cross-browser template
```java
@TestTemplate
void crossBrowser(WebDriver driver) { ... }
```
with a browser scenario in `browsers.json` on the classpath (the default), for example `{"browsers": [[{"type": "chrome-in-docker", "version": "latest"}], [{"type": "chrome-in-docker", "version": "beta"}]]}`; the location can be changed with `sel.jup.browser.template.json.file`.

## Failure evidence
`sel.jup.screenshot.when.failure=true`, `sel.jup.screenshot.format=png` (also `base64`, `base64andpng`) and `sel.jup.output.folder` set in `selenium-jupiter.properties`, Java system properties or environment variables (precedence: environment variables, then system properties, then Java configuration). Docker browsers can record: `@DockerBrowser(type = CHROME, recording = true)`. From version 6.3.0 an ExtentReports report is generated out of the box.

## Gotchas
- A shared driver (`@SingleSession`) carries browser state between tests; order tests deliberately.
- Docker browsers need a Docker Engine in CI.

## Verify
`mvn test` runs the template once per configured browser; failing tests leave screenshots in the output folder.

## Checked

Checked 2026-10-25 against the Selenium-Jupiter repository (bonigarcia/selenium-jupiter, pushed 2026-10-19; README, CHANGELOG and the documentation page, version 6.3.x). Confirmed: Maven coordinates io.github.bonigarcia:selenium-jupiter, `SeleniumJupiter` extension, `@Arguments`, `@DockerBrowser` with `type`, `version` and `recording`, `@TestTemplate` with `browsers.json`, `sel.jup.*` keys and precedence, `@SingleSession`, default per-test driver lifecycle. Corrected: there is no `@BrowsersTemplate` annotation; the screenshot key is `sel.jup.screenshot.when.failure`; the template uses the plain JUnit `@TestTemplate`. Removed: the hand-written extension alternative and the parameter-versus-field injection remark.

Method: documentation only; no commands were run.
