---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-agent-log-file-collection
name: cloudwatch-agent-log-file-collection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-agent, agent-logs-collection, log-file-collection, multi-line-logs, windows-event-logs, ssm-parameter-config]
level: practitioner
status: docs-checked
description: "Collect log files with the CloudWatch agent: collect_list entries, group and stream naming, multi-line and timestamp parsing, rotation, retention and SSM fleet rollout."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/installing-cloudwatch-agent-ssm.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/troubleshooting-CloudWatch-Agent.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch agent log file collection

## 1. Config section
```json
{
  "agent": {"run_as_user": "cwagent"},
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {"file_path": "/var/log/app/app.log",
           "log_group_name": "/ec2/app/prod",
           "log_stream_name": "{instance_id}",
           "retention_in_days": 30,
           "timestamp_format": "%Y-%m-%dT%H:%M:%S.%f%z",
           "multi_line_start_pattern": "^\\d{4}-\\d{2}-\\d{2}T",
           "encoding": "utf-8"},
          {"file_path": "/var/log/nginx/access.log*",
           "log_group_name": "/ec2/nginx/access",
           "log_stream_name": "{instance_id}",
           "retention_in_days": 14}
        ]
      }
    },
    "force_flush_interval": 5
  }
}
```
- `file_path` accepts Unix glob patterns (`**` matches a directory tree); only the latest file by modification time is pushed, so use a wildcard for a series of files of one kind and a separate entry (and stream) for each other kind.
- If `log_group_name` is omitted, the `file_path` up to the final dot becomes the group name; `log_group_class` accepts `STANDARD` (default) or `INFREQUENT_ACCESS` and cannot change after creation.
- `{instance_id}` (the default stream name), `{hostname}`, `{local_hostname}` and `{ip_address}` can be used in both `log_stream_name` and `log_group_name`; other placeholders are not supported, so template the config per environment. Many per-host groups count toward the 1,000,000 log groups per Region limit.
- `retention_in_days` sets the group's retention (new group: otherwise never expire; existing group: only if you specify it). The agent role needs `logs:PutRetentionPolicy`. **Setting it on an existing group deletes older events beyond that age**, and conflicting values for one group in several entries stop the agent with an error.
- `multi_line_start_pattern` keeps stack traces as one event; `{timestamp_format}` uses
  the timestamp format as the pattern.
- `filters` (`include` or `exclude`, RE2 regex) drop noise before shipping; an event must pass all filters, and putting the filter that drops most events first is cheaper:
  `"filters": [{"type": "exclude", "expression": "GET /health"}]`.

## 2. Windows
```json
"windows_events": {"collect_list": [
  {"event_name": "System", "event_levels": ["ERROR", "CRITICAL"], "log_group_name": "/ec2/windows/system", "log_stream_name": "{instance_id}"},
  {"event_name": "Security", "event_levels": ["INFORMATION"], "log_group_name": "/ec2/windows/security", "log_stream_name": "{instance_id}"}]}
```

## 3. Fleet rollout
1. Store config in SSM Parameter Store: `aws ssm put-parameter --name AmazonCloudWatch-linux-app
   --type String --value file://cwagent.json`.
2. Install the `AmazonCloudWatchAgent` package with Run Command document `AWS-ConfigureAWSPackage`.
3. Apply config with Run Command document `AmazonCloudWatch-ManageAgent`
   (`action=configure`, `optionalConfigurationSource=ssm`,
   `optionalConfigurationLocation=AmazonCloudWatch-linux-app`, `optionalRestart=yes`), or
   on the host apply a local file with `amazon-cloudwatch-agent-ctl -a fetch-config -c file:<path>` (`append-config` adds a second configuration without replacing the first).
4. Instance role needs `CloudWatchAgentServerPolicy`.

## 4. Troubleshooting
- Agent log: `/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log`.
- `sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status` shows the running state.
- Permission denied on the file: `run_as_user` cannot read it; add to the right group or
  adjust permissions.
- Network: the host needs a route to the CloudWatch Logs endpoint.

## Verify
- [ ] Log events arrive within seconds in the expected group/stream names.
- [ ] Multi-line stack traces appear as single events.
- [ ] Retention set on agent-created groups; config versioned in Parameter Store.

## Checked
Checked 2026-10-27 against the live CloudWatch agent documentation (current release).
- Agent configuration file details: run_as_user, collect_list fields (file_path glob and latest-file behaviour, log_group_name and log_stream_name variables, log_group_class, retention_in_days behaviour and warning, filters, timestamp_format symbols, multi_line_start_pattern with {timestamp_format}, encoding, force_flush_interval), windows_events fields and event levels, fetch-config and append-config, put-parameter example.
- Installing with Systems Manager page: AWS-ConfigureAWSPackage, AmazonCloudWatchAgent package, AmazonCloudWatch-ManageAgent with configure, ssm source, location and restart, CloudWatchAgentServerPolicy.
- Troubleshooting page: agent log path and the -m ec2 -a status command.
- Removed unconfirmed claims: rotation tracking by file identity, the --tier Advanced remark, the ssm fetch-config form, copytruncate advice, the IIS path line.

Method: documentation only; no commands were run.
