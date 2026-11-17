---
id: computing-software.qa-testing-engineering.test-automation.keyword-driven-testing-robot-framework
name: keyword-driven-testing-robot-framework
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [keyword-driven-testing, robot-framework, test-automation-strategy, keywords, browser-library, requests-library]
level: practitioner
status: verified
description: "Use keyword-driven testing with Robot Framework: test cases from reusable keywords, resource files, libraries (Browser, Requests), variables and tags."
sources:
  - https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
  - https://robotframework-browser.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword-driven testing with Robot Framework

**Goal:** tests written as readable keywords that domain experts can review, implemented once by automation engineers.

## Test file
```robot
*** Settings ***
Library     Browser
Resource    resources/checkout.resource
Suite Setup    New Browser    chromium    headless=True
Test Tags    checkout

*** Variables ***
${BASE_URL}    https://staging.example.com

*** Test Cases ***
Gold Customer Gets Ten Percent Discount
    [Tags]    smoke    SHOP-123
    Log In As    gold_user
    Add Product To Basket    Coffee    quantity=4
    Basket Total Should Be    90.00
```
```robot
# resources/checkout.resource
*** Keywords ***
Log In As
    [Arguments]    ${user}
    New Page    ${BASE_URL}/login
    Fill Text    id=email    ${USERS}[${user}][email]
    Fill Secret    id=password    $PASSWORD
    Click    role=button[name="Sign in"]
```

## Running
```bash
pip install robotframework robotframework-browser robotframework-requests robotframework-pabot && rfbrowser init chromium
robot --include smoke --variable BASE_URL:https://qa.example.com --outputdir results tests/
pabot --processes 4 tests/     # parallel
```
Outputs `log.html`, `report.html`, `output.xml` (xunit with `--xunit xunit.xml`). Run on Robot Framework 7.5 and robotframework-browser 20.6.0: the test file and resource above (with a local login page) passed headless on Chromium; `Fill Secret` accepts a `$PASSWORD` local variable (no braces), and the `Secret` type from RF 7.4 as `${var}`, per the library docs; `Test Tags` works; `--include smoke` and `--variable` worked. `rfbrowser init` downloads browsers to the Playwright cache under your user profile unless `PLAYWRIGHT_BROWSERS_PATH` is set.

## Design
- High-level keywords (business) built from low-level keywords (UI/API actions).
- Python libraries for complex logic (`@keyword` decorator) instead of long keyword chains.
- Libraries: Browser (Playwright-based), SeleniumLibrary, RequestsLibrary, DatabaseLibrary, AppiumLibrary.

## Gotchas
- Programming in Robot syntax (loops, complex IFs) gets unreadable; push logic into Python.
- Keyword sprawl: maintain a keyword catalogue (`libdoc`).

## Verify
A non-programmer can read a test case and describe what it checks; `robot --dryrun` shows no missing keywords (a test calling an undefined keyword failed the dry run with "No keyword with name '...' found").
