---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-price-classes-and-flat-rate-plans
name: cloudfront-price-classes-and-flat-rate-plans
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, cloudfront-price-class, flat-rate-pricing, cost-optimization, cdn]
level: practitioner
status: docs-checked
description: "Choose CloudFront price classes to trade edge coverage for cost, and compare pay-as-you-go with CloudFront flat-rate pricing plans."
sources: ["https://aws.amazon.com/cloudfront/pricing/", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFront price classes and flat-rate plans

## 1. Price classes
| Class | Edge locations used |
|---|---|
| `PriceClass_All` | all edge locations |
| `PriceClass_200`, `PriceClass_100` | a subset of edge locations; the mapping to Regions is on the CloudFront pricing page, which this skill does not restate |
API documentation: with a class other than `PriceClass_All`, CloudFront serves from the lowest-latency edge location within your price class, and viewers in or near excluded regions may see slower performance. The price class field is not supported for multi-tenant distributions.
```bash
aws cloudfront get-distribution-config --id E123 > d.json
jq '.DistributionConfig.PriceClass="PriceClass_100" | .DistributionConfig' d.json > cfg.json
aws cloudfront update-distribution --id E123 --if-match $(jq -r .ETag d.json) --distribution-config file://cfg.json
```
Decide from your own viewer location data and the pricing page's class-to-Region mapping.

## 2. Flat-rate plans
The CloudFront pricing page (read 2026-10-27) describes flat-rate plans per distribution (Free, Pro, Business, Premium, plus custom pricing) that combine the CDN with WAF and DDoS protection, Route 53 DNS, a TLS certificate, CloudWatch Logs ingestion, serverless edge compute and monthly S3 storage credits, with no overage charges. Features, allowances and prices differ by tier and change over time, so take them from the pricing page. Distribution quotas for request and transfer rates do not apply to distributions on flat-rate plans. Compare against your pay-as-you-go bill before switching.

## 3. Other cost levers
- Cache hit ratio (cache policies, Origin Shield) cuts origin fetches and origin data transfer.
- Compression (gzip/brotli) reduces bytes billed.

## Verify
- [ ] Cost Explorer CloudFront data transfer by Region drops in the excluded Regions after the change.
- [ ] Latency from key markets (RUM or synthetic canaries) stays within target.

## Checked
2026-10-27. Documentation: Amazon CloudFront API model documentation for DistributionConfig.PriceClass (botocore 2020-05-31), CloudFront pricing page and Developer Guide quotas page, read this date. Confirmed: PriceClass enum values, serving behaviour for non-All classes, flat-rate plan names and bundled features, no-overage statement, quota exemption for flat-rate distributions. Removed region-coverage descriptions of PriceClass_100 and PriceClass_200 and the Security Savings Bundle line as unconfirmed; no prices are stated.
Method: documentation only; no commands were run.
