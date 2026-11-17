---
id: computing-software.cloud-infrastructure-engineering.velero.api-pagination-client-page-size
name: api-pagination-client-page-size
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [client-page-size, pagination, list-api, apiserver-request-duration, backup-performance]
level: advanced
status: docs-checked
description: "Tune Velero backup LIST pagination with the server flag --client-page-size, including disabling pagination with 0."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Velero paginates the LIST API call for each resource type in the Kubernetes API while collecting items into a backup. The Velero server flag `--client-page-size` sets the size of each page.

Depending on the cluster's scale, tuning the page size can improve backup performance. You can experiment with higher values, noting their impact on the relevant `apiserver_request_duration_seconds_*` metrics from the Kubernetes apiserver.

Setting `--client-page-size` to `0` disables pagination entirely: all items are requested in a single unpaginated LIST call.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Kubernetes API Pagination", read in full). Removed unsourced claims: memory and apiserver load warning, deployment edit and `velero install --server-args` instructions, and the comparison-backup advice.

Method: documentation only; no commands were run.
