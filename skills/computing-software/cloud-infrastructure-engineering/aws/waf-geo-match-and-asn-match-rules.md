---
id: computing-software.cloud-infrastructure-engineering.aws.waf-geo-match-and-asn-match-rules
name: waf-geo-match-and-asn-match-rules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, waf, geo-match, asn-match, geo-blocking, waf-labels, country-restriction]
level: practitioner
status: docs-checked
description: "Manage traffic by country, region and network with AWS WAF geo match and ASN match statements, geo labels, forwarded IP settings and the CloudFront geo restriction caveat."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-geo-match.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-asn-match.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-labels.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF geo match and ASN match

## 1. Geo match statement
- Country: a geo match rule alone matches `CountryCodes`, two-character ISO 3166 alpha-2 codes such as `["US","CN"]`.
  The page notes that Hong Kong is filtered with `HK`.
- Region: a geo match rule cannot match region codes alone. Use a geo match rule (usually with Count) followed by a label match rule.
- Location comes from the request IP using MaxMind GeoIP databases. The page says MaxMind reports very high accuracy at
  country level, varying by country and IP type, and links a correction request form.
- Settings: 1 WCU, nestable. Optional forwarded IP configuration (header such as `X-Forwarded-For`; WAF uses the first IP in
  the header) with a fallback behavior of match or no match for a malformed IP.
- Console: rule builder Request option "Originates from a country in". API: `GeoMatchStatement`.

Block countries but let certain IPs through (page pseudocode): AND of the geo match and a NOT of an IP set match, with a
Block action.

## 2. Geo labels
The geo match statement adds country and region labels to every request it inspects, whether or not it matches:
- origin IP: `awswaf:clientip:geo:country:<ISO country code>` and `awswaf:clientip:geo:region:<country>-<region>` (for
  example `awswaf:clientip:geo:region:US-OR`)
- forwarded IP: the same with `awswaf:forwardedip:` in place of `awswaf:clientip:`
- if a code is unavailable the label uses `XX`, for example `awswaf:clientip:geo:country:XX`.

WAF adds labels at the end of a rule's evaluation, so label matching on them must be in a separate, later rule. Page example
(rule 1 Count, rule 2 Block US except Oregon and Washington, using forwarded IP labels):
```json
{"Name": "geoMatchForLabels", "Priority": 10,
 "Statement": {"GeoMatchStatement": {"CountryCodes": ["US"],
   "ForwardedIPConfig": {"HeaderName": "X-Forwarded-For", "FallbackBehavior": "MATCH"}}},
 "Action": {"Count": {}},
 "VisibilityConfig": {"SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "geoMatchForLabels"}}
```
The second rule is an `AndStatement` of a `LabelMatchStatement` (`Scope` `LABEL`, `Key` `awswaf:forwardedip:geo:country:US`)
and a `NotStatement` over an `OrStatement` of the `US-OR` and `US-WA` region labels, with a Block action.
The page also shows rate-based rules with a `ScopeDownStatement` on geo labels to give Oregon a higher limit than the rest
of the US.

## 3. CloudFront geo restriction
The page says the CloudFront geo restriction does not forward blocked requests to WAF (allowed ones are forwarded). To block
on geography combined with other criteria, use the WAF geo match statement and not the CloudFront feature.

## 4. ASN match statement
- Matches the request IP's Autonomous System Number against `AsnList`: values 0 to 4294967295, up to 100 per rule.
- If WAF cannot determine an ASN for a valid IP it assigns ASN 0, which you can include in the list.
- Optional forwarded IP configuration: use the first, last or any address in the header, plus a fallback of match or no match
  for malformed or missing IPs.
- 1 WCU, nestable. Console: "Originates from ASN in". API: `AsnMatchStatement`.
- The page says ASN matching supplements, and does not replace, authentication and authorization.

## 5. Labels in general
A label is metadata a matching rule adds; it stays on the request until the web ACL evaluation ends and can be matched
by later rules. Labels generate CloudWatch label metrics. A common pattern is to set earlier rules to Count with labels, then
decide in a later rule. Dynamic label interpolation (`${namespace:}`) can place label values in custom request headers
and custom response headers or bodies.

## Verify
- [ ] The geo rule is at a lower priority number than the rules that match its labels.
- [ ] Sampled requests or label metrics show the expected geo labels.

## Checked
Date: 2026-11-07. Read in full: the geographic match statement page including both JSON examples, the ASN match page,
and the "Web request labeling" page. Not opened: Label match statement, Using forwarded IP addresses, Dynamic label
interpolation, and Label metrics pages.
Removed because no page read states them: ASN labels (`awswaf:clientip:asn:`), per-ASN rate-limit keys, example ASNs
16509 and 14618 and the embargo country list, "put the NotStatement after the partner allow list", ISO 3166-2 matching in
`CountryCodes`, `InsertHeaders` and `CloudFront-Viewer-Country` advice, the managed anonymous-IP rule pairing, the Logs
Insights query and `httpRequest.country` log field, the claim that status 451 is not selectable, and VPN/mobile accuracy
statements. The ASN page's example JSON puts `ForwardedIPConfig` as a sibling of `AsnMatchStatement`; treat the page's
settings text as authoritative and check the API reference for placement.
Method: documentation only; no commands were run.
