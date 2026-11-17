---
id: computing-software.cloud-infrastructure-engineering.external-dns.aws-govcloud-caveats
name: aws-govcloud-caveats
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aws-govcloud, aws-prefer-cname, govcloud-region, cross-account-credentials]
level: sme
status: docs-checked
description: "Run ExternalDNS against Route53 in AWS GovCloud: AWS_REGION, no alias so use --aws-prefer-cname with txt-prefix, private zones only, and commercial-account keys."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GovCloud caveats

Route53 in GovCloud differs, so adjust the deployment.

1. **Region:** set env `AWS_REGION` to `us-gov-west-1` or `us-gov-east-1`. Otherwise ExternalDNS looks up a region that does not exist in GovCloud and errors.
2. **No aliases:** GovCloud Route53 does not allow aliases. Pass:
```yaml
args:
- --aws-prefer-cname
- --txt-prefix={{ YOUR_PREFIX }}
```
The `txt-prefix` is mandatory here; without one ExternalDNS tries to create a TXT record with the same name as the CNAME, which is not allowed.
3. **Private zones only, no cross-account IAM:** GovCloud Route53 supports only private zones, and there is no cross-account IAM between GovCloud and commercial AWS. To write entries into a public zone in a commercial account, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for a commercial-account key with enough rights (the secret from a Kubernetes Secret).

See the TXT prefix and suffix skill for how prefixes avoid CNAME and TXT clashes.

## Checked

2026-11-04. Read the AWS tutorial (Govcloud caveats). Confirmed AWS_REGION with us-gov-west-1 or us-gov-east-1, no aliases so --aws-prefer-cname with a mandatory --txt-prefix, private zones only, no cross-account IAM, and the commercial-account key and secret workaround. Removed nothing.

Method: documentation only; no commands were run.
