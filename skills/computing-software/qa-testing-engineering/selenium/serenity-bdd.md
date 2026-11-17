---
id: computing-software.qa-testing-engineering.selenium.serenity-bdd
name: serenity-bdd
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [serenity-bdd, screenplay-serenity, living-documentation-reports, java-bdd]
level: practitioner
status: docs-checked
description: "Use Serenity BDD with Selenium for Java: Screenplay actors and tasks, Cucumber/JUnit 5 integration, serenity.conf drivers, and the living-documentation report."
sources:
  - https://serenity-bdd.github.io/docs/guide/user_guide_intro
  - https://serenity-bdd.github.io/docs/screenplay/screenplay_fundamentals
  - https://serenity-bdd.github.io/docs/reporting/living_documentation
  - https://github.com/serenity-bdd/serenity-bdd.github.io
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serenity BDD

Serenity wraps WebDriver with lifecycle management, the Screenplay pattern and rich reports that map tests to requirements.

## Setup (Maven)
Dependencies: `serenity-core`, `serenity-junit5` (or `serenity-cucumber`), `serenity-screenplay`, `serenity-screenplay-webdriver`; plugin `serenity-maven-plugin` with `aggregate` goal bound to `post-integration-test`.

## serenity.conf
```hocon
webdriver {
  driver = chrome
  autodownload = true
  capabilities {
    browserName = "chrome"
    "goog:chromeOptions" { args = ["--headless=new", "--window-size=1440,900"] }
  }
}
environments {
  default { webdriver.base.url = "http://localhost:3000" }
  staging { webdriver.base.url = "https://staging.example.com" }
}
serenity.take.screenshots = FOR_FAILURES
```
`mvn verify -Denvironment=staging`.

## Screenplay test (JUnit 5)
```java
@ExtendWith(SerenityJUnit5Extension.class)
class AddToCartTest {
  @CastMember(name = "Toby") Actor toby;

  @Test void addsItem() {
    toby.attemptsTo(
      Open.url("/shop"),
      Click.on(Button.withText("Add to cart")),
      Ensure.that(Target.the("cart count").locatedBy("[data-test=cart-count]")).text().isEqualTo("1")
    );
  }
}
```
Custom tasks: `Task.where("{0} logs in", Enter.theValue(user).into(EMAIL), Click.on(SUBMIT))`.

## Reports
`target/site/serenity/` holds the aggregated report: steps with screenshots and a requirements hierarchy built from your package structure or feature files. Good for stakeholders; heavy for fast dev loops.

## Gotchas
- Serenity manages the driver lifecycle; creating your own `WebDriver` bypasses screenshots/reports.
- The aggregate report comes from the `serenity-maven-plugin` `aggregate` goal bound to `post-integration-test` (run `mvn verify`); by default `aggregate` does not fail the build on test failures.
- `serenity.take.screenshots` accepts `FOR_EACH_ACTION`, `BEFORE_AND_AFTER_EACH_STEP`, `AFTER_EACH_STEP`, `FOR_FAILURES` and `DISABLED`; the documented default is `BEFORE_AND_AFTER_EACH_STEP`, and `FOR_FAILURES` takes the fewest screenshots.

## Verify
`mvn verify` produces the aggregate report with requirement tree and failing-step screenshots.

## Checked

Checked 2026-10-25 against the Serenity BDD documentation source (serenity-bdd/serenity-bdd.github.io, pushed 2026-04-07). Confirmed: artifacts `serenity-core`, `serenity-junit5`, `serenity-cucumber`, `serenity-screenplay-webdriver`; `serenity-maven-plugin` `aggregate` goal in `post-integration-test`; `webdriver.driver`, `autodownload`, `capabilities` with `goog:chromeOptions`; `environments { ... }` selected with `-Denvironment=`; `webdriver.base.url`; `serenity.take.screenshots` values; `@CastMember`, `SerenityJUnit5Extension`, `Ensure.that(...).text().isEqualTo`, `Task.where`, `Open.url`, `Button.withText`. Corrected: headless mode is configured through `goog:chromeOptions` args, not an undocumented `headless.mode` key; `chrome.switches` replaced by the same capability. Removed: the claim that `mvn test` alone never produces HTML (the docs only say the report is aggregated by the plugin goal) and the claim that the screenshot setting 'massively' slows suites.

Method: documentation only; no commands were run.
