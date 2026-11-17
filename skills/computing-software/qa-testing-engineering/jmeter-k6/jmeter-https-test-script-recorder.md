---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-https-test-script-recorder
name: jmeter-https-test-script-recorder
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, jmeter-recorder, http-recording, test-script-recorder, jmeter-test-plan, har-import, correlation]
level: practitioner
status: docs-checked
description: "Record browser traffic with JMeter's HTTP(S) Test Script Recorder: proxy and certificate setup, URL filters, grouping into transactions, and cleaning the result."
sources:
  - https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step.html
  - https://jmeter.apache.org/usermanual/component_reference.html#HTTP(S)_Test_Script_Recorder
  - https://jmeter.apache.org/usermanual/best-practices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter HTTP(S) Test Script Recorder

**Goal:** a starting script from real browser traffic, then cleaned into a maintainable test.

## Setup
1. Templates > **Recording** (creates Thread Group, Recording Controller, HTTP Request Defaults, Cookie Manager, recorder).
2. Set the recorder port (the tutorial uses 8888) and press Start: JMeter generates `ApacheJMeterTemporaryRootCA.crt` in `JMETER_HOME/bin` (generation needs `keytool` from a JDK and can take a while).
3. Install that CA in the browser, and set the browser's manual proxy to `localhost` and the recorder port for all protocols. Install it only if the certificate is yours; a browser prompting to accept the certificate should accept it only temporarily.
4. **URL patterns**: use Include patterns (for example `.*\.jsp`) or Exclude patterns (for example `.*\.gif`) to filter out requests you do not need, such as images, stylesheets and third-party domains; test the patterns, then erase and re-record.
5. Grouping: "Put each group in a new transaction controller" so requests from one click become a transaction; leave the required gap between clicks.

## After recording: clean up
- Rename transactions to business names.
- Move common host/protocol to HTTP Request Defaults.
- **Correlate** dynamic values (session ids, CSRF tokens, ids) with extractors; recorded literal values will fail on replay (`correlation-and-data-driven-load-tests`).
- Parameterise users/data with CSV Data Set Config.
- Replace any recorded pauses with designed timers.
- Remove noise requests (telemetry, polling) unless they are part of the load.

## Gotchas
- Generated certificates are valid for 7 days by default (`proxy.cert.validity`); to force regeneration delete `proxyserver.jks` from the JMeter directory, then reinstall the new CA.
- Browsers only prompt for the main URL's certificate; browse manually to other secured domains (CDNs) to accept it for them.

## Verify
The cleaned script replays for 2 different users from CSV with all assertions passing.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: Recording template, ApacheJMeterTemporaryRootCA.crt location, tutorial port 8888, keytool requirement, `proxy.cert.validity` default 7, regenerating by deleting proxyserver.jks, include/exclude pattern guidance, grouping options. Removed unconfirmed suggested-excludes button, HAR converters and protocol limitations.

Method: documentation only; no commands were run.
