---
id: computing-software.devops-ci-cd.packer.aws-secretsmanager-function
name: aws-secretsmanager-function
category: computing-software
field: devops-ci-cd
product: packer
tags: [aws-secretsmanager, secrets, function, aws, fn-secretsmanager]
level: advanced
status: docs-checked
description: "Read a secret from AWS Secrets Manager with aws_secretsmanager(name, key); it always fetches the AWSCURRENT version."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/contextual/aws_secretsmanager/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`aws_secretsmanager(name, key)` returns a secret stored in AWS Secrets Manager. Support always obtains the latest version, essentially `AWSCURRENT`; previous versions are not supported.

```hcl
locals {
  secret = aws_secretsmanager("multikey/secret", "shell")
}
```

You can use the function in a `locals` block or inline where you want the value, for example in a provisioner's `inline` commands.

Behaviour of the key argument:

- When `key` is `null` or empty (`""`), the function returns the first secret key stored in secret `name`. This is how you read single-key and plaintext secrets.
- For a secret with several keys, set `key` to the one you want. Given `{"test": "kitchen", "shell": "powershell"}`, `key = "shell"` returns `powershell`.

To use it you must configure valid AWS credentials by one of: environment variables, CLI configuration files, container credentials or instance profile credentials.

To hide the value in output, wrap it in a singular `local` block with `sensitive = true` (a `local` block's sensitive flag filters the value from logs, as described on the Packer local variables page):

```hcl
local "db_password" {
  expression = aws_secretsmanager("db", "password")
  sensitive  = true
}
```

## Checked

Method: docs-checked 2026-11-09 against the Packer aws_secretsmanager function page (read in full as published page source); the sensitive local behaviour was confirmed on the Packer local variables page. Dropped the vault() comparison, the claim about IAM permissions and the rotation remark.
