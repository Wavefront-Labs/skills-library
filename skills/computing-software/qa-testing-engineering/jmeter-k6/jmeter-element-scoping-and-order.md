---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-element-scoping-and-order
name: jmeter-element-scoping-and-order
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-scoping, execution-order, test-plan-structure, jmeter-hierarchy]
level: practitioner
status: docs-checked
description: "Apply JMeter scoping rules and execution order (config, pre-processors, timers, sampler, post-processors, assertions, listeners) so elements hit the right samplers."
sources:
  - https://jmeter.apache.org/usermanual/test_plan.html#executionorder
  - https://jmeter.apache.org/usermanual/test_plan.html#scoping_rules
  - https://jmeter.apache.org/usermanual/component_reference.html#Transaction_Controller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Element scoping and execution order rules

## Execution order for each sampler (User Manual)
0. Configuration elements
1. Pre-Processors
2. Timers
3. Sampler
4. Post-Processors (only if the sample result is not null)
5. Assertions (only if result not null)
6. Listeners (only if result not null)

Within the same type, elements execute in tree order (top to bottom).

## Scoping rules
- Timers, assertions, pre- and post-processors only run if there is a sampler they apply to. They apply to **all samplers at their level and below** in the tree, and a config element in an inner branch takes precedence over the same element in a parent branch.
- A post-processor as a child of one sampler applies only to that sampler.
- A post-processor at Thread Group level runs after *every* sampler in the group: a JSON Extractor there re-extracts (and possibly overwrites) after each request. Usually a bug.
- Logic Controllers and samplers run in tree order; other elements run by scope and type. User Defined Variables are the exception: processed at the start of the test wherever placed.

## Example
```
Thread Group
├── HTTP Header Manager            (all samplers)
├── Uniform Random Timer           (before EVERY sampler: often not intended)
├── Login (HTTP Request)
│   └── JSON Extractor token       (only Login)
└── Transaction Controller "Browse"
    ├── Response Assertion (200)   (all samplers in Browse)
    ├── List products
    └── View product
        └── Constant Timer 2s      (only before View product)
```

## Common mistakes
- Timers inside a Transaction Controller add to the transaction time when "Include duration of timer and pre-post processors in generated sample" is checked.
- Listeners, like other elements, only apply to samplers in their scope.

## Verify
Run with 1 thread and View Results Tree: extracted variables, timers and assertions occur only where intended (Debug Sampler shows variables).

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: execution order list and its null-result condition, scoping rules, precedence of inner config elements, UDV exception, Transaction Controller timer-duration checkbox.

Method: documentation only; no commands were run.
