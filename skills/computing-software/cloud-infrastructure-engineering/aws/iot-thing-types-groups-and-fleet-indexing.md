---
id: computing-software.cloud-infrastructure-engineering.aws.iot-thing-types-groups-and-fleet-indexing
name: iot-thing-types-groups-and-fleet-indexing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot, fleet-indexing, thing-types, thing-groups, dynamic-thing-groups, fleet-metrics, iot-registry]
level: practitioner
status: docs-checked
description: "Organise IoT fleets with thing types, static and dynamic thing groups and billing groups, then query and measure them with fleet indexing searches, aggregations and fleet metrics."
sources: ["https://docs.aws.amazon.com/iot/latest/developerguide/thing-types.html", "https://docs.aws.amazon.com/iot/latest/developerguide/dynamic-thing-groups.html", "https://docs.aws.amazon.com/iot/latest/developerguide/managing-index.html", "https://docs.aws.amazon.com/iot/latest/developerguide/index-aggregate.html", "https://docs.aws.amazon.com/iot/latest/developerguide/managing-fleet-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thing types, thing groups and fleet indexing

## Registry structure
- **Thing type:** category (e.g. `sensor-v2`) with searchable attributes. Things with a thing type can
  have up to 50 attributes (without one, 3); a thing has one type; the name cannot change and the
  type is immutable, but it can be deprecated to stop new associations. Delete only after deprecating,
  waiting five minutes, and with no things associated.
- **Static thing groups:** hierarchical (region > site > line); attach policies and jobs to groups so devices inherit them.
- **Dynamic thing groups:** membership by a fleet indexing query; devices join and leave automatically.
  They cannot be part of a hierarchy and cannot have policies applied.
- **Billing groups:** group things for cost allocation (`create-billing-group`).
```bash
aws iot create-thing-type --thing-type-name sensor-v2 --thing-type-properties searchableAttributes=model,fwChannel
aws iot create-thing --thing-name s-0001 --thing-type-name sensor-v2 --attribute-payload '{"attributes":{"model":"T200","site":"lyon"}}'
aws iot add-thing-to-thing-group --thing-group-name lyon --thing-name s-0001
```

## Fleet indexing
```bash
aws iot update-indexing-configuration --thing-indexing-configuration \
  'thingIndexingMode=REGISTRY_AND_SHADOW,thingConnectivityIndexingMode=STATUS,deviceDefenderIndexingMode=VIOLATIONS,namedShadowIndexingMode=ON' \
  --thing-group-indexing-configuration thingGroupIndexingMode=ON
aws iot search-index --query-string 'connectivity.connected:false AND attributes.site:lyon'
aws iot search-index --query-string 'shadow.reported.firmware:1.2.* AND thingTypeName:sensor-v2'
aws iot get-statistics --query-string 'thingTypeName:sensor-v2' --aggregation-field shadow.reported.battery
```
- Indexes registry attributes, shadows (classic and named), connectivity status and Defender violations.
  Modes: `thingIndexingMode` `OFF|REGISTRY|REGISTRY_AND_SHADOW`, `thingConnectivityIndexingMode`
  `OFF|STATUS`, `deviceDefenderIndexingMode` `OFF|VIOLATIONS`, `namedShadowIndexingMode` `OFF|ON`
  (with the shadow names listed in the indexing `filter.namedShadowNames`), thing group indexing `OFF|ON`.
- Aggregation fields must be managed fields or custom fields declared in `update-indexing-configuration`
  with a type (`Number`, `String` or `Boolean`); without `--aggregation-field`, `registry.version` is used.
  The aggregation APIs are `GetStatistics`, `GetCardinality`, `GetPercentiles` and `GetBucketsAggregation`.
- Index only what you query; indexing and queries are metered (see the AWS IoT pricing page).

## Dynamic groups and fleet metrics
```bash
aws iot create-dynamic-thing-group --thing-group-name low-battery \
  --query-string 'shadow.reported.battery < 20'
aws iot create-fleet-metric --metric-name offline-lyon --query-string 'connectivity.connected:false AND attributes.site:lyon' \
  --aggregation-type name=Statistics,values=count --aggregation-field registry.version --period 300
```
- The fleet metric `period` is 60 to 86,400 seconds; fleet indexing must be enabled with the data
  sources and custom fields first.
- Target jobs at dynamic groups (e.g. firmware older than X) so devices that later match are included
  (continuous jobs).
- Fleet metrics publish to CloudWatch for alarms ("more than 5% offline").

## Gotchas
- Dynamic thing group membership is eventually consistent; not for transactional checks.
- Deleting a thing type requires deprecating it and removing things from it.
- Group policy inheritance can grant more than intended; review effective policies.

## Verify
- [ ] Search for offline devices returns expected things; fleet metric in CloudWatch with an alarm.
- [ ] Dynamic group membership updates when a test device's shadow changes.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS IoT Core Developer Guide thing types, deprecate and delete thing type, dynamic thing groups, managing thing indexing, aggregate queries and fleet metrics pages; botocore iot 2015-05-28 model. Fixed: things with a thing type may have up to 50 attributes (the up-to-3 limit applies to things without one) and no page states a 3-searchable-attribute limit, so it was removed; dynamic thing groups cannot be in a hierarchy or have policies; dynamic group membership is eventually consistent. Confirmed: five-minute wait before deleting a deprecated type, indexing mode enums, custom field types Number/String/Boolean, registry.version default aggregation field, four aggregation APIs, fleet metric period 60-86400 seconds. Removed the unsourced indexing charge and seconds-level consistency claims.
Method: documentation only; no commands were run.
