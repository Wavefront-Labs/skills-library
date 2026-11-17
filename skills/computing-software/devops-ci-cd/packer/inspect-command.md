---
id: computing-software.devops-ci-cd.packer.inspect-command
name: inspect-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [inspect, template, machine-readable, variables, cmd-inspect]
level: practitioner
status: docs-checked
description: "packer inspect lists a template's variables, locals, builds, sources, provisioners and post-processors."
sources:
  - https://developer.hashicorp.com/packer/docs/commands/inspect/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer inspect` takes a template and outputs the components it defines: the variables it accepts, the builders (sources) it defines, the provisioners and the order they will run, and more. It lets you learn a template without reading the HCL.

```text
$ packer inspect template.pkr.hcl
> input-variables:

var.aws_access_key: "<sensitive>"
var.aws_secret_key: "<sensitive>"

> local-variables:

> builds:

  > <unnamed build 0>:

    sources:

      amazon-ebs.foo
      amazon-instance.bar
      virtualbox-iso.basic

    provisioners:

      shell

    post-processors:

      <no post-processor>
```

It is extra useful with machine-readable output enabled, which makes the components parseable by machines. It does not validate the configuration of the components (that is `packer validate`), but it validates template syntax by necessity.

## Checked

2026-11-08. Read the full inspect command page (Packer 1.16 docs source). Removed unsourced claims about credentials and CI usage.

Method: documentation only; no commands were run.
