---
id: computing-software.qa-testing-engineering.test-automation.reqnroll-specflow-bdd-dotnet
name: reqnroll-specflow-bdd-dotnet
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [reqnroll, specflow, bdd, gherkin, dotnet, test-first]
level: practitioner
status: docs-checked
description: "Set up BDD in .NET with Reqnroll (SpecFlow successor): bindings, Cucumber expressions, context injection, hooks, data tables and SpecFlow migration."
sources:
  - https://docs.reqnroll.net/latest/
  - https://docs.reqnroll.net/latest/guides/migrating-from-specflow.html
  - https://docs.reqnroll.net/latest/installation/setup-project.html
  - https://docs.reqnroll.net/latest/automation/hooks.html
  - https://docs.reqnroll.net/latest/automation/datatable-helpers.html
  - https://docs.reqnroll.net/latest/automation/cucumber-expressions.html
  - https://cucumber.io/docs/cucumber/cucumber-expressions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reqnroll / SpecFlow BDD in .NET

**Goal:** executable Gherkin specifications in C#. Reqnroll is the SpecFlow successor: packages and namespaces were renamed, and a compatibility package eases migration.

## Setup
```bash
dotnet new nunit -n Shop.Specs
dotnet add Shop.Specs package Reqnroll.NUnit      # or Reqnroll.xUnit / Reqnroll.MsTest
```
Alternatively install the templates (`dotnet new install Reqnroll.Templates.DotNet`) and run `dotnet new reqnroll-project`. Add `Features/Checkout.feature`.

## Bindings
```csharp
using Reqnroll;

[Binding]
public class CheckoutSteps
{
    private readonly CartDriver _cart;            // context injection via constructor
    public CheckoutSteps(CartDriver cart) => _cart = cart;

    [Given("a cart containing {int} items of {string}")]
    public void GivenCart(int qty, string sku) => _cart.Add(sku, qty);

    [When("the customer checks out")]
    public void WhenCheckout() => _cart.Checkout();

    [Then("the order total is {decimal}")]
    public void ThenTotal(decimal total) => Assert.That(_cart.Total, Is.EqualTo(total));
}
```
Expressions containing placeholders such as `{int}` or `{string}` are treated as Cucumber expressions; regular expressions also work.

## Hooks and state
`[BeforeScenario]`, `[AfterScenario]`, `[BeforeTestRun]` and `[BeforeFeature]` (these two must be static), scoped with tags: `[BeforeScenario("@db")]`. Share state by injecting driver classes through the constructor (context injection) rather than `ScenarioContext` dictionaries.

## Data tables
`table.CreateSet<OrderLine>()` / `table.CreateInstance<Customer>()` map rows to objects; `table.CompareToSet(actual)` asserts (order is ignored unless you pass `true` as the second argument).

## Migrating from SpecFlow
Replace `SpecFlow.*` packages with the matching `Reqnroll.*` package, change the `TechTalk.SpecFlow` namespace to `Reqnroll`, rename `specflow.json` to `reqnroll.json`; or add `Reqnroll.SpecFlowCompatibility` to keep the old namespace during transition.

## Gotchas
- Keep step definitions thin; put automation logic in drivers/page objects.

## Verify
`dotnet test` runs the scenarios.

## Checked
2026-11-01. Confirmed from the Reqnroll docs source (installation/setup-project, guides/migrating-from-specflow, automation/hooks, datatable-helpers, cucumber-expressions): package names, `dotnet new reqnroll-project`, hook list and static requirement, CreateSet/CreateInstance/CompareToSet, Cucumber-expression detection, migration steps and `Reqnroll.SpecFlowCompatibility`. Removed: SpecFlow end-of-life claim, build-time generation claim, parallel-execution and undefined-step claims, "one instance per scenario" wording.
Method: documentation only; no commands were run.
