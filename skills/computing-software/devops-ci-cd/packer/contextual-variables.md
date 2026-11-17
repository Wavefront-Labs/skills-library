---
id: computing-software.devops-ci-cd.packer.contextual-variables
name: contextual-variables
category: computing-software
field: devops-ci-cd
product: packer
tags: [build-variables, packerruntime, ssh-key, connection, contextual-vars]
level: practitioner
status: docs-checked
description: "Use build.*, packer.version and source.* variables inside provisioners and post-processors."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/contextual-variables/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Contextual variables return connection and basic instance state information and depend on the configuration context. They are used from provisioners and post-processors.

`build` variables (all special build variables live in `build`; the page marks them as beta):

- `build.name`: the name of the build block, different from the source block name.
- `build.ID`: the VM being provisioned: the instance ID on Amazon, the Droplet ID on DigitalOcean, the VM name on VMware.
- `build.Host`, `build.Port`, `build.User`, `build.Password`: what Packer uses to access the machine; useful for running Ansible or Inspec against the instance from a shell-local provisioner.
- `build.ConnType`: the communicator type, for example "ssh" for the SSH communicator.
- `build.PackerRunUUID`: the current build's unique ID, usable to name artifacts so concurrent builds do not collide.
- `build.PackerHTTPIP`, `build.PackerHTTPPort`, `build.PackerHTTPAddr`: the IP, port and `IP:PORT` address of the file server Packer creates to serve the "http" dir to the VM.
- `build.SSHPublicKey`, `build.SSHPrivateKey`: the keys Packer uses to connect. They exist only with the SSH communicator and are unset otherwise. They can contain escape sequences and special characters, so single-quote them, for example `echo '${build.SSHPrivateKey}' > /tmp/packer-session.pem`.
- `WinRMPassword` remains available for backwards compatibility and equals `Password`.

All build variables work with HCL2 functions, for example `${upper(build.ID)}`. For builder-specific variables see the builder docs.

`source` variables: `source.name` and `source.type` give the name and type of the source being built, e.g. `echo ${source.name} and ${source.type}`. With a build named `roles` and a source renamed `consul`, `roles.null.consul` returns `consul` and `null`.

`packer.version` is the running Packer version: the release number only on a released build, or release number, dev flag and commit on a development build (e.g. `1.6.5-dev (a69392129+CHANGES)`). Wrap it in single quotes in shell commands, since the parentheses can break escaping.

When a build pushes metadata to HCP Packer, `packer.versionFingerprint` is set to the version fingerprint of the run. `packer.iterationID` is deprecated and slated for removal; use the fingerprint.

```hcl
provisioner "shell-local" {
  inline = ["echo ${source.type}.${source.name} on ${build.Host}"]
}
```

## Checked

Method: docs-checked 2026-11-09 against the Packer contextual variables page and its included source-variables section (both read in full as published page source). Dropped the claims about build.Host fill-in varying by builder and about not echoing the password, which are not on the page; added the HCP fingerprint and deprecation facts.
