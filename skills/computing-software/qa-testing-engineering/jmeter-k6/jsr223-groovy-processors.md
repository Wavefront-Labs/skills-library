---
id: computing-software.qa-testing-engineering.jmeter-k6.jsr223-groovy-processors
name: jsr223-groovy-processors
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, jsr223, groovy-scripting, pre-processor, post-processor, jmeter-test-plan, vars-props]
level: practitioner
status: docs-checked
description: "Script JMeter with JSR223 Groovy pre/post-processors: vars, props, prev and sampler objects, compilation caching, and replacing BeanShell for performance."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#JSR223_PreProcessor
  - https://jmeter.apache.org/usermanual/component_reference.html#JSR223_PostProcessor
  - https://jmeter.apache.org/usermanual/best-practices.html#bsh_scripting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSR223 Groovy pre- and post-processors

**Goal:** custom logic (signing requests, building payloads, parsing responses) without slowing the test.

## Objects available
`vars` (thread variables: `vars.get/put`), `props` (JMeter properties, a `java.util.Properties`), `prev` (previous SampleResult, in post-processors and assertions), `sampler` (current sampler), `ctx` (JMeterContext), `log`, `Label`, `Parameters` (string), `args` (parameters split on whitespace), `OUT` (System.out).

## Pre-processor example (HMAC signature header)
```groovy
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec
def body = sampler.getArguments().getArgument(0).getValue()
def ts = String.valueOf(System.currentTimeMillis())
def mac = Mac.getInstance("HmacSHA256")
mac.init(new SecretKeySpec(props.get("apiSecret").bytes, "HmacSHA256"))
vars.put("ts", ts)
vars.put("sig", mac.doFinal((ts + body).bytes).encodeHex().toString())
```
Use `${ts}` and `${sig}` in an HTTP Header Manager.

## Post-processor example
```groovy
def json = new groovy.json.JsonSlurper().parseText(prev.getResponseDataAsString())
vars.put("orderIds", json.orders*.id.join(","))
if (json.orders.isEmpty()) prev.setSuccessful(false)
```

## Performance rules
- Language **groovy**, "Cache compiled script if available" checked (advised). If you leave it unchecked with Groovy, set the JVM property `-Dgroovy.use.classvalue=true`.
- Do **not** use `${var}` inside the script body (a changing value changes the script, so it cannot be cached); use `vars.get("var")` or pass via Parameters.
- Script files (`Script file` field) are also compiled when the engine supports it; a relative path is relative to the `user.dir` system property.
- Prefer an engine implementing `Compilable`: Groovy does; the manual says to avoid BeanShell and JavaScript for intensive load testing.

## Gotchas
- Check `jmeter.log` for script errors after runs.
- `props` are JMeter-wide, shared by all threads: use for read-mostly config, not per-user state.

## Verify
Watch injector CPU on a trial run; script-heavy samplers should not dominate it. jmeter.log shows no script errors.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01; latest release 5.6.3). Confirmed: JSR223 variable list (log, Label, Parameters, args, ctx, vars, props, sampler, prev, OUT), compilation caching setting and the `groovy.use.classvalue` note, `${var}` caching caveat, Script file relative path rule, Compilable engines in best practices. The method calls in the example (`sampler.getArguments()`, `Arguments.getArgument(int)`, `Argument.getValue()`, `SampleResult.getResponseDataAsString()`, `setSuccessful(boolean)`) were confirmed to exist in the JMeter source; the example itself was not run.

Method: documentation only; no commands were run.
