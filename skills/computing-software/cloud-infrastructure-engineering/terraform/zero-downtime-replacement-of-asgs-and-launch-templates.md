---
id: computing-software.cloud-infrastructure-engineering.terraform.zero-downtime-replacement-of-asgs-and-launch-templates
name: zero-downtime-replacement-of-asgs-and-launch-templates
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, zero-downtime-replacement, create-before-destroy, autoscaling-group, launch-template, instance-refresh]
level: practitioner
status: docs-checked
description: "Roll out new AMIs and launch template versions without downtime: instance_refresh, name_prefix with create_before_destroy, and blue/green ASGs behind a load balancer."
sources: ["https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/autoscaling_group", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/launch_template", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zero-downtime replacement for ASGs

## Preferred: launch template versions + instance_refresh
```hcl
resource "aws_launch_template" "app" {
  name_prefix            = "app-"
  image_id               = var.ami_id
  instance_type          = var.instance_type
  update_default_version = true
}
resource "aws_autoscaling_group" "app" {
  name                = "app"
  min_size            = 2
  max_size            = 6
  desired_capacity    = 3
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  launch_template {
    id      = aws_launch_template.app.id
    version = aws_launch_template.app.latest_version
  }
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 90
      instance_warmup        = 120
      auto_rollback          = true
    }
  }
  lifecycle { ignore_changes = [desired_capacity] }
}
```
A refresh is started whenever `launch_template`, `launch_configuration` or
`mixed_instances_policy` change on the group; `triggers` adds other properties.
Pointing `version` at `latest_version` makes a new template version change the
group, so instances roll without replacing the ASG. `strategy` must be `Rolling`.
`auto_rollback` defaults to `false` and can be `true` only with a launch template or
mixed instances policy. `min_healthy_percentage` defaults to `90`; `instance_warmup`
defaults to the group's health check grace period.

## Blue/green ASG (when the ASG itself must be replaced)
```hcl
resource "aws_autoscaling_group" "app" {
  name_prefix           = "app-"
  min_elb_capacity      = 2     # waits for healthy instances in the load balancer on creation
  wait_for_elb_capacity = 2     # also on update; takes precedence over min_elb_capacity
  # ...
  lifecycle { create_before_destroy = true }
}
```
`name_prefix` creates a unique name (conflicts with `name`) so old and new groups
can coexist. `min_elb_capacity` waits only on creation; `wait_for_elb_capacity`
applies on create and update. Set only the one you need.

## Gotchas
- `create_before_destroy` is opt-in because many remote objects have unique-name
  constraints; Terraform cannot enable a random-suffix feature for you, so use
  `name_prefix`.
- Terraform propagates `create_before_destroy` to all resource dependencies of that
  resource.
- If autoscaling policies manage `desired_capacity`, ignore it in `lifecycle` to
  avoid perpetual diffs.
- Instance refresh runs on the AWS side after the group update; monitor with
  `aws autoscaling describe-instance-refreshes --auto-scaling-group-name <NAME>`.

## Verify
- [ ] Load balancer healthy-host count never drops below the minimum during rollout.
- [ ] A plan for an AMI change shows in-place updates on the ASG, not replacement.

## Checked
2026-11-09. Confirmed against the AWS provider `aws_autoscaling_group` page (`instance_refresh` block, `strategy`, `preferences` defaults, `triggers`, `min_elb_capacity` vs `wait_for_elb_capacity`, `name_prefix`), the `aws_launch_template` page (`update_default_version`, `latest_version`, `name_prefix`), the Terraform lifecycle page (`create_before_destroy` and dependency propagation) and the botocore autoscaling model (`DescribeInstanceRefreshes`).
Removed as unconfirmed: the `AlreadyExists` error text for a fixed name with `create_before_destroy`, the claim that an in-place `~` on the template always results, and example sizes and instance type.
Method: documentation only; no commands were run.
