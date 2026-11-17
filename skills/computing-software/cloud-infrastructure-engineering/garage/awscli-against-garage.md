---
id: computing-software.cloud-infrastructure-engineering.garage.awscli-against-garage
name: awscli-against-garage
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [awscli, aws-endpoint-url, s3-client, awsrc]
level: intro
status: docs-checked
description: "Configure awscli with an endpoint, region and Garage key, then list, upload and download objects."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Quick Start uses awscli as its example S3 client. Install it with `python -m pip install --user awscli`, then save the connection details in a sourceable file such as `~/.awsrc`:

- `export AWS_ENDPOINT_URL='http://localhost:3900'`
- `export AWS_DEFAULT_REGION='garage'`
- `export AWS_ACCESS_KEY_ID=` the Garage key ID
- `export AWS_SECRET_ACCESS_KEY=` the Garage secret

The region must match `s3_region` in the `[s3_api]` section, which the guide sets to `garage`. The `AWS_ENDPOINT_URL` variable needs awscli 1.29.0 or later, or 2.13.0 or later; older versions require `--endpoint-url` on every call.

Run `source ~/.awsrc` whenever you want to talk to that cluster. Keeping several files, one per cluster or key, makes switching a matter of sourcing the right one.

Example commands from the guide:

- `aws s3 ls` lists buckets
- `aws s3 ls s3://default-bucket` lists objects
- `aws s3 cp /proc/cpuinfo s3://default-bucket/cpuinfo.txt` uploads
- `aws s3 cp s3://default-bucket/cpuinfo.txt /tmp/cpuinfo.txt` downloads

Garage does not implement every S3 feature, for example ACLs and bucket policies, so check the S3 compatibility list. Other documented clients are minio-client, s3cmd, rclone, Cyberduck and WinSCP.

## Checked

2026-11-04. Read the Quick Start page in full. Confirmed the pip install line, the four exported variables, the awscli version gates, the source step, the four example commands, the ACL and policy remark and the other client list. The region/s3_region link is confirmed by the Configuration page (requests for other regions fail with AuthorizationHeaderMalformed). Nothing removed.
Method: documentation only; no commands were run.
