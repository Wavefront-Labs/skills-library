---
id: computing-software.qa-testing-engineering.selenium.loadable-component-page-readiness
name: loadable-component-page-readiness
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [loadable-component, page-object-model, selenium, page-readiness, waits, slowloadablecomponent]
level: practitioner
status: docs-checked
description: "Use Selenium's LoadableComponent and SlowLoadableComponent to make page objects verify and reach their loaded state, with clear failures and nested parent pages."
sources:
  - https://www.selenium.dev/documentation/legacy/selenium_2/loadable_component/
  - https://www.selenium.dev/documentation/test_practices/design_strategies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoadableComponent and page readiness checks

**Goal:** (legacy pattern; the Selenium docs now point to their design-patterns pages) page objects that know how to get themselves loaded and prove they are loaded, so tests fail with "Login page not loaded" instead of a random NoSuchElementException later.

## LoadableComponent (Java, Selenium support library)

```java
public class EditIssuePage extends LoadableComponent<EditIssuePage> {
  private final WebDriver driver;
  private final ProjectPage parent;

  public EditIssuePage(WebDriver driver, ProjectPage parent) { this.driver = driver; this.parent = parent; }

  @Override protected void load() {
    parent.get();                              // ensure prerequisite page is loaded first
    driver.get(parent.url() + "/issues/new");
  }

  @Override protected void isLoaded() throws Error {
    String url = driver.getCurrentUrl();
    if (!url.endsWith("/issues/new")) throw new Error("Not on new issue page: " + url);
    if (driver.findElements(By.id("issue_title")).isEmpty()) throw new Error("Title field missing");
  }
}

EditIssuePage page = new EditIssuePage(driver, new ProjectPage(driver)).get();
```

`get()` navigates to the page if necessary, and a call on a nested component loads its parents first. `isLoaded()` performs assertions (it returns void) with messages that explain why a page failed to load.

## Readiness checks to use in isLoaded
URL/route, a landmark element unique to the page, spinner gone, key data rendered. Avoid checking `document.readyState` alone in SPAs.

## Verify
Calling `get()` on a page from a cold start navigates through parents and returns a loaded page, and a broken route fails with the `isLoaded` message.

## Checked

Checked 2026-10-25 against the Selenium documentation source (legacy LoadableComponent page, pushed 2026-10-23). Confirmed: the `load()`/`isLoaded()` contract, `get()` navigating when needed, nested components loading parents via `get()`, and that the page is legacy with design-patterns pages as the current guidance. Removed: the SlowLoadableComponent constructor details and the Playwright aside, which are not covered by the Selenium docs.

Method: documentation only; no commands were run.
