---
id: computing-software.web-development.phoenix.security-injection
name: security-injection
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, security, rce, sqlinjection, ssrf, ecto, binary-to-term, injection]
level: advanced
status: docs-checked
description: "Avoid RCE, SQL injection and SSRF in Phoenix apps: unsafe functions, binary_to_term, Ecto fragment and raw SQL parameters, and user-controlled URLs."
sources:
  - https://hexdocs.pm/phoenix/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: recognise and avoid server-side injection bugs in Phoenix code.

## Remote code execution (RCE)
Never pass untrusted input to: `Code.eval_string/3`, `Code.eval_file/2`, `Code.eval_quoted/3`, EEx `eval_string/3` and `eval_file/3`, `:os.cmd/2`, `System.cmd/3`, `System.shell/2`.

The less obvious case is `binary_to_term`. The `:safe` option only stops new atoms being created; it does not stop executable terms from malicious input.
```elixir
# Not safe
:erlang.binary_to_term(user_input, [:safe])

# Safe
Plug.Crypto.non_executable_binary_to_term(user_input, [:safe])
```
(The guide cites CVE-2020-15150 in the Paginator library as a real case.)

## SQL injection
Ecto query syntax is safe by default; pin values with `^`:
```elixir
from(f in Fruit, where: f.quantity >= ^min_q and f.secret == false)
```
- `fragment("... #{min_q} ...")` with string interpolation fails to compile with an `Ecto.Query.CompileError` (fragment does not allow interpolated strings as first argument).
- Safe: pass values as fragment arguments, `fragment("f0.quantity >= ? AND f0.secret = FALSE", ^min_q)` (the guide first does `String.to_integer(min_q)`).
- Safe raw SQL: parameterise, `Ecto.Adapters.SQL.query(Repo, q, [String.to_integer(min_q)])` with `WHERE f.quantity > $1`.
- Vulnerable: building the SQL string with `#{min_q}` and calling `Ecto.Adapters.SQL.query(Repo, q)`.

Rule: when writing raw SQL, never interpolate; use parameters.

## Server Side Request Forgery (SSRF)
SSRF needs both: (1) user input is used to build outbound request URLs, and (2) an attacker can reach some vulnerable server on your network. Cloud metadata services (AWS: `169.254.169.254`) can return account credentials; internal databases, Redis, Elasticsearch or micro-services may also be reachable via your server. AWS added IMDSv2 session authentication in 2019.

A base URL is not a security barrier:
```elixir
req = Req.new(base_url: "https://elixir-lang.org/")
user_input = "https://dashbit.co/blog"
Req.get!(req, url: user_input)   # requests dashbit.co, not elixir-lang.org
```
Tesla behaves the same: with `plug Tesla.Middleware.BaseUrl, "https://example.com/foo"`, `MyClient.get("http://example.com/bar")` requests `http://example.com/bar`. Avoid sending requests built from user input where possible.

Related: computing-software.web-development.phoenix.security-web

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/security.md, main branch, read in full), the published form of the cited hexdocs page: unsafe RCE functions, binary_to_term advice, Ecto fragment and raw SQL examples and the SSRF conditions and Req/Tesla base URL behaviour. Removed: nothing.

Method: documentation only; no commands were run.
