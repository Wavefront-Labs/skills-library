---
id: computing-software.cloud-infrastructure-engineering.aws.s3-notification-configuration-in-iac
name: s3-notification-configuration-in-iac
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, notification-configuration, put-bucket-notification, cloudformation, cdk, terraform, eventbridge]
level: practitioner
status: docs-checked
description: "Manage S3 bucket notifications in CloudFormation, CDK and Terraform without one stack overwriting another, ordering permissions first, and switching to EventBridge."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketNotificationConfiguration.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-s3-bucket-notificationconfiguration.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-s3/README.md", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/s3_bucket_notification.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 notification configuration in IaC

## 1. The core problem
`PutBucketNotificationConfiguration` **replaces the entire** notification configuration of
a bucket. Any tool that writes it owns all of it. Two stacks (or a stack and a console
change) adding notifications to the same bucket overwrite each other silently.

## 2. CloudFormation
- `NotificationConfiguration` lives on `AWS::S3::Bucket`, so only the stack that owns the
  bucket can set it.
- Circular dependency trap (documented): if you create the target and its permission in the same
  template, CloudFormation cannot create the bucket until the bucket has permission to invoke the function
  (it checks), and a `Ref` to the bucket in the permission makes a cycle. The documented way out is to create
  all resources without the notification configuration, then update the stack to add it.
- Properties are `NotificationConfiguration.LambdaConfigurations`, `QueueConfigurations`,
  `TopicConfigurations` and `EventBridgeConfiguration`.
- For existing buckets owned elsewhere: a custom resource that does read-modify-write of
  the configuration (merging only its own entries).

## 3. CDK
```ts
bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.SqsDestination(queue),
  { prefix: 'incoming/', suffix: '.csv' });
```
CDK implements notifications with a Lambda-backed custom resource and adds the destination's resource
policy for you. The CDK README also documents `addEventNotification` on imported buckets and a
`notificationsSkipDestinationValidation` flag. Because `PutBucketNotificationConfiguration` replaces the whole
configuration, keep one owner per bucket and test on a non-production bucket before relying on any merging.

## 4. Terraform
```hcl
resource "aws_s3_bucket_notification" "raw" {
  bucket = aws_s3_bucket.raw.id
  queue {
    queue_arn     = aws_sqs_queue.ingest.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "incoming/"
  }
  lambda_function {
    lambda_function_arn = aws_lambda_function.thumbs.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "images/"
  }
  depends_on = [aws_lambda_permission.allow_s3, aws_sqs_queue_policy.ingest]
}
```
Only **one** `aws_s3_bucket_notification` per bucket across all Terraform state; a second
one causes a perpetual diff and applying it overwrites existing notifications. Collect all destinations
in one resource (nested `queue`, `lambda_function`, `topic` blocks). The provider also has an
`aws_s3_bucket_notification` data source to adopt existing notifications.

## 5. Escape hatch: EventBridge
Enable once (`aws s3api put-bucket-notification-configuration --bucket b
--notification-configuration '{"EventBridgeConfiguration": {}}'` as part of the bucket's
config) and then any number of teams create **EventBridge rules** in their own stacks
without touching the bucket (the Terraform provider documentation recommends this pattern for shared
buckets). Rules support richer filtering (prefix, suffix, numeric and wildcard operators) and multiple targets.
EventBridge pricing applies. EventBridge must be included in the single configuration object, so the bucket
owner adds it alongside any direct destinations.

## Gotchas
- S3 verifies SNS and SQS destinations when the configuration is written, so a notification that still points at a deleted queue or topic can make later `PutBucketNotificationConfiguration` calls fail until fixed.
- Validation happens at write time: permissions must exist first (`depends_on`).
- `get-bucket-notification-configuration` is the source of truth; diff it after deploys.

## Verify
- [ ] `aws s3api get-bucket-notification-configuration --bucket b` lists every expected destination after each deploy.
- [ ] Deploying the second consumer does not remove the first (test in staging).
- [ ] For shared buckets, EventBridge enabled and consumers use rules.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: put replaces the whole configuration (botocore model), CloudFormation property names and the documented circular-dependency avoidance, CDK README behaviour (custom resource, imported buckets, skip-validation flag), Terraform resource behaviour (one resource per bucket, perpetual diff, data source, EventBridge recommendation, `depends_on` example). Removed unconfirmed CDK merge/ID-prefix behaviour and the name-string DependsOn workaround.

Method: documentation only; no commands were run.
