---
id: computing-software.cybersecurity-defensive.application-security.api-security-testing
name: api-security-testing
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security-testing, bola-testing, schemathesis, zap-api-scan, owasp-api-top-10]
level: practitioner
status: docs-checked
description: "Test APIs for security defects: map tests to the OWASP API Top 10 2023, run the ZAP API scan and Schemathesis from a spec, and add authorisation tests."
sources: ["https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0x11-t10.md", "https://www.zaproxy.org/docs/docker/api-scan/", "https://schemathesis.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API security testing

Use the OWASP API Security Top 10 2023 as the test plan, and a spec-driven scanner for breadth.

## 1. Inventory
API9:2023 Improper Inventory Management: APIs expose more endpoints than traditional web
applications, so keep documentation up to date, and inventory hosts and deployed API versions to
catch deprecated versions and exposed debug endpoints. Testing starts from that inventory.

## 2. ZAP API scan
- `zap-api-scan.py -t <target> -f <format> [options]`, available in the ZAP Docker images.
  Target is an OpenAPI or SOAP definition (file or URL) or a GraphQL endpoint URL; format is
  `openapi`, `soap` or `graphql` (`--schema` gives the GraphQL schema location).
- It imports the definition, then runs an active scan tuned to APIs (it does not look for XSS).
  Two scripts raise alerts for HTTP server error responses and for content types not usually
  associated with APIs.
- Options include `-r` HTML, `-w` Markdown, `-x` XML and `-J` JSON reports; `-c`/`-u` a rule
  config file; `-g` generates a default config (all rules WARN); `-S` safe mode skips the active
  scan and runs a baseline scan; `-U` and `-n` run authenticated scans from a context file.
- Exit codes: 0 success, 1 at least one FAIL, 2 at least one WARN and no FAIL, 3 other
  failure. By default all alerts are WARN, so set rules to FAIL in a config file if CI must
  break on them.

## 3. Schemathesis
It generates property-based tests from OpenAPI (2.0, 3.0, 3.1, 3.2) and GraphQL schemas, and
from gRPC service descriptors (unary methods). It chains operations into workflows, catches
server errors and schema violations, ships a minimal curl or grpcurl reproducer with every
finding, and runs from a CLI or pytest with CI integrations.

## 4. Test plan from the Top 10
- API1 Broken Object Level Authorization: check every function that uses a user-supplied ID
  to read a data source. Use two users and swap object IDs.
- API2 Broken Authentication: token compromise and implementation flaws.
- API3 Broken Object Property Level Authorization: covers excessive data exposure and mass
  assignment; check responses and writable properties per property.
- API4 Unrestricted Resource Consumption: bandwidth, CPU, memory, storage, and paid per-request
  integrations (email, SMS, phone, biometrics).
- API5 Broken Function Level Authorization: unclear separation of administrative and regular
  functions; call admin functions as a regular user.
- API6 Unrestricted Access to Sensitive Business Flows: flows such as buying a ticket or posting
  a comment, abused through automation; not necessarily an implementation bug.
- API7 SSRF: APIs that fetch a remote resource from an unvalidated user-supplied URI.
- API8 Security Misconfiguration, API10 Unsafe Consumption of APIs (data from third-party APIs
  trusted more than user input).

## Verify
- [ ] Every ID-bearing endpoint has a cross-user test.
- [ ] CI uses ZAP exit codes or a config file to fail on chosen rules.

## Checked
Confirmed 2026-11-09 against the OWASP API Security Top 10 2023 index (raw markdown), the ZAP API scan page (usage, options, exit codes) and the Schemathesis home page.
Removed as unconfirmed: the full docker run command line and image name, ZAP_AUTH_HEADER variables, the schemathesis CLI flags, specific status code expectations, Postman/Newman and Burp Autorize usage, pagination and rate-limit test values, JWT, CORS and verbose error checks, the CI cadence advice, and the WSTG source, which is an unreadable host.
Method: docs-checked 2026-11-09 against OWASP API Security 2023 Top 10 index, zaproxy.org api-scan and schemathesis.readthedocs.io
