---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-assertions
name: jmeter-assertions
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, jmeter-assertions, response-assertion, json-assertion, duration-assertion, jmeter-test-plan, functional-checks]
level: practitioner
status: docs-checked
description: "Validate responses in JMeter: Response, JSON/JSONPath, Duration, Size and JSR223 assertions, scoping, cost under load, and making errors visible in results."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#assertions
  - https://jmeter.apache.org/usermanual/test_plan.html#assertions
  - https://jmeter.apache.org/usermanual/best-practices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter assertions

**Goal:** a 200 OK with an error page counts as a failure, without making the injector the bottleneck.

## Types
- **Response Assertion**: field to test (Text Response, Request data, Response Code, Response Message, Response Headers, Request Headers, URL sampled, Document (text)), rule (Contains, Matches, Equals, Substring, optionally Not), patterns. Contains and Matches use Perl5-style regular expressions; Equals and Substring are plain, case-sensitive text. E.g. response code equals 200 and text contains `"orderId"`. "Ignore status" forces the sample to successful before the assertion runs, which is how negative tests expect 4xx/5xx.
- **JSON Assertion**: JSONPath `$.status` (Jayway JsonPath), optional expected value (or regex, or null), or just "path exists". With an indefinite path you must also assert a value; since 5.5 an empty result with no expected value fails.
- **Duration Assertion**: fail any response slower than N ms (marks SLA breaches as errors; use carefully, it mixes performance and functional failures).
- **Size Assertion**: response size equal to, greater than, less than or not equal to N bytes (catch truncated pages; an empty response counts as 0 bytes, not as an error).
- **JSR223 Assertion** (Groovy) for complex logic:
  ```groovy
  def json = new groovy.json.JsonSlurper().parseText(prev.getResponseDataAsString())
  if (json.items.size() == 0) { AssertionResult.setFailure(true); AssertionResult.setFailureMessage("empty cart") }
  ```
- Also available: XML, XML Schema, XPath, XPath2, HTML, MD5Hex, JSON JMESPath and Compare (debugging only) assertions.

## Scope
Assertions apply to all samplers at their level and below; place them as children of the specific sampler to avoid applying to everything.

## Load-friendly
- Prefer Substring or Equals (plain text) over regex rules; prefer the JSON Assertion over regex on JSON.
- Avoid assertions on every sampler of huge responses; assert key ones.
- Do not use the Compare Assertion in a load test (the manual says it consumes a lot of memory and CPU); use JSR223 with Groovy rather than BeanShell, as the manual recommends.

## Gotchas
- Failed assertions count towards the error percentage in the aggregate and summary reports; the HTML dashboard has a Top 5 Errors by Sampler table.
- Duration Assertion failures inflate error rate; separate SLA evaluation from correctness if reports are consumed by others.

## Verify
Point a sampler at an endpoint returning an error page with 200: the assertion marks it failed.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: Response Assertion fields and rule types, Ignore status, JSON Assertion behaviour, Duration and Size assertions, the JSR223 `AssertionResult` variable, Compare Assertion load warning, scoping note, Top 5 Errors by Sampler.

Method: documentation only; no commands were run.
