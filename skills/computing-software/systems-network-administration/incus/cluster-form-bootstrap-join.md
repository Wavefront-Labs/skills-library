---
id: computing-software.systems-network-administration.incus.cluster-form-bootstrap-join
name: cluster-form-bootstrap-join
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cluster, bootstrap, join-token, cluster-enable, cluster-add, core-https-address]
level: practitioner
status: docs-checked
description: "Form an Incus cluster: bootstrap with incus admin init or cluster enable, set core.https_address, and join members with cluster add tokens."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/cluster_form.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form a cluster

Bootstrap: run `incus admin init`, answer yes to clustering, give a reachable IP or DNS name, answer no to joining an existing cluster.

Converting an existing server:
```
incus config set core.https_address=[IP_OR_DNS]:8443
incus cluster enable <memberName>
```
The wildcard default address is not allowed in clustered mode.

Join:
```
incus cluster add <new_member_name>      # on an existing member
sudo incus admin init                    # on the joiner
incus cluster list
```
- The single-use token (lifetime `cluster.join_token_expiry`) carries member addresses, a secret and the cluster certificate fingerprint, so it answers several prompts.
- Joining servers should be freshly installed; their existing data is lost. Confirm when prompted.
- Check the clustering requirements page first.

## Checked

2026-11-09. Confirmed against the Incus doc howto/cluster_form.md (interactive configuration): bootstrap answers, converting an existing server, wildcard address restriction, join token contents and expiry key, fresh-server and data-loss warnings. Removed: nothing needed removing.

Method: documentation only; no commands were run.
