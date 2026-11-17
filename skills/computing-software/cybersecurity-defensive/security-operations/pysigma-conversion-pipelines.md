---
id: computing-software.cybersecurity-defensive.security-operations.pysigma-conversion-pipelines
name: pysigma-conversion-pipelines
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-as-code, sigma, pysigma, sigma-cli, processing-pipelines, field-mapping, splunk, kql]
level: advanced
status: verified
description: "Convert Sigma rules with pySigma: choosing backends, writing processing pipelines for your field names and indexes, and automating conversion output."
sources: ["https://github.com/SigmaHQ/pySigma", "https://sigmahq-pysigma.readthedocs.io/en/latest/", "https://github.com/SigmaHQ/sigma-cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting with pySigma backends and pipelines

**Goal:** Sigma rules become queries that match your SIEM's actual field names, indexes
and sourcetypes, reproducibly in CI.

## Pieces
- **Backend:** target query language (`pySigma-backend-splunk`, `-kusto`, `-elasticsearch`, `-qradar`...). Install via `sigma plugin install splunk`;
  plugin ids come from `sigma plugin list` (`sigma plugin install microsoft365defender` fails with "not found" on sigma-cli 3.1.0).
- **Processing pipeline:** transformations applied before conversion: field renames, adding
  index/sourcetype conditions, dropping unsupported rules. Shipped pipelines exist
  (`sysmon`, `windows-audit` and `windows-logsources` from the `windows` plugin, `splunk_windows`, `ecs_windows`). `sigma list pipelines` shows each id, priority and plugin.
- **Output format:** default query, or `savedsearches` (Splunk conf; produced `[default]` dispatch settings plus one stanza with `search = ...` per rule), `kibana_ndjson` (lucene target), etc. List them with `sigma list formats <target>`.

## CLI
```
sigma list targets
sigma list pipelines splunk
sigma convert -t splunk -p splunk_windows -p ./pipelines/org.yml -f savedsearches rules/ -o out/savedsearches.conf
```
Pipelines stack in order; put your org pipeline last so it overrides.

## Writing an org pipeline (YAML)
```yaml
name: org-splunk
priority: 30
transformations:
  - id: index_proc
    type: add_condition
    conditions:
      index: edr
      sourcetype: 'crowdstrike:events:sensor'
    rule_conditions:
      - type: logsource
        category: process_creation
  - id: field_names
    type: field_name_mapping
    mapping:
      Image: process_path
      CommandLine: process_cmdline
      ParentImage: parent_process_path
      User: user
  - id: unsupported
    type: rule_failure
    message: No registry telemetry in this environment
    rule_conditions:
      - type: logsource
        category: registry_set
```
Priority orders pipelines (lower runs first; checked: `sysmon` 10, `splunk_windows` 20, this one 30, and the org mapping was applied on top, giving `index="edr" sourcetype="crowdstrike:events:sensor" ... process_path IN (...) NOT process_cmdline=...`). `rule_failure` stops conversion with a clear
error instead of producing a query that never matches.

## In Python (for CI)
```python
from sigma.collection import SigmaCollection
from sigma.backends.splunk import SplunkBackend
from sigma.processing.resolver import ProcessingPipelineResolver
from sigma.pipelines.sysmon import sysmon_pipeline
rules = SigmaCollection.load_ruleset(["rules/"])
print(SplunkBackend(sysmon_pipeline()).convert(rules))   # convert() returns a list of queries, one per rule
```

## Gotchas
- An unmapped field converts silently to the Sigma name, producing a query that never
  matches; list all fields used by rules and assert each is mapped.
- Backends differ in support for modifiers (`re`, `cidr`, `fieldref`); a rule may convert
  for one target and fail for another.
- Pin pySigma and plugin versions; output changes between releases.

## Verify
Convert a known rule, run it in the SIEM over data containing the test event, and confirm a
hit; diff converted output in CI on each change.
