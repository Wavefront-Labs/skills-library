---
id: computing-software.cloud-infrastructure-engineering.aws.iot-core-and-greengrass
name: iot-core-and-greengrass
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot-core, greengrass, greengrass-v2, mqtt, device-shadow, iot-rules-engine, iot-policies, x509-certificates, fleet-provisioning, just-in-time-provisioning, device-defender, iot-jobs, ota-updates, thing-groups, iot-components, edge-computing, basic-ingest, device-management]
level: practitioner
status: draft
description: "Connect device fleets with AWS IoT Core (X.509 identity, fleet provisioning, least-privilege policies, MQTT topics, shadows, rules, jobs) and run edge workloads with Greengrass v2 components."
sources: ["AWS IoT Core Developer Guide - Security (X.509 certificates, policies, provisioning)", "AWS IoT Core Developer Guide - Rules for AWS IoT and Device Shadow service", "AWS IoT Greengrass Version 2 Developer Guide - Components and deployments", "AWS IoT Core Developer Guide - Jobs and Device Defender"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IoT Core and Greengrass — a million devices with per-device identity, and code that runs at the edge

**Goal:** every device authenticates with its own certificate and a policy that only lets
it touch its own topics; telemetry flows through the rules engine without Lambda in the
middle; firmware and config roll out as jobs/deployments; edge logic runs in Greengrass
components with the same tooling.

## 1. Identity and provisioning
- One **X.509 certificate per device**; the **thing** (registry record, attributes, thing
  groups) is attached to the cert; an **IoT policy** is attached to the cert. Endpoint:
  `aws iot describe-endpoint --endpoint-type iot:Data-ATS` (`…-ats.iot.<region>.amazonaws.com`, port 8883 MQTT/TLS or 443 ALPN `x-amzn-mqtt-ca`).
- Provisioning options:
  | Method | Use |
  |---|---|
  | **Fleet provisioning by claim** | Factory burns a shared *claim* cert; device calls `$aws/certificates/create` + `$aws/provisioning-templates/<t>/provision` to swap for a unique cert; template can call a **pre-provisioning hook** Lambda to validate serials |
  | **Fleet provisioning by trusted user** | Installer app (Cognito) gets a one-time token for the device |
  | **JITP / JITR** | Your own CA registered with IoT; certs signed by it are provisioned on first connect |
  | **Bulk registration** | CSV/JSON of pre-generated certs |
- Store private keys in a secure element/TPM (PKCS#11) where the hardware allows; never ship the same key to two devices.
- Policy with thing-bound variables (least privilege):
  ```json
  {"Effect":"Allow","Action":"iot:Connect","Resource":"arn:aws:iot:<r>:<a>:client/${iot:Connection.Thing.ThingName}"},
  {"Effect":"Allow","Action":"iot:Publish","Resource":"arn:aws:iot:<r>:<a>:topic/dt/${iot:Connection.Thing.ThingName}/*"},
  {"Effect":"Allow","Action":"iot:Subscribe","Resource":"arn:aws:iot:<r>:<a>:topicfilter/cmd/${iot:Connection.Thing.ThingName}/*"},
  {"Effect":"Allow","Action":"iot:Receive","Resource":"arn:aws:iot:<r>:<a>:topic/cmd/${iot:Connection.Thing.ThingName}/*"}
  ```
  Client id must equal thing name for the variables to resolve. `Subscribe` uses `topicfilter/`, `Receive` uses `topic/`.
- Revoke: `update-certificate --new-status REVOKED` + detach; **Device Defender** audit flags shared certs, overly permissive policies, revoked-but-active certs.

## 2. Topics, shadows, rules
- Topic design: `dt/<fleet>/<thing>/<sensor>` (telemetry), `cmd/<thing>/<action>` (commands), `cfg/…`; ≤ 7 levels, no leading `/`, reserve `$aws/`. MQTT 5 supported (shared subscriptions `$share/…`, user properties).
- **Basic Ingest** (`$aws/rules/<ruleName>/...`) skips the message broker fee when data only feeds a rule.
- **Device Shadow** (classic + named): `$aws/things/<t>/shadow/name/<n>/update` with `desired`/`reported`; devices subscribe to `/update/delta` to pick up config while offline-then-reconnect. Keep shadows small (≤ 8 KB); not a telemetry store.
- **Rules engine** (SQL-like): `SELECT temp, topic(3) AS thing, timestamp() AS ts FROM 'dt/+/+/temp' WHERE temp > 80`
  → actions: Kinesis/Firehose (bulk telemetry → S3/Timestream), DynamoDBv2, SNS/SQS, Lambda, IoT Analytics/SiteWise, republish, CloudWatch metrics/logs, HTTP, OpenSearch, Kafka (MSK).
  Always set an **error action** (SQS/CloudWatch) and enable IoT logging (`set-v2-logging-options --default-log-level ERROR` → `INFO` while debugging).
- **Jobs**: `create-job --targets <thing-group-arn> --document-source s3://…/ota.json --job-executions-rollout-config '{"maximumPerMinute":100,"exponentialRate":{...}}' --abort-config …`
  for OTA/firmware/config; devices run the jobs agent (`$aws/things/<t>/jobs/…`), report `SUCCEEDED/FAILED`; rollout rate + abort thresholds protect the fleet. **Continuous jobs** on dynamic thing groups onboard new devices automatically.
- Fleet metrics / **Fleet Hub** for queries over the registry (`thingName:sensor* AND connectivity.connected:true`) — enable **fleet indexing** with connectivity and shadow fields.

## 3. Greengrass v2
- Install **Greengrass Core (nucleus)** on Linux/Windows edge devices (`greengrass-nucleus` JAR,
  `--provision true` uses an IAM user with limited rights to create the thing/cert/role alias,
  or fleet provisioning plugin). The core assumes an IAM role via **role alias** for AWS calls.
- **Components** = recipe (YAML/JSON: lifecycle `Install/Run/Shutdown`, dependencies,
  configuration, artifacts in S3) + artifacts. Public components: `aws.greengrass.Cli`,
  `LogManager`, `StreamManager` (buffered upload to Kinesis/S3/SiteWise), `SecretManager`,
  `TokenExchangeService`, `Nucleus`, `ShadowManager`, `DockerApplicationManager`, `LambdaLauncher`, `ML inference` bundles.
- **Deployments** target a thing or thing group with component versions + config merges
  (`--deployment-policies` failure handling `ROLLBACK`, rollout config); devices in the group
  converge on reconnect. Deployments are the OTA mechanism for edge software.
- Local dev: `greengrass-cli deployment create --recipeDir … --artifactDir … --merge "com.example.Sensor=1.0.0"`; logs in `/greengrass/v2/logs/<component>.log`.
- **IPC** (`awsiot.greengrasscoreipc`) for components to publish MQTT via the core, read config, get secrets; **local MQTT broker** (`aws.greengrass.clientdevices.mqtt.Moquette`/EMQX) + **client device auth** lets leaf devices connect through the core.
- Harden: run components as a non-root `ggc_user`, pin component versions, restrict the token exchange role to the S3 prefixes/topics needed.

## 4. Operations
- Monitor: `AWS/IoT` metrics (`Connect.Success/AuthError`, `PublishIn.Success`, `RuleMessageThrottled`, `Failure` per action); Device Defender **detect** for anomalous message rates/ports; Greengrass `aws.greengrass.telemetry` metrics.
- Quotas: ~500 messages/s per connection outbound, 512 KB payload (MQTT), rule concurrency per account — batch telemetry on-device.
- Cost: connection-minutes + messages (5 KB increments) + rules + shadow/registry ops — Basic Ingest and batching cut most of it.
- Multi-region/DR: certs are regional; design for re-provisioning or register the CA in both regions.

## Gotchas
- `iot:Subscribe` allowed but `iot:Receive` missing = subscription succeeds, no messages arrive (silent).
- Wildcards in `Resource` for `Connect` (`client/*`) let a stolen cert impersonate any device — always bind client id to thing name.
- Rules with `SELECT *` into DynamoDB with a hashed key from the payload break on malformed messages; error action catches it.
- Shadows updated faster than ~1/s per device throttle; use telemetry topics for streams.
- Greengrass deployment `FAILED` with no component error is usually a component dependency/version constraint or disk space; check `greengrass.log`.
- Unconfirmed: MQTT 5 feature coverage per region and current rule action list — check the developer guide.

## Verify
- [ ] A device with a cert for `thing-A` cannot publish to `dt/fleet/thing-B/...` (`AuthError` in CloudWatch).
- [ ] Fleet provisioning swaps the claim cert for a unique one and the hook rejects an unknown serial.
- [ ] Rule writes telemetry to Firehose → S3; a malformed message lands in the error SQS queue.
- [ ] A job to a thing group rolls out at the configured rate and aborts when > 10 % fail.
- [ ] Greengrass deployment installs a component; `greengrass-cli component list` shows `RUNNING`; a bad version rolls back.
