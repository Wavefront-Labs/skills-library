---
id: computing-software.cloud-infrastructure-engineering.aws.nlb-listeners-proxy-protocol-and-idle-timeout
name: nlb-listeners-proxy-protocol-and-idle-timeout
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nlb, proxy-protocol, nlb-idle-timeout, tcp-udp-listeners, tls-listener, target-group-attributes]
level: advanced
status: docs-checked
description: "Configure NLB TCP, UDP, TCP_UDP and TLS listeners: proxy protocol v2 for client IPs, the TCP idle timeout, connection termination on deregistration and ALPN."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-listeners.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-health-checks.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-security-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NLB listeners, proxy protocol and idle timeout

## 1. Listener protocols
| Protocol | Use | Notes |
|---|---|---|
| `TCP` | any TCP service, TLS pass-through | targets terminate TLS |
| `TLS` | NLB terminates TLS with an ACM cert, forwards TCP or TLS to targets | security policy, ALPN (`HTTP2Preferred`, `HTTP2Only`, `HTTP1Only`, `HTTP2Optional`; default is no ALPN) |
| `UDP` | DNS, syslog, game servers, QUIC | health checks use TCP, HTTP or HTTPS on any target port |
| `TCP_UDP` | same port both protocols (DNS 53) | target group protocol TCP_UDP |
```bash
aws elbv2 create-listener --load-balancer-arn <nlb> --protocol TLS --port 443 \
  --certificates CertificateArn=<acm> --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06 \
  --alpn-policy HTTP2Preferred --default-actions Type=forward,TargetGroupArn=<tg>
```

## 2. Client IP: preservation vs proxy protocol
- **Client IP preservation** (target group attribute `preserve_client_ip.enabled`): off by default only for
  IP-address targets with TCP or TLS protocol, otherwise on; it cannot be disabled for UDP, TCP_UDP, QUIC or TCP_QUIC.
  When on, targets see the real client IP, so their SGs must allow client CIDRs (not just
  the NLB).
- **Proxy protocol v2** (`proxy_protocol_v2.enabled`): NLB prepends a binary header with the
  original source/destination; targets must parse it (nginx `listen 443 proxy_protocol;`,
  HAProxy `accept-proxy`, Envoy listener filter). Enabling it without target support breaks
  every connection (the app sees garbage before the TLS ClientHello).
```bash
aws elbv2 modify-target-group-attributes --target-group-arn <tg> \
  --attributes Key=proxy_protocol_v2.enabled,Value=true
```

## 3. Idle timeout
A TCP flow with no data for longer than the idle timeout is no longer tracked; the next packet gets a RST.
The TCP listener timeout is 350 seconds by default and can be set to 60-6000 seconds per listener. TLS listeners
are fixed at 350 seconds and UDP flows at 120 seconds (neither can be changed).
```bash
aws elbv2 modify-listener-attributes --listener-arn <listener> \
  --attributes Key=tcp.idle_timeout.seconds,Value=1800
```
Better still, enable TCP keepalive on clients or targets below the timeout for long-lived connections (databases,
MQTT, websockets); on TLS listeners keepalive packets must carry no data. If you raise the timeout above 350 s, make
sure the target ENI connection tracking timeout (`TcpEstablishedTimeout`) is at least as long.

## 4. Target group behaviour attributes
- `deregistration_delay.timeout_seconds` (0-3600, default 300) and
  `deregistration_delay.connection_termination.enabled` (close connections at the end of
  the delay; default true for new UDP/TCP_UDP target groups, otherwise false, so existing flows continue until they end).
- `target_health_state.unhealthy.connection_termination.enabled` (default true): close
  connections to targets that turn unhealthy.
- `stickiness` source-IP based (`stickiness.type=source_ip`).
- Cross-zone is off by default on the NLB (`load_balancing.cross_zone.enabled`; the target group default is
  `use_load_balancer_configuration`); off means each AZ's NLB node only sends to its own AZ's targets, so keep targets
  balanced per AZ or turn it on.

## 5. Health checks
TCP (connect only; the default protocol), HTTP/HTTPS (path default `/`, matcher range 200-599, default 200-399). UDP
services need a TCP, HTTP or HTTPS health endpoint on the target. Interval 5-300 s (default 30), timeout 2-120 s,
healthy threshold 2-10 (default 5), unhealthy threshold 2-10 (default 2).

## Gotchas
- Security groups can be associated with an NLB only when you create it; if it was created without one you cannot add
  one later (with one or more you can change them later). Without an SG, targets must allow client IPs or NLB private IPs directly.
- Long-lived connections stay on the target they started on; scaling out does not
  rebalance until clients reconnect.

## Verify
- [ ] Target logs show the real client IP (preservation or parsed proxy header).
- [ ] An idle connection held for longer than the configured timeout is either kept alive by keepalives or closed predictably.
- [ ] Deregistering a target drains as configured; no RSTs to active clients before the delay.

## Checked

Checked 2026-10-27 against the Elastic Load Balancing documentation for Network Load Balancers (listeners, target groups, health checks, load balancer attributes, security groups) and the botocore elbv2 model.
- Corrected: TCP listener idle timeout 350 s default and 60-6000 s configurable, TLS listeners fixed at 350 s, UDP fixed at 120 s; health check interval 5-300 s (default 30), matcher range 200-599; client IP preservation defaults; ALPN default is none; security groups can be attached only at NLB creation; connection termination on deregistration defaults.
- Confirmed: attribute names (`preserve_client_ip.enabled`, `proxy_protocol_v2.enabled`, `deregistration_delay.*`, `target_health_state.unhealthy.connection_termination.enabled`, `stickiness.type=source_ip`, `tcp.idle_timeout.seconds`), cross-zone off by default on the NLB, policy `ELBSecurityPolicy-TLS13-1-2-2021-06`.
- Removed: hairpinning, PrivateLink TLV and TLS-target-certificate claims that the pages did not confirm.

Method: documentation only; no commands were run.
