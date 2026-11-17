---
id: computing-software.cloud-infrastructure-engineering.datadog.synthetics-browser-tests
name: synthetics-browser-tests
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, browser-test, synthetics-browser, recorder, multistep]
level: practitioner
status: docs-checked
description: "Record browser tests with the Datadog recorder, add assertions and variables, and run from managed locations."
sources: ["https://docs.datadoghq.com/synthetics/browser_tests/", "https://docs.datadoghq.com/synthetics/browser_tests/test_steps/", "https://docs.datadoghq.com/synthetics/browser_tests/advanced_options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic browser tests
Goal: monitor critical user journeys.

```
# Steps recorded with the Datadog test recorder extension (Start Recording)
1. Navigate to https://shop.example.net/login
2. Type {{ USERNAME }} in the email field
3. Type {{ PASSWORD }} in the password field (variable with "Hide and obfuscate variable value")
4. Click "Sign in"
5. Assert an element is present on the page   (the test must end with an assertion)
```

- Record with the test recorder extension, or add steps manually with Interaction; the extension does not auto-record Hover, Press Key, Scroll and Wait steps, so add those manually.
- Use global variables from Settings in the starting URL, advanced options and recordings (type `{{` to list them). Select "Hide and obfuscate variable value" for credentials.
- Assertions include element content, element attribute, element present, checkbox state, text present or absent, URL content, email received, custom JavaScript (needs a site that accepts external JavaScript), downloaded file (name, size, MD5) and request count.
- Run from managed locations or private locations; frequency ranges from every minute to once a week. The Continuous Testing Tunnel can trigger tests against local or CI environments.
- Alert rule: alert if any assertion fails for X minutes from any n of N locations; you can retry X times before a location is marked failed, with an optional fast retry interval.
- The privacy option Do not capture any screenshots keeps sensitive data out of results, at the cost of harder troubleshooting.
- When the recorder picks the wrong element, set a User Specified Locator (CSS or XPath 1.0).

Gotcha: when capturing HTTP payloads only variables marked secret are redacted, so other sensitive data may be visible to anyone with test access or in exported HAR files. Use test accounts with minimal privileges.

## Verify
- Test results show step results and screenshots (unless disabled); confirm an alert by temporarily breaking an assertion.

## Checked
2026-11-09. Confirmed against the Browser tests overview, Browser test steps and Advanced options pages (recorder extension, assertion types, JavaScript caveat, manual steps list, hide-and-obfuscate variable, global variables, locations, frequency, Continuous Testing Tunnel, alert rule and retries, screenshot privacy option, user specified locator, HAR warning). Removed: the `datadog-ci synthetics run-tests` CLI and exit-code claim (not on the fetched pages), the `data-test-id` selector advice and the `#email` style selectors, the `min_failure_duration` setting name, and the maintenance-cost and cleanup advice.
Method: documentation only; no commands were run.
