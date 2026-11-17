---
id: computing-software.firmware-embedded-development.zephyr.bsd-sockets-networking
name: bsd-sockets-networking
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-networking, zephyr-sockets, zsock-socket, zsock-getaddrinfo, tls-sockets, net-buffers, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write TCP/UDP/TLS clients on Zephyr with the BSD socket API: Kconfig, zsock_* calls, DNS, TLS credentials, poll-based loops and buffer sizing."
sources:
  - https://docs.zephyrproject.org/latest/services/connectivity/networking/api/sockets.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/sockets/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/net/sockets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BSD sockets networking

## Config
```
CONFIG_NETWORKING=y
CONFIG_NET_IPV4=y
CONFIG_NET_TCP=y
CONFIG_NET_UDP=y
CONFIG_NET_SOCKETS=y
CONFIG_DNS_RESOLVER=y
CONFIG_NET_DHCPV4=y              # or static address via CONFIG_NET_CONFIG_*
CONFIG_POSIX_API=y               # optional: plain socket()/connect() names
```
Without `CONFIG_POSIX_API` the operations are exposed with a `zsock_` prefix (`zsock_socket`,
`zsock_close`); enabling it adds aliases without the prefix. UDP sockets need `CONFIG_NET_UDP`,
TCP sockets `CONFIG_NET_TCP`, TLS sockets `CONFIG_NET_SOCKETS_SOCKOPT_TLS`.

## TCP client
```c
#include <zephyr/net/socket.h>

int http_get(const char *host)
{
    struct zsock_addrinfo hints = { .ai_family = AF_INET, .ai_socktype = SOCK_STREAM }, *res;
    int rc = zsock_getaddrinfo(host, "80", &hints, &res);
    if (rc) return -EHOSTUNREACH;

    int s = zsock_socket(res->ai_family, res->ai_socktype, IPPROTO_TCP);
    if (s < 0) { zsock_freeaddrinfo(res); return -errno; }

    struct timeval to = { .tv_sec = 5 };
    zsock_setsockopt(s, SOL_SOCKET, SO_RCVTIMEO, &to, sizeof(to));

    rc = zsock_connect(s, res->ai_addr, res->ai_addrlen);
    zsock_freeaddrinfo(res);
    if (rc < 0) { rc = -errno; zsock_close(s); return rc; }
    /* zsock_send / zsock_recv loop: both can return short counts */
    zsock_close(s);
    return 0;
}
```

## TLS
```
CONFIG_NET_SOCKETS_SOCKOPT_TLS=y      # implies TLS_CREDENTIALS; selects the crypto stack (Mbed TLS / PSA Crypto)
```
DTLS needs `CONFIG_NET_SOCKETS_ENABLE_DTLS`.
```c
#define CA_TAG 1
tls_credential_add(CA_TAG, TLS_CREDENTIAL_CA_CERTIFICATE, ca_der, sizeof(ca_der));
int s = zsock_socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);
sec_tag_t tags[] = { CA_TAG };
zsock_setsockopt(s, SOL_TLS, TLS_SEC_TAG_LIST, tags, sizeof(tags));
zsock_setsockopt(s, SOL_TLS, TLS_HOSTNAME, host, strlen(host));   /* hostname check */
```
The protocol constant is the minimum TLS version. The hostname check is enforced by default for
TLS clients (a NULL hostname disables it). Credentials types: CA certificate, public
certificate, private key, PSK and PSK identity; DER is supported by default and PEM needs Mbed TLS
settings. When `CONFIG_MBEDTLS_ENABLE_HEAP` is on, `CONFIG_MBEDTLS_HEAP_SIZE` sets the Mbed TLS
heap; its help text says streaming communication with arbitrary HTTPS servers may need 32 KB plus
up to another 20 KB of overhead. Also note: after a non-blocking send returns `EAGAIN`, the next
send must carry the same data.

## Event loops
`zsock_poll(fds, n, timeout_ms)` over several sockets (the limit is `CONFIG_ZVFS_POLL_MAX`;
`CONFIG_NET_SOCKETS_POLL_MAX` was deprecated in Zephyr 4.0 in its favour). One network thread
with poll avoids a thread per socket on small RAM.

## Wait for the network
Don't connect at boot blindly. Wait for L4 connectivity through net_mgmt events (see
network-management-events) or `conn_mgr`; otherwise the first connect can fail.

## Buffer sizing
TCP throughput and stability depend on `CONFIG_NET_PKT_RX_COUNT` and `CONFIG_NET_PKT_TX_COUNT`
(default 4 each), `CONFIG_NET_BUF_RX_COUNT` and `CONFIG_NET_BUF_TX_COUNT` (default 16 each) and
`CONFIG_NET_BUF_DATA_SIZE` (default 128, fixed-size allocator). Each data buffer occupies
`NET_BUF_DATA_SIZE` plus a small header. `CONFIG_NET_PKT_LARGE_DEFAULTS` raises the defaults
(14 packets, 36 buffers). Enable `CONFIG_NET_SHELL` to inspect usage.

## Verify
- [ ] Every socket call's error path closes the socket (no fd leak after 1000 failed connects).
- [ ] Recv/send timeouts set; the app survives the server disappearing mid-transfer.
- [ ] TLS hostname verification on; tested against a cert with the wrong name (must fail).

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/services/connectivity/networking/api/sockets.rst, include/zephyr/net/socket.h, subsys/net/ip/Kconfig, subsys/net/lib/sockets/Kconfig, modules/mbedtls/Kconfig.tf-psa-crypto and the 4.0 migration guide.
Confirmed: `zsock_` prefix and `CONFIG_POSIX_API` aliases; `CONFIG_NET_SOCKETS`, `NET_UDP`, `NET_TCP`, `NET_SOCKETS_SOCKOPT_TLS` (implies `TLS_CREDENTIALS`); `IPPROTO_TLS_1_2` as minimum version; `tls_credential_add`, `TLS_CREDENTIAL_CA_CERTIFICATE`, `TLS_SEC_TAG_LIST`, `TLS_HOSTNAME` (check enforced by default); `NET_PKT_RX/TX_COUNT` default 4, `NET_BUF_RX/TX_COUNT` default 16, `NET_BUF_DATA_SIZE` default 128, large-defaults values; `MBEDTLS_HEAP_SIZE` help text; `CONFIG_NET_SOCKETS_POLL_MAX` deprecated for `CONFIG_ZVFS_POLL_MAX`; `DNS_RESOLVER`, `NET_DHCPV4`, `NET_SHELL` options exist.

Method: documentation only; no commands were run.
