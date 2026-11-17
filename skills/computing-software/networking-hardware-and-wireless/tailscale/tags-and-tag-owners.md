---
id: computing-software.networking-hardware-and-wireless.tailscale.tags-and-tag-owners
name: tags-and-tag-owners
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tags, tag-owners, tagged-devices]
level: practitioner
status: docs-checked
description: "Define tags with tagOwners and apply them to servers instead of user identities."
sources: ["https://tailscale.com/kb/1068"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tags and tagOwners

Goal: give servers an identity that is not tied to a person.

**How tags work**

- There is no `tags` section. You define a tag by listing its owners in `tagOwners`; only owners can apply it. Owner, Admin and Network admin can apply any tag.
- Applying a tag removes user-based authentication from the device. Its identity is the combination of all its tags.
- A device can have many tags; manage each tag's permissions separately.
- Tags are free; defining one in the policy needs Owner, Admin or Network admin.

```
"tagOwners": { "tag:prod": ["group:ops"] }
```

**Limitations**

- You cannot remove every tag from a device; a tag-identity device needs at least one.
- With an auth key you cannot remove tags via `--advertise-tags`; generate a new key with the new tag set.
- IP sets do not support tags.
- Tagged devices can SSH only into other tagged devices, not user-owned ones.

**Use for** servers not tied to a user, or devices several users manage. **Do not use for** laptops, phones or other end-user devices.

Key expiry is disabled by default on tagged devices.

**Checklist**

1. Tag defined in `tagOwners`.
2. Used only for non-human machines.
3. Auth keys regenerated when tags change.

## Checked

Confirmed against Tailscale kb/1068 (Tags), read in full: tagOwners as the only place tags are defined, who may apply tags, tag identity replacing user identity, the limitations list (at least one tag, auth key and advertise-tags, IP sets, SSH direction), the free-feature statement, and key expiry being off by default on tagged devices. Nothing was removed.

Method: docs-checked 2026-11-09 against https://tailscale.com/kb/1068
