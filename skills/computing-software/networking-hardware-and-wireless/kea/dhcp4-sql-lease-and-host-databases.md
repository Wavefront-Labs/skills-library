---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-sql-lease-and-host-databases
name: dhcp4-sql-lease-and-host-databases
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, mysql, postgresql, lease-database, timeouts]
level: practitioner
status: docs-checked
description: "Point kea-dhcp4 at MySQL or PostgreSQL for leases, and set connection, read, write and TCP user timeouts."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 SQL lease database
`Dhcp4/lease-database` takes `type` of memfile, mysql or postgresql. For SQL backends also set `name` (the database created earlier), `host` (empty string when local), `port` if non-default, and a longer connection timeout if the database is remote.

- Database access must be configured for kea-dhcp4 even if already configured for kea-dhcp6; each server stores independently, on separate databases or the same one.
- Kea requires the database timezone to match the system timezone.

Timeouts, to mitigate hangs on database I/O:
- MySQL: `read-timeout` and `write-timeout` in seconds; Not supported before MySQL 5.6; a configuration error on other backends.
- PostgreSQL: `tcp-user-timeout`; a configuration error on other backends.
- These only take effect on TCP connections; the MySQL client library typically uses a UNIX domain socket when the host is localhost, but a TCP connection for 127.0.0.1. Since Kea 3.3.1 `password-file` can replace `password`.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter sections Lease Database Configuration and Tuning Database Timeouts (type values, independent per-server storage, timezone requirement, read-timeout, write-timeout, tcp-user-timeout, MySQL 5.6, TCP-only). The statement that 0 means MySQL defaults and waiting indefinitely was not located and is removed.
