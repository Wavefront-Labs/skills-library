---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-logic-controllers
name: jmeter-logic-controllers
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, logic-controllers, transaction-controller, jmeter-test-plan, if-controller, throughput-controller, once-only-controller]
level: practitioner
status: docs-checked
description: "Structure JMeter scripts with logic controllers: Transaction (business timings), If, Loop, While, Once Only, Throughput, Switch and Module controllers."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#logic_controllers
  - https://jmeter.apache.org/usermanual/component_reference.html#Transaction_Controller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter logic controllers

**Goal:** model user flows and transaction mix, and report business-level timings.

## Transaction Controller
Groups samplers into one business transaction ("Checkout") with total time. Options:
- "Generate parent sample": report only the transaction (children nested); cleaner reports.
- "Include duration of timer and pre-post processors in generated sample": when checked, timer delays and processors count towards the transaction time; leave it off to exclude think time.

## Flow controllers
- **If Controller**: check "Interpret Condition as Variable Expression" and use `${__jexl3("${status}" == "OK")}` or `${__groovy(vars.get("status") == "OK")}`; the unchecked JavaScript mode has a performance penalty that can be very big. By default the condition is evaluated only on entry.
- **Loop Controller** (fixed count), **While Controller** (runs until the condition evaluates to the string `false`; blank or `LAST` means exit when the last sample fails; the condition is evaluated before and after the children, so avoid non-idempotent functions; add a counter guard to avoid infinite loops), **ForEach Controller** (iterates over `inputVar_1..inputVar_n`, for example variables created by an extractor; runs nothing if `inputVar_1` is null).
- **Once Only Controller**: login once per thread.
- **Runtime Controller**: run children for N seconds.

## Mix controllers
- **Throughput Controller**: "Percent Executions" mode runs the controller for that percentage of iterations (e.g. 70% browse, 20% search, 10% buy); uncheck "per user" to calculate globally rather than per thread. The manual notes it does not control throughput.
- **Switch Controller**: runs the child whose index (from 0) or name equals the switch value; an out-of-range or empty value runs child 0, and a non-matching name runs the child named `default`. Use a variable for the switch value (for example from `__Random`) to pick a flow; ranges are not supported.
- **Interleave Controller**: alternate children per iteration.

## Reuse
- **Test Fragment** + **Module Controller** to call a shared flow (login) from several places.
- **Include Controller** to pull another .jmx fragment.

## Gotchas
- Transaction Controller timing includes child timers if the option is checked: inflated numbers.
- Throughput Controller percentages apply to iterations through the controller, not to global requests per second.

## Verify
The Aggregate Report shows transaction-level rows with counts matching the intended mix percentages.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: If Controller variable-expression mode and JavaScript penalty, While Controller condition rules, ForEach input variable naming and null case, Throughput Controller modes and per-user option, Switch Controller semantics, Runtime Controller (seconds), Transaction Controller timer option. Removed the unconfirmed weighted-switch plugin claim.

Method: documentation only; no commands were run.
