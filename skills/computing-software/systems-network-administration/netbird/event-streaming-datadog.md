---
id: computing-software.systems-network-administration.netbird.event-streaming-datadog
name: event-streaming-datadog
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, datadog, cloud-siem, log-collection-api, integration-test]
level: practitioner
status: docs-checked
description: "Connect NetBird event streaming to Datadog Cloud SIEM: create an API key, pick the region, connect in the dashboard and verify the two test events."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/activity/event-streaming/datadog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Streams network activity to Datadog through its Log Collection HTTP API; events appear in Log Explorer. Available in NetBird Cloud and self-hosted with an enterprise licence.

Prerequisite: a Datadog account allowed to create API keys.

1. In Datadog organization settings open API Keys, create a key with a descriptive name (e.g. "NetBird Event Streaming") and copy it.
2. In the NetBird Dashboard go to Integrations > Event Streaming, enable Datadog, select the region matching your Datadog account, enter the API key and click Connect.

Verify: in Datadog Log Explorer, look for two events from the `netbird` service: "integration test" (credentials valid, streaming works) and "integration created".

## Checked

2026-11-04. Confirmed against the NetBird Datadog event streaming page: Log Collection HTTP API, Log Explorer, availability note, API key steps, region selection, Connect, and the two verification events from the netbird service. Removed the retry and five-minute claims, which are on the general event streaming page, not this one.
Method: documentation only; no commands were run.
