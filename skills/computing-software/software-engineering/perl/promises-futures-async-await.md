---
id: computing-software.software-engineering.perl.promises-futures-async-await
name: promises-futures-async-await
category: computing-software
field: software-engineering
product: perl
tags: [perl, future-async-await, async-sub, await-keyword, cancel-block, futures, promises-futures-async-await]
level: advanced
status: docs-checked
description: "Write async sub and await with Future::AsyncAwait: return wrapping, top-level await, CANCEL blocks, supported constructs, local limits and perl version needs."
sources: ["https://metacpan.org/pod/Future::AsyncAwait"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Future::AsyncAwait

**Goal:** write futures-based asynchronous flows as straight-line code.

```perl
use v5.14;
use Future::AsyncAwait;

async sub do_a_thing {
    my $first  = await do_first_thing();
    my $second = await do_second_thing();
    return combine_things($first, $second);
}
do_a_thing()->get;
```

## Semantics
- `async` goes just before `sub` (named, anonymous `async sub {...}`, lexical `my async sub` on 5.18+ since 0.69, and `async sub Other::Pkg::name` since 0.70). It permits `await` in the body and wraps the return value in a Future that completes on `return` or falling off the end; an exception in the body fails the Future.
- If the last expression is itself a Future, `await` it; returning it directly double-wraps. An `async sub` with no awaits turns `return @result` into an immediate Future, and exceptions become an immediate-failed Future instead of propagating from the call.
- `await $f` yields the result like `->get`, but if the Future is pending the whole function suspends and returns a new pending Future, resuming when `$f` completes. It gives scalar context to its operand and is only allowed inside `async sub`.
- Top-level `await` (since 0.47) outside any `async sub` just calls `->get`; meant for tests and scripts.
- Supported around `await`: statement, `1 + await($f) + 3`, `while`, `if`, `foreach` (also `foreach my ($k,$v)` on perl 5.35.5+), `do { }`, `eval { }`. Plain lexicals survive suspension. Signatures work on 5.26+ with the feature on; since 0.55 signature errors are thrown synchronously, not as a failed Future.

## Cancellation
- Cancelling the returned Future stops a suspended `async sub`; the request also propagates back into the Future being awaited (perl 5.24+ only; documented as still experimental).
- Experimental `CANCEL { ... }` block (since 0.44) runs only if the still-pending Future is cancelled, once per execution of the block (so per loop iteration) and is discarded if the function finishes. It warns in the `experimental` category; silence selectively with `use Future::AsyncAwait qw( :experimental(cancel) );`.

## Limits
- `local` across an `await` is not supported yet (TODO list), and `foreach` over a non-lexical variable such as `$_` is disallowed for the same reason.
- Needs perl 5.16 or later; threaded builds before 5.22 are not supported. The page says it is still under active development and occasional memory leaks may remain, especially when pending futures are abandoned.
- `use Future::AsyncAwait future_class => "Subclass::Of::Future";` (lexically scoped) changes the class of immediate results; the subclass should implement Future::AsyncAwait::Awaitable.

## With other modules (integration-tested per the page)
Syntax::Keyword::Try (try/catch with `return` inside an `async sub`), Syntax::Keyword::Dynamically, Syntax::Keyword::Defer and `finally` (run even on cancellation since 0.50), Object::Pad (`async method`) and Syntax::Keyword::MultiSub (`async multi sub`).

## Self-check
- [ ] `do_a_thing()->get` returns the combined value, and an `async sub { die "x" }->()` returns a failed Future rather than dying at the call.

## Checked
Method: 2026-11-08 read the full plain-text POD of Future::AsyncAwait. The Future and Mojo::Promise pages were not read, so their URLs and the v1 claims about combinators (`needs_all`, `wait_any`), `Mojo::Promise` methods and `Mojo::Base -async_await`, Net::Async::HTTP and deadlock advice were removed.
