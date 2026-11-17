---
id: computing-software.cybersecurity-defensive.network-defence.suricata-rule-writing
name: suricata-rule-writing
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ids, suricata-rule-writing, suricata, ids-signatures, sticky-buffers, flowbits, rule-performance]
level: advanced
status: docs-checked
description: "Write efficient Suricata rules: header and sticky buffers, fast_pattern, flow and flowbits, thresholds, metadata, and testing against PCAPs before deployment."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html", "https://docs.suricata.io/en/latest/rules/payload-keywords.html", "https://docs.suricata.io/en/latest/rules/http-keywords.html", "https://docs.suricata.io/en/latest/rules/meta.html", "https://docs.suricata.io/en/latest/rules/thresholding.html", "https://docs.suricata.io/en/latest/rules/ja-keywords.html", "https://docs.suricata.io/en/latest/rule-management/rule-profiling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Suricata rules

**Goal:** precise, performant signatures for threats you care about, tested against real traffic before deployment.

## Anatomy
```
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ORG MALWARE ExampleLoader checkin"; \
  flow:established,to_server; http.method; content:"POST"; \
  http.uri; content:"/gate.php"; endswith; \
  http.user_agent; content:"Mozilla/4.0 (compatible; ExLoader)"; fast_pattern; \
  http.request_body; content:"id="; startswith; pcre:"/^id=[a-f0-9]{32}&/"; \
  reference:url,intel.corp.example/reports/123; classtype:trojan-activity; \
  sid:9000101; rev:1; metadata:created_at 2026_10_16, confidence High;)
```
- Action, protocol (use app-layer protocols like `http`, `tls`, `dns` for protocol detection independent of port), addresses/ports from variables, direction.
- **Sticky buffers** (`http.uri`, `http.host`, `tls.sni`, `dns.query`, `file.data`) apply to following content matches; they replace older modifiers like `http_uri`.
- `fast_pattern` on the most unique content; the MPM engine prefilters on it.
- `flow:established,to_server` limits evaluation.
- Pick `sid` values that avoid the published reserved ranges (recorded at sidallocation.org); a sid must be unique within its rule group and suricata-update keys on the sid alone, so keep it unique overall. Bump `rev` on edits.

## Useful keywords
- `dns.query; content:"evil.example"; nocase; endswith;` for DNS.
- `tls.sni; content:"bad.example"; isdataat:!1,relative;` exact SNI; `ja3.hash` / `ja4.hash` (sticky buffers; set `app-layer.protocols.tls.ja3-fingerprints` / `ja4-fingerprints`, which are enabled automatically when a loaded rule needs them unless set to `no`).
- `flowbits:set,org.stage1; noalert;` then `flowbits:isset,org.stage1;` for multi-step detection.
- `threshold:type limit, track by_src, count 1, seconds 3600;` to limit alert volume.
- `filestore` / `filemd5` lists for file-based detection.

## Test
```
suricata -T -c /etc/suricata/suricata.yaml -S local.rules        # syntax
suricata -r sample.pcap -S local.rules -l out/          # then read alerts in out/eve.json and out/fast.log
```
Run against benign traffic captures too (false positives). Rule profiling needs a build with `--enable-profiling-rules`; then `suricatasc -c ruleset-profile-start`, `ruleset-profile-stop` and `ruleset-profile` produce a per-rule cost report.

## Deploy
Manage with `suricata-update` (add local rule files via `--local`), version control, staged rollout (alert before drop in IPS mode).

## Verify
- [ ] Rule fires on the malicious PCAP and not on a day of baseline traffic.
- [ ] No rule without `fast_pattern`-capable content lands in the top profiling list.

## Checked

Checked 2026-10-25 against Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation). Confirmed: sticky buffers `http.method`, `http.uri`, `http.user_agent`, `http.request_body`, `dns.query`, `tls.sni`, `tls.cert_subject`, `file.data`; `startswith`/`endswith` and `isdataat:!1,relative`; `threshold: type limit, track by_src, count, seconds` grammar; `filestore`, `filemd5`; `metadata: key value` syntax; JA3/JA4 keywords and their enabling options; `-T`, `-S`, `-r`, `-l` command line options. Corrected: the rule profiling build flag and the sid range guidance (the docs point to sidallocation.org, not a fixed local range). Removed the unconfirmed `ja4` version gate and the jq pipeline.

Method: documentation only; no commands were run.
