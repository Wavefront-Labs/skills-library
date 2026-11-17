---
id: computing-software.collaboration-platform-administration.mattermost.data-retention-policy
name: data-retention-policy
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [data-retention, retention-policy, compliance, deletion-job]
level: advanced
status: docs-checked
description: "Configure Mattermost global and custom data retention, the daily deletion job, pinned post preservation, and what deletion removes and logs."
sources: ["https://docs.mattermost.com/administration-guide/comply/data-retention-policy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data retention policies

By default Mattermost keeps all message history. Enterprise customers can set a global retention policy and custom policies for channel messages, direct messages and file uploads. Warning: normal user deletions are "soft" (hidden in the UI but kept in the database), while retention deletion is permanent and irreversible, so set durations carefully.

Global policy: System Console > Compliance > Data Retention Policies, Edit on the Global retention policy table. Choose a Channel & direct message retention option and a duration in hours, days or years; older messages and attachments are deleted. Choose a File retention option the same way; expired files are removed from storage, either local disk or S3 as set in Environment > File Storage. From v10.10 you can enable Preserve pinned posts so pinned posts survive retention. Under Policy log, Edit sets the start time of the daily job; pick a quiet time.

Custom policy: Add policy in the Custom retention policies table, name it, choose durations, then Add teams or Add channels (selecting only teams covers all their channels). If a global job time exists the custom policies share it.

Run Deletion Job Now starts a run on demand. If you use Elasticsearch, make the aggregate search indexes setting larger than your retention period.

FAQ essentials: deleting removes the post from the Posts table, search and saved lists, and the file from FileInfo and storage. Clients cache posts until the cache is cleared. A Pending job with no detail usually means another run is in progress. Job status is shown on the same page; failures log "Failed job" with a job_id from worker EnterpriseDataRetention. The job runs once daily, and changing the period does not trigger an extra run. Since v5.20 audits keep their activity. Archived channels are included. Deletion runs in batches of 1000 records. DEBUG logs "Scheduling data retention job" and INFO logs "Worker EnterpriseDataRetention: Job is complete". Mobile apps v1.5+ purge expired content when opened or backgrounded.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/comply/data-retention-policy (global and custom policy, FAQ, log lines, batches of 1000). Nothing removed.

Method: documentation only; no commands were run.
