---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-endpoint-overrides-and-retry-settings
name: provider-endpoint-overrides-and-retry-settings
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, custom-endpoints, endpoint-override, localstack, api-throttling, retry-mode]
level: practitioner
status: docs-checked
description: "Point providers at custom endpoints (LocalStack, FIPS, Azure environments, proxies) and tune AWS retries: endpoints, max_retries, retry_mode, plus Azure and Google equivalents."
sources: ["https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/custom-service-endpoints", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs#max_retries", "https://docs.localstack.cloud/user-guide/integrations/terraform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider endpoints and retries

## AWS endpoints
```hcl
provider "aws" {
  region = "eu-west-1"
  endpoints {
    s3  = "https://bucket.vpce-0abc-xyz.s3.eu-west-1.vpce.amazonaws.com"
    sts = "https://sts.eu-west-1.amazonaws.com"         # regional STS
  }
}
```
Use cases: FIPS endpoints (`use_fips_endpoint = true`), regional STS, test doubles such as
LocalStack. Endpoints can also be set with `AWS_ENDPOINT_URL` (all services) or
`AWS_ENDPOINT_URL_<SERVICE>` (one service), or with `endpoint_url` in a shared-config profile;
`AWS_IGNORE_CONFIGURED_ENDPOINT_URLS` makes the provider ignore those.

## LocalStack
```hcl
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true      # only with the http://localhost:4566 fallback below
  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    lambda   = "http://localhost:4566"
    iam      = "http://localhost:4566"
    sts      = "http://localhost:4566"
  }
}
```
LocalStack's docs prefer the virtual-hosted S3 endpoint `http://s3.localhost.localstack.cloud:4566`
(no path-style needed) and use `http://localhost:4566` plus `s3_use_path_style = true` only as a
fallback. `lstk terraform` (alias `lstk tf`) writes a temporary override file pointing every
service at LocalStack; it supersedes the deprecated `tflocal` wrapper.

## Retries
```hcl
provider "aws" {
  max_retries = 25            # default 25; delay between retries grows exponentially
  retry_mode  = "adaptive"    # valid values: standard, adaptive
}
```
Env: `AWS_MAX_ATTEMPTS`, `AWS_RETRY_MODE`. See the parallelism-and-provider-api-throttling skill
for `-parallelism`.

## Other providers
- **azurerm**: `environment` (`public`, `usgovernment`, `german`, `china`; also `ARM_ENVIRONMENT`);
  `metadata_host` (`ARM_METADATA_HOSTNAME`) to obtain a custom Azure environment, and
  `environment` must then match a name in that host's list.
- **google**: per-service `<service>_custom_endpoint` arguments (e.g. `compute_custom_endpoint`),
  `request_timeout`, `batching` settings.
- **Proxies (AWS provider)**: `http_proxy`, `https_proxy`, `no_proxy` or the `HTTP_PROXY`,
  `HTTPS_PROXY`, `NO_PROXY` environment variables.

## Gotchas
- An endpoint override applies to every resource of that service in the provider
  configuration; use an aliased provider (`alias`) when only some resources need it.
- Override each service you use (see the service table in the AWS custom endpoints guide for
  names), or use `AWS_ENDPOINT_URL` to set one base endpoint.

## Verify
- [ ] A plan/apply against the overridden endpoints succeeds with the intended credentials only.

## Checked
- 2026-10-28. Confirmed against the AWS provider's "Custom Service Endpoints" guide (`endpoints` block, `AWS_ENDPOINT_URL`, `AWS_ENDPOINT_URL_<SERVICE>`, `endpoint_url`, `AWS_IGNORE_CONFIGURED_ENDPOINT_URLS`, aliased providers), the AWS provider docs (`max_retries` default 25 with exponential delay, `retry_mode` values, `AWS_MAX_ATTEMPTS`, `AWS_RETRY_MODE`, `use_fips_endpoint`, proxy arguments, `s3_use_path_style`), LocalStack's Terraform page (port 4566, `skip_credentials_validation`, `skip_metadata_api_check`, virtual-hosted endpoint, `lstk terraform`, deprecated `tflocal`), the azurerm provider docs (`environment` values, `metadata_host`) and the Google provider reference (`*_custom_endpoint`, `request_timeout`, `batching`).
- Removed: interface VPC endpoint use case, `skip_requesting_account_id` from the LocalStack example, the claims about adaptive mode, SDK HTTP retries in azurerm, all-provider proxy support and public-endpoint fallback (not in the fetched docs).
Method: documentation only; no commands were run.
