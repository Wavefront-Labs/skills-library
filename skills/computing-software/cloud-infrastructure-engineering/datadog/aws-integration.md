---
id: computing-software.cloud-infrastructure-engineering.datadog.aws-integration
name: aws-integration
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, aws-integration, cloudwatch, iam-role, cloud-integration]
level: practitioner
status: docs-checked
description: "Connect an AWS account to Datadog with a cross-account IAM role and the datadog_integration_aws_account Terraform resource."
sources: ["https://docs.datadoghq.com/integrations/guide/aws-terraform-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS integration
Goal: connect an AWS account to Datadog through an IAM role that Datadog assumes, using one `terraform apply`.

```
resource "datadog_integration_aws_account" "datadog_integration" {
  account_tags   = []
  aws_account_id = "<ACCOUNT_ID>"
  aws_partition  = "aws"
  aws_regions { include_all = true }
  auth_config { aws_auth_config_role { role_name = "DatadogIntegrationRole" } }
  resources_config {
    cloud_security_posture_management_collection = false
    extended_collection                          = true
  }
  traces_config { xray_services {} }
  logs_config { lambda_forwarder {} }
  metrics_config { namespace_filters {} }
}
```

- The `datadog_integration_aws_account` resource replaced `datadog_integration_aws` in version 3.50.0 of the Datadog Terraform provider.
- The role `DatadogIntegrationRole` is created in Terraform too: its trust policy allows `sts:AssumeRole` from the Datadog principal listed in the page, with a `StringEquals` condition on `sts:ExternalId` set to the resource's `auth_config.aws_auth_config_role.external_id`.
- Permissions come from the `datadog_integration_aws_iam_permissions` data source, split into several managed policies to stay under the policy size limit, plus the AWS `SecurityAudit` managed policy.
- Cloud Security collection is off in the template; set `cloud_security_posture_management_collection = true` under `resources_config` to enable it.
- Automatic log collection takes the ARN of the Datadog Forwarder Lambda function and the sources to enable (see the page's commented example).

Gotcha: keep the ExternalId condition in the trust policy; it is part of the documented setup.

## Verify
- After `terraform apply`, wait up to 10 minutes for data, then open the out-of-the-box AWS overview dashboard.

## Checked
2026-11-09. Confirmed against the Datadog documentation source for The AWS Integration with Terraform (hugo/content/en/integrations/guide/aws-terraform-setup.md in DataDog/documentation): the resource skeleton and attribute names above, the 3.50.0 replacement note, the role name, `sts:AssumeRole` with the `sts:ExternalId` StringEquals condition, the permissions data source and policy chunking, `SecurityAudit`, the Cloud Security toggle, the Forwarder ARN comment, and the 10-minute wait with the AWS overview dashboard. Removed as not supported by the page: the `include_only` region and namespace filters, "read-only permissions", CloudWatch delay of several minutes, Kinesis Firehose log forwarding, tag filters, cost remarks (CloudWatch API cost, CUR and Cloud Cost Management), the Agent-on-EC2 advice, and the Metrics Summary check on `aws.ec2.cpuutilization`.
Method: documentation only; no commands were run.
