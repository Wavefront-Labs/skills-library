---
id: computing-software.software-engineering.perl.mocking-test2-v0
name: mocking-test2-v0
category: computing-software
field: software-engineering
product: perl
tags: [perl, test2-v0, test-mockmodule, mocking, test2-tools-mock, strict-mode, mocking-test2-v0]
level: advanced
status: docs-checked
description: "Replace Perl dependencies in tests with Test::MockModule (mock, redefine, strict mode, exports) or Test2::Tools::Mock (mock, track, accessors)."
sources: ["https://metacpan.org/pod/Test::MockModule", "https://metacpan.org/pod/Test2::Tools::Mock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocking in Perl tests

**Goal:** isolate code from networks, clocks and databases without leaking mocks between tests.

## Test::MockModule
```perl
use Test::MockModule;
{
    my $module = Test::MockModule->new('Module::Name');
    $module->mock('subroutine', sub { ... });          # replace; a scalar becomes a sub returning it
    $module->redefine('other_subroutine', sub { ... }); # dies if the sub does not already exist
    $module->define('another_subroutine', sub { ... }); # dies if the sub already exists
    Test::MockModule->new('Foo')->mock(a => sub { ... })->redefine(b => sub { ... });   # chainable
}   # all mocks for the package are restored when the last mock object goes out of scope
```
- `redefine` guards against interface drift (also accepts a sub provided by a parent class); `define` asserts the sub is absent and does not check inheritance.
- Strict mode: `use Test::MockModule qw(strict);` makes `mock()` a fatal runtime error so only `redefine` works. It is lexically scoped and must be set at compile time with `use` (`nostrict` to opt out in a block). `use Test::MockModule 'global-strict';` makes any later `nostrict` fail at compile time.
- Scalars: `mock(purge => [localtime()])` returns the same arrayref each time; use `sub { [localtime()] }` for a fresh one. `mock(x => undef)` installs an empty sub (returns empty list), not one returning undef.
- Calling `mock` on the same sub many times and then `unmock` restores the original, not the previous mock. `unmock_all` restores everything. `noop('a','b')` replaces subs with ones returning 1. `mock_all()` mocks every unmocked sub to die ("was not mocked"); `mock_all(noop => 1)` returns 1 and `handler => sub {...}` customises; `import` is skipped.
- Wrap the original: `my $orig = $mock->original('get_path_for');` captured BEFORE mocking, then `$mock->redefine(get_path_for => sub { $orig->('/my/custom/path') });`. Closures that capture `$mock` can stop it being destroyed at scope end.
- `new` returns a singleton per package while the first is alive; `distinct => 1` gives independent stackable mock objects (then prefer `Test::MockModule->original_for($pkg, $sub)` in closures). `no_auto => 1` stops it auto-loading the package. `is_mocked($sub)` and `mocked_subs` inspect state.

### Exported subs
Mocking `POSIX::strftime` does not change callers that already imported `strftime`. Mock the fully qualified call, or mock the importing package (`Test::MockModule->new('MyModule', no_auto => 1)->mock(strftime => ...)`); `main` works the same way for test-file code.

### Moose, Moo
For Moose and Mouse classes mocks are registered with the meta-class (role `requires` and method modifiers see them); immutable Moose classes fall back to symbol-table only with a warning (call `make_mutable` first). Moo, Role::Tiny and Object::Pad are not detected: mocks work for direct calls but not for role application or modifier resolution.

## Test2::Tools::Mock (exports `mock`, `mocked` and others by default)
```perl
my $mock = mock 'Some::Class' => (
    track    => 1,                                 # track calls for subs defined after this point
    add      => [ new_method => sub { ... } ],     # add a method (class must not have it)
    override => [ replace_method => sub { ... } ], # replace an existing method
    set      => [ replace_or_inject => sub { ... } ],
);
$mock->override(...);                              # more later
$mock = undef;                                     # restores all original methods
my $obj = mock {} => (add => [ is_active => sub { ... } ]);   # blessed hashref into an anonymous package
```
- `mock()` / `mock {...}` / `mock 'obj', ...` build instances where methods vivify as read/write accessors; `mock $class_or_instance => (...)` mocks a package (an instance mocks its class). `mocked($object_or_class)` returns the Test2::Mock control objects. Argument keys may repeat.
- Explicit forms: `mock_obj`, `mock_class`; builder forms `mock_build $mock => sub { mock_do ... }`. Generators `mock_accessor`, `mock_getter`, `mock_setter` and plural `mock_accessors(qw/a b/)` return `name => coderef` pairs for `add`.
- The control object is a Test2::Mock; its methods are documented there (not read).

## Rules
- Mock at the boundary you own; prefer `redefine`/`override` over `mock`/`set` so renamed subs break the test.
- Hold the mock object in a lexical block and let it go out of scope.

## Self-check
- [ ] The test passes offline, and `Module::Name::subroutine` is the original again after the block.

## Checked
Method: 2026-11-08 read the full plain-text POD of Test::MockModule and Test2::Tools::Mock via the MetaCPAN API. Test2::V0 (checks such as `is`, `dies`, `bag`) and Test::MockObject were not read, so their source URL and the v1 claims about them, plus the Test::MockTime, SQLite :memory:, dependency-injection and BEGIN advice, were removed. The Test2::Mock method list was not read.
