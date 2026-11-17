---
id: computing-software.devops-ci-cd.gitea.package-generic
name: package-generic
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-generic-package, gitea, generic-registry-put, package-upload-curl, package-file-delete, package-status-codes]
level: practitioner
status: docs-checked
description: "Publish, download and delete generic files in the Gitea package registry with curl PUT, GET and DELETE, name rules and 201, 400, 409, 404 status codes."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/packages/generic.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea generic packages

For release binaries and other build output, owned by a user or organization. Authenticate with HTTP Basic or custom headers; with 2FA or OAuth use a personal access token as the password.

## Publish
`PUT https://gitea.example.com/api/packages/{owner}/generic/{package_name}/{package_version}/{file_name}` with the file as body:
```shell
curl --user your_username:your_password_or_token \
     --upload-file path/to/file.bin \
     https://gitea.example.com/api/packages/testuser/generic/test_package/1.0.0/file.bin
```
`package_name` and `file_name` may use only `a-z A-Z 0-9 . - + _`. `package_version` is a non-empty string without leading or trailing whitespace. Same file name twice in a package is refused; delete first.
Status: `201 Created`, `400 Bad Request` (invalid name, version or file name), `409 Conflict` (file already exists).

## Download
`GET .../api/packages/{owner}/generic/{package_name}/{package_version}/{file_name}` returns the bytes as `application/octet-stream`: `200 OK` or `404 Not Found`.

## Delete
- Whole version (all files): `DELETE .../generic/{package_name}/{package_version}`, e.g. `curl --user ... -X DELETE https://gitea.example.com/api/packages/testuser/generic/test_package/1.0.0`. `204 No Content` or `404`.
- One file: `DELETE .../generic/{package_name}/{package_version}/{filename}`. If it was the last file the version goes too. `204` or `404`.

A CI upload that re-runs for the same version fails with `409`; either make versions unique per build or delete the file before uploading.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
