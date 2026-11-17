---
id: computing-software.cloud-infrastructure-engineering.kubespray.offline-authenticated-registry-and-files-repo
name: offline-authenticated-registry-and-files-repo
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [offline, registry, containerd, credentials, ansible-vault, files-repo]
level: advanced
status: docs-checked
description: "Use credentials with an offline files_repo and registry: vaulted passwords, registry_user and registry_pass, registry mirrors header for containerd 2, registry_auth for 1.7."
sources:
  - https://kubespray.io/docs/operations/offline-environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Files repo with credentials.** Put the username and password in the URL (url-encoding):

```yaml
files_repo_host: example.com
files_repo_path: /repo
files_repo_user: download
files_repo_pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          (encrypted value)
files_repo: "https://{{ files_repo_user ~ ':' ~ files_repo_pass ~ '@' ~ files_repo_host ~ files_repo_path }}"
```

The boolean `unsafe_show_logs` makes the task "Download_file | Show url of file to download" print these credentials. Disable it in the job template when running AWX, AAP or Semaphore.

**Registry with credentials.** Set `registry_user` and `registry_pass` for `registry_addr`, and encrypt the password with ansible-vault.

**Containerd 2+** takes the credentials as a mirror header:

```yaml
containerd_registries_mirrors:
  - prefix: "{{ registry_addr }}"
    mirrors:
      - host: "https://{{ registry_addr }}"
        capabilities: ["pull", "resolve"]
        skip_verify: false
        header:
          Authorization: ["Basic {{ (registry_user + ':' + registry_pass) | b64encode }}"]
```

**Containerd 1.7** uses:

```yaml
containerd_registry_auth:
  - registry: "{{ registry_host }}"
    username: "{{ registry_user }}"
    password: "{{ registry_pass }}"
```

The page's insecure-registry example uses the same `containerd_registries_mirrors` structure with `skip_verify: true`.

## Checked

Both credential patterns and the unsafe_show_logs warning were confirmed in the Access Control section of the Offline environment page; the vault ciphertext was replaced with a placeholder.

Method: docs-checked 2026-11-09 against the Kubespray docs/operations/offline-environment.md page (full file read).
