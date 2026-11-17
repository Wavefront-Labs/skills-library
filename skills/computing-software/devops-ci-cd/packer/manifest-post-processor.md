---
id: computing-software.devops-ci-cd.packer.manifest-post-processor
name: manifest-post-processor
category: computing-software
field: devops-ci-cd
product: packer
tags: [manifest, artifacts, json, ci, pp-manifest]
level: practitioner
status: docs-checked
description: "Record build artifacts into packer-manifest.json, with strip_path, strip_time and custom_data."
sources:
  - "https://developer.hashicorp.com/packer/docs/post-processors/manifest/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `manifest` post-processor writes a JSON file listing all the artifacts Packer produced during a run, so that with multiple builds you can tell which output (files, AMI IDs, Docker containers) belongs to which build. It is invoked each time a build completes and updates the manifest file. Builds are identified by name and type and include build time, artifact ID and file list.

```hcl
post-processor "manifest" {
  output     = "manifest.json"
  strip_path = true
  custom_data = {
    my_custom_data = "example"
  }
}
```

Settings (all optional):

- `output`: file to write; defaults to `packer-manifest.json`.
- `strip_path`: write only the filename without the path; defaults to false.
- `strip_time`: do not write the `build_time` field.
- `custom_data`: map of strings added to the manifest. It is a template engine field, so user variables and template functions can be used.

Behaviours:

- With `-force`, the manifest file is truncated automatically during each run. Otherwise subsequent builds are added to the file, and you can use timestamps to see which is latest.
- Re-running a build adds to the manifest rather than replacing it; specific builds can be picked out with `packer_run_uuid`. The file has a `builds` list and a `last_run_uuid`.
- You can specify `manifest` more than once, writing each build to its own file or all to one, and chain it with other post-processors such as Docker and Artifice.
- `keep_input_artifact` does not apply: the input artifact is always retained, because deleting the files just recorded is not expected behaviour.

The manifest is useful for cleaning up old artifacts or printing values to logs. The docs find an AMI ID with jq:

```bash
AMI_ID=$(jq -r '.builds[-1].artifact_id | split(":") | .[1]' manifest.json)
```

## Checked

Method: docs-checked 2026-11-09 against the Packer manifest post-processor page and its generated optional configuration reference (read in full as published page source).
