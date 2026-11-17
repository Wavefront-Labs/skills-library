---
id: computing-software.qa-testing-engineering.test-automation.screenplay-pattern
name: screenplay-pattern
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [screenplay-pattern, test-automation-patterns, serenity-js, actors-tasks-questions, page-objects]
level: practitioner
status: docs-checked
description: "Structure acceptance tests with the Screenplay pattern: actors with abilities perform interactions and tasks and answer questions, using Serenity/JS or Serenity BDD."
sources:
  - https://serenity-js.org/handbook/design/screenplay-pattern/
  - https://serenity-bdd.github.io/docs/screenplay/screenplay_fundamentals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screenplay pattern

**Goal:** tests that express what actors do to reach their goals in domain language, built from layers of reusable activities.

## Design principle (Serenity/JS handbook)
Automated acceptance tests should use domain language to express the activities actors perform to accomplish their goals. The handbook lists benefits: scenarios are easier to understand for a wider audience, failures can be related to business impact, and reusable business-focused activities reduce duplication and let you compose new scenarios from existing steps. It frames each scenario as a small screenplay answering who the actors are, why they interact, what they need to do and how.

## Five building blocks
- **Actors**: people and external systems interacting with the system under test, each playing a role. The handbook stresses roles are not a permission mechanism: nothing stops a "writer" from trying to act as a "publisher", which you need to be able to test access control.
- **Abilities**: thin wrappers around the integration libraries needed to interact with the system (for example browsing the web).
- **Interactions**: low-level activities an actor can perform using a given interface.
- **Tasks**: sequences of activities modelled as meaningful business workflow steps.
- **Questions**: retrieve information from the system under test and the test execution environment.

## Serenity/JS specifics
- `actorCalled('Wendy')` creates an actor or returns the one already created under that name in the scenario; actors are identified by name.
- The test runner adapters (Playwright Test, Cucumber.js, Mocha, Jasmine) dismiss actors created in a scenario when it finishes to avoid state leaking between scenarios.
- The handbook's example uses two actors: one sets up data through the REST API, another uses the web UI.

## Serenity BDD (Java) specifics
- Actors are defined with `Actor.named("Toby")`, then given abilities, e.g. `.whoCan(BrowseTheWeb.with(driver))` with a `@Managed` WebDriver; the `@CastMember` annotation can create an actor with a managed browser, naming it from the variable or a `name` attribute.
- Actors perform with `attemptsTo(...)` and are queried with `asksFor(...)`.
- JUnit 5 is the recommended runner via `SerenityJUnit5Extension`; JUnit 4 support is deprecated as of Serenity 5.0.0 and slated for removal in 6.0.0.
- In Cucumber, actors are referred to by name in scenarios, so they are set up in step definitions.

## Trade-off (practitioner judgement, not from the pages)
Screenplay adds vocabulary and indirection, so a small suite may be simpler with page objects or fixtures.

## Verify
Tests read as business steps, tasks are reused, and locator or interface changes are contained in interactions and abilities.

## Checked
2026-11-08. Confirmed against the Serenity/JS Screenplay handbook page (partly; the Abilities, Interactions, Tasks and Questions sections after the first part were not read in full) and the Serenity BDD fundamentals page (setup, actors, abilities, JUnit 4 deprecation). Removed: the TypeScript example (`Task.where`, `PageElement`, `Ensure.that`), `CallAnApi` and `Send.a(GetRequest...)` names, Java `Performable`/`Question<T>`/`seeThat` details, the claim that Screenplay scales better than page objects, and the gotchas about one-click tasks and side-effect-free questions.
Method: documentation only; no commands were run.
