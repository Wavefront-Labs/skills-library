---
id: computing-software.software-engineering.perl.autoload-destroy-can
name: autoload-destroy-can
category: computing-software
field: software-engineering
product: perl
tags: [perl, autoload, destroy, universal-can, universal-isa, perlobj, autoload-destroy-can]
level: advanced
status: docs-checked
description: "Implement AUTOLOAD and DESTROY safely, override can, and use UNIVERSAL::isa/can/DOES without breaking on non-objects."
sources: ["https://perldoc.perl.org/perlobj", "https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/UNIVERSAL"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AUTOLOAD, DESTROY, can and UNIVERSAL methods

**Goal:** the metaprogramming hooks and their traps.

```perl
package Dyn;
our $AUTOLOAD;
sub new { bless {}, shift }
sub AUTOLOAD {
    my $self = shift;
    (my $name = $AUTOLOAD) =~ s/.*:://;
    return if $name eq 'DESTROY';          # never autoload DESTROY
    die "No method $name" unless $name =~ /^(?:alpha|beta)\z/;
    no strict 'refs';
    *{$AUTOLOAD} = sub { return "$name!" };   # install, so AUTOLOAD runs once per method
    unshift @_, $self;
    goto &$AUTOLOAD;                          # transparent tail call
}
sub can { my ($s, $m) = @_; $s->SUPER::can($m) || ($m =~ /^(?:alpha|beta)\z/ ? sub { shift->$m(@_) } : undef) }
```

## DESTROY
```perl
sub DESTROY {
    my $self = shift;
    local ($., $@, $!, $^E, $?);        # do not clobber caller's globals
    $self->{fh}->close if $self->{fh};
}
```
- It runs when the last reference disappears (and at global destruction, where other objects may already be gone).
- Do not `die` in DESTROY (the error becomes a warning "(in cleanup)").

## UNIVERSAL
`$x->isa('C')`, `$x->can('m')`, `$x->DOES('Role')`, `$x->VERSION`. These are meant for blessed references or package names (perl UNIVERSAL); check an arbitrary value with `Scalar::Util::blessed` first.

## Failure modes
- AUTOLOAD without a DESTROY guard turns object cleanup into a "No method DESTROY" error.

## Self-check
- [ ] Objects with AUTOLOAD survive `undef $obj` with no warnings under `use warnings`.

## Checked
2026-11-02: confirmed against perlobj (DESTROY: localise globals, "(in cleanup)" warning, global destruction) and UNIVERSAL (isa, can, DOES, VERSION). Removed: DESTROY ordering, accessor-speed and UNIVERSAL::isa remarks.
Method: documentation only; no commands were run.
