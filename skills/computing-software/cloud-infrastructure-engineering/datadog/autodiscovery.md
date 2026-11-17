---
id: computing-software.cloud-infrastructure-engineering.datadog.autodiscovery
name: autodiscovery
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, autodiscovery, container-labels, annotations, ad-identifiers]
level: practitioner
status: docs-checked
description: "Configure Autodiscovery with Kubernetes pod annotations (v2) or Docker labels, template variables and ad_identifiers so the Agent monitors containers dynamically."
sources: ["https://docs.datadoghq.com/containers/kubernetes/integrations/", "https://docs.datadoghq.com/containers/docker/integrations/", "https://docs.datadoghq.com/containers/guide/template_variables/", "https://docs.datadoghq.com/containers/troubleshooting/log-collection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autodiscovery templates
Goal: attach integration configs to containers as they appear.

```yaml
# Kubernetes pod annotations, v2 format (Agent v7.36+), from the docs' Postgres example
metadata:
  name: postgres
  annotations:
    ad.datadoghq.com/postgres.checks: |
      {
        "postgres": {
          "instances": [
            {
              "host": "%%host%%",
              "port": "5432",
              "username": "datadog",
              "password": "%%env_PG_PASSWORD%%"
            }
          ]
        }
      }
```

General form: `ad.datadoghq.com/<CONTAINER_NAME>.checks` (JSON object keyed by integration name with `init_config` and `instances`) and `ad.datadoghq.com/<CONTAINER_NAME>.logs: '[<LOGS_CONFIG>]'`. `<CONTAINER_NAME>` is the container name in the pod spec. The older v1 form uses `.check_names`, `.init_configs` and `.instances` annotations.

Docker labels: `com.datadoghq.ad.checks` takes `{"<INTEGRATION_NAME>": {"instances": [...], "logs": [...]}}`; `com.datadoghq.ad.logs` takes `[<LOGS_CONFIG>]`. The older label set is `com.datadoghq.ad.check_names`, `.init_configs`, `.instances`.

- Template variables: `%%host%%` (container network IP), `%%port%%` (highest exposed port, sorted numerically), `%%port_<NUMBER_X>%%` and `%%port_<NAME>%%`, `%%hostname%%`, `%%pid%%`, `%%env_<ENV_VAR>%%` (the `$<ENV_VAR>` environment variable as seen by the Agent process, not the monitored container).
- File-based templates use `ad_identifiers`, a list of container identifiers; an identifier such as `redis` matches the image name, so `foo/redis:latest` and `bar/redis:v2` both match.
- To see what the Agent loaded and resolved, run `agent configcheck` in the Agent container: `kubectl exec -it <AGENT_POD> -- agent configcheck` or `docker exec -it <CONTAINER_NAME> agent configcheck`.

Gotcha: `%%env_<ENV_VAR>%%` is resolved from the Agent's environment, so the variable must be set on the Agent, not the application container.

## Verify
- `agent configcheck` shows the resolved check for the container, and `agent status` lists it under running checks.

## Checked
2026-11-03. Confirmed against the Kubernetes and Docker integrations pages, the template variables guide and the log collection troubleshooting page. Replaced the unconfirmed nginx example with the docs' Postgres example. Removed: the claim that a mismatched container name is the top failure, the `kubectl exec ds/datadog-agent` form, `ad.datadoghq.com/<container>.instances` shared-config advice and pod-template rollout advice.
Method: documentation only; no commands were run.
