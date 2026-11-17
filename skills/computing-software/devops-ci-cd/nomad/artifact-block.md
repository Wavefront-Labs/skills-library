---
id: computing-software.devops-ci-cd.nomad.artifact-block
name: artifact-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, artifact-block, artifact, go-getter, checksum, git, sshkey, archive, destination, headers, s3, hcl]
level: practitioner
status: docs-checked
description: "Fetch files and repos into a Nomad task with the artifact block using go-getter sources, destination, mode, checksum, git ref and depth, ssh keys, headers and unarchive."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/artifact.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad artifact block

`artifact` (task level) fetches a remote resource with the go-getter library before the task starts. Supported: `http`, `https`, `git`, `hg`, `S3`. Archives (`zip`, `tgz`, `bz2`, `xz`) are unpacked automatically.

```hcl
artifact {
  source      = "https://example.com/file.tar.gz"
  destination = "local/some-directory"
  options {
    checksum = "md5:df6a4178aec9fbdc1d6d7e3634d1bc33"
  }
}
```

## Parameters
- `source` (required) - go-getter URL.
- `destination` (`"local/"`) - relative to the task working directory; treated as a directory unless `mode = "file"`.
- `mode` (`"any"`) - `any`, `file` or `dir`.
- `options` - map appended to the source URL as go-getter parameters (`checksum`, `archive`, `ref`, `depth`, `sshkey`).
- `headers` - HTTP headers for http/https downloads (interpolation like `${NOMAD_ALLOC_ID}` works in values).
- `chown` (`false`) - recursively chown to the task user's uid and gid.

## Recipes
- Basic auth: put URL-encoded credentials in the host part, `https://exampleUser:pass%2Fword%21@example.com/file.txt`.
- Git: `source = "git::https://github.com/hashicorp/nomad-guides"` with `destination = "local/repo"`; pin with `options { ref = "main" depth = 1 }`.
- Private git over ssh: `options { sshkey = "${base64encode(file("/path/to/private-key"))}" }` (base64 key; on Linux `base64 -w0 <file>`). The system known-hosts file must already contain the host (for example via `ssh-keyscan`).
- Disable auto-unpack: `options { archive = false }`.
- Verify: `options { checksum = "md5:<hex>" }`; an invalid checksum returns an error.

## Gotchas
- The downloader does not inherit the client's environment variables unless the client option `artifact.set_environment_variables` allows it.
- Client `artifact` limits (size, time) interrupt the task so it fails to start; read the task events to see why.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 artifact job specification page: go-getter protocols and archive formats, destination and mode defaults, options, headers, chown, basic auth, git, ssh key, ref and depth, archive = false, checksum, environment and operation limits. Removed: the task-does-not-start wording for a checksum mismatch.

Method: documentation only; no commands were run.
