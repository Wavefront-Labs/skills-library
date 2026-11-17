---
id: computing-software.software-engineering.perl.dbix-class-orm
name: dbix-class-orm
category: computing-software
field: software-engineering
product: perl
tags: [perl, dbix-class, resultset, schema-loader, orm, deploy-schema, dbix-class-orm]
level: advanced
status: draft
description: "Define a schema with DBIx::Class, query through ResultSets with joins and prefetch, use txn_do and deploy migrations."
sources: ["https://metacpan.org/pod/DBIx::Class", "https://metacpan.org/pod/DBIx::Class::Manual::Intro", "https://metacpan.org/pod/DBIx::Class::Migration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DBIx::Class ORM basics

**Goal:** query relational data through objects without hand-written SQL.

```perl
package MyApp::Schema::Result::Artist;
use base 'DBIx::Class::Core';                  # or Moo-based via DBIx::Class::Candy
__PACKAGE__->table('artist');
__PACKAGE__->add_columns(id => { data_type => 'integer', is_auto_increment => 1 }, name => { data_type => 'varchar', size => 100 });
__PACKAGE__->set_primary_key('id');
__PACKAGE__->has_many(albums => 'MyApp::Schema::Result::Album', 'artist_id');
1;
```
```perl
my $schema = MyApp::Schema->connect($dsn, $user, $pass, { RaiseError => 1, quote_names => 1 });
my $rs = $schema->resultset('Artist')->search({ 'me.name' => { -like => 'A%' } },
         { join => 'albums', prefetch => 'albums', order_by => { -asc => 'me.name' }, rows => 10 });
while (my $a = $rs->next) { say $a->name, ': ', join ',', map { $_->title } $a->albums }
my $new = $schema->resultset('Artist')->create({ name => 'X' });
$new->update({ name => 'Y' });  $new->delete;  $rs->update({ ... });   # bulk update via ResultSet
$schema->txn_do(sub { ... });                      # transaction, rolls back on die
my $c = $rs->count;  my $one = $rs->find($id);  $rs->search(undef, { columns => ['name'], group_by => 'name' });
```

## Rules
- ResultSets are lazy: a query runs when you iterate, `->all`, `->count` or `->first`; chain `search` calls to refine.
- `prefetch` avoids N+1 queries when you will traverse the relation; `join` alone does not fetch related rows.
- Column names in conditions should be prefixed `me.`/`alias.` when joining.
- Generate result classes from an existing DB with `dbicdump` (DBIx::Class::Schema::Loader), then freeze them for production.
- Set `DBIC_TRACE=1` in the environment to log SQL; `$schema->storage->debug(1)` too.
- Migrations: DBIx::Class::Migration or `DBIx::Class::DeploymentHandler`; `$schema->deploy` only for fresh DBs.
- Raw DBI access: `$schema->storage->dbh_do(sub { ... })`.
- Alternatives: Mojo::Pg/Mojo::SQLite (non-blocking, Mojolicious), `SQL::Abstract` + DBI, Rose::DB::Object, Dancer2::Plugin::DBIC.

## Failure modes
- N+1 query storms from loops that call a relation accessor.
- `delete` on a ResultSet vs row (`delete_all` runs row-level hooks, `delete` issues one statement).

## Self-check
- [ ] With `DBIC_TRACE=1` the artist listing logs one query (using prefetch), not one per artist.
