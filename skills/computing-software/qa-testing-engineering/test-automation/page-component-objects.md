---
id: computing-software.qa-testing-engineering.test-automation.page-component-objects
name: page-component-objects
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [page-components, page-fragments, page-object-model, component-objects, test-automation-patterns]
level: practitioner
status: docs-checked
description: "Model recurring UI parts as page component objects: one class per widget or panel, composed into page objects so only one place knows that part's HTML structure."
sources:
  - https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
  - https://martinfowler.com/bliki/PageObject.html
  - https://playwright.dev/docs/pom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component (page fragment) objects

**Goal:** wrap a recurring part of the UI once, instead of repeating its locators in every page object.

## What the sources say
- Selenium docs: a page object need not represent a whole page; it can be composed of Page Object Components for sections that appear often in a site or page, such as site navigation. The essential principle is that only one place in the test suite knows the HTML structure of a given page or part of a page.
- Selenium docs credit Martin Fowler with first noting this (he called them "panel objects"); the same principles as page objects apply, and component objects expose references to the elements in their chunk plus methods for its behaviour.
- Fowler: page objects should usually be built for the significant elements on a page rather than one per page. A page of albums has an album-list object containing album objects, plus header and footer objects. Model the structure that makes sense to the application's user; do not reveal structure that exists only to lay out the UI.
- Fowler's rule of thumb: if you swapped the concrete control (for example a text box for another widget), the page object interface should not change. Text fields use string accessors, check boxes use booleans, buttons are action-named methods.
- Playwright docs: page objects simplify authoring with a higher-level API and simplify maintenance by capturing selectors in one place; the example class takes a `Page` in its constructor and defines `Locator`s there.

## Illustrative shape (not from the pages)
```ts
export class DataTable {
  constructor(private root: Locator) {}
  row(text: string) { return this.root.getByRole('row').filter({ hasText: text }); }
}
export class OrdersPage {
  readonly table: DataTable;
  constructor(page: Page) { this.table = new DataTable(page.getByRole('table', { name: 'Orders' })); }
}
```
The page owns the root locator; the component finds everything relative to it.

## Guidelines supported by the sources
- Public methods are the services the component offers; do not expose its internals.
- Generally no assertions in the component; the exception is a check that the page or critical elements loaded.
- Methods return data, other page or component objects, or (optionally) themselves for fluent syntax.

## Verify
Each widget's locators live in one class, pages compose components, and a markup change to a widget needs one edit.

## Checked
2026-11-08. Confirmed against the Selenium page object models page, Fowler's PageObject bliki and the Playwright POM page: components may be parts of pages, one place knows the HTML structure, composition of objects, no-assertion rule with a loaded-check exception, selectors captured in one place. Removed: the claims that elements should be found lazily to avoid stale references, that broad root locators cause Playwright strictness errors, the guidance on `nth(i)` instances and the specific widget list (none is in the pages), the Java `Header` example and the "avoid deep inheritance" gotcha (not stated in these pages). The TypeScript snippet is kept as an illustration and labelled as such.
Method: documentation only; no commands were run.
