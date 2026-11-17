---
id: computing-software.systems-network-administration.cisco-networking.netdevops-ci-with-batfish
name: netdevops-ci-with-batfish
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, batfish, netdevops, pybatfish, ci-cd, network-validation, config-analysis, pre-change-validation, github-actions]
level: practitioner
status: draft
description: "Validate network config changes in CI with Batfish: snapshots from generated configs, pybatfish questions (undefined references, reachability, BGP sessions), and gating merges."
sources:
  - https://batfish.readthedocs.io/en/latest/
  - https://pybatfish.readthedocs.io/en/latest/questions.html
  - https://github.com/batfish/batfish
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetDevOps CI with Batfish validation

## Concept
Batfish builds a vendor-independent model of the network from configs (no devices needed) and
answers questions: parse errors, undefined references, BGP session compatibility, routing tables,
ACL/firewall behaviour, end-to-end reachability. Put it in CI so every pull request with config
changes is validated before deployment.

## Run Batfish
```
docker run -d --name batfish -p 9996:9996 batfish/allinone   # or batfish/batfish service
pip install pybatfish
```
Snapshot layout: `snapshot/configs/<device>.cfg` (plus optional `hosts/`, `iptables/`, `batfish/layer1_topology.json`).

## Questions in a test script
```python
from pybatfish.client.session import Session
bf = Session(host="localhost")
bf.set_network("campus")
bf.init_snapshot("snapshot", name="candidate", overwrite=True)

assert bf.q.fileParseStatus().answer().frame().query("Status != 'PASSED'").empty
assert bf.q.undefinedReferences().answer().frame().empty
assert bf.q.unusedStructures().answer().frame().shape[0] < 50
sessions = bf.q.bgpSessionStatus().answer().frame()
assert (sessions["Established_Status"] == "ESTABLISHED").all()
r = bf.q.reachability(pathConstraints=None,
       headers={"srcIps": "10.10.0.0/24", "dstIps": "10.0.0.53", "applications": ["dns"]}).answer().frame()
assert not r.empty and (r["Traces"].map(lambda ts: all(t.disposition == "ACCEPTED" for t in ts))).all()
```
Differential analysis: init the current production snapshot too and compare (`bf.q.differentialReachability`).

## CI pipeline (outline)
1. Render configs from templates + source of truth.
2. Start Batfish service container; run pytest with the questions above.
3. Fail the PR on any assertion; publish answers as artifacts.
4. On merge, deploy with Ansible/Nornir in check mode first, then apply.

## Gotchas
- Batfish models what configs say, not device bugs or hardware limits.
- Unsupported/unrecognised lines show as parse warnings; review once and allow-list.
- Without a layer-1 topology file, Batfish infers adjacency from IP subnets.

## Verify
- [ ] A deliberate mistake (ACL name typo) makes the CI job fail.
