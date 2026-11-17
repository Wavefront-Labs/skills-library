---
id: computing-software.cloud-infrastructure-engineering.aws.alb-redirects-and-fixed-responses
name: alb-redirects-and-fixed-responses
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, alb, http-to-https-redirect, fixed-response, redirect-action, listener-rules, maintenance-page]
level: practitioner
status: docs-checked
description: "Use ALB redirect and fixed-response actions: HTTP to HTTPS, apex/host and path redirects with placeholders, maintenance pages, blocking paths, and default actions."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-action-types.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-rules.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALB redirect and fixed-response actions

## 1. HTTP to HTTPS (every internet-facing ALB)
```bash
aws elbv2 create-listener --load-balancer-arn <alb> --protocol HTTP --port 80 \
  --default-actions 'Type=redirect,RedirectConfig={Protocol=HTTPS,Port=443,Host="#{host}",Path="/#{path}",Query="#{query}",StatusCode=HTTP_301}'
```
Placeholders `#{protocol}`, `#{host}`, `#{port}`, `#{path}`, `#{query}` keep the original
values; any component you do not set retains its original value, so `Protocol=HTTPS,Port=443,StatusCode=HTTP_301`
is enough. HTTPS to HTTP redirects are not allowed; status codes are `HTTP_301` and `HTTP_302`. Hostname, path and query are each limited to 128 characters. Use `HTTP_301` (permanent, cached by browsers) only once HTTPS is verified;
`HTTP_302` while testing. Add HSTS headers at the app or via CloudFront.

## 2. Host and path redirects as rules
Rules are evaluated in priority order (lowest number first); the default action is last.
```bash
# apex -> www
aws elbv2 create-rule --listener-arn <https-listener> --priority 10 \
  --conditions Field=host-header,Values=example.com \
  --actions 'Type=redirect,RedirectConfig={Host=www.example.com,StatusCode=HTTP_301}'
# old path -> new path, keep the remainder
aws elbv2 create-rule --listener-arn <https-listener> --priority 20 \
  --conditions Field=path-pattern,Values='/docs/*' \
  --actions 'Type=redirect,RedirectConfig={Path="/help/#{path}",StatusCode=HTTP_301}'
```
Note `#{path}` retains the whole original path (use it as `/help/#{path}`, as in the documented `/new/#{path}` example), so the example
produces `/help/docs/a/b`. ALB cannot strip a prefix with placeholders; to rewrite paths, do it in
the app or in CloudFront Functions. A rule that redirects to a path matching itself loops.

## 3. Fixed responses
```bash
aws elbv2 create-rule --listener-arn <https-listener> --priority 5 \
  --conditions Field=path-pattern,Values='/admin*' Field=source-ip,SourceIpConfig={Values=[0.0.0.0/0]} \
  --actions 'Type=fixed-response,FixedResponseConfig={StatusCode=403,ContentType=text/plain,MessageBody="Forbidden"}'
```
- Status code must be 2XX, 4XX or 5XX; the optional message body is up to 1,024 bytes (the API accepts a content type string such as `text/plain`, `text/html` or `application/json`).
- Uses: block internal paths (`/actuator/*`, `/.git/*`), health endpoint for the ALB itself,
  default 404 for unknown hosts (default action fixed-response instead of forwarding to
  some app), `robots.txt`.

## 4. Maintenance page switch
Add a top-priority rule during maintenance and remove it after:
```bash
aws elbv2 create-rule --listener-arn <https-listener> --priority 1 \
  --conditions Field=path-pattern,Values='/*' \
  --actions 'Type=fixed-response,FixedResponseConfig={StatusCode=503,ContentType=text/html,MessageBody="<h1>Back soon</h1>"}'
```
Exclude your own IP with a higher-priority forward rule on `source-ip` so you can test.
The 1 KB body limit means a minimal page; link to a status page on S3/CloudFront.

## 5. Managing rules
- `describe-rules --listener-arn` to see priorities; `set-rule-priorities` to reorder
  atomically.
- Quotas (read 2026-10-27): 100 rules per ALB (adjustable, excluding the default rule), 5 condition values per rule, 6 condition wildcards per rule and 5 match evaluations per rule (not adjustable); plan host/path combinations accordingly.
- Keep rules in IaC; console edits drift.

## Gotchas
- Redirect to a different host requires that host to have a valid certificate wherever
  it is served, or users see TLS errors after the redirect.
- Health checks from Route 53 or monitoring hitting port 80 get a 301; point them at 443.
- Redirect and fixed-response actions are recorded in the access logs and counted by the `HTTP_Redirect_Count` and `HTTP_Fixed_Response_Count` metrics.

## Verify
- [ ] `curl -sI http://app.example.com/x?y=1` returns 301 to `https://app.example.com:443/x?y=1`.
- [ ] Blocked paths return the fixed 403; unknown Host headers get the default 404.
- [ ] Maintenance rule toggles cleanly and your source-IP bypass works.

## Checked

Checked 2026-10-27 against the Elastic Load Balancing documentation for Application Load Balancers (rule action types, listener rules, quotas) and the botocore elbv2 model.
- Corrected: quotas are 100 rules, 5 condition values, 6 wildcards and 5 match evaluations per rule; HTTPS-to-HTTP redirects are not allowed; fixed-response and redirect actions are logged and counted in metrics (the old "target fields" claim was removed); `#{path}` usage follows the documented `/new/#{path}` pattern.
- Confirmed: redirect status codes `HTTP_301`/`HTTP_302`, fixed-response codes 2XX/4XX/5XX with a body up to 1,024 bytes, placeholders `#{protocol}`, `#{host}`, `#{port}`, `#{path}`, `#{query}`, 128-character limits for host, path and query.

Method: documentation only; no commands were run.
