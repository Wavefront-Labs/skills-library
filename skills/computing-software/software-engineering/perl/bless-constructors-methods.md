---
id: computing-software.software-engineering.perl.bless-constructors-methods
name: bless-constructors-methods
category: computing-software
field: software-engineering
product: perl
tags: [perl, bless, constructor, methods, perlobj, perlootut, bless-constructors-methods, perl-oop-core]
level: practitioner
status: docs-checked
description: "Write a class with bless, a new constructor, accessors and method calls, including indirect object syntax to avoid."
sources: ["https://perldoc.perl.org/perlobj", "https://perldoc.perl.org/perlootut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packages, bless, constructors and methods

**Goal:** the bare-Perl object model.

```perl
package Counter;
use strict; use warnings;

sub new {
    my ($class, %args) = @_;
    my $self = bless { count => $args{start} // 0 }, $class;
    return $self;
}
sub inc   { my $self = shift; $self->{count}++; return $self }   # chainable
sub count { $_[0]{count} }
1;

package main;
my $c = Counter->new(start => 5);
$c->inc->inc;  print $c->count;       # 7
my $method = 'count';  $c->$method;    # dynamic method name
my $class  = 'Counter'; $class->new;   # class from a string
```

## Rules
- An object is a reference blessed into a package; a class is a package; a method is a sub whose first argument is the invocant.
- `Class->method(@a)` is `Class::method('Class', @a)`; `$obj->method` passes the object. Use `shift` for the invocant, not `ref`-guessing.
- Use the two-argument form `bless {...}, $class` so subclasses get their own class name.
- Subclass constructors call `$class->SUPER::new(%args)` (resolution is relative to the package where the sub was compiled).
- Avoid indirect object syntax (`new Counter(1)`); it can be turned off with `no feature 'indirect'` (see the feature docs).
- Keep data private by convention (`_name`), via inside-out objects or closures.
- `ref($self)` returns the class; `$self->isa('X')` and `$self->can('m')` are safer than string compares.
- Hand-written accessors are boilerplate; object frameworks can generate them.

## Failure modes
- Forgetting `return $self` from a chainable method.
- Calling `Counter::new(...)` as a function loses inheritance.
- A missing `1;` at the end of a module file dies at `require` unless the `module_true` feature is enabled (see the feature docs).

## Self-check
- [ ] `perl -e 'package P; sub new{bless{},shift} package main; print ref(P->new)'` prints `P`.

## Checked
2026-11-02: confirmed against perlobj (bless one and two argument forms, SUPER resolution, indirect object syntax and the indirect feature) and feature (module_true). Removed: version numbers, Object::Pad/Moo remarks.
Method: documentation only; no commands were run.
