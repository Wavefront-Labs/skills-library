---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.writing-zeek-scripts-for-investigations
name: writing-zeek-scripts-for-investigations
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [zeek-scripts, zeek, network-security-monitoring, protocol-forensics, dfir]
level: advanced
status: docs-checked
description: "Write Zeek scripts for investigations: event handlers, custom logs, notices, intel-like matching and running them over historical PCAP."
sources: ["https://docs.zeek.org/en/master/frameworks/logging.html", "https://docs.zeek.org/en/master/frameworks/notice.html", "https://github.com/zeek/zeek/blob/master/src/analyzer/protocol/http/events.bif", "https://github.com/zeek/zeek/blob/master/src/analyzer/protocol/smb/smb2_com_write.bif"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Zeek scripts for investigations

**Goal:** answer a case-specific question across days of PCAP (or live) that default Zeek logs do
not answer directly - e.g. "every HTTP POST over 1 MB to new domains" or "all SMB writes of .exe files to ADMIN$".

## Event-driven basics
```zeek
# big_posts.zeek
module BigPosts;
export {
    redef enum Log::ID += { LOG };
    type Info: record {
        ts: time &log; uid: string &log; orig: addr &log; host: string &log &optional;
        uri: string &log &optional; bytes: count &log;
    };
}
event zeek_init() { Log::create_stream(BigPosts::LOG, [$columns=Info, $path="big_posts"]); }

event http_message_done(c: connection, is_orig: bool, stat: http_message_stat)
    {
    if ( is_orig && c$http?$method && c$http$method == "POST" && stat$body_length > 1000000 )
        Log::write(BigPosts::LOG, [$ts=network_time(), $uid=c$uid, $orig=c$id$orig_h,
                   $host=c$http?$host ? c$http$host : "", $uri=c$http?$uri ? c$http$uri : "", $bytes=stat$body_length]);
    }
```
```bash
zeek -C -r day1.pcap big_posts.zeek       # writes big_posts.log alongside default logs
for f in pcaps/*.pcap; do mkdir -p "out/$(basename "$f")" && (cd "out/$(basename "$f")" && zeek -C -r "../../$f" ../../big_posts.zeek); done   # one output directory per pcap
```

## Useful events
`connection_state_remove` (final conn state), `dns_request`/`dns_A_reply`, `http_request`, `ssl_established`,
`smb2_create_request`/`smb2_write_request`, `file_new`/`file_hash`, `ssh_auth_result`.

## Notices
```zeek
@load base/frameworks/notice
redef enum Notice::Type += { Suspicious_UA };
event http_header(c: connection, is_orig: bool, name: string, value: string)
    { if ( is_orig && name == "USER-AGENT" && /python-requests|Go-http-client/ in value )
        NOTICE([$note=Suspicious_UA, $conn=c, $msg=value, $identifier=cat(c$id$orig_h)]); }
```

## Practice
- Test on a small PCAP with a known positive; check `reporter.log` for script errors.
- Keep scripts in the case folder with version control; record the Zeek version.

## Gotchas
- Optional fields need `?$` checks or the script throws errors on missing values.
- Heavy per-packet events (`new_packet`) are slow; prefer protocol-level events.

## Verify
The custom log reproduces known positives and the script/version are saved with the case.

## Checked

Checked 2026-10-25 against the Zeek sources (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)). Confirmed: `Log::create_stream` with `$columns` and `$path`, `Log::write`, `redef enum Log::ID`, `NOTICE([$note, $conn, $msg, $identifier])` and `redef enum Notice::Type`, event signatures `http_message_done(c, is_orig, stat)` with `http_message_stat$body_length`, `http_header` (header name converted to upper case), `http_request`, `dns_request`, `dns_A_reply`, `ssl_established`, `connection_state_remove`, `file_new`, `file_hash`, `new_packet`, `smb2_create_request`, `smb2_write_request`, `ssh_auth_result`. Changed: the loop example writes each pcap into its own directory because Zeek overwrites logs in the working directory. Replaced the scripting basics source with the logging, notice and event definition pages.

Method: documentation only; no commands were run.
