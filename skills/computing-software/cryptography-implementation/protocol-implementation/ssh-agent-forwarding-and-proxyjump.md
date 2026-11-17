---
id: computing-software.cryptography-implementation.protocol-implementation.ssh-agent-forwarding-and-proxyjump
name: ssh-agent-forwarding-and-proxyjump
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, ssh-agent, openssh, agent-forwarding, proxyjump, ssh-add, destination-constraints, bastion]
level: practitioner
status: docs-checked
description: "Use ssh-agent safely: key lifetimes and confirmation, why agent forwarding exposes keys to remote root, ProxyJump instead, and agent destination constraints."
sources: ["https://man.openbsd.org/ssh-add", "https://man.openbsd.org/ssh_config#ProxyJump", "https://www.openssh.com/agent-restrict.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ssh-agent, agent forwarding and ProxyJump

## Loading keys with limits
```
ssh-add -t 4h ~/.ssh/id_ed25519        # lifetime
ssh-add -c ~/.ssh/id_ed25519           # confirm each use (uses the SSH_ASKPASS program)
ssh-add -l                             # list loaded keys
ssh-add -D                             # remove all
```
`~/.ssh/config`: `AddKeysToAgent` (values include `yes`, `ask`, `confirm`, a duration, `no`), and `IdentitiesOnly yes`
with `IdentityFile` per host so only the chosen identities in the agent are offered.

## Why agent forwarding is risky
With `ForwardAgent yes`, the remote host can use your agent to authenticate on your behalf. OpenSSH's agent-restrict
note says it is generally better to avoid a forwarded agent altogether (for example by using ProxyJump), because the
agent protocol itself offers little defence against abuse by the remote side.

## Use ProxyJump instead
```
ssh -J bastion.example.com app01.internal
# ~/.ssh/config
Host app01.internal
    ProxyJump bastion.example.com
```
ssh connects to the bastion, then establishes a TCP forwarding to the final target from there, so no agent forwarding
is involved.

## If you must forward: destination constraints (OpenSSH 8.9+)
```
ssh-add -h bastion.example.com -h "bastion.example.com>git.example.com" ~/.ssh/id_ed25519
```
The key can be used only to authenticate to the bastion and, via the bastion, to git.example.com. Constraints were
added in OpenSSH 8.9; support in both the remote ssh client and server is required over a forwarded agent. They are
enforced by the agent only when the key is used or forwarded by a cooperating ssh, and do not stop an attacker with
access to a remote `SSH_AUTH_SOCK` from forwarding it again to a permitted destination.

## Hardware-backed keys
FIDO keys (`ed25519-sk` is an ssh-keygen key type) that require user-presence confirmation offer some extra defence,
but the confirmation prompt cannot show the destination or forwarding path (OpenSSH agent-restrict note).

## Verify
- [ ] No `ForwardAgent yes` in shared configs except with destination constraints.
- [ ] `ForwardAgent` is not enabled for general hosts.

## Checked

2026-11-01. Confirmed against ssh-add(1) (`-t life`, `-c`, `-h` destination constraints, `>` hop syntax, 8.9 introduction,
remote client and server support, enforcement limits), ssh_config(5) (AddKeysToAgent values, IdentitiesOnly with
IdentityFile, ProxyJump behaviour) and the OpenSSH agent-restrict note. Removed: the claim that a remote root user
cannot copy keys, the claim that exposure lasts only while connected, and the `ssh -G` check (not in the sources).
Method: documentation only; no commands were run.
