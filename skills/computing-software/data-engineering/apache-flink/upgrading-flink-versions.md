---
id: computing-software.data-engineering.apache-flink.upgrading-flink-versions
name: upgrading-flink-versions
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-version-upgrade, savepoint, state-compatibility, flink-2, migration]
level: advanced
status: docs-checked
description: "Upgrade a Flink job to a new Flink version safely: savepoint compatibility tables, connector versions, removed APIs in 2.0, and a staged rollout with rollback."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/upgrading/
  - https://nightlies.apache.org/flink/flink-docs-release-2.0/release-notes/flink-2.0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Flink versions

## Plan
1. Read release notes for every minor version you cross. Look for config key renames, default changes, removed APIs.
2. Check the **Compatibility Table** in the upgrading docs: it says which Flink versions can restore savepoints from which. "Compatible" there means the internal savepoint data format only; it does not cover SQL operator or other upper-level changes. Any change to a Table/SQL query plus a Flink version change can break state, because each new major-minor version may bring new optimizer rules or runtime operators; the community tries to keep patch versions state-compatible.
3. API guarantees: patch upgrades keep Public APIs binary compatible; minor upgrades keep source compatibility only (recompile); major upgrades (1.x to 2.x) give neither, so code changes may be required.
4. Connectors are released separately from Flink: pick the build matching the target Flink version. Connectors that depend on the removed SourceFunction, SinkFunction and Sink V1 APIs do not work on Flink 2.x.
5. Set an explicit `uid` on every stateful operator before upgrading; the docs call this a soft precondition for restore.

## Removed or changed in Flink 2.0 (release notes)
- Removed: the DataSet API (migrate to DataStream or Table/SQL), the Scala DataStream and DataSet APIs (use Java DataStream), and SourceFunction, SinkFunction and Sink V1 (use Source and Sink V2).
- `flink-conf.yaml` is no longer supported: use `config.yaml` (standard YAML); a migration tool converts old files (see the configuration docs).
- Kryo was upgraded to 5.6; prefer POJO or Avro serializers over Kryo for state you must carry across versions.
- `open(Configuration)` is replaced by `open(OpenContext)` on rich functions.

## Procedure
Two approaches are documented: in-place upgrade (stop with a savepoint, deploy the new version, restore) and shadow copy (start the new version from a savepoint next to the running job, compare, then switch).
```bash
flink stop --savepointPath <savepoint-dir> <job-id>
# deploy the job built against the new Flink version
flink run -s <savepoint-dir>/savepoint-<id> -d <job-jar>
```
- Allow non-restored state only if you intentionally removed operators.

## Rollback
Keep the old image and the pre-upgrade savepoint. Do not assume a savepoint taken by the new version restores on the old one (the compatibility table is directional), so rollback may mean replaying from source offsets. Run the new version as a shadow copy against production input first.

## Verify
- [ ] Staging restore from a production savepoint succeeds; outputs match the old version over the same input window.
- [ ] Checkpoint sizes and durations comparable after upgrade; no deprecation warnings left for keys you set.

## Checked
2026-11-09. Confirmed in the Flink upgrading page (API compatibility guarantees, compatibility table note, SQL state caveat, uid advice, in-place vs shadow copy) and the Flink 2.0 release notes (removed APIs, config.yaml, Kryo 5.6, OpenContext). Removed: canonical vs native savepoint advice, Kubernetes operator upgrade-mode advice, the Time-to-Duration and 1.19 config-file claims, and the connector version example. The upgrading page was read from the stable-docs copy as fetched; the table rows themselves were not reproduced.
Method: documentation only; no commands were run.
