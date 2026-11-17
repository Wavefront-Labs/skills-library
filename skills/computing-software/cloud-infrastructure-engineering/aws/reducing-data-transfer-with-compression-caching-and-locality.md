---
id: computing-software.cloud-infrastructure-engineering.aws.reducing-data-transfer-with-compression-caching-and-locality
name: reducing-data-transfer-with-compression-caching-and-locality
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, data-transfer, transfer-compression, data-locality, caching, cross-az-traffic, egress-reduction]
level: practitioner
status: draft
description: "Cut AWS data transfer bills by design: compress payloads and streams, cache at the edge and in-region, keep chatty traffic AZ-local, and move compute to the data."
sources: ["AWS Well-Architected Cost Optimization Pillar - Plan for data transfer", "Amazon CloudFront Developer Guide - Serving compressed files", "Amazon MSK Developer Guide - Best practices (rack awareness, follower fetching)", "Elastic Load Balancing documentation - Cross-zone load balancing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing data transfer with compression, caching and locality

## Compression
| Where | How |
|---|---|
| Web/API responses | CloudFront automatic compression (gzip/Brotli) with a cache policy enabling compression; app-level `Content-Encoding` for APIs |
| Kafka/MSK | `compression.type=zstd` (or lz4) on producers: cuts cross-AZ replication and client traffic |
| Kinesis | KPL aggregation plus compressed payloads |
| Logs | agents and Firehose with gzip; Parquet/ORC for analytics data |
| Service-to-service | gRPC/protobuf instead of verbose JSON; request only needed fields |
Typical text payloads shrink 70-90%.

## Caching
- CloudFront in front of S3, ALB and API Gateway: fewer origin bytes, cheaper egress tiers.
- ElastiCache/DAX in the same AZ as callers for hot reads instead of cross-region or cross-AZ database reads.
- Client-side caching headers (`Cache-Control`, ETags) to avoid re-downloads.

## Locality
- **Cross-AZ costs** both directions per GB: keep chatty pairs in the same AZ where availability allows:
  - MSK: rack awareness and follower fetching (`client.rack` = AZ id) so consumers read from a same-AZ replica.
  - Load balancers: NLB cross-zone load balancing off (on means cross-AZ traffic charges for NLB); ALB cross-zone is free but routes across AZs.
  - Service meshes/ECS Service Connect/Kubernetes topology-aware routing to prefer same-zone endpoints.
  - Aurora: AZ-local custom reader endpoints for heavy readers.
- **Cross-region:** process data in the region it lives (Athena, EMR, Redshift next to the bucket); replicate only aggregates.
- **AWS service traffic without NAT:** gateway endpoints for S3/DynamoDB; interface endpoints where volume justifies the hourly fee.
- **Edge filtering:** drop or sample data at the source (IoT Greengrass, Lambda@Edge) before sending.

## Measure
Cost Explorer by usage type (`DataTransfer-Regional-Bytes` for cross-AZ, `AWS-Out-Bytes` inter-region,
`DataTransfer-Out-Bytes` internet, `NatGateway-Bytes`); VPC Flow Logs with `pkt-src-aws-service`/AZ fields to attribute flows.

## Verify
- [ ] Top 5 transfer usage types have an owner and a reduction action.
- [ ] Compression enabled on CloudFront behaviours and Kafka producers; measured before/after bytes.
