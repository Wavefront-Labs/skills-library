---
id: computing-software.cybersecurity-defensive.application-security.log-injection-prevention
name: log-injection-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [log-injection, log-forging, crlf-injection, structured-logging, log4shell, cwe-117]
level: practitioner
status: docs-checked
description: "Prevent log injection and forging: encode untrusted data for the log format, prefer structured logs, keep logger lookups away from user input, protect log viewers."
sources: ["https://owasp.org/www-community/attacks/Log_Injection", "https://cwe.mitre.org/data/definitions/117.html", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "https://logging.apache.org/log4j/2.x/security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log injection prevention

Untrusted data written to logs can forge entries, corrupt log files, or attack whatever later reads them.

## Attack forms (OWASP Log Injection)
1. **Forging**: input containing newline characters creates bogus log events (CWE-117). It can also corrupt
   the file format, skew statistics, or cover tracks.
2. **XSS** aimed at a vulnerable web application that displays the logs.
3. **Command execution** through parsers that execute content, for example PHP code in a web-accessible
   log file.
4. **Logger lookups**: Log4j 2 JNDI lookups were exploitable for code execution (CVE-2021-44228); the
   Log4j security page also says any lookup placed in thread-context values can expose private details.

## Defences
- OWASP Logging Cheat Sheet: encode data correctly for the output (logged) format; validate event data from
  other trust zones before logging, and omit or safely replace a malformed field while still recording the
  event and the validation failure.
- Avoid unstructured text formats: CR/LF characters can inject entries (CWE-93). Use a structured encoder that
  escapes values. Parameterised logging alone does not prevent CR/LF injection; keep message templates
  constant with Log4j and SLF4J.
- Do not expose logs at web-accessible locations; if you must, restrict access and serve plain text, not HTML.
- Log4j: do not put user-controlled values (such as HTTP headers in the context map) into configuration
  lookups; replace Context Lookups in PatternLayout with Thread Context Map patterns (`%X`, `%mdc`, `%MDC`).
  Keep Log4j patched per the security page.
- Escape any rejected input you retain before logging it.

## Verify
A test value containing a newline sequence and markup produces a single, escaped event and renders inertly in
the log viewer.

## Checked
2026-11-01. Confirmed against OWASP Log Injection, OWASP Logging Cheat Sheet, and the Apache Logging
security page (CVE-2021-44228 entry, context lookup mitigation, `%X`/`%mdc`/`%MDC`). Removed: the Logstash,
structlog and slog examples, the `%enc{%m}{CRLF}` converter, the fixed-version claim for 2.17.1 (read the
security page for current fixed versions), and the sample payloads.
Method: documentation only; no commands were run.
