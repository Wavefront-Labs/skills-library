---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-listeners-and-jtl-config
name: jmeter-listeners-and-jtl-config
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-listeners, jtl, results-file-config, simple-data-writer, saveservice]
level: practitioner
status: docs-checked
description: "Configure JMeter results collection: which listeners to use in load runs, JTL CSV vs XML, saveservice properties, response data saving and listener overhead."
sources:
  - https://jmeter.apache.org/usermanual/listeners.html
  - https://jmeter.apache.org/usermanual/best-practices.html
  - https://jmeter.apache.org/usermanual/properties_reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listener overhead and JTL results configuration

## Listener choice
- **Debugging (GUI, 1-5 threads)**: View Results Tree, Debug Sampler, Assertion Results.
- **Load runs (non-GUI)**: no GUI listeners at all; `-l run.jtl` writes results. Optionally a Simple Data Writer for a filtered file (errors only), and Backend Listener for live metrics.
- Disable or delete View Results Tree and View Results in Table before load runs; the manual says to use them only while scripting. For minimal memory use the Simple Data Writer with CSV format.

## JTL format (jmeter.properties / user.properties)
```properties
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.response_data.on_error=false
jmeter.save.saveservice.samplerData=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.url=true
jmeter.save.saveservice.thread_counts=true
jmeter.save.saveservice.timestamp_format=ms
jmeter.save.saveservice.autoflush=false
```
The manual advises CSV rather than XML and saving only the data you need; the dashboard needs CSV.

## Capturing failures
A Simple Data Writer with the "Errors" option selected (write only results with errors) and response data saved in XML, writing to a separate file such as `errors.xml`, keeps failure bodies out of the main JTL.

## Gotchas
- With `-l` set, listeners can all be deleted or disabled (best practices); any left in the plan still process samples.
- `jmeter.save.saveservice.autoflush` is false by default; leave it off unless you need results flushed as they are written.

## Verify
JTL contains the fields the dashboard requires (see the dashboard skill).

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: save-service property names, output_format csv/xml, autoflush default false, Simple Data Writer Errors option, best-practice advice on listeners, CSV and saved data. Removed unconfirmed file-size estimates and file-corruption claim.

Method: documentation only; no commands were run.
