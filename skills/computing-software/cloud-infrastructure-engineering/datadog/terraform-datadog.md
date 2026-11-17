---
id: computing-software.cloud-infrastructure-engineering.datadog.terraform-datadog
name: terraform-datadog
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, terraform, datadog-provider, monitor-as-code, infrastructure-as-code]
level: practitioner
status: docs-checked
description: "Manage monitors, dashboards and SLOs as code with the Datadog Terraform provider."
sources: ["https://github.com/DataDog/terraform-provider-datadog/blob/master/docs/index.md", "https://github.com/DataDog/terraform-provider-datadog/blob/master/docs/resources/monitor.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform provider for Datadog
Goal: version-controlled Datadog resources.

```hcl
terraform {
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }
}

provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
  # api_url = "https://api.datadoghq.eu/"   # only for a non-default site
}
```

```shell
terraform import datadog_monitor.bytes_received_localhost 2081
```

- The provider requires Terraform 1.1.5 or later.
- `api_key` and `app_key` can also come from the `DD_API_KEY` and `DD_APP_KEY` environment variables. Both are required while `validate` is true (the default) unless using AWS workload identity federation, a bearer token or Terraform Dynamic Provider Credentials.
- `api_url` (or `DD_HOST`) defaults to `https://api.datadoghq.com` and must not end in `/api/`. Other sites use their own API URL, for example `https://api.datadoghq.eu/`, `https://api.us3.datadoghq.com/`, `https://api.us5.datadoghq.com/`.
- `datadog_monitor` takes `name`, `type`, `query`, `message` and a `monitor_thresholds` block with `critical`. The `query` is not the same text as the UI shows and `terraform plan` validates it unless `validate` is false.
- Import an existing resource with `terraform import <resource>.<name> <id>`.
- `ignore_tag_keys` (monitors, SLOs) keeps tags managed elsewhere from showing as drift; the provider block also takes `default_tags` (experimental for a listed set of resources).
- The `datadog_service_definition_yaml` resource manages Catalog service definitions (provider v3.16.0 or later).

Gotcha: do not commit API or application keys or state files that contain them.

## Verify
- `terraform plan` shows no diff after apply.

## Checked
2026-11-09. Confirmed against the provider index and `datadog_monitor` resource docs on GitHub (source, required Terraform version, keys and environment variables, `validate`, `api_url` rules and examples, monitor arguments, import example, `ignore_tag_keys`, `default_tags`) and the Catalog create-entities page (`datadog_service_definition_yaml`, v3.16.0). Removed: my invented monitor example values (query, message, `@slack-ops`), the claim that a wrong `api_url` returns 403, `lifecycle { ignore_changes }` advice, the `datadog_monitor_json` suggestion, module and CI advice, and the claim that the monitor shows a Terraform tag.
Method: documentation only; no commands were run.
