---
id: computing-software.cloud-infrastructure-engineering.ansible.sharing-controller-credentials-and-prompt-on-launch-fields
name: sharing-controller-credentials-and-prompt-on-launch-fields
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-credentials, credential-sharing, credential-prompt, machine-credential]
level: practitioner
status: draft
description: "Share credentials safely via organization and team Use roles, and use prompt-on-launch credential fields (passwords, key passphrases, vault) for interactive or per-run secrets."
sources: ["Automation controller user guide - credentials (https://docs.ansible.com/automation-controller/latest/html/userguide/credentials.html)", "Job templates - prompt on launch (https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sharing credentials and prompt-on-launch fields

## Sharing model
- A credential belongs to one organization (or is private to a user if no org).
- **Use** role: may attach it to templates/inventories and run with it, never see the secret.
- **Admin** role: may edit (still cannot read encrypted values back through the UI/API; they are write-only).
- Grant `use` to teams that build templates; job runners need only Execute on templates that already carry the credential.

```yaml
- ansible.controller.credential:
    name: prod-ssh
    organization: Platform
    credential_type: Machine
    inputs:
      username: automation
      ssh_key_data: "{{ lookup('file', 'keys/prod_ed25519') }}"
- ansible.controller.role:
    team: template-builders
    role: use
    credentials: [prod-ssh]
```
Cross-organization use is not possible: duplicate the credential (via config as code from the same vault source) or use an external secret lookup in each org.

## Prompt-on-launch fields
Machine credential fields can be set to "Prompt on launch" (`ASK`):
```yaml
inputs:
  username: automation
  password: ASK                 # asked at launch
  ssh_key_unlock: ASK           # passphrase for an encrypted key
  become_password: ASK
```
Vault credentials can ask for the vault password similarly. The template then cannot run unattended (schedules, webhooks, workflows without prompts fail), so use it for break-glass templates only.

Template-level "Prompt on launch" for **credentials** lets the launcher pick which credentials to use (of those they have Use on).

## Gotchas
- Encrypted SSH keys without a stored passphrase fail with "Passphrase required" unless `ssh_key_unlock` is set or ASK.
- Rotating a shared credential's secret affects every template using it at once: coordinate or version credentials (`prod-ssh-2026`).

## Verify
- [ ] A team member with Execute only can run the template but sees no secret fields.
