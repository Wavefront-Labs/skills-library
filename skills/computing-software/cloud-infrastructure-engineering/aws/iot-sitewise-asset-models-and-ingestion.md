---
id: computing-software.cloud-infrastructure-engineering.aws.iot-sitewise-asset-models-and-ingestion
name: iot-sitewise-asset-models-and-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot, sitewise, iot-sitewise, industrial-iot, asset-models, opc-ua, sitewise-edge]
level: practitioner
status: docs-checked
description: "Model and ingest industrial data with AWS IoT SiteWise: asset models with measurements, transforms and metrics, hierarchies, property aliases, edge gateways and storage tiers."
sources: ["https://docs.aws.amazon.com/iot-sitewise/latest/userguide/ingest-api-batch-putasset.html", "https://docs.aws.amazon.com/iot-sitewise/latest/userguide/gateways.html", "https://docs.aws.amazon.com/iot-sitewise/latest/userguide/manage-data-streams.html", "https://docs.aws.amazon.com/iot-sitewise/latest/userguide/configure-storage.html", "https://docs.aws.amazon.com/iot-sitewise/latest/userguide/industrial-alarms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IoT SiteWise asset models and ingestion

## Model
- **Asset model** = template: properties of four kinds:
  | Property | Meaning |
  |---|---|
  | Attribute | static (serial number, location) |
  | Measurement | raw time series from equipment (temperature, rpm) |
  | Transform | per-datapoint formula on measurements (`temp_f = temp_c * 9/5 + 32`) |
  | Metric | aggregated over a window (`avg(temp_c)` every 5 minutes, tumbling) and across child assets |
- **Hierarchies:** site -> line -> machine; metrics roll up (e.g. line OEE from machines).
- **Assets** are created from models and carry per-asset values such as data stream aliases and attributes.
```bash
aws iotsitewise create-asset-model --asset-model-name Pump --asset-model-properties file://props.json
aws iotsitewise create-asset --asset-name pump-07 --asset-model-id "$MODEL"
aws iotsitewise update-asset-property --asset-id "$ASSET" --property-id "$PROP" --property-alias /plant1/line2/pump07/temp
```

## Ingest
| Path | When |
|---|---|
| SiteWise Edge gateway (on Greengrass V2 or Siemens Industrial Edge) collecting OPC-UA and MQTT sources | plant floor equipment; keeps collecting during internet outages and syncs afterwards |
| `BatchPutAssetPropertyValue` API | custom collectors, up to 10 entries per call with up to 10 values each; data older than 7 days or more than 10 minutes in the future is rejected |
| IoT Core rule action `iotSiteWise` | devices already publishing MQTT (Basic Ingest can cut messaging cost) |
| Partner data source integration through the gateway | existing sources |
- **Property aliases** (`/plant1/line2/pump07/temp`) identify a data stream. Sending data with an alias that no property uses creates a
  data stream automatically; attach it later to a measurement with `AssociateTimeSeriesToAssetProperty`, or assign the alias first with
  `UpdateAssetProperty`. A property links to only one data stream, and only measurements can be associated.
- Timestamps in seconds + nanoseconds; quality GOOD/BAD/UNCERTAIN.

## Storage
- Data starts in the hot tier. Storage settings can add a service-managed **warm tier** and replicate to a
  customer-managed **cold tier** in your S3 bucket, with retention periods per tier (no hot-tier retention
  period means data stays there indefinitely). The guide documents the cold tier file paths and schemas.

## Use the data
- `get-asset-property-value-history`, `get-asset-property-aggregates`, and the SQL-like `execute-query` API.
- Dashboards: SiteWise Monitor portals are documented in the guide (check current availability for new customers before relying on them).
- Alarms: AWS ended support for AWS IoT Events, so IoT Events alarms are no longer a sound basis for new work; SiteWise also
  supports external alarms (ingest an external alarm state). Check the current alarm options in the guide.

## Verify
- [ ] Measurements for a test asset arrive; transforms and metrics compute.
- [ ] Gateway buffers and backfills after a simulated network outage.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS IoT SiteWise User Guide ingestion API, SiteWise Edge gateways, data streams, storage settings, metrics, transforms and alarms pages (table of contents read for page names); botocore iotsitewise 2019-12-02 model. Fixed: gateways collect OPC-UA and MQTT (Modbus TCP and EtherNet/IP are not listed on the gateway page); BatchPutAssetPropertyValue limits 10 entries and 10 values, and data older than 7 days or 10 minutes ahead is rejected; data streams are created automatically and are linked to measurements with AssociateTimeSeriesToAssetProperty; storage has hot, optional warm and cold tiers; AWS ended support for AWS IoT Events. Confirmed: quality enum GOOD/BAD/UNCERTAIN, ExecuteQuery, GetAssetPropertyValueHistory and GetAssetPropertyAggregates exist. Removed the unsourced model-propagation, Athena, partner-aggregator and Grafana plugin claims; SiteWise Monitor availability is deferred to the guide.
Method: documentation only; no commands were run.
