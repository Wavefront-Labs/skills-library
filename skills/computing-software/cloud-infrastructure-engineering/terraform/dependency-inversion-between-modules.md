---
id: computing-software.cloud-infrastructure-engineering.terraform.dependency-inversion-between-modules
name: dependency-inversion-between-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, dependency-inversion, module-composition, module-design, module-interface]
level: practitioner
status: docs-checked
description: "Compose modules by passing IDs and objects in rather than having modules create or look up their own dependencies, following HashiCorp's dependency inversion guidance."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/composition#dependency-inversion", "https://developer.hashicorp.com/terraform/language/modules/develop/composition"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency inversion between modules

## The idea
A module should **receive** the objects it depends on as inputs, not create them or
discover them itself. The root module composes modules and wires outputs to inputs.
HashiCorp strongly recommends keeping the module tree flat, with only one level of
child modules, and using expressions to describe relationships between modules.

Bad (module hides its dependency):
```hcl
# modules/app/main.tf
data "aws_vpc" "main" { tags = { Name = "main" } }        # assumes a VPC named "main"
resource "aws_vpc" "this" { ... }                          # or creates its own VPC
```
Good:
```hcl
# modules/app/variables.tf
variable "vpc_id"     { type = string }
variable "subnet_ids" { type = list(string) }

# root main.tf
module "network" { source = "./modules/network" }
module "app" {
  source     = "./modules/app"
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.private_subnet_ids
}
```

## Benefits
- A module that embeds its own network is hard to coexist with other infrastructure in
  that network; keep modules small and pass dependencies in.
- The module does not know or care how the identifiers are obtained. If the network
  later moves to its own configuration, the root can pass the same values from data
  sources instead.
- The root can connect the same modules in different ways to produce different
  results.

## Conditional creation: pass the object in
When an object exists in some environments and must be created in others, do not write
a module that detects it. Accept the object through an input variable typed with only
the attributes the module needs (Terraform accepts any object with at least those
attributes), and let the caller supply either a managed resource or a data source:
```hcl
variable "ami" {
  type = object({
    id           = string
    architecture = string
  })
}

# caller, AMI managed here:      ami = aws_ami_copy.example
# caller, AMI already exists:    ami = data.aws_ami.example
```
The caller then states explicitly which case applies, and a future reader does not
have to inspect remote state to understand the intent.

## Passing whole objects
For many attributes, pass an object rather than ten scalars, using the same
"at least these attributes" typing:
```hcl
variable "network" {
  type = object({
    vpc_id             = string
    private_subnet_ids = list(string)
  })
}
```
If the caller's object does not have those attributes, build the object in the root.

## Related: data-only modules
A module may contain only data sources, to encapsulate how shared infrastructure is
looked up; the source of the data can change without updating every consumer.

## Checked
Date: 2026-11-07
Read in full: Module Composition page (modules/develop/composition), including the Dependency Inversion, Conditional Creation of Objects, Assumptions and Guarantees, Multi-cloud Abstractions and Data-only Modules sections (both cited URLs resolve to this one page).
Confirmed: flat tree with one level of child modules; modules receive dependencies from the root; a self-contained network makes coexistence hard; refactor to data-source values without the module caring; conditional-creation pattern with an object-typed variable that accepts any object having at least the declared attributes; data-only modules.
Removed: "no depends_on needed", the "test fixture" benefit, the "TF >= 0.12 allows module reference objects" claim, the section on aws_caller_identity/aws_region/aws_partition lookups, and the Verify checklist (none of these are stated on the page).
Method: documentation only; no commands were run.
