---
id: computing-software.networking-hardware-and-wireless.tailscale.log-streaming-destinations
name: log-streaming-destinations
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [log-streaming, siem, configuration-logs]
level: advanced
status: docs-checked
description: "Add a configuration log streaming destination with the correct endpoint URL rules per vendor."
sources: ["https://tailscale.com/kb/1255"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Log streaming

Goal: export audit and administrative activity to your monitoring or storage platform.

**Supported destinations**

- SIEM: Axiom, Cribl, Datadog, Elasticsearch Logstash (data stream), Panther, Splunk (HTTP Event Collector), plus additional systems.
- Storage: Amazon S3 and S3-compatible services (Storj, Wasabi named), Azure Blob Storage, Google Cloud Storage.
- Other: private endpoints, Vector.

**Who.** Owner, Admin, Network admin or IT admin can add, edit and delete streaming destinations. You need an endpoint and credentials from your vendor first.

**Add a SIEM destination**

1. Open the Configuration logs page of the admin console and select Start streaming.
2. Choose the SIEM destination.
3. URL: must use HTTPS; any port is allowed.
   - Splunk needs an endpoint ending in `/services/collector/event`.
   - Elasticsearch data streams need an endpoint ending in `<stream_id>/_bulk?pretty`.
4. Enter Username if your SIEM needs one, and the API Token.
5. Select Start streaming, then check the SIEM to verify. There may be a delay depending on network conditions.

**Checklist**

1. Endpoint is HTTPS.
2. Vendor-specific path suffix applied.
3. Credentials stored with the vendor.
4. Confirm events arrive in the SIEM.

## Checked

Confirmed against Tailscale kb/1255 (Log streaming), read in full: the supported SIEM, storage and other destination lists, the roles allowed to manage destinations, the configuration logs steps, the HTTPS-only URL rule, and the Splunk and Elasticsearch endpoint suffixes. Nothing was removed.

Method: docs-checked 2026-11-09 against https://tailscale.com/kb/1255
