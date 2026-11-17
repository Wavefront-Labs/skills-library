---
id: computing-software.cloud-infrastructure-engineering.google-cloud.default-and-required-log-sinks-and-buckets
name: default-and-required-log-sinks-and-buckets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-logging, default-log-sink-config, required-log-bucket, log-router, default-sink-settings, _default]
level: practitioner
status: docs-checked
description: "Configure the _Required and _Default log sinks and buckets: contents, retention, filtering or disabling _Default, and org-wide default log settings."
sources: ["https://cloud.google.com/logging/docs/routing/overview", "https://cloud.google.com/logging/docs/default-settings", "https://cloud.google.com/logging/docs/buckets", "https://cloud.google.com/logging/quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# _Default and _Required log sinks and buckets

Every project, folder, organization and billing account has two system sinks, each with a
correspondingly named bucket:

| Sink -> bucket | Contents | Retention | Editable |
|---|---|---|---|
| `_Required` -> `_Required` | Admin Activity and System Event audit logs | 400 days, not configurable | no: cannot be disabled, deleted or reconfigured |
| `_Default` -> `_Default` | everything not routed to `_Required` | 30 days default (1 to 3650 configurable) | filters, exclusions, disable, destination |

## Common configuration
```bash
gcloud logging sinks describe _Default --project=<P>
gcloud logging sinks update _Default --project=<P> --add-exclusion=name=no-lb-debug,filter='resource.type="http_load_balancer" AND severity<WARNING'
gcloud logging buckets update _Default --location=global --retention-days=90 --project=<P>
gcloud logging sinks update _Default --project=<P> --disabled        # when an aggregated org sink handles everything
```

## Org-wide defaults for new projects
```bash
gcloud logging settings update --organization=<ORG> --storage-location=europe-west2 \
  --disable-default-sink
gcloud logging settings describe --organization=<ORG>
```
`--storage-location` sets where new child resources' `_Default`/`_Required` buckets are created
(data residency); locations of existing buckets are not changed. `--disable-default-sink` stops
new projects routing to `_Default` (use with a central aggregated sink).

## Gotchas
- Disabling `_Default` without another sink means logs are dropped (except `_Required`).
- Set org or folder default settings before projects are created; they do not move existing buckets.
- A CMEK setting in default settings requires a storage location in the same settings (`--kms-key-name`).
- Intercepting aggregated sinks never stop an entry reaching the `_Required` sink of its originating resource.

## Verify
- [ ] A new test project's buckets are in the chosen region and `_Default` exclusions take effect.

## Checked
2026-10-28. Confirmed against the Log routing overview, Default resource settings, Log buckets and Logging quotas pages: sink and bucket names, `_Required` 400 days and not configurable, `_Required` cannot be disabled or deleted, `_Default` can be modified or disabled, 30-day default and 1 to 3650 range, default settings applying to new resources only, CMEK needing a location. gcloud flags checked against the reference with check_commands.py. Removed: Access Transparency and Workspace contents of `_Required`, cost column, free-tier claim, `byte_count` check, claim that a bucket region cannot be changed.
Method: documentation only; no commands were run.
