---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-acquisition-datasources
name: crowdsec-acquisition-datasources
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [acquisition, datasources, acquis-d, labels, transform, time-machine, log-sources]
level: practitioner
status: docs-checked
description: "Define what the Log Processor reads with acquisition files: the datasource types, mandatory labels, transform and use_time_machine."
sources: ["https://raw.githubusercontent.com/crowdsecurity/crowdsec-docs/main/crowdsec-docs/docs/log_processor/data_sources/introduction.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Datasources tell the Security Engine where logs are. They are defined in acquisition files (for example under `/etc/crowdsec/acquis.d/`; one file can hold several datasources separated by `---`) or given on the command line for cold log analysis.

## Modules

Appsec (HTTP service for the WAF), AWS CloudWatch, AWS Kinesis, AWS S3, docker, file, HTTP, journald, Kafka, Kubernetes, Kubernetes Audit, Loki, VictoriaLogs, syslog service and Windows Event. All support streaming; one-shot (cold analysis) is supported only by CloudWatch, S3, docker, file, journald, Loki, VictoriaLogs and Windows Event.

## Common parameters

- `source`: required for every module except file.
- `log_level`: defaults to `info`.
- `labels`: a map added to events. The `type` label is **mandatory**: it selects which parser handles the line.
- `transform`: an expression run on each line before parsing. It may return a string that replaces `evt.Line.Raw`, or a list of strings that each become an event. Example for JSON lines with a `Records` array: `map(JsonExtractSlice(evt.Line.Raw, "Records"), ToJsonString(#))`.
- `use_time_machine`: by default, real-time reads stamp events with the read time. Set true to use the timestamp in the log. It is mandatory if the application buffers logs before writing them, such as IIS or most AWS services writing to S3, otherwise CrowdSec thinks everything happened at once and can raise false positives.

## Example

```yaml
filenames:
  - /var/log/nginx/*.log
labels:
  type: nginx
```

The `labels` and `type` fields are necessary to dispatch the log lines to the right parser.

## Checked
2026-11-08. Confirmed against the Acquisition Datasources introduction (page source in the crowdsec-docs repository, since the docs.crowdsec.net URL returned 404): module table, common parameters, transform example and return types, use_time_machine, labels, example. Removed: the `acquis.yaml` file name, the duplicate-type false-positive warning and the first-thing-to-check advice (not on the page).
Method: documentation only; no commands were run.
