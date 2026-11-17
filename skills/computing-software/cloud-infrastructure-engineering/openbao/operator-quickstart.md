---
id: computing-software.cloud-infrastructure-engineering.openbao.operator-quickstart
name: operator-quickstart
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, operator, init, unseal, audit-device]
level: intro
status: docs-checked
description: "Operator first steps for a real OpenBao server: status, init, unseal, login, an audit device to stdout, and joining raft HA nodes."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/get-started/operator-qs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator quickstart

Command order from the operator guide:

```
bao status
bao operator init
bao operator unseal
bao login
```

`init` prints unseal key shares and an initial root token. The page warns these values are highly sensitive and grant access to your instance. Store them carefully.

## Audit device in config

```hcl
audit "file" "to-stdout" {
  description = "Write audit information to standard output."
  options {
    file_path = "stdout"
    log_raw = "true"
  }
}
```

Warning: make sure you have a log collection solution that durably stores this output. If you edit the config file while OpenBao is running, restart it or send it SIGHUP to reload the file.

## Try the cubbyhole

```
bao write cubbyhole/my-secret my-value=s3cr3t
bao read cubbyhole/my-secret
```

Cubbyhole is ephemeral and scoped to the lifetime of the token.

## HA

Add further nodes with `operator raft join`. Only the first instance must be initialized with a seal.

## Client apps

Apply the principle of least privilege: do not hand applications the root token.

## Checked

2026-11-04. Confirmed against the Operator quick start page: command order, init output and the sensitivity warning, the stdout audit device block, the log collection warning, the cubbyhole example and its ephemeral scope, operator raft join with only the first node initialized with a seal, and the least-privilege advice. Added the SIGHUP reload option the page also gives.

Method: documentation only; no commands were run.
