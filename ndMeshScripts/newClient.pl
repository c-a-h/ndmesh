#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI::Carp qw(fatalsToBrowser);
use IO::Socket;

my $host = "localhost";
my $host1 = "172.30.100.41";
my $host2 = "129.74.152.233";
my $snoopy = "snoopy.cse.nd.edu";
my $port = 8081;

my $command = "/SnapshotJPEG?Resolution=192x144";

my ($mainHost, $kidpid, $handle, $line);

$handle = IO::Socket::INET->new(Proto => "tcp",
                                PeerAddr => $host2,
                                PeerPort => $port)
        or die "can't connect to port $port on $host2:  $1\n";
        
$handle->autoflush(1);
die "can't fork: $! \n" unless defined($kidpid = fork());

if($kidpid){
    while (defined ($line = <$handle>)){
        print STDOUT $line;
    }
    kill("TERM",$kidpid);
}

else{
    while(defined ($line = <STDIN>)){
        if($line == 2){
            print $handle "172.30.100.41 $command";
        }
        else{
            print "didn't send a command\n";
        }
    }
}
