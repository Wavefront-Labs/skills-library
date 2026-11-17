---
id: computing-software.data-engineering.apache-pinot.apache-pinot-segment-creation-and-ingestion-job-spec
name: apache-pinot-segment-creation-and-ingestion-job-spec
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, segment, ingestion-job-spec, launchdataingestionjob, segmentcreationandtarpush, jobtype, pushjobspec, recordreaderspec, pinotfsspecs]
level: practitioner
status: docs-checked
description: "Batch segment generation with a Pinot YAML ingestion job spec: jobType choices, key sections, LaunchDataIngestionJob and Groovy templating."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/table/segment/README.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/reference/configuration-reference/job-specification.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment creation and the ingestion job spec

Batch data becomes segments through a YAML job spec run by `LaunchDataIngestionJob`. The controller must be running (to serve the table config and schema) unless the spec points at their files:
```
bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile job.yaml
```

`jobType` supported values: `SegmentCreation`, `SegmentMetadataPush`, `SegmentTarPush`, `SegmentUriPush`, `SegmentCreationAndMetadataPush`, `SegmentCreationAndUriPush`, `SegmentCreationAndTarPush`.
- `SegmentCreationAndTarPush` builds segments and pushes the tarball payload through the controller; use it when you cannot copy segments to the data store externally (for example NFS behind the controller).
- `SegmentCreationAndMetadataPush` is the recommended choice for production when a Pinot deep store is configured: it bypasses the controller for the segment payload.
- `SegmentCreationAndUriPush` is the alternative when a deep store is configured.

Main spec sections: `executionFrameworkSpec`, `jobType`, `inputDirURI`, `includeFileNamePattern`, `excludeFileNamePattern`, `outputDirURI`, `overwriteOutput`, `pinotFSSpecs` (a scheme and class per entry), `recordReaderSpec` (`dataFormat`, reader `className`, `configClassName`, `configs`), `tableSpec` (`tableName`, `schemaURI`, `tableConfigURI`), `pinotClusterSpecs` (`controllerURI`) and `pushJobSpec` (`pushParallelism`, `pushAttempts`, `pushRetryIntervalMillis`).

The spec supports Groovy-syntax templating, so one file serves daily runs:
```
inputDirURI: 'examples/batch/airlineStats/rawdata/${year}/${month}/${day}'
```
```
bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile job.yaml -values year=2014 month=01 day=03
```

Gotcha: split creation and push (`SegmentCreation`, then a push-only type) when you want to inspect or validate segments before they become queryable. For production scale the docs recommend Hadoop or Spark runners rather than the standalone scripts.

## Checked

2026-11-09. Read the Pinot docs segment page (job spec YAML, create and push, templating sections) and the `job-specification.md` reference (jobType table). Confirmed the command, jobType values and their guidance, spec sections, push settings and the `-values` templating. Corrected: the old draft listed only three jobTypes and recommended TarPush paths without the documented MetadataPush recommendation; the `/data/${year}/` example was replaced by the page's own example. Not read: the Spark and Hadoop runner sections beyond the jobType table.
Method: documentation only; no commands were run.
