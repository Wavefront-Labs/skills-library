---
id: computing-software.data-engineering.data-warehouse-architecture.private-connectivity-for-data-platforms
name: private-connectivity-for-data-platforms
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, private-connectivity, privatelink, vpc-service-controls, network-security]
level: advanced
status: docs-checked
description: "Keep data platform traffic off the public internet: PrivateLink for Snowflake and Databricks on AWS, VPC Service Controls for BigQuery, DNS, and egress controls."
sources:
  - https://docs.snowflake.com/en/user-guide/admin-security-privatelink
  - https://docs.databricks.com/aws/en/security/network/classic/privatelink
  - https://cloud.google.com/vpc-service-controls/docs/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private connectivity (PrivateLink / VPC Service Controls)

**Goal:** clients, pipelines and the platform talk over private networks, and data cannot be exfiltrated to unapproved destinations.

## Inbound private access to SaaS platforms
- **Snowflake on AWS**: authorize your account for PrivateLink, call `SYSTEM$GET_PRIVATELINK_CONFIG` as ACCOUNTADMIN and record the `privatelink-vpce-id` value, create the VPC endpoint, and create CNAME records in your DNS that resolve the values returned by that function to your VPC endpoint's DNS name. `SYSTEM$GET_PRIVATELINK` confirms authorization. After testing, you can optionally block public access with a Snowflake network policy that allows only a specified CIDR range. Snowflake recommends pinning private endpoints for inbound traffic. Snowflake does not configure the AWS VPC endpoints, security groups or DNS for you. Azure and GCP have their own Snowflake pages; this skill did not check them.
- **Databricks on AWS**: classic compute plane (back-end) Private Link, and inbound (front-end) Private Link for workspaces with a classic compute plane. Both need a customer-managed VPC; a dedicated subnet for the VPC endpoints is advised, and a private access settings object (reusable across workspaces in a region) is attached to the workspace. Serverless-only workspaces and outbound (serverless compute plane) Private Link do not need a customer-managed VPC.
- **GCP**: clients outside a perimeter that are on Google Cloud or on-premises use Private Google Access to reach resources inside it.

## Perimeters against exfiltration
- **VPC Service Controls (GCP)**: perimeters protect the services you specify, including Cloud Storage and BigQuery. Clients inside a perimeter cannot reach unauthorized resources outside it, and operations such as `gcloud storage cp` or `bq mk` cannot copy data out. Ingress and egress rules govern exchange across perimeters. It is independent of IAM; Google recommends using both. Use dry run mode first to monitor requests without blocking them.
- Other clouds (VPC endpoint policies, bucket policies, Azure private endpoints) are common practice but were not checked against the pages here.

## DNS is the usual failure
Snowflake's page requires the DNS record to resolve to private IP addresses in your VPC; if it resolves to public addresses, the record is not configured correctly. Test resolution from every client network. Newer Snowflake client versions use a format that helps when several accounts share a region, and OCSP host names need firewall allowance with PrivateLink.

## Gotchas
- Enabling private-only access before all clients (BI SaaS, ingestion SaaS) are connected cuts them off: inventory clients first.
- Private endpoints add cloud charges; check your provider's pricing.

## Verify
From inside the VPC, the Snowflake privatelink hostname resolves to a private IP and connections succeed; from the internet, connections are refused by the network policy.

## Checked
Date: 2026-11-09. Confirmed against the Snowflake PrivateLink page (AWS procedure, functions, CNAME, private-IP DNS, network policy), the Databricks classic Private Link page (customer-managed VPC, front-end/back-end, private access settings) and the VPC Service Controls overview (perimeters, dry run, IAM independence). Read via targeted search, not every section. Removed: Azure/GCP Snowflake endpoint names, Databricks NCC and serverless egress wording, Snowflake external access integrations, AWS/Azure perimeter specifics, nslookup hostname pattern and endpoint cost details.
Method: documentation only; no commands were run.
