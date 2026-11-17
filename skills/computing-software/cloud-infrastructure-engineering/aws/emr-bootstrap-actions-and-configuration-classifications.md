---
id: computing-software.cloud-infrastructure-engineering.aws.emr-bootstrap-actions-and-configuration-classifications
name: emr-bootstrap-actions-and-configuration-classifications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, emr, bootstrap-actions, configuration-classifications, reconfigure]
level: practitioner
status: docs-checked
description: "Customise EMR with bootstrap actions and configuration classifications, reconfigure a running instance group, and know how failures behave."
sources: ["https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-bootstrap.html", "https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html", "https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps-create-cluster.html", "https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps-running-cluster.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EMR bootstrap actions and configuration classifications

## Bootstrap actions
Scripts that run on cluster instances after EMR launches them from the Amazon Linux AMI and before EMR installs the applications.
```bash
aws emr create-cluster ... \
  --bootstrap-actions Path=s3://<BUCKET>/install-libs.sh,Args=[arg1,arg2]
```
- They run as the `hadoop` user by default; use `sudo` for root.
- Up to 16 bootstrap actions per cluster.
- A nonzero exit code is a failure and EMR terminates that instance; if too many instances fail, EMR terminates the cluster, otherwise it tries to reallocate the failed ones. The cluster `lastStateChangeReason` code identifies bootstrap failures.
- To run only on the primary node, test `/mnt/var/lib/info/instance.json` for `isMaster` in the script and exit early on other nodes.
- A bootstrap action can write shutdown scripts to `/mnt/var/lib/instance-controller/public/shutdown-actions/`; each must finish within 60 seconds and is not guaranteed to run if the node terminates with an error. On EMR 4.0 and later create that directory yourself.
- Keep scripts in an S3 bucket in the same Region as the cluster for best performance.

## Configuration classifications
A configuration object has a classification, properties and optional nested configurations. Supply them as shorthand or a JSON file:
```json
[
 {"Classification":"core-site","Properties":{"hadoop.security.groups.cache.secs":"250"}},
 {"Classification":"mapred-site","Properties":{"mapreduce.map.sort.spill.percent":"0.90"}}
]
```
```bash
aws emr create-cluster ... --configurations file://configurations.json
```
- A classification usually maps to an application config file (for example `hive-site` maps to `hive-site.xml`).
- Available classifications vary by EMR release: check the release's configuration classification page.
- Configuration values appear in plaintext in Describe and List API output: do not put secrets in them (the docs point to Secrets Manager).

## Reconfigure a running cluster
From EMR 5.21.0 you can reconfigure applications per instance group in a running cluster through the console, CLI or SDK.
- You can override but not delete configuration given at cluster creation; manual edits made over SSH are reset if they differ from the supplied file.
- Core and task groups are reconfigured on a rolling basis, 10 percent of instances at a time, and affected applications restart.
- After the restart EMR checks every application is running; if one is not, the operation fails and the previous working configuration is restored.
- Each request gets a configuration version number; track it through CloudWatch events.

## Verify
- [ ] Cluster reaches a running state with no bootstrap failure in `lastStateChangeReason`.
- [ ] The intended properties appear in the application's configuration file on a node.

## Checked
2026-10-28. Confirmed in the EMR Management Guide (bootstrap actions) and EMR Release Guide pages (configure applications, create cluster, reconfigure an instance group) in `sources`; commands checked with check_commands.
Removed (not confirmed on fetched pages): the pip install sample, log paths, behaviour on nodes added by scaling, `Name=` argument, Spark/YARN/Hadoop-env/Glue example properties and the Java path, and the Secrets-less guidance beyond the warning.
Method: documentation only; no commands were run.
