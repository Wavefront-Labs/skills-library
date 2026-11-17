---
id: computing-software.qa-testing-engineering.test-automation.injection-and-input-validation-testing
name: injection-and-input-validation-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [injection-testing, input-validation-testing, security-testing, sql-injection, xss, owasp-wstg]
level: practitioner
status: draft
description: "Design injection and input validation tests (SQL, NoSQL, command, XSS, path traversal) from OWASP WSTG, with safe payloads, oracles and automated regression checks."
sources:
  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/README
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Injection and input validation test cases

**Goal:** prove untrusted input cannot change queries, commands or markup. Follows OWASP WSTG 4.7 Input Validation Testing. Test only systems you own or are authorised to test.

## Map inputs
Every parameter: query string, body fields, headers (`User-Agent`, `X-Forwarded-For`), cookies, file names, uploaded content, JSON keys, GraphQL variables.

## Probe payloads and oracles
| Class | Probe | Oracle of a defect |
|---|---|---|
| SQL injection | `'`, `' OR '1'='1`, `1 AND SLEEP(5)` | 500/SQL error text, changed result count, 5 s delay |
| NoSQL (Mongo) | `{"$ne": null}` in JSON field | auth bypass or all records returned |
| OS command | `; sleep 5`, `$(id)` | delay, command output in response |
| Reflected/stored XSS | `"><svg onload=alert(1)>` | payload rendered unescaped in DOM |
| Path traversal | `../../../../etc/passwd`, `..%2f` | file contents, different error |
| Template injection | `{{7*7}}`, `${7*7}` | `49` in output |
| Header injection | `%0d%0aSet-Cookie:x=1` | new header in response |

Use time-based probes when errors are suppressed.

## Validation checks
- Server-side validation exists independently of client-side (send requests with curl, bypassing the UI).
- Allow-list validation: length, type, range, format; reject rather than sanitise when possible.
- Output encoding is context-aware (HTML, attribute, JS, URL).

## Automate the regression
```python
@pytest.mark.parametrize("payload", ["'", "' OR '1'='1", '"><svg onload=alert(1)>', "../../etc/passwd"])
def test_search_rejects_or_escapes(api, payload):
    r = api.get("/search", params={"q": payload})
    assert r.status_code in (200, 400)
    assert "SQL" not in r.text and payload not in r.text   # escaped or rejected
```
Tools: sqlmap (authorised targets only), ZAP active scan, Burp Intruder with payload lists.

## Gotchas
- WAFs hide vulnerabilities in test; test the app behind the WAF too.
- Second-order injection: payload stored now, executed later (report export, admin view).

## Verify
Each input has at least one injection probe per relevant class, and fixed vulnerabilities have parametrised regression tests.
