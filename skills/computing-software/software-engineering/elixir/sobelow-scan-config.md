---
id: computing-software.software-engineering.elixir.sobelow-scan-config
name: sobelow-scan-config
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, sobelow, security-scan, mix-sobelow, sobelow-skip, xss, sql-injection, sobelow-config, elixir-security]
level: practitioner
status: draft
description: "Run Sobelow on Phoenix apps in CI, interpret findings and use .sobelow-conf and skips for accepted risks."
sources: ["https://hexdocs.pm/sobelow"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static security scanning with Sobelow

**Goal:** catch common web vulnerabilities early.

```bash
mix sobelow --config                # reads .sobelow-conf
mix sobelow --exit medium --skip    # fail CI on medium+ findings, honour skips
mix sobelow --format json
mix sobelow.gen.config               # create .sobelow-conf
```
```elixir
# .sobelow-conf
[verbose: true, private: true, skip: false, router: "lib/my_app_web/router.ex", exit: "Low", format: "txt", out: "", threshold: "Low", ignore: ["Config.HTTPS"], ignore_files: []]
```

## Rules
- It checks for XSS (`raw/1`), SQL injection (raw queries), command injection, traversal, insecure config (HTTPS, CSP, CSRF), unsafe deserialization.
- A finding is a lead, not a verdict; fix, or fingerprint-skip with a comment.
- Pair with `mix deps.audit` / `mix hex.audit` for dependency advisories (mix_audit).
- Sobelow targets Phoenix; coverage for plain libraries is limited.

## Self-check
Introduce `raw(user_input)` in a template and confirm Sobelow flags XSS.
