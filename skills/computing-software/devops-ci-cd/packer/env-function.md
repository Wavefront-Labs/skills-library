---
id: computing-software.devops-ci-cd.packer.env-function
name: env-function
category: computing-software
field: devops-ci-cd
product: packer
tags: [env, function, environment-variable, default, fn-env]
level: intro
status: docs-checked
description: "The env function reads environment variables, and only works inside a variable's default."
sources:
  - https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/contextual/env/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`env("NAME")` gets the value of an environment variable inside input variables. It is the only function callable from a `variable` block, and it works only in the `default` input.

```hcl
variable "aws_region" {
  default = env("AWS_DEFAULT_REGION")
}
```

The variable takes the environment value unless it is also set in a manner that takes precedence (variable definition precedence).

Why only there: user variables are meant to be the single source of configurable input. Allowing environment variables anywhere in a configuration would confuse users about a template's possible inputs; confined to defaults, inputs stay discoverable with `packer inspect`.

If the environment variable is not set at all, `env` returns an empty string rather than an error. To force it to be set, add a custom validation rule:

```hcl
variable "aws_region" {
  default = env("AWS_DEFAULT_REGION")

  validation {
    condition     = length(var.aws_region) > 0
    error_message = <<EOF
The aws_region var is not set: make sure to at least set the AWS_DEFAULT_REGION env var.
To fix this you could also set the aws_region variable from the arguments, for example:
$ packer build -var=aws_region=us-something-1...
EOF
  }
}
```

## Checked

2026-11-08. Read the full env function page (Packer 1.16 docs source). Removed unsourced claims about PKR_VAR_, hcl2_upgrade and sensitive marking.

Method: documentation only; no commands were run.
