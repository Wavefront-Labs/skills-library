---
id: computing-software.networking-hardware-and-wireless.envoy.access-log-configuration
name: access-log-configuration
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, access-log, response-flags, log-format, json-format, file-access-log, filters]
level: practitioner
status: docs-checked
description: "Configure Envoy access logs (HCM, TCP, listener, start-of-stream), choose default or custom format, and filter what gets logged."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/observability/access_logging.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/observability/access_log/usage.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access log configuration
HTTP connection manager, TCP proxy and Thrift proxy support extensible access logs: multiple logs per stream, filters that route requests to separate logs, and independent downstream connection logging via listener access logs. By default a record is written at the end of each UDP session, TCP connection or HTTP stream; reporting at the start or periodically can be enabled.

```yaml
access_log:
- name: envoy.access_loggers.file
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog
    path: /dev/stdout
    log_format:
      text_format_source:
        inline_string: "[%START_TIME%] \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %UPSTREAM_HOST%\n"
```
The default format string (used when none is given) is `[%START_TIME%] "%REQUEST_HEADER(:METHOD)% %REQUEST_HEADER(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%" %RESPONSE_CODE% %RESPONSE_FLAGS% %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESPONSE_HEADER(X-ENVOY-UPSTREAM-SERVICE-TIME)% "%REQUEST_HEADER(X-FORWARDED-FOR)%" "%REQUEST_HEADER(USER-AGENT)%" "%REQUEST_HEADER(X-REQUEST-ID)%" "%REQUEST_HEADER(:AUTHORITY)%" "%UPSTREAM_HOST%"`.

Gotchas: `%RESPONSE_FLAGS%` and `%RESPONSE_CODE_DETAILS%` explain locally generated errors (no healthy upstream, timeouts) and are the first thing to add; a missing trailing newline in a custom format glues records together. Verify by curling and checking the log line.

## Checked

2026-11-03. Confirmed against: access_log usage.rst (default format string, json formats), access_logging.rst, the file access logger proto and the substitution formatter page (RESPONSE_CODE_DETAILS, DYNAMIC_METADATA). Removed or corrected: nothing.

Method: documentation only; no commands were run.
