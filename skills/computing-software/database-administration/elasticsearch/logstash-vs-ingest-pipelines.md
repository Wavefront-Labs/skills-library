---
id: computing-software.database-administration.elasticsearch.logstash-vs-ingest-pipelines
name: logstash-vs-ingest-pipelines
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, logstash, ingest-pipelines, elastic-agent, beats, elasticsearch-ingest]
level: practitioner
status: docs-checked
description: "Decide between Logstash and Elasticsearch ingest pipelines for parsing and routing data, and run Logstash with persistent queues, pipeline-to-pipeline and output tuning."
sources:
  - https://github.com/elastic/logstash/blob/main/docs/reference/logstash-settings-file.md
  - https://github.com/elastic/logstash/blob/main/docs/reference/persistent-queues.md
  - https://github.com/elastic/logstash/blob/main/docs/reference/dead-letter-queues.md
  - https://github.com/elastic/logstash/blob/main/docs/reference/pipeline-to-pipeline.md
  - https://github.com/elastic/logstash/blob/main/docs/reference/monitoring-logstash.md
  - https://github.com/logstash-plugins/logstash-output-elasticsearch/blob/main/docs/index.asciidoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logstash pipelines vs ingest pipelines

## Decision table
| Need | Ingest pipeline | Logstash |
|---|---|---|
| Parse/enrich docs bound for Elasticsearch | Yes, simplest | Yes |
| Outputs other than Elasticsearch (Kafka, S3, SIEM) | No | Yes |
| Inputs that are not Beats/Agent/HTTP (JDBC, syslog TCP at scale, Kafka consume) | No | Yes |
| Buffering during ES outages | No (client retries) | Persistent queue, DLQ |
| Complex multi-event logic (aggregate, throttling) | No | Yes |
| Operational footprint | None extra | JVM fleet to run |

Default: Elastic Agent/Beats to ingest pipelines. Add Logstash when you need its inputs/outputs or buffering (this table is a design guideline, not a vendor statement).

## Logstash essentials
```ruby
# /etc/logstash/conf.d/syslog.conf
input  { tcp { port => 5514 codec => line } }
filter {
  grok { match => { "message" => "%{SYSLOGLINE}" } tag_on_failure => ["_grok_syslog_fail"] }
  date { match => ["timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss"] }
}
output { elasticsearch { hosts => ["https://es:9200"] api_key => "${ES_API_KEY}" ssl_certificate_authorities => ["/etc/logstash/ca.crt"]
                         data_stream => true data_stream_dataset => "syslog" } }
```
`logstash.yml`:
```yaml
queue.type: persisted          # survives restarts and absorbs ES slowdowns
queue.max_bytes: 8gb
dead_letter_queue.enable: true # mapping errors from ES go here
pipeline.workers: 8            # default = number of CPU cores
pipeline.batch.size: 250       # default 125
```

## Splitting with pipeline-to-pipeline
`pipelines.yml` with a distributor pipeline sending to per-source pipelines (`pipeline { send_to => ["nginx"] }`) isolates failures and tuning.

## Monitoring
The Logstash monitoring (node stats) API listens on port 9600 by default (it binds the first free port in 9600-9700) and reports JVM, process, event and pipeline runtime stats; see the Node stats API reference for the exact endpoints. Ship metrics to Stack Monitoring with Elastic Agent.

## Verify
Stop Elasticsearch briefly in staging: the persistent queue on disk grows and drains after recovery without data loss; check the queue stats in the node stats API.

## Checked

Checked 2026-10-25 against elastic/logstash `main` docs and the logstash-output-elasticsearch plugin docs. Confirmed: `queue.type: persisted`, `queue.max_bytes`, `dead_letter_queue.enable` (disabled by default), `pipeline.workers` default (CPU cores) and `pipeline.batch.size` default 125, API port 9600-9700, output options `api_key`, `ssl_certificate_authorities`, `data_stream` and `data_stream_dataset` exist. The grok, date and tcp input option examples and the Ingest-vs-Logstash comparison are standard plugin usage and design judgement rather than quoted figures; the exact node stats endpoint path was not confirmed so it was removed.

Method: documentation only; no commands were run.
