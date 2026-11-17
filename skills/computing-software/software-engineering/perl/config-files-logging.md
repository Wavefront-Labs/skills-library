---
id: computing-software.software-engineering.perl.config-files-logging
name: config-files-logging
category: computing-software
field: software-engineering
product: perl
tags: [perl, config-tiny, log-any, ini-files, logging-facade, config-files-logging]
level: practitioner
status: docs-checked
description: "Read and write INI config with Config::Tiny and log through the Log::Any facade (levels, formatted methods, context, adapters)."
sources: ["https://metacpan.org/pod/Config::Tiny", "https://metacpan.org/pod/Log::Any"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration files and logging

**Goal:** externalise settings and keep library logging decoupled from the application.

## Config::Tiny (INI)
```perl
use Config::Tiny;
my $cfg = Config::Tiny->read('file.conf', 'utf8') or die Config::Tiny->errstr;  # encoding without '<:' prefix
my $port = $ENV{APP_PORT} // $cfg->{server}{port} // 8080;     # your own precedence rule
my $c2 = Config::Tiny->read_string("[init]\nalpha=bet");
$cfg->{newsection} = { this => 'that' };
$cfg->write('file.conf');                                        # or write_string
```
```ini
rootproperty=blah          ; properties before any section land in $cfg->{_}
[section]
greetings[]=Hello          ; key[] pushes onto an array (since 2.30)
greetings[]=World!
```
- `read` returns undef on error; get the message from `Config::Tiny->errstr` (do not rely on `$!`).
- Comments start with `#` or `;` at the start of a line only. `key=value # note` sets the value to `value # note`. A trailing ` ; text` (whitespace, semicolon, whitespace) is stripped, but `key = Prefix;Suffix` is kept.
- A repeated key keeps the last value unless the `[]` array syntax is used. The `=` sign is mandatory. `$cfg` is a blessed object, so use `$cfg->{section}{key}`.
- Writing discards comments, whitespace and key order. Section headers with leading/trailing whitespace or newlines may be written incorrectly and corrupt the file. For richer needs the page points to Config::Simple, Config::General, Config::Tiny::Ordered (order) and others.

## Log::Any (producer side, for modules)
```perl
use Log::Any '$log';                                   # logger for the current package
$log->error("an error occurred");                      # no trailing newline
$log->info("started", { pid => $$ });                  # one hashref of structured data
$log->errorf("failed %s: %s", $id, $err);              # sprintf-style; refs become one-line Data::Dumper, undef becomes <undef>
$log->debug("args: " . Dumper(\@_)) if $log->is_debug; # guard expensive messages
die $log->fatal("fatal error");                        # logging methods return the message
local $log->context->{file} = $name;                   # context added to every message; localisable
```
- Levels (aliases): trace, debug, info (inform), notice, warning (warn), error (err), critical (crit, fatal), alert, emergency. Adapters translate them; Log::Log4perl has six levels, so notice maps to info and the top three to fatal.
- Formatted `...f` methods check the level for you. Some mechanisms cannot detect levels, so `is_*` returns 1 there; the default Null logger returns 0.
- The default is Null logging, so a module can log safely without an application choosing anything. Log::Any has no non-core dependencies.
- Category defaults to the calling package; `Log::Any->get_logger(category => ...)`. In Moo classes use `has log => (is => 'ro', default => sub { Log::Any->get_logger })`.

## Log::Any::Adapter (consumer side, for applications)
```perl
use Log::Any::Adapter ('File', '/path/to/file.log');
Log::Any::Adapter->set('Log4perl');
Log::Any::Adapter->set('Dispatch', dispatcher => $log);
use Log::Any '$log', default_adapter => 'Stderr';      # fallback when no adapter is set (or LOG_ANY_DEFAULT_ADAPTER)
```
- The library chooses nothing about the destination; the application picks one or more adapters. `Log::Any->has_consumer` detects a consumer; Log::Any::Test helps test logging code. Adapter details are in the Log::Any::Adapter docs (not read).

## Self-check
- [ ] `info` messages reach the chosen adapter while a module that logs without any adapter configured produces no output and no errors.

## Checked
Method: 2026-11-08 read the full plain-text POD of Config::Tiny and Log::Any 1.720 via the MetaCPAN API. Log::Log4perl (about 87KB) was not read, so its section and URL were removed; YAML::PP, Config::General, Dotenv, secrets-file, logrotate, syslog and 12-factor advice from v1 were dropped as unsupported by these pages.
