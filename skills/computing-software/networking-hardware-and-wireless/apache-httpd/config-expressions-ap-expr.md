---
id: computing-software.networking-hardware-and-wireless.apache-httpd.config-expressions-ap-expr
name: config-expressions-ap-expr
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, expressions, ap-expr, if, require-expr, variables, functions]
level: advanced
status: docs-checked
description: "Write ap_expr expressions for If, Require expr, Header expr=, CustomLog expr= and SetEnvIfExpr: operators, variables, functions and evaluation-timing caveats."
sources:
  - https://httpd.apache.org/docs/2.4/expr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ap_expr expressions
## Where used
`<If>`/`<ElseIf>`/`<Else>`, `Require expr`, `Header ... "expr=..."`, `CustomLog ... "expr=..."`, `RewriteCond`, `SetEnvIfExpr`, `FilterProvider`, `ErrorDocument`.

## Operators
- String: `==`, `!=`, `<`, `>`, `=~`, `!~`
- Integer: `-eq -ne -lt -le -gt -ge`
- `-ipmatch` (CIDR), `-strmatch`, `-fnmatch`, `-in {'a','b'}`
- Unary: `-f -d -e -s -n -z -R` (remote address in CIDR)
- Logic: `&&`, `||`, `!`
- Regex: `/re/` or `m#re#`, trailing `i` for case-insensitive; `$0`-`$9` hold captures.

## Variables and functions
`%{REQUEST_URI}` (no query string), `%{HTTP_HOST}`, `%{TIME_HOUR}`, `%{HTTP:name}`. Functions: `req`, `resp`, `reqenv`, `env`, `tolower`, `base64`, `md5`, `sha1`. `req` and `http` add the header to Vary; `req_novary` avoids that.

```apache
<If "%{HTTP_HOST} == 'example.com'">
    Redirect permanent "/" "http://www.example.com/"
</If>
Require expr %{TIME_HOUR} -gt 9 && %{TIME_HOUR} -lt 17
CustomLog logs/access-errors.log common "expr=%{REQUEST_STATUS} >= 400"
```

## Caveats
- `%{REMOTE_USER}` is not set during `<If>` because authentication has not run.
- Results depend on the processing phase where the expression is evaluated.
- `SSLRequire` is deprecated; rewrite as `Require expr`.

## Checked

2026-11-08. Operators (string, integer, -ipmatch, -strmatch, -fnmatch, -in, unary tests, -R), regex forms with the i suffix and $0-$9, variables, the req/http/req_novary Vary behaviour, listed functions, the example expressions, the REMOTE_USER and If timing caveat, and SSLRequire deprecation confirmed against the expressions page.

Method: documentation only; no commands were run.
