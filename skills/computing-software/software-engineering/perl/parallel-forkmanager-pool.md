---
id: computing-software.software-engineering.perl.parallel-forkmanager-pool
name: parallel-forkmanager-pool
category: computing-software
field: software-engineering
product: perl
tags: [perl, parallel-forkmanager, process-pool, fork-pool, parallel-jobs, parallel-forkmanager-pool]
level: practitioner
status: docs-checked
description: "Run jobs in parallel with Parallel::ForkManager: start/finish, callbacks, data returned from children, rand seeding, blocking-wait mode and limits."
sources: ["https://metacpan.org/pod/Parallel::ForkManager"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process pools with Parallel::ForkManager

**Goal:** bounded parallelism with plain processes (version 2.04 documented).

```perl
use Parallel::ForkManager;
my $pm = Parallel::ForkManager->new(4);        # max 4 children; 0 = no forking (debugging)
my %results;
$pm->run_on_finish(sub {                        # declare callbacks BEFORE the first start()
    my ($pid, $exit, $ident, $signal, $core, $data) = @_;
    $results{$ident} = $data if defined $data;  # children are not forced to send anything
});
$pm->run_on_start(sub { srand });               # different rand seed per child
JOB:
for my $job (@jobs) {
    $pm->start($job) and next JOB;              # parent: pid (true) so skip; child: 0
    my $out = do_work($job);
    $pm->finish(0, \$out);                      # exit code + a REFERENCE to send back
}
$pm->wait_all_children;                         # blocking
```

## Behaviour
- `start` dies if fork fails. The optional identifier shows up in `run_on_finish`/`run_on_start`. You cannot call `start` inside a child; create a second ForkManager object there. If you use several objects in the parent, make sure all children of the first are gone before using the second.
- `finish($code, $ref)` exits the child; default code 0. A data reference (string, array, hash or object ref) is serialised with Storable into temporary files and read back in the parent. Keep it small because of the cost. Pass a tempdir as the second `new` argument (`new($n, $tempdir)`) or use `new(max_proc => 4, tempdir => ..., child_role => ...)` since v2.00; otherwise `File::Temp::tempdir()` is used.
- `run_on_finish` args: pid, exit code, identifier, exit signal, core dump flag, data ref (or undef). `run_on_wait($code, $period)` runs while `start` or `wait_all_children` waits.
- `start_child([$id,] \&cb)` runs a callback as the child and sends its return value back as data.
- Other methods: `set_max_procs`, `reap_finished_children` (non-blocking; run callbacks when `start` is called rarely), `running_procs`, `wait_for_available_procs($n)`, `is_parent`, `is_child`.
- Children are reported running until harvested by the next `start` or `wait_all_children`.
- All forked children share one random seed, so `rand` repeats; `$pm->run_on_start(sub { srand })` fixes it.

## Blocking calls
- By default the module polls with non-blocking `waitpid` plus a sleep (default 1 s), the safest way not to steal other code's child notifications. `set_waitpid_blocking_sleep(0)` switches to truly blocking `waitpid` for any child, more efficient but it may capture termination notices that other code is waiting for.

## Limits and security
- Do not use it where other fork/wait code can interfere with the main program.
- Return-data temp file names are based on process ids and are easy to guess; keep the directory private to the user (the default tempdir is).
- PerlIO::gzip in children can garble files; the docs suggest the `unix` layer (`open(IN, '<:unix:gzip', ...)`).
- Since 2.0.0 it uses Moo, and forked child objects consume `Parallel::ForkManager::Child`, which can be replaced via `child_role` to change how data is stored or how children exit.

## Self-check
- [ ] With `new(4)`, eight one-second jobs finish in roughly two seconds (note the default 1 s polling granularity).

## Checked
Method: 2026-11-08 read the full plain-text POD of Parallel::ForkManager 2.04 via the MetaCPAN API. Dropped unsupported v1 claims (DBI InactiveDestroy advice, Windows threading caveats, flock logging, MCE/Parallel::Runner/xargs alternatives, zombie notes).
