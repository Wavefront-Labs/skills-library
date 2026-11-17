---
id: computing-software.software-engineering.perl.moose-meta-object-protocol
name: moose-meta-object-protocol
category: computing-software
field: software-engineering
product: perl
tags: [perl, moose, make-immutable, metaclass, build-buildargs, namespace-autoclean, moose-meta-object-protocol]
level: sme
status: draft
description: "Use Moose idioms: make_immutable, BUILD and BUILDARGS, namespace::autoclean, subtypes and the meta introspection API."
sources: ["https://metacpan.org/pod/Moose", "https://metacpan.org/pod/Moose::Manual"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moose, immutability and the metaobject protocol

**Goal:** production Moose classes and introspection.

```perl
package Account;
use Moose;
use namespace::autoclean;                       # removes imported helpers (has, extends...) from the symbol table
use Moose::Util::TypeConstraints;

subtype 'PositiveInt', as 'Int', where { $_ > 0 }, message { "$_ is not positive" };
coerce  'PositiveInt', from 'Str', via { int $_ };

has balance => (is => 'rw', isa => 'Num', default => 0);
has limit   => (is => 'ro', isa => 'PositiveInt', coerce => 1, required => 1);
has history => (traits => ['Array'], is => 'ro', isa => 'ArrayRef[Str]', default => sub { [] },
                handles => { add_history => 'push', all_history => 'elements' });

around BUILDARGS => sub {                        # accept ->new($limit)
    my ($orig, $class, @a) = @_;
    return $class->$orig(limit => $a[0]) if @a == 1 && !ref $a[0];
    return $class->$orig(@a);
};
sub BUILD { my $s = shift; die "limit too low" if $s->limit < 1 }

__PACKAGE__->meta->make_immutable;               # inlines the constructor; faster
no Moose;  1;
```

## Introspection
```perl
my $meta = Account->meta;
$meta->get_attribute_list;            $meta->get_all_methods;
$meta->find_method_by_name('x');      $meta->does_role('Role::Logs');
Account->meta->get_attribute('limit')->type_constraint->name;
```

## Rules
- Always `make_immutable` for production classes (and call it last); subclasses must too.
- `BUILD` runs parent-first after construction; `BUILDARGS` customises constructor arguments; `DEMOLISH` replaces `DESTROY`.
- Startup cost: Moose loads a large MOP; for short scripts prefer Moo or Class::Tiny.
- `no Moose` or `namespace::autoclean` prevents imports being callable as methods.
- Type constraint names are strings; Type::Tiny constraints also work with Moose.

## Self-check
- [ ] `perl -MMoose -e 'print Moose->VERSION'` works; tests still pass after `make_immutable`.
