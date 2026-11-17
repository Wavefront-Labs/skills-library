---
id: computing-software.systems-network-administration.pi-hole.unbound-root-reachability-test
name: unbound-root-reachability-test
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dns-interception, root-server-test, unbound-prerequisites]
level: advanced
status: draft
description: "Check that your network can reach DNS root servers directly, without ISP interception or CG-NAT TCP drops, before installing Unbound."
sources: ["https://docs.pi-hole.net/guides/dns/unbound/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Test root server access before Unbound

Some ISPs, parental-filter software and consumer router firmware silently redirect outbound port 53 traffic. That stops Unbound reaching the roots and causes failures that are hard to diagnose. Run these on the host that will run Unbound, against `a.root-servers.net` (`198.41.0.4`).

**1. UDP and interception**

```bash
dig @198.41.0.4 . NS +norec +time=3
```

A direct root answer has the `aa` flag and no `ra` flag, for example `flags: qr aa`. If `ra` is present and `aa` is absent, a resolver or proxy is answering instead.

**2. TCP**

```bash
dig @198.41.0.4 . NS +norec +tcp +time=3
```

Unbound relies on TCP/53 for large DNSSEC responses and retries. Some CG-NAT setups pass UDP but silently drop TCP DNS, so a timeout here after step 1 succeeded points to that.

**3. Identity via CHAOS class**

```bash
dig @198.41.0.4 version.bind CH TXT +time=3
```

A real root server returns a TXT record containing `ATLAS`. Anything else, a timeout or SERVFAIL means your DNS is being proxied, even if steps 1 and 2 passed. Reliability and privacy of unencrypted queries may be affected.

**If any test fails,** the guide advises not installing Unbound until you have found and fixed the cause, such as ISP redirection, CG-NAT blocking TCP, or router filtering.

**Checklist**

1. Run all three tests.
2. Investigate any failure.
3. Proceed to Unbound only when all pass.
