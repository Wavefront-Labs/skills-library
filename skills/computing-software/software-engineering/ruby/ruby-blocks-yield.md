---
id: computing-software.software-engineering.ruby.ruby-blocks-yield
name: ruby-blocks-yield
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-blocks, blocks-yield]
level: intro
status: gated
description: "Write methods that take blocks using yield, block_given? and &block."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocks yield and block_given
- `def each_item; return enum_for(:each_item) unless block_given?; @items.each { |i| yield i }; end`
- `&block` captures the block as a Proc (allocation); `yield` is faster. Pass it on with `&block` or anonymous `&` (3.1).
- `next`/`break` in blocks: `break` exits the method that yielded, `next` returns from the block. (gated: unconfirmed, source is paywalled or blocked)
Verify: test both with and without a block.

## Checked
2026-11-02. Confirmed: doc/syntax/methods.rdoc: yield, &block and anonymous & block forwarding.
Gated: block_given?, Proc allocation cost, version 3.1 note and break/next semantics (not in the syntax docs read).
Method: documentation only; no commands were run.
