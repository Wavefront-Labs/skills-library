---
id: computing-software.cloud-infrastructure-engineering.google-cloud.app-engine-standard-and-flexible
name: app-engine-standard-and-flexible
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, app-engine, app-engine-standard, app-engine-flexible, gae, app-yaml, dispatch-yaml, app-engine-services, app-engine-versions, traffic-splitting, instance-classes, automatic-scaling, basic-scaling, app-engine-cron, serverless-vpc-access, app-engine-firewall, migrate-app-engine-to-cloud-run]
level: practitioner
status: docs-checked
description: "Operate App Engine: standard vs flexible, app.yaml scaling and instance classes, versions and traffic splitting, dispatch and cron, VPC access, and when to move to Cloud Run."
sources: ["https://cloud.google.com/appengine/docs/the-appengine-environments", "https://cloud.google.com/appengine/docs/standard/reference/app-yaml", "https://cloud.google.com/appengine/docs/standard/how-instances-are-managed", "https://cloud.google.com/appengine/docs/standard/splitting-traffic", "https://cloud.google.com/appengine/docs/standard/reference/dispatch-yaml", "https://cloud.google.com/appengine/migration-center/run/compare-gae-with-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Engine standard and flexible

**Goal:** keep an existing App Engine estate healthy and cheap, know which knobs matter,
and recognise when the right move is Cloud Run.

## 1. Standard vs flexible
| | Standard | Flexible |
|---|---|---|
| Runtime | sandboxed runtime of a supported language | Docker container on Compute Engine VMs (custom runtime via Dockerfile) |
| Scale to zero | yes (startup in seconds) | no (minimum 1 instance, startup in minutes) |
| Billing | instance hours | vCPU, memory and persistent disk usage |
| Request timeout | 10 min automatic scaling, 24 h basic/manual | 60 min |
| WebSockets | no | yes |
| Use | sudden traffic spikes, scale to zero | custom runtimes, native-code frameworks, Compute Engine network access |

## 2. app.yaml that scales sensibly (standard)
```yaml
runtime: python312
service: api
instance_class: F2           # automatic scaling: F1 (default), F2, F4, F4_1G; basic/manual: B1-B8
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1           # avoids cold starts; needs warmup requests enabled
  max_instances: 20          # limits cost; projects created after March 2025 default to 20
  max_concurrent_requests: 20  # default 10; can be raised on F2 or higher
  min_pending_latency: 30ms
  max_pending_latency: automatic
env_variables: {LOG_LEVEL: info}
vpc_access_connector: {name: projects/<P>/locations/<R>/connectors/gae-conn, egress_setting: private-ranges-only}
inbound_services: [warmup]   # with a /_ah/warmup handler
handlers:
- url: /static
  static_dir: static
  secure: always
- url: /.*
  script: auto
  secure: always
```
- `basic_scaling` (`max_instances`, `idle_timeout`) and `manual_scaling` need a B-class `instance_class`; manual-scaling instances stay in memory and keep state.

## 3. Services, versions, traffic
- `gcloud app deploy app.yaml --version=v42 --no-promote` deploys without taking traffic; `gcloud app services set-traffic api --splits=v41=0.9,v42=0.1 --split-by=cookie` canaries (`--split-by=ip|cookie|random`); `--migrate` attempts to move traffic gradually from the previous version, giving the autoscaler time to respond.
- Old versions keep running until stopped or deleted (`gcloud app versions delete`). `--stop-previous-version` on deploy does not work for auto-scaled standard services, whose instances are always running.
- `dispatch.yaml` routes paths or hostnames to services; deploy it with `gcloud app deploy dispatch.yaml` after every service it names is deployed. Each service also has `<service>-dot-<project>.<region>.r.appspot.com`.
- Deploy `cron.yaml` with `gcloud app deploy cron.yaml`.

## 4. Networking and security
- Egress to a VPC uses a **Serverless VPC Access connector** (`vpc_access_connector` in app.yaml; `egress_setting` defaults to `private-ranges-only`).
- The App Engine firewall (`gcloud app firewall-rules create 100 --action=deny --source-range=...`) allows or denies inbound requests by IP range.
- `gcloud app deploy --service-account=<SA>` sets the identity a version runs as; otherwise the App Engine default service account is used.

## 5. When to leave
Cloud Run runs on much of the same infrastructure as App Engine standard. Google's "Compare App Engine and Cloud Run" page maps `app.yaml` scaling settings to Cloud Run flags (`max_concurrent_requests` to `--concurrency`, `min_instances`/`max_instances` to the min/max instance settings). The standard environment does not support WebSockets; flexible does.

## Gotchas
- Warmup requests need `inbound_services: [warmup]`; `min_instances` only works properly when warmup requests are enabled and handled. Manual and basic scaling instances do not receive `/_ah/warmup`.
- Set `max_instances` explicitly: it limits cost, and the default (20) applies only to projects created after March 2025.
- Flexible environment VMs are restarted weekly to apply OS and security updates; design for it.
- Second-generation runtimes reach legacy bundled services only through `app_engine_apis: true` or, preferably, the narrower `app_engine_bundled_services` list.

## Verify
- [ ] `gcloud app versions list` shows the expected serving version per service and its traffic allocation.
- [ ] After a split, requests reach each version in roughly the configured proportion (cookie splitting is more precise than IP splitting).

## Checked
2026-10-27. Confirmed against App Engine environments comparison, how-instances-are-managed, app.yaml reference (instance classes and defaults, max_concurrent_requests default 10, inbound_services warmup, vpc_access_connector egress_setting, app_engine_apis and app_engine_bundled_services, max_instances default 20), splitting traffic, dispatch.yaml reference, testing-and-deploying and Compare App Engine and Cloud Run pages; gcloud reference for app deploy, services set-traffic, firewall-rules create and versions delete. Removed: instance memory/CPU figures, version cap of 210, target_throughput_utilization, cron header advice, default-SA Editor claim, CI role list, one-region claim, Cloud NAT static IP claim, flexible-only app.yaml keys, request-log field names. Corrected: standard request timeout is 10 min for automatic scaling and 24 h for basic/manual (not 60 s on legacy runtimes); --stop-previous-version does not work on auto-scaled standard.
Method: documentation only; no commands were run.
