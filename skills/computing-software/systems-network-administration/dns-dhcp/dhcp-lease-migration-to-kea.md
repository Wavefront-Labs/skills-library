---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-lease-migration-to-kea
name: dhcp-lease-migration-to-kea
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, isc-dhcp-migration, lease-migration, dhcpd-leases, memfile, lease-csv, lease4-add, lease-commands-hook, kea-lfc, address-stability]
level: advanced
status: verified
description: "Carry active leases from ISC dhcpd (or another server) into Kea so clients keep their addresses: parse dhcpd.leases, build memfile CSV or use lease4-add via the API, and verify."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#memfile-basic-storage-for-leases
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-lease-cmds-so-lease-commands-for-easier-lease-management
  - https://github.com/isc-projects/dhcp/blob/master/server/dhcpd.leases.5
  - https://kb.isc.org/docs/migrating-from-isc-dhcp-to-kea-dhcp-using-the-migration-assistant
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/export-dhcpserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating leases into Kea

Without lease migration, Kea starts with an empty lease database: it may offer addresses that are
still in use (conflicts), and it does not know the clients' old leases. For a client in INIT-REBOOT
that asks for an address Kea has no record of, Kea stays silent by default and only NAKs when
`authoritative` is true (ARM, authoritative DHCPv4 behaviour). Migrating leases avoids these problems.

## Option A: memfile CSV (server stopped)
ISC publishes an experimental lease migration tool, keama-leases, and its KB article says keama
itself does not convert leases. To do it by hand: Kea's memfile backend stores leases in
`kea-leases4.csv` (default `var/lib/kea` under the install prefix; since Kea 2.7.9 the file must be
in that directory or the one named by `KEA_DHCP_DATA_DIR`) with this header, taken from the Kea
source (schema 3.0):
```
address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context,pool_id
```
(older schema versions lack the last columns: copy the header from a file your Kea version created).
`expire` is the lease's last-transmission time plus `valid_lifetime`, as epoch seconds, `state` 0 is
default and `client_id` and `hwaddr` are colon-separated hex.
dhcpd's `dhcpd.leases` is a journal (dhcpd.leases(5)): a lease is rewritten at the end of the file
every time it changes, so the last declaration of an address wins. Times such as
`ends 3 2026/10/21 10:00:00;` are UTC, the first number is the weekday (0 = Sunday, so 3 =
Wednesday, checked), and a non-printable `uid` is printed as a quoted string with octal escapes.
Keep only `binding state active` entries with `ends` in the future, map each IP to the Kea
subnet id that contains it, set `expire` to the epoch of `ends` (2026-10-22 09:00:00 UTC is
1792659600) and `valid_lifetime` to your lease time. This script does that; it was run on a
sample journal (a superseded duplicate, a free lease, a lease outside every subnet, a colon-hex uid
and an octal-escaped uid) and produced one CSV row per surviving address:
```python
import re, sys, ipaddress, datetime

SUBNETS = {ipaddress.ip_network("10.20.10.0/24"): 10}   # edit: prefix -> "id" in kea-dhcp4.conf
VALID = 86400                                            # your lease time in seconds
BS = chr(92)

def decode_quoted(s):
    """dhcpd prints a non-printable uid as a quoted string with octal escapes."""
    s, out, i = s[1:-1], bytearray(), 0
    while i < len(s):
        if s[i] == BS and s[i + 1] in "01234567":
            out.append(int(s[i + 1:i + 4], 8)); i += 4
        elif s[i] == BS:
            out.append(ord(s[i + 1])); i += 2
        else:
            out.append(ord(s[i])); i += 1
    return bytes(out)

def parse(path):
    leases = {}
    text = open(path, encoding="latin-1").read()
    for m in re.finditer(r"(?m)^lease ([0-9.]+) [{](.*?)^[}]", text, re.S):
        ip, body = m.group(1), m.group(2)
        e = re.search(r"ends (never|[0-9] [0-9/]+ [0-9:]+);", body)
        h = re.search(r"hardware ethernet ([0-9a-fA-F:]+);", body)
        EB = re.escape(BS)
        u = re.search(r'uid ("(?:[^"' + EB + r']|' + EB + r'.)*"|[0-9a-fA-F:]+);', body)
        n = re.search(r'client-hostname "([^"]*)";', body)
        s = re.search(r"binding state ([a-z]+);", body)
        cid = ""
        if u:
            v = u.group(1)
            raw = decode_quoted(v) if v.startswith('"') else bytes.fromhex(v.replace(":", ""))
            cid = ":".join("%02x" % x for x in raw)
        leases[ip] = dict(ends=e.group(1) if e else None, mac=h.group(1).lower() if h else "",
                          cid=cid, host=n.group(1) if n else "", state=s.group(1) if s else "")
    return leases        # the file is a journal: the last declaration of an IP wins

def main(path, now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc).timestamp()
    print("address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context,pool_id")
    for ip, d in parse(path).items():
        if d["state"] != "active" or not d["ends"] or d["ends"] == "never":
            continue
        ends = datetime.datetime.strptime(d["ends"][2:], "%Y/%m/%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        sid = next((i for n, i in SUBNETS.items() if ipaddress.ip_address(ip) in n), None)
        if ends.timestamp() > now and sid is not None:
            print(",".join([ip, d["mac"], d["cid"], str(VALID), str(int(ends.timestamp())), str(sid),
                            "0", "0", d["host"], "0", "", "0"]))

if __name__ == "__main__":
    main(sys.argv[1])
```
Write the CSV with Kea stopped, then start Kea and check it loaded the count you expected.

## Option B: lease commands API (server running)
Load `libdhcp_lease_cmds.so` hook, then:
```
curl -s -X POST http://127.0.0.1:8000/ -H 'Content-Type: application/json' -d '{
 "command": "lease4-add",
 "arguments": {"ip-address": "10.20.10.57", "hw-address": "00:11:22:33:44:55",
               "subnet-id": 10, "valid-lft": 86400, "hostname": "pc1"}}'
```
`ip-address` and `hw-address` are required; `subnet-id` is optional (Kea runs subnet selection when it is
omitted or 0, and a given value must match an existing subnet); `valid-lft` is the lifetime in seconds
and `expire` can set an absolute expiry timestamp instead; `hostname` must be non-empty if `fqdn-fwd`
or `fqdn-rev` is true. Add `"service": ["dhcp4"]` when going through a Control Agent (Kea 3.0.x and
earlier). Script it per lease; `lease4-get-all` to verify. Works for database backends too.

## Practical notes
- Shorten lease times on the old server a few days before cutover so fewer, fresher leases move and
  clients renew soon after (catching problems early).
- Set subnet ids explicitly in Kea config (`"id": 10`): without them Kea numbers subnets from 1 in
  file order and the ids are not stable across config changes, so lease records would map to
  the wrong subnets after an edit.
- Windows DHCP: `Export-DhcpServer -Leases -File leases.xml` exports configuration plus lease data
  to a file (Microsoft cmdlet reference; the XML schema is not covered here, so inspect it before
  writing a converter).

## Verify
- [ ] Kea lease count after import matches active leases on the old server.
- [ ] A sample of clients renew and keep their address (`DHCPACK` in Kea logs, no NAKs).
