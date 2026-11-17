---
id: computing-software.cloud-infrastructure-engineering.terraform.moved-blocks-into-modules-and-count-to-for-each
name: moved-blocks-into-modules-and-count-to-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, moved-block, moved-to-module, module-move, count-to-for-each, moved-count-to-for-each, refactoring]
level: practitioner
status: verified
description: "Write moved blocks to pull resources into or out of modules and convert count to for_each without destroy/recreate, including generating many blocks."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/refactoring", "https://developer.hashicorp.com/terraform/language/block/moved", "https://opentofu.org/docs/language/modules/develop/refactoring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `moved` blocks: modules and count → for_each

## Into a module
```hcl
module "app" {
  source = "./modules/app"
}

moved {
  from = aws_instance.web
  to   = module.app.aws_instance.web
}
moved {
  from = aws_security_group.web
  to   = module.app.aws_security_group.web
}
```
Out of a module is the mirror image. Renaming a module call:
`moved { from = module.old  to = module.new }` moves everything inside.

## count → for_each
```hcl
resource "aws_subnet" "private" {
  for_each   = var.private_subnets          # { "eu-west-1a" = "10.0.1.0/24", ... }
  cidr_block = each.value
  availability_zone = each.key
}

moved {
  from = aws_subnet.private[0]
  to   = aws_subnet.private["eu-west-1a"]
}
moved {
  from = aws_subnet.private[1]
  to   = aws_subnet.private["eu-west-1b"]
}
```
Map the old indices to keys by checking `terraform state show 'aws_subnet.private[0]'`
- never assume list order equals key order (in the test, index 0 held the value that
belonged to the second key).

Adding/removing `count` on a **resource** needs nothing: Terraform treats `aws_x.y` and
`aws_x.y[0]` as the same object automatically (plan: `x has moved to x[0]`). Module calls
do **not** get this: adding `count = 1` to `module "db"` plans destroy of `module.db...` and
create of `module.db[0]...`, so add
`moved { from = module.db  to = module.db[0] }`.

## Generating many blocks
```bash
terraform state list 'aws_subnet.private' | while read -r a; do
  az=$(terraform state show "$a" | awk -F'"' '/availability_zone /{print $2}')
  printf 'moved {\n  from = %s\n  to   = aws_subnet.private["%s"]\n}\n' "$a" "$az"
done > moved.tf
```

## Gotchas
- `from` and `to` must be the same resource type, except for provider-supported cross-type
  moves (Terraform 1.8+, e.g. `null_resource` to `terraform_data`; see the moved-limitations
  skill).
- Plan must show `has moved to` lines and **no** create/destroy for those addresses;
  if it still shows destroy, a key or index is wrong.
- Moves apply on the next `apply`; a `-target` that leaves out a moved resource fails
  with `Error: Moved resource instances excluded by targeting` and lists the `-target`
  options to add.
- Keep moved blocks until every workspace/environment has applied.

## Verify
- [ ] `terraform plan` lists each `# aws_subnet.private[0] has moved to aws_subnet.private["eu-west-1a"]`.
- [ ] Plan summary shows `0 to add, 0 to destroy` for the refactor commit.

## Checked
- Terraform 1.17.0 with `terraform_data` and a local module: moving two root resources into `module.app` with `moved` blocks, count-to-`for_each` with per-index `moved` blocks (plan showed every `has moved to` line and `0 to add, 0 to change, 0 to destroy`; a wrong or missing mapping planned destroy/create), renaming a module call with `moved { from = module.service to = module.app2 }`, and adding `count = 1` to a resource (automatic) and to a module (needed the moved block) all ran as described; the generation loop (`state list | while read ... awk ... printf`) produced correct `moved` blocks (it matched `input` in place of `availability_zone`); `-target` that excluded a moved resource failed with the quoted error. Module renames need `terraform init` again.
- AWS resource names are the same address syntax; `aws_subnet.availability_zone` is in the provider docs source.
