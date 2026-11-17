---
id: computing-software.devops-ci-cd.concourse-ci.resource-webhooks
name: resource-webhooks
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [webhooks, webhook-token, check, resources, instanced-pipelines, api]
level: practitioner
status: docs-checked
description: "Trigger an immediate resource check from an external service using webhook_token, including the full API path, instanced pipeline vars in the URL, and why the payload is ignored."
sources:
  - https://concourse-ci.org/docs/resources/
  - https://concourse-ci.org/docs/internals/checker/
  - https://concourse-ci.org/docs/operation/tuning/
  - https://concourse-ci.org/docs/vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If a resource has `webhook_token`, an external service can ask Concourse to check it immediately. The token is a primitive form of authentication passed as a query parameter. Append this path to your external URL in the hook sender:

```
/api/v1/teams/TEAM_NAME/pipelines/PIPELINE_NAME/resources/RESOURCE_NAME/check/webhook?webhook_token=WEBHOOK_TOKEN
```

For an instanced pipeline you must target a single instance (there are no webhooks for all instances of a pipeline) by adding the pipeline's instance vars as URL parameters in the form `vars.MY-VAR="SOME-VALUE"`:

```
/api/v1/teams/TEAM_NAME/pipelines/PIPELINE_NAME/resources/RESOURCE_NAME/check/webhook?webhook_token=WEBHOOK_TOKEN&vars.my-var="some-value"&vars.second-var="two"
```

The request payload is ignored entirely. Configure the resource as if there were no webhooks, since the resource config is still the source of truth; the webhook only brings the check forward.

Configuring a webhook does not stop periodic checking. To rely only on webhooks set `check_every: never`, or raise `CONCOURSE_RESOURCE_WITH_WEBHOOK_CHECKING_INTERVAL` on the web node, for example to a large value such as `99h`.

The token can be a `((var))` because `resource.webhook_token` is one of the attributes a credential manager may fill.

## Checked

2026-11-04. Paths, instance var syntax and ignored payload confirmed on the Resources page; check_every never and webhook polling on the Resource Checker and Performance Tuning pages; var support on the Vars page.

Method: documentation only; no commands were run.
