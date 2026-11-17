---
id: computing-software.networking-hardware-and-wireless.open-vswitch.actions-learn-conjunction
name: actions-learn-conjunction
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, learn, conjunction, multipath, fin-timeout, sample, mac-learning, conjunctive-match]
level: advanced
status: docs-checked
description: "Use the learn, fin_timeout, conjunction, multipath and sample actions in Open vSwitch flows: learn argument keys, conjunctive match k/n, multipath algorithms, MAC learning."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# actions: learn, conjunction, multipath
- `learn(...)` adds or modifies a flow when a packet matches (like `ovs-ofctl --strict mod-flows`). Arguments: `table=` (default table 1, not 0), `idle_timeout=`, `hard_timeout=`, `priority=`, `cookie=`, `send_flow_rem`, `delete_learned`, `limit=`, `result_dst=`, `fin_idle_timeout=`, `fin_hard_timeout=`, plus match fields (`field=value`, `field=src`, `field`) and `load:`/`output:` specs.
- `fin_timeout(idle_timeout=s,hard_timeout=s)` shortens timeouts on TCP FIN or RST; it is normally added to a learned flow by `learn`.
- `conjunction(id,k/n)` marks a flow as clause k of n; a flow matching `conj_id=id` fires when all n clauses match. A flow with a conjunction action may have no other actions except `note`.
- `multipath(fields,basis,algorithm,n_links,arg,dst)` hashes into n links and stores the choice in `dst`. Algorithms: `modulo_n`, `hash_threshold`, `hrw`, `iter_hash`. The page says `bundle` or `bundle_load` are usually easier.
- `sample(...)` samples packets and sends them to a sample collector set (IPFIX; see ipfix-sampling).

MAC-learning example from the advanced tutorial (table 2 learns into table 10):
`learn(table=10, NXM_OF_VLAN_TCI[0..11], NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[], load:NXM_OF_IN_PORT[]->NXM_NX_REG0[0..15])`
Table 3 then runs `resubmit(,10)` to look up the learned entry.

Ordinarily `ofproto/trace` has no side effects and does not run `learn`; with `-generate` it does execute `learn` actions, after which `ovs-ofctl dump-flows br0 table=10` shows the learned flow.

## Checked
2026-11-04. Confirmed against ovs-actions(7) (learn, fin_timeout, multipath, conjunction, sample sections) and the OVS advanced tutorial (learn flow, table 3 resubmit, `-generate`). Removed the claim that sample goes to sFlow collectors (page names IPFIX only) and the cross-product remark.
Method: documentation only; no commands were run.
