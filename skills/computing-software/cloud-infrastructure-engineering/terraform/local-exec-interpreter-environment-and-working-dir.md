---
id: computing-software.cloud-infrastructure-engineering.terraform.local-exec-interpreter-environment-and-working-dir
name: local-exec-interpreter-environment-and-working-dir
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, local-exec-interpreter, local-exec-environment, local-exec, provisioners, terraform-data]
level: practitioner
status: docs-checked
description: "Configure local-exec: command, interpreter, environment for passing values instead of interpolation, working_dir and quiet, plus using terraform_data to host the provisioner."
sources: ["https://developer.hashicorp.com/terraform/language/resources/provisioners/local-exec", "https://developer.hashicorp.com/terraform/language/block/resource", "https://developer.hashicorp.com/terraform/language/resources/terraform-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `local-exec` arguments

`local-exec` runs an executable on the machine where Terraform runs, after the resource
is created (or at destroy with `when = destroy`). HashiCorp recommends purpose-built
tools over provisioners, so treat this as a last resort.

```hcl
resource "terraform_data" "bootstrap" {
  triggers_replace = [
    aws_instance.web.id,
    aws_instance.database.id
  ]

  provisioner "local-exec" {
    command     = "bootstrap-hosts.sh"
    working_dir = "scripts"
    interpreter = ["/bin/bash", "-c"]
    environment = {
      API_URL = "https://example.invalid"
    }
    quiet = true
  }
}
```

## Arguments (from the resource block reference)
| Argument | Notes |
|---|---|
| `command` | required string; absolute path or path relative to the current working directory |
| `working_dir` | where Terraform runs the command; relative to the current working directory or absolute; the directory must already exist |
| `interpreter` | list; first element is the interpreter path (relative to the working directory or absolute), the rest are its arguments; with none, Terraform uses operating system defaults |
| `environment` | key-value pairs set as the command's environment |
| `when` | the Terraform command that triggers the provisioner (see destroy-time provisioners) |
| `quiet` | boolean; stops the command line being printed |

The syntax shown on the page for `environment` is a block (`environment { KEY = VALUE }`);
the page's overview table lists it as `environment` as well. Check your Terraform version
if an assignment form (`environment = { ... }`) is rejected.

## Use `environment`, not interpolation
The docs say Terraform evaluates the command in a local shell and can use environment
variables for substitution, and recommend against putting Terraform variables straight
into the command string because it can cause shell injection. Pass values via
`environment` and reference them as environment variables in the command.

## `quiet`
Per the page, `quiet` "disables printing the command argument's output to stdout" and,
when true, Terraform prints "Suppressed by quiet=true"; the same section also says Terraform
still prints the command's output. Do not rely on `quiet` to hide secrets without testing.
Sensitive values used in provisioner blocks are suppressed in all log output.

## Hosting the provisioner
`terraform_data` implements the normal resource lifecycle without a provider (built-in
provider `terraform.io/builtin/terraform`) and is useful for triggering provisioners when
no other managed resource fits. `triggers_replace` stores a value and replaces the
resource when it changes, which re-runs creation-time provisioners.

## Failure behaviour
A failing creation-time provisioner makes `terraform apply` fail and taints the resource;
set `on_failure = continue` to ignore the error and carry on. Inside a resource, refer
to the resource with `self`, not by name.

## Checked
Date: 2026-11-07
Read in full: the provisioners overview (language/provisioners, reached by the cited local-exec URL), the resource block reference's local-exec argument sections (language/block/resource, command through quiet), and the terraform_data reference (language/resources/terraform-data).
Confirmed: every argument description above; the shell-injection recommendation; quiet behaviour as quoted; sensitive-value suppression; terraform_data purpose and triggers_replace; tainting and on_failure; `self` rule.
Removed: the OS default interpreter table (the page only says OS defaults apply), the dash/bash `[[ ]]` claim, the Python interpreter row, "path.module" and "paths resolve from the root module" claims, the HCP Terraform runner image and `jq`/`aws` remarks, "environment values are not shown in the plan's command string", and the Verify checklist.
Not opened: the destroy-time provisioner and on_failure reference sections beyond their summaries.
Method: documentation only; no commands were run.
