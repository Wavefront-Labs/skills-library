---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-notifications-and-notifiers
name: cloud-build-notifications-and-notifiers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-build, cloud-build-notifications, build-notifier, pubsub, slack]
level: practitioner
status: docs-checked
description: "Send Cloud Build results to Slack, email or webhooks: the cloud-builds Pub/Sub topic and deploying the notifier on Cloud Run with a CEL filter."
sources: ["https://cloud.google.com/build/docs/configuring-notifications/notifiers", "https://cloud.google.com/build/docs/configuring-notifications/configure-slack", "https://cloud.google.com/build/docs/subscribe-build-notifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Build notifications and notifiers

Cloud Build publishes every build status change to the Pub/Sub topic `cloud-builds` by default (create the topic if it doesn't exist); `options.pubsubTopic` in the build config selects a custom topic.

## 1. Notifier config (Slack example)
`slack.yaml`:
```yaml
apiVersion: cloud-build-notifiers/v1
kind: SlackNotifier
metadata: {name: prod-builds-slack}
spec:
  notification:
    filter: build.status == Build.Status.FAILURE
    delivery:
      webhookUrl: {secretRef: slack-webhook}
  secrets:
  - name: slack-webhook
    value: projects/<P>/secrets/slack-webhook/versions/latest
```
Other notifiers: `smtp`, `http` (JSON payload to an endpoint), `googlechat`, `githubissues`, `bigquery` (writes build data to a table).

## 2. Deploy
```bash
gcloud storage cp slack.yaml gs://<B>/notifiers/slack.yaml
gcloud run deploy build-slack-notifier --region=<R> --no-allow-unauthenticated \
  --image=us-east1-docker.pkg.dev/gcb-release/cloud-build-notifiers/slack:latest \
  --update-env-vars=CONFIG_PATH=gs://<B>/notifiers/slack.yaml,PROJECT_ID=<P> \
  --service-account=build-notifier@<P>.iam.gserviceaccount.com
gcloud pubsub subscriptions create build-slack-sub --topic=cloud-builds \
  --push-endpoint=$(gcloud run services describe build-slack-notifier --region=<R> --format='value(status.url)') \
  --push-auth-service-account=pubsub-invoker@<P>.iam.gserviceaccount.com
```
Notifier SA: Secret Manager Secret Accessor on the secret and Storage Object Viewer on the config. The Pub/Sub service agent needs `roles/iam.serviceAccountTokenCreator` on the subscription identity service account, and that account needs the Cloud Run Invoker role on the service.

## Gotchas
- Cloud Build publishes a message when a build is created, starts working and completes, so without a filter you are notified for every state change.
- The `filter` is a CEL expression over the `build` variable; other fields come from the Build resource.
- Notifier images are kept for nine months and then deleted, so pin a specific image version rather than `latest` if you need a stable one.

## Verify
- [ ] A deliberately failing build on `main` posts exactly one Slack message with the build log link.

## Checked

2026-10-27. Confirmed in the notifiers overview, Slack notifier and subscribe-to-notifications pages: the `cloud-builds` topic and `options.pubsubTopic`, notifier config shape (`apiVersion: cloud-build-notifiers/v1`, `kind: SlackNotifier`, CEL `filter`, `secretRef`, `secrets`), the list of notifier types, `gcloud run deploy` with the notifier image, `--no-allow-unauthenticated`, `CONFIG_PATH` and `PROJECT_ID`, Secret Accessor and Storage Object Viewer roles, Pub/Sub token-creator and Invoker steps, nine-month image retention. Removed: the branch-name and TIMEOUT filter example, `build.build_trigger_id`, `--set-env-vars` (page uses `--update-env-vars`). The missing token-creator step was added. Read end to end.

Method: documentation only; no commands were run.
