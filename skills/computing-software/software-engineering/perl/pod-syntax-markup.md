---
id: computing-software.software-engineering.perl.pod-syntax-markup
name: pod-syntax-markup
category: computing-software
field: software-engineering
product: perl
tags: [perl, pod, pod-syntax, head1, pod-formatting-codes, perlpod, pod-syntax-markup, perl-pod-docs]
level: intro
status: docs-checked
description: "Write POD: commands (=head1, =over, =item), formatting codes (B<> I<> C<> L<> E<>), verbatim blocks and standard module sections."
sources: ["https://perldoc.perl.org/perlpod", "https://perldoc.perl.org/perlpodstyle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# POD syntax and markup

**Goal:** documentation that renders everywhere (`perldoc`, MetaCPAN, man pages).

```pod
=encoding utf8

=head1 NAME

My::Module - one-line abstract

=head1 SYNOPSIS

    use My::Module;
    my $obj = My::Module->new(name => 'x');
    $obj->run;

=head1 DESCRIPTION

Text with B<bold>, I<italic>, C<code>, F<file/name>, E<lt>tagE<gt> and L<Other::Module>,
L<perlfunc/open>, L<link text|https://example.org/>.

=head2 Methods

=over 4

=item new(%args)

Creates an object.  C<<< $a <=> $b >>> uses extra delimiters for code containing C<< > >>.

=item run

=back

=head1 AUTHOR

=head1 LICENSE

=cut
```

## Rules
- A POD block starts with a `=command` at the beginning of a line (preceded by a blank line) and runs to `=cut`; Perl skips POD at compile time. Code indented in POD is verbatim.
- Lists: `=over N`, `=item *` (bullets), `=item 1.` (numbered), `=item text`, closed with `=back`.
- Escape `<` `>` with `E<lt>` `E<gt>`; wide characters need `=encoding utf8`.
- Standard sections (perlpodstyle): NAME, SYNOPSIS, DESCRIPTION, OPTIONS, BUGS, AUTHOR, COPYRIGHT AND LICENSE, SEE ALSO. The NAME line is `Module::Name - abstract`.
- `=for`, `=begin html ... =end html` carry format-specific text.
- `=pod` starts POD without a heading; `=cut` returns to code.

## Failure modes
- Missing blank line before `=head1` makes it part of the paragraph.
- Unbalanced `=over`/`=back`.

## Self-check
- [ ] `podchecker lib/My/Module.pm` (see perlpod) reports no errors.

## Checked

2026-11-02. Confirmed in perlpod (commands, `=over`/`=item`/`=back`, bullet and numbered items, `=begin`/`=for`, `=encoding`, `=cut`, blank-line rules, formatting codes) and perlpodstyle (NAME, SYNOPSIS, DESCRIPTION, OPTIONS, BUGS, AUTHOR, SEE ALSO sections). Removed: the third-party POD tool list, the exact `podchecker` output text and unverified section names.

Method: documentation only; no commands were run.
