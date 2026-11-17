---
id: computing-software.qa-testing-engineering.selenium.robot-framework-seleniumlibrary
name: robot-framework-seleniumlibrary
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [seleniumlibrary, robot-framework, keyword-driven-ui, browser-library]
level: practitioner
status: docs-checked
description: "Automate browsers from Robot Framework with SeleniumLibrary: keywords, locators, waits, test setup/teardown, screenshots, and when to switch to Browser library (Playwright)."
sources:
  - https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
  - https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
  - https://github.com/robotframework/SeleniumLibrary
  - https://github.com/MarketSquare/robotframework-browser
  - https://github.com/mkorpela/pabot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robot Framework SeleniumLibrary

```bash
pip install robotframework robotframework-seleniumlibrary
```

```robotframework
*** Settings ***
Library           SeleniumLibrary    timeout=10s    implicit_wait=0s    run_on_failure=Capture Page Screenshot
Suite Setup       Open Browser    ${URL}    headlesschrome
Suite Teardown    Close All Browsers
Test Setup        Go To    ${URL}/login

*** Variables ***
${URL}            http://localhost:3000

*** Test Cases ***
Valid Login
    Input Text        id:email       a@b.test
    Input Password    id:password    ${PASSWORD}
    Click Button      css:[data-test=submit]
    Wait Until Page Contains Element    css:[data-test=dashboard]
    Element Text Should Be    css:h1    Dashboard

*** Keywords ***
Log In As
    [Arguments]    ${user}    ${pass}
    Input Text    id:email    ${user}
    Input Password    id:password    ${pass}
    Click Button    css:[data-test=submit]
```

## Locator syntax
`id:`, `name:`, `css:`, `xpath:`, `link:`, `partial link:`, `class:`, `tag:`, `data:test:submit` (data-* attribute), or default strategy (id/name).

## Waiting
`Wait Until Element Is Visible`, `Wait Until Page Contains`, `Wait Until Page Contains Element`, `Wait Until Element Is Enabled`; the default timeout is set with the library `timeout` argument (5 seconds if unset). Prefer waits over `Sleep`.

## Running
```bash
robot --variable URL:https://staging.test --include smoke --outputdir results tests/
pabot --processes 4 tests/          # parallel; pip install -U robotframework-pabot
```
Outputs `output.xml`, `log.html` and `report.html`; `--xunit xunit.xml` writes an xUnit-compatible file for CI.

## SeleniumLibrary vs Browser library
The Browser library (robotframework-browser) is built on Playwright. Choose it or SeleniumLibrary by the browsers, Grid or vendor support you need; SeleniumLibrary stays the Selenium/WebDriver option.

## Gotchas
- `Input Password` does not log the value at the normal log levels, but Robot Framework logs all keyword arguments at TRACE level, so never run with a level below DEBUG when passwords must stay out of logs; `--removekeywords` can strip sensitive keywords from the output.
- Keep business keywords in resource files and review them like code.

## Verify
The `robot` exit code is the number of failed tests (up to 249; 250 means 250 or more); `log.html` shows screenshots on failure.

## Checked

Checked 2026-10-25 against the SeleniumLibrary source (robotframework/SeleniumLibrary, library docstring and keyword modules), the Robot Framework user guide source, the robotframework-browser README and the pabot README. Confirmed: `pip install --upgrade robotframework-seleniumlibrary`; library import arguments `timeout`, `implicit_wait`, `run_on_failure` and the default `Capture Page Screenshot`; the `headlesschrome` browser name; locator prefixes including `data:`; the keyword names used; `Input Password` logging behaviour; `--include`, `--outputdir`, `--xunit`, `--removekeywords`, `pabot --processes`; return code rules. Corrected: the exit code is capped at 250; `Input Password` is logged at TRACE level. Removed: the Browser-versus-SeleniumLibrary performance and shadow DOM comparison, which the Browser README does not state.

Method: documentation only; no commands were run.
