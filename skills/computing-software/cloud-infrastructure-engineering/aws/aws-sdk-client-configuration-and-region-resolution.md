---
id: computing-software.cloud-infrastructure-engineering.aws.aws-sdk-client-configuration-and-region-resolution
name: aws-sdk-client-configuration-and-region-resolution
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-sdk, sdk-client-config, region-resolution, boto3, connection-pool, endpoint-configuration, sdk-timeouts]
level: practitioner
status: docs-checked
description: "Configure AWS SDK clients correctly: region and credential resolution order, timeouts, retry modes, connection pool sizes, client reuse in Lambda, and endpoint overrides."
sources: ["https://docs.aws.amazon.com/sdkref/latest/guide/feature-region.html", "https://github.com/boto/botocore/blob/develop/botocore/config.py", "https://github.com/boto/botocore/blob/develop/botocore/endpoint.py", "https://github.com/aws/aws-cli/blob/v2/awscli/botocore/configprovider.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS SDK client configuration and region resolution

## Region resolution
- A region given for a client in code (`region_name=` / `region:`) takes precedence over any global setting.
- Otherwise the global `region` setting applies: the `region` key in the shared `config` file, the `AWS_REGION` environment variable (and the `aws.region` JVM property for Java and Kotlin). There is no default; you must supply a region.
- Environment variable names differ by tool: AWS CLI v2 uses `AWS_REGION` before `AWS_DEFAULT_REGION`; AWS CLI v1 and boto3 use `AWS_DEFAULT_REGION`. Check your SDK's reference.
- `aws-global` is a valid value for services with a separate global endpoint, such as STS and S3.
Set the region explicitly in libraries; do not rely on profile defaults in servers.

## Python (boto3)
```python
from botocore.config import Config
cfg = Config(region_name="eu-west-1",
             retries={"mode": "standard", "max_attempts": 5},   # or "adaptive" for client-side rate limiting
             connect_timeout=2, read_timeout=10,
             max_pool_connections=50,                            # botocore default is 10
             tcp_keepalive=True)
s3 = boto3.client("s3", config=cfg)    # create once (module scope in Lambda), reuse
```
- `retries` takes `mode` (`legacy`, `standard`, `adaptive`) and `max_attempts` (botocore: the number of retries after the first request; the AWS CLI's `max_attempts` setting counts total attempts including the first). `adaptive` adds client-side throttling.
- Create clients once and reuse them rather than per request.
## Other SDKs
JavaScript, Java, Go and the other SDKs configure timeouts, connection limits and retries through their own client and HTTP-handler options; use each SDK's developer guide for the option names.

## Shared settings (all SDKs, config file or env)
```ini
[profile app]
region = eu-west-1
retry_mode = standard
max_attempts = 5
```
Environment equivalents: `AWS_REGION`, `AWS_RETRY_MODE`, `AWS_MAX_ATTEMPTS`.
Endpoint overrides (botocore lookup order): a service-specific environment variable (for example `AWS_ENDPOINT_URL_DYNAMODB`), the global `AWS_ENDPOINT_URL`, a service-specific parameter in a `services` section of the shared config file, then the global parameter in a `services` section.

## Gotchas
- botocore's default `connect_timeout` and `read_timeout` are both 60 s; in request paths set shorter timeouts plus retries.
- Retries multiply under fan-out; budget total time against your caller's timeout.
- The credential provider chain decides which identity you are (its order varies by SDK); log `sts get-caller-identity` at startup when debugging.

## Verify
- [ ] Clients created once; timeouts and retry mode set explicitly in config.
- [ ] Load test shows no connection-pool warnings and no throttling storms.

## Checked
Date: 2026-10-24. Sources: AWS SDKs and Tools Reference Guide region page, botocore develop branch (config.py, endpoint.py), aws-cli v2 branch endpoint-URL provider.
Confirmed: per-client region precedence, region config key and AWS_REGION, AWS CLI v2 AWS_REGION before AWS_DEFAULT_REGION and boto3/CLI v1 AWS_DEFAULT_REGION, aws-global value, botocore Config options (retries mode and max_attempts, connect_timeout and read_timeout default 60 s, max_pool_connections default 10, tcp_keepalive), endpoint override lookup order including AWS_ENDPOINT_URL and services sections.
Corrected: a fixed region order with IMDS fallback was replaced by the documented behaviour; the documented boto3 variable is AWS_DEFAULT_REGION.
Removed as unconfirmed: JavaScript and Java client option snippets, sts_regional_endpoints/FIPS/dualstack settings, thread-safety claims, pool-full warning text, API Gateway 29 s figure.
Method: documentation only; no commands were run.
