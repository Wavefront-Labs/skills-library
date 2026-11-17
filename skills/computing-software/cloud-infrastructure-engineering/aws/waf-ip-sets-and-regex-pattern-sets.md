---
id: computing-software.cloud-infrastructure-engineering.aws.waf-ip-sets-and-regex-pattern-sets
name: waf-ip-sets-and-regex-pattern-sets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, waf, ip-set, regex-pattern-set, forwarded-ip-config, lock-token, automated-blocklist]
level: practitioner
status: docs-checked
description: "Manage AWS WAF IP sets and regex pattern sets: create and update with lock tokens, forwarded-IP matching, automated blocklists from logs, and limits."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/waf-ip-set-managing.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-regex-pattern-set-managing.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-ipset-match.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-regex-pattern-set-match.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF IP sets and regex pattern sets

## 1. IP sets
Reusable lists of CIDRs referenced by `IPSetReferenceStatement` in many rules/web ACLs.
```bash
aws wafv2 create-ip-set --name blocked-ips --scope REGIONAL --ip-address-version IPV4 \
  --addresses 198.51.100.0/24 203.0.113.7/32
```
- One IP version per set (create a second set for IPv6). A set holds up to 10,000 addresses or
  ranges; all IPv4 and IPv6 CIDR ranges are supported except /0.
- Regional sets work only with regional resources; CloudFront web ACLs need `--scope CLOUDFRONT`
  (Global in the console).
- The name cannot be changed after creation.
- **Updates replace the whole list** and need the current lock token:
```bash
read ID TOKEN < <(aws wafv2 list-ip-sets --scope REGIONAL \
  --query "IPSets[?Name=='blocked-ips'].[Id,LockToken]" --output text)
aws wafv2 get-ip-set --name blocked-ips --scope REGIONAL --id $ID --query 'IPSet.Addresses'
aws wafv2 update-ip-set --name blocked-ips --scope REGIONAL --id $ID --lock-token $TOKEN \
  --addresses 198.51.100.0/24 203.0.113.7/32 192.0.2.44/32
```
  A stale token returns `WAFOptimisticLockException`: re-read and retry. Automation must
  read-modify-write in a loop, never blind-overwrite.

## 2. Matching on forwarded IPs
Behind a proxy or CDN that is not CloudFront, the source IP is the proxy. Use
`ForwardedIPConfig`:
```json
{"IPSetReferenceStatement": {"ARN": "<ipset-arn>",
  "IPSetForwardedIPConfig": {"HeaderName": "X-Forwarded-For", "FallbackBehavior": "NO_MATCH",
                             "Position": "FIRST"}}}
```
`Position` is FIRST, LAST or ANY; `FallbackBehavior` (MATCH or NO_MATCH) applies when the header
IP is malformed. ANY adds 4 WCUs to the statement. Headers are
client-controllable, so only trust them when the edge in front sets/overwrites them.
CloudFront-fronted ALB: WAF on CloudFront sees the real IP directly; put IP rules there.

## 3. Regex pattern sets
```bash
aws wafv2 create-regex-pattern-set --name bad-ua --scope REGIONAL \
  --regular-expression-list RegexString='(?i)sqlmap' RegexString='(?i)nikto' RegexString='^curl/7\.[0-9]+'
```
Reference with `RegexPatternSetReferenceStatement` on a request component plus **text
transformations** (`LOWERCASE`, `URL_DECODE`, `HTML_ENTITY_DECODE`, `COMPRESS_WHITE_SPACE`)
applied before matching. A set needs at least one pattern; with several, a request matches if
any pattern matches (OR). Each `RegexString` is 1 to 512 characters. Syntax is the PCRE
(libpcre) syntax with some exceptions: read "Supported regular expression syntax in AWS WAF".
Updates use lock tokens like IP sets.

## 4. Automated blocklists
Pattern: WAF logs to S3 or CloudWatch Logs, a scheduled Lambda (or Logs Insights query)
finds abusive IPs (e.g. > N blocked requests or 4xx bursts), and updates an IP set with
expiry tracked in DynamoDB. Prefer rate-based rules for simple
volumetric abuse; use automation for cross-signal decisions.

## 5. Sharing and organisation
- Sets are per account and scope (Region or CloudFront).
- Name sets by purpose (`allow-office`, `block-threatintel`); tag with owner.

## Gotchas
- Deleting a set that a web ACL or rule group references triggers a warning; WAF rarely cannot
  detect a reference, so check web ACLs and rule groups yourself before deleting.

## Verify
- [ ] `get-ip-set` returns the expected list; automation logs show lock-token retries handled.
- [ ] A request from a listed IP (or with a listed forwarded IP, if configured) is blocked and logged with the rule name.
- [ ] Regex set matches a test user agent after the configured transformations.

## Checked
2026-10-28. Confirmed against the WAF Developer Guide pages "Creating and managing an IP set", "Creating and managing a regex pattern set" and "IP set match rule statement" (10,000 addresses, /0 excluded, ANY +4 WCU, OR logic, PCRE) and the wafv2 botocore model (UpdateIPSet requires LockToken, list-ip-sets returns LockToken, WAFOptimisticLockException, ForwardedIPPosition FIRST/LAST/ANY, FallbackBehavior MATCH/NO_MATCH, RegexString 1-512 characters, text transformation names). Corrected the regex length limit (was 200). Removed unconfirmed claims: 10 regexes per set, 10 IPs for ANY, us-east-1 requirement, propagation time, IPv4-mapped behaviour, Firewall Manager sharing, the Security Automations solution, per-field list.
Method: documentation only; no commands were run.
