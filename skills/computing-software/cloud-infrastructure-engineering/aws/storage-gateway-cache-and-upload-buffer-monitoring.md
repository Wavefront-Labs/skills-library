---
id: computing-software.cloud-infrastructure-engineering.aws.storage-gateway-cache-and-upload-buffer-monitoring
name: storage-gateway-cache-and-upload-buffer-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, storage-gateway, cache-utilization, upload-buffer, cachehitpercent, gateway-health, file-gateway]
level: practitioner
status: docs-checked
description: "Monitor and size Storage Gateway cache and upload buffer: key CloudWatch metrics per gateway type, alarms, adding cache disks, and what happens when they fill."
sources: ["https://docs.aws.amazon.com/filegateway/latest/files3/monitoring-file-gateway.html", "https://docs.aws.amazon.com/filegateway/latest/files3/Requirements.html", "https://docs.aws.amazon.com/storagegateway/latest/vgw/monitoring-volume-gateway.html", "https://docs.aws.amazon.com/storagegateway/latest/vgw/ManagingLocalStorage-common.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Gateway cache and upload buffer monitoring

## 1. Local storage roles
- **Cache** (all gateway types): recently accessed data served locally; writes land here
  before upload (S3 File Gateway uses the cache as the write buffer).
- **Upload buffer** (Volume cached/stored and Tape gateways): staging area for data waiting
  to upload to AWS.
Undersized cache means reads go to AWS (slow) and writes stall when dirty data cannot be
flushed fast enough.

## 2. Metrics that matter (namespace `AWS/StorageGateway`, dimension GatewayId/GatewayName)
| Metric | Meaning | Alarm when |
|---|---|---|
| `CachePercentUsed` | cache space used | sustained > 90% is normal for a full cache, look at dirty instead |
| `CachePercentDirty` | share of cache not yet uploaded | > 50% sustained (uploads cannot keep up) |
| `CacheHitPercent` | reads served from cache | < 80% for workloads expected to be warm |
| `CloudBytesUploaded`, `CloudBytesDownloaded` | throughput to/from AWS | compare with link bandwidth |
| `WriteBytes` | client write load | trend |
| `HealthNotifications`, `AvailabilityNotifications` | gateway health events | any |
| `IoWaitPercent` | local disk latency | > 10% (slow cache disks) |
| `FilesFailingUpload` (File Gateway) | objects that cannot upload (permissions, KMS) | > 0 |

Example alarm:
```bash
aws cloudwatch put-metric-alarm --alarm-name sgw-dirty-high --namespace AWS/StorageGateway \
  --metric-name CachePercentDirty --dimensions Name=GatewayId,Value=sgw-12AB34CD Name=GatewayName,Value=office-fgw \
  --statistic Average --period 300 --evaluation-periods 6 --threshold 50 \
  --comparison-operator GreaterThanThreshold --alarm-actions <sns-arn>
```
Also enable the gateway's CloudWatch log group for File Gateway audit/health logs.

## 3. Sizing rules of thumb
- Heuristic: cache at least the size of the active working set plus a day's writes. Documented limits for S3 File Gateway: cache minimum 150 GiB, maximum 64 TiB.
- Upload buffer sizing for Volume and Tape gateways: follow the sizing guidance in their user guides; with a slow WAN, size for peak write bursts.
- Use fast local storage (SSD) for cache; `IoWaitPercent` high points to slow disks.

## 4. Adding capacity
Add a new virtual disk to the VM/EC2 instance, then:
```bash
aws storagegateway list-local-disks --gateway-arn <arn>
aws storagegateway add-cache --gateway-arn <arn> --disk-ids <disk-id>
aws storagegateway add-upload-buffer --gateway-arn <arn> --disk-ids <disk-id>
```
When adding cache to an existing gateway, create new disks; do not resize disks already allocated as cache.
Maximum cache for an S3 File Gateway is 64 TiB.

## 5. When things fill
- Treat a cache that stays full of dirty data as an outage risk: add cache and check upload bandwidth.
- A full upload buffer on a Volume or Tape gateway: add buffer and let uploads catch up; see their troubleshooting pages for volume states.
- Bandwidth throttling schedules (`update-bandwidth-rate-limit-schedule`) may be too strict
  during business hours.

## Verify
- [ ] Alarms on CachePercentDirty, HealthNotifications and FilesFailingUpload exist per gateway (plus upload buffer alarms for Volume and Tape gateways).
- [ ] CacheHitPercent meets expectations under normal load.
- [ ] Dirty data drains overnight back to near zero.

## Checked

Checked 2026-10-27 against the S3 File Gateway User Guide pages on monitoring (Understanding gateway metrics) and requirements, the Volume Gateway monitoring pages, and the botocore storagegateway model.
Confirmed for S3 File Gateway: metrics CachePercentUsed, CachePercentDirty, CacheHitPercent, CacheFree, CloudBytesUploaded, CloudBytesDownloaded, FilesFailingUpload, HealthNotifications, AvailabilityNotifications, IoWaitPercent, WriteBytes; the CloudWatch log group option for health logs; cache minimum 150 GiB and maximum 64 TiB; guidance to add new disks rather than resize cache disks; add-cache, add-upload-buffer, list-local-disks and update-bandwidth-rate-limit-schedule operations. Removed upload buffer metric names, the QueuedWrites metric, the 20 percent sizing rule and the volume state names because they could not be confirmed on a readable page; alarm thresholds in the table are suggestions, not documented limits.

Method: documentation only; no commands were run.
