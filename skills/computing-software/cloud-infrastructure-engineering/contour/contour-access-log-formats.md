---
id: computing-software.cloud-infrastructure-engineering.contour.contour-access-log-formats
name: contour-access-log-formats
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [access-logging, accesslog-format, json-fields, accesslog-format-string, envoy-access-log, req-without-query]
level: practitioner
status: docs-checked
description: "Envoy access logging via Contour: default stdout destination, text format string, JSON fields and key=operator pairs, unsupported operators, REQ_WITHOUT_QUERY."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/access-logging.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour access log formats

Envoy writes HTTP and HTTPS access logs to `/dev/stdout` by default. Change destinations with `contour serve --envoy-http-access-log` and `--envoy-https-access-log`.

Text format (`accesslog-format: envoy`, the default): customise with `accesslog-format-string` in the config file; it must end in a linefeed `\n` and use Envoy command operators, e.g. `[%START_TIME%] "%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%" %RESPONSE_CODE% ...\n`.

JSON format: `--accesslog-format=json` or `accesslog-format: json`. Without `json-fields` a default set is used. Customise:

```yaml
accesslog-format: json
json-fields:
  - "@timestamp"
  - "method"
  - "response_code"
  - "customer_id=%REQ(X-CUSTOMER-ID)%"
```

- Plain names must be built-in jsonFields (case-sensitive) or simple Envoy operators (case-insensitive); unknown names fail validation.
- `fieldName=%OPERATOR(...)%` pairs support complex operators and custom names; unknown operators fail validation.
- `DYNAMIC_METADATA` and `FILTER_STATE` operators are not supported.
- Empty fields are omitted from JSON logs automatically.

Formatter extensions supported: `REQ_WITHOUT_QUERY` (like REQ but strips the query string, avoiding logging sensitive data) and `METADATA`.

Verbosity is controlled separately by `accesslog-level` (info, error, critical, disabled). After editing the config and restarting Contour, the new format takes effect shortly.

## Checked

2026-11-04. Confirmed against the Contour access logging page (config/access-logging.md) and the configuration reference (accesslog-level): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
