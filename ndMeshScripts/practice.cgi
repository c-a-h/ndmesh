#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI::Carp qw(fatalsToBrowser);
use IO::Socket;

my $test = new IO::Socket::INET(
    LocalHost => 'snoopy.cse.nd.edu',
    LocalPort => '7079',
    Listen => 1,
    Reuse => 1,
);

die "didn't work   $!  \n" unless $test;
