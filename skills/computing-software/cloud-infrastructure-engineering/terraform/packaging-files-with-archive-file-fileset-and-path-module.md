---
id: computing-software.cloud-infrastructure-engineering.terraform.packaging-files-with-archive-file-fileset-and-path-module
name: packaging-files-with-archive-file-fileset-and-path-module
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, archive-file, local-file-data, filesystem-functions, fileset, path-module, lambda-packaging, file-function]
level: practitioner
status: verified
description: "Package and upload local files with archive_file, local_file, fileset() and path.module/path.root: Lambda zips, S3 sync of a directory, and avoiding perpetual diffs."
sources: ["https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file", "https://registry.terraform.io/providers/hashicorp/local/latest/docs/data-sources/file", "https://developer.hashicorp.com/terraform/language/functions/fileset", "https://developer.hashicorp.com/terraform/language/expressions/references#filesystem-and-workspace-info"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Files: `archive_file`, `local_file`, `fileset()`, `path.*`

## Paths
- `path.module` — directory of the current module. Use for files shipped with a module.
- `path.root` — root module directory. `path.cwd` — where Terraform was run (avoid).
- Never hard-code relative paths without `path.module`: they break when the module is
  called from elsewhere.

## Lambda zip
```hcl
data "archive_file" "fn" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/.build/fn.zip"
  excludes    = ["__pycache__", "tests"]
}
resource "terraform_data" "fn" {   # stand-in for a function resource that takes a zip and a hash
  input = {
    filename         = data.archive_file.fn.output_path
    source_code_hash = data.archive_file.fn.output_base64sha256
  }
}
```
A hash argument such as `source_code_hash` (on the real function resources) makes code changes, and only code changes, show in the plan:
`output_base64sha256` changed only when file contents changed (touching a file's modified time, including setting it to 2001, left the hash unchanged),
`excludes = ["__pycache__", "tests"]` kept both out of the zip (`['app.py']`), and the `.build/` output directory was created by the data source.

## Upload a directory to S3
```hcl
resource "terraform_data" "site" {   # stand-in for one object-upload resource per file
  for_each = fileset("${path.module}/site", "**")
  input = {
    key          = each.value
    source       = "${path.module}/site/${each.value}"
    etag         = filemd5("${path.module}/site/${each.value}")
    content_type = lookup(local.mime, regex("\\.[^.]+$", each.value), "application/octet-stream")
  }
}
```
`fileset` patterns: `*`, `**`, `?`, `{a,b}`; returns paths relative to the base, files only. Tested on Windows with `site/index.html` and
`site/css/a.css`: `*` gave `["index.html"]`, `**` gave `["css/a.css","index.html"]` (no directory entries), `i?dex.html` and `*.{html,css}` matched
`index.html`, the instance keys were `css/a.css` and `index.html`, and `content_type` resolved to `text/css` and `text/html`.
A brace group that contains a path separator (`{index.html,css/a.css}`) failed on Windows with `failed to glob pattern ... syntax error in pattern`; keep separators outside the braces.

## Reading files
- `file(path)` — UTF-8 text at plan time; `filebase64()` for binary.
- `data "local_file"` — same, but as a data source (useful when the file is produced by
  another resource in the same run: reading is deferred until it exists).
- `templatefile()` for rendering.

## Gotchas
- Zips must be reproducible: archive_file normalises timestamps, but files generated
  in CI with different permissions change the hash. Set `output_file_mode = "0666"` (an `archive_file` data source argument; present in the
  provider schema of `hashicorp/archive` 2.8.1).
- `.build/` must be in `.gitignore` (the data source writes the zip there).
- `file()` on a file created during apply errors at plan time (`no file exists at "./made.txt"; this function works only with files that are
  distributed as part of the configuration source code`) — use the `local_file` data source with a dependency (its content showed `(known after apply)`
  in the plan and `"made"` after apply), or build artifacts before Terraform.
- Large directories via `fileset` → thousands of resources; use a sync tool for big sites.

## Verify
- [ ] Two consecutive plans with no code change show `No changes` for the Lambda.
- [ ] Editing one file in `site/` changes exactly one per-file resource (`etag` is the file's md5).

## Checked
- Terraform 1.17.0 with `hashicorp/archive` 2.8.1 and `hashicorp/local` on Windows: every snippet in the Paths/Lambda/S3/Reading sections ran with `terraform_data` stand-ins for the AWS resources; two consecutive plans showed `No changes`; changing one file changed `output_base64sha256`; `fileset` and `file()`/`local_file` behaviour as quoted above; `output_file_mode` appears in the data source schema.
- `path.module` was `.` in the root and `sub` in a child module, `path.root` was `.` in both, `path.cwd` was the absolute working directory.
- The AWS resources themselves (`aws_lambda_function`, `aws_s3_object`) were replaced by stand-ins in the examples, and the HCP Terraform remark was removed.
