---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-functions-variables-properties
name: jmeter-functions-variables-properties
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, jmeter-properties, jmeter-functions, user-defined-variables, jmeter-test-plan, command-line-parameters]
level: practitioner
status: docs-checked
description: "Use JMeter functions, variables and properties correctly: __P for CLI parameters, __Random, __time, __UUID, variable scope per thread, and property sharing across threads."
sources:
  - https://jmeter.apache.org/usermanual/functions.html
  - https://jmeter.apache.org/usermanual/test_plan.html#config_elements
  - https://jmeter.apache.org/usermanual/get-started.html#override
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter functions, variables and properties

**Goal:** parameterised, reusable test plans.

## Variables vs properties
- **Variables** (`${name}`): per thread. Set by User Defined Variables (initial values copied to each thread), extractors, CSV Data Set, `vars.put`.
- **Properties** (`${__P(name,default)}`): global to the JMeter process, set via `-Jname=value` on the command line, `user.properties`, or `props.put`. Use for environment and load settings.

```bash
jmeter -n -t plan.jmx -Jhost=staging.example.com -Jthreads=200 -Jduration=1800 -l results.jtl
```
In the plan: Server Name `${__P(host,localhost)}`, threads `${__P(threads,1)}`.
Remote workers: `-G` sets properties on all remote servers (`-Gthreads=50`).

## Useful functions
| Function | Use |
|---|---|
| `${__Random(1,100)}` | random number between min and max |
| `${__RandomString(8,abcdef123)}` | random string of given length from the given characters |
| `${__UUID()}` | unique ids / idempotency keys |
| `${__time(yyyy-MM-dd'T'HH:mm:ss,)}` | timestamps |
| `${__timeShift(yyyy-MM-dd,,P1D,,)}` | tomorrow's date (shift is a `Duration` such as `P1D` or `PT15M`) |
| `${__threadNum}` | thread number (data partitioning) |
| `${__counter(FALSE)}` | global counter (`TRUE` keeps each user's count separate); several calls in one iteration do not increment further |
| `${__groovy(expr)}` | inline Groovy; use `vars.get("x")` rather than string replacement so the script can be cached |
| `${__urlencode(${q})}` | encode values |
| `${__V(item_${i})}` | nested variable names (`${item_${i}}` does not work) |

## Gotchas
- User Defined Variables are processed at the start of the test regardless of position, in plan order, then copied to each thread; do not expect them to change per iteration.
- A random function in a UDV is evaluated once, so every thread starts with the same value; put it in the sampler or use the Random Variable config element.
- Function helper dialog (Tools > Function Helper Dialog) shows exact syntax.

## Verify
Run the same .jmx with different `-J` values for smoke vs load without editing the file.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: __Random, __RandomString, __counter, __timeShift, __time, __V, __groovy parameters and caching note, Function Helper under the Tools menu, `-G` (property on all servers), `-J` (local property), UDV processing.

Method: documentation only; no commands were run.
