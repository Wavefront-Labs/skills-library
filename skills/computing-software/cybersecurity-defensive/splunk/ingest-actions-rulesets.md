---
id: computing-software.cybersecurity-defensive.splunk.ingest-actions-rulesets
name: ingest-actions-rulesets
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, ingest-actions, data-masking, s3-destination, federated-search, log-reduction, rulesets]
level: practitioner
status: draft
description: "Build Splunk Ingest Actions rulesets to mask PII, filter noisy events and route full-fidelity copies to S3, with preview, deployment and verification steps."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Data/DataIngest", "https://docs.splunk.com/Documentation/Splunk/latest/Data/DataIngestRulesets", "https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/DataIngest"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ingest Actions rulesets

Ingest Actions (Splunk Enterprise 9.0+, Splunk Cloud) is a UI over index-time transforms:
build a ruleset per sourcetype, preview against sample data, then deploy.

## Where
Settings > Data > Ingest Actions. Run on indexers (via cluster manager), heavy forwarders, or
Splunk Cloud. Universal forwarders cannot run rulesets.

## Rule types (applied in order)
1. **Mask with regular expression**: replace card numbers, tokens, passwords.
   Regex `(?<=password=)[^&\s]+` replace with `****`.
2. **Set index**: route by condition (e.g. events from DMZ hosts to `dmz_fw`).
3. **Filter using eval expression / regex**: drop events (`action="allowed" AND dest_port=53`).
4. **Route to destination**: send a copy (or the rest) to an S3-compatible destination,
   with optional "Clone events" so Splunk still indexes a reduced set.

## Typical security pattern
- Firewall allow logs: keep denies and allows to/from critical subnets in Splunk; clone all
  allows to S3 (cheap retention). Use Federated Search for Amazon S3 or re-ingest when an
  investigation needs them.
- Mask secrets in application logs before they ever reach disk.

## Steps
1. New ruleset, choose sourcetype, load sample (from indexed data or paste).
2. Add rules; the preview pane shows affected events and the volume reduction estimate.
3. Save, then deploy: on a cluster manager, Ingest Actions pushes the bundle; on standalone HF
   it writes `props.conf`/`transforms.conf` in `splunk_ingest_actions` app.
4. S3 destinations: Settings > Data > Ingest Actions > Destinations; output is newline-delimited
   JSON or raw, partitioned by day; needs IAM credentials or instance role.

## Gotchas
- Rulesets apply only to events that are still being parsed on that tier. If a heavy forwarder
  upstream already parsed the data, rules on the indexer do nothing.
- Masking regexes run on `_raw`; test with real samples including multiline events.
- Filtered data is gone unless cloned to a destination first; order rules accordingly.
- S3 writes batch; failures queue on the instance and can fill disk (watch `splunkd.log`
  `RfsOutputProcessor`).

## Verify
- Compare per-sourcetype volume before/after in the Monitoring Console licence usage view.
- Search for masked patterns: `index=app password=* NOT password=****` should be empty.
- List objects in the S3 bucket for today's partition.
