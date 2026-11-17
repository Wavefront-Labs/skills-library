---
id: computing-software.web-development.node-express.keeping-secrets-and-pii-out-of-logs
name: keeping-secrets-and-pii-out-of-logs
category: computing-software
field: web-development
product: node-express
tags: [security-logging, log-redaction, pii-in-logs, secrets, gdpr, pino]
level: practitioner
status: verified
description: "Keeping passwords, tokens, keys and personal data out of logs: logger redaction config, safe request logging, error serialisation, and scrubbing APM and error trackers."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude
  - https://getpino.io/#/docs/redaction
  - https://docs.sentry.io/platforms/javascript/data-management/sensitive-data/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping secrets and PII out of logs

## 1. Never log
Passwords (even failed attempts), session IDs, access/refresh tokens, API keys, `Authorization`/`Cookie`/`Set-Cookie` headers, OTP codes, password-reset links, payment card data (PCI DSS), national IDs, health data, encryption keys, connection strings. Minimise emails/names/IPs per your privacy policy.

## 2. Redact at the logger
```js
import pino from "pino";
const logger = pino({
  redact: {
    paths: ["req.headers.authorization", "req.headers.cookie", "res.headers['set-cookie']",
            "password", "token", "*.password", "*.token", "*.accessToken", "*.refreshToken", "*.apiKey", "*.card.number"],
    censor: "[REDACTED]",
  },
});
```
Wildcards cover one level (run on pino 10.4: `user.password` and `user.card.number` were redacted, but `a.b.password` and a top-level `password` were not, hence the bare `"password"`/`"token"` paths above); deeper paths must be listed or use a serializer. winston: custom format; Python `logging.Filter`; structlog processor; Rails `config.filter_parameters += [:password, :token, :secret, :otp, :ssn]`.

## 3. Common leak paths
- Request logging middleware dumping full bodies/headers (`morgan` with custom tokens; `express-winston`'s default `requestWhitelist` is `url, headers, method, httpVersion, originalUrl, query`, so it logs headers and query strings unless you narrow it). Log method, route template, status, latency, request ID - not bodies.
- URLs with tokens in query strings (`?token=`, OAuth `code`, magic links) - in access logs, proxies, analytics and Referer. Put secrets in headers/bodies; strip query from logged URLs where needed.
- Error objects: Axios errors include `config.headers.Authorization` (`JSON.stringify(err.toJSON())` contained the bearer token in a test); DB errors include the failing SQL with values. Serialise errors through a sanitiser.
- `console.log(user)` of whole ORM objects including `passwordHash`.
- Third-party: Sentry/APM breadcrumbs and request capture. Sentry: `sendDefaultPii: false`, `beforeSend` scrubbing, server-side data scrubbing rules; session replay masking (`maskAllText`).

## 4. If a secret was logged
Treat it as compromised: rotate it, then purge/restrict the log data. Logs are often retained and widely readable.

## Verify
Automated test logs in a request with known canary values (`password=CANARY123`, `Authorization: Bearer CANARY`) and asserts they never appear in captured output; periodic grep of log stores for patterns like `eyJ`, `sk_live_`, `AKIA`.
