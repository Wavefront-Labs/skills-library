---
id: computing-software.cloud-infrastructure-engineering.ansible.signing-collections-and-validating-signatures-in-automation-hub
name: signing-collections-and-validating-signatures-in-automation-hub
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, automation-hub, collection-signing, gpg-sign, hub-signing, signature-validation, keyring]
level: advanced
status: docs-checked
description: "Make ansible-galaxy verify GPG signatures of collections at install and afterwards: keyrings, extra signatures, required counts, ignored status codes and requirements.yml."
sources: ["https://docs.ansible.com/projects/ansible/latest/collections_guide/collections_installing.html", "https://docs.ansible.com/projects/ansible/latest/collections_guide/collections_verifying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing collections and validating signatures

A distribution server that signs a collection provides ASCII-armored, detached signatures used to verify the authenticity of the collection's `MANIFEST.json` before the manifest is used to verify the contents. Not every distribution server supports signing: check the "Distributing collections" table in the Ansible docs. Setting up signing inside a private automation hub (signing service, installer variables) is covered by the Red Hat documentation for your hub version, which could not be read as text in this review.

## Verifying at install
```bash
gpg --import --no-default-keyring --keyring ~/.ansible/pubring.kbx my-public-key.asc
ansible-galaxy collection install my_namespace.my_collection --keyring ~/.ansible/pubring.kbx
```
- `--keyring` is not needed once a GnuPG keyring is configured for ansible-galaxy (the environment variable is `ANSIBLE_GALAXY_GPG_KEYRING`).
- Add signatures beyond those the server provides with `--signature URI` (repeatable; URIs such as `https://...asc` or `file:///path/...asc`), together with `--keyring`:
```bash
ansible-galaxy collection install my_namespace.my_collection \
  --signature https://examplehost.com/detached_signature.asc --keyring ~/.ansible/pubring.kbx
```
- GnuPG verification only happens for collections installed from a distribution server. User-provided signatures are not used for Git repositories, source directories, or URLs and paths to `tar.gz` files.
- In `requirements.yml`, add a `signatures:` list under the collection; the `--keyring` option must be provided when signatures are specified.
- If verification fails, the collection is not installed. GnuPG verification can be disabled with `--disable-gpg-verify` or `GALAXY_DISABLE_GPG_VERIFY`.

## How many signatures are required
- By default verification succeeds if at least 1 signature verifies. Change it with `--required-valid-signature-count` or the `ANSIBLE_GALAXY_REQUIRED_VALID_SIGNATURE_COUNT` environment variable; `all` requires every signature.
- Prefix the value with `+` (`+1`, `+all`) to fail when no valid signature is found at all.
- Some GnuPG errors can be ignored with `--ignore-signature-status-code` (repeatable), for example `NO_PUBKEY`.
```bash
export ANSIBLE_GALAXY_GPG_KEYRING=~/.ansible/pubring.kbx
export ANSIBLE_GALAXY_REQUIRED_VALID_SIGNATURE_COUNT=all
ansible-galaxy collection install my_namespace.my_collection --ignore-signature-status-code NO_PUBKEY
```

## Verifying after install
```bash
ansible-galaxy collection verify my_namespace.my_collection --keyring ~/.ansible/pubring.kbx
ansible-galaxy collection verify my_namespace.my_collection --signature file:///path/to/local/detached_signature.asc --keyring ~/.ansible/pubring.kbx
ansible-galaxy collection verify -r requirements.yml --keyring ~/.ansible/pubring.kbx
ansible-galaxy collection verify my_namespace.my_collection --offline --keyring ~/.ansible/pubring.kbx
```
When a collection is installed from a distribution server, the server's signatures are saved with it, so `--offline` can check internal consistency without contacting the server.

## Gotchas
- A count of `1` does not fail an install that has no valid signatures; use `+1` when unsigned content must be rejected.

## Verify
- [ ] Install with `--required-valid-signature-count +1` succeeds for signed content and fails for content without a valid signature.

## Checked
2026-10-28. Confirmed in the Ansible collections guide (installing with signature verification, verifying collections): keyring import, `--keyring`, `--signature`, requirements.yml `signatures`, restriction to distribution-server installs, default of one valid signature, `+` prefix and `all`, `--ignore-signature-status-code`, `--disable-gpg-verify`, `collection verify` forms and `--offline`. Removed because not confirmed: the private automation hub installer variables, the manual gpg signing commands, the `[galaxy]` ini keys, ansible-builder signature options and controller project content signing steps.
Method: documentation only; no commands were run.
