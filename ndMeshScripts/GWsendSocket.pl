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

my $sock = new IO::Socket::INET (
    PeerAddr => $host2,
    PeerPort => '7071',
    Proto => 'tcp',
    );
die "could not create socket $!\n" unless $sock;

print $sock "5\n";

close($sock);

my $hello = "hello world\n";
my $bye = "911\n";
my $index;
my $incoming;
print "Content-type: text/html\n\n";
print "you made it this far\n";

#for($index=0; $index<10; $index++){
    $incoming = new IO::Socket::INET (
        LocalHost => 'snoopy.cse.nd.edu',
        LocalPort => '7070',
        Proto => 'tcp',
        Listen => 10,
        Reuse => 1,    
    );
#}
#close($incoming);
#die "oops\n";

#this is where to change the command to do
#whatever you like


#view image????

die "Could not create LISTENING SOCKET  $!  \n" unless $incoming;
my $in;

#print "Content-type: text/html\n\n";
#for ($in=0; $in<1000; $in++){
print "listening socket has been made, waiting for incoming...";
    my $new_incoming = $incoming->accept();
    while(<$new_incoming>){
        
        print $_;
        
    }
#}
close($incoming);




print "Content-type: text/html\n\n";
print "your script ran perfectly \n";

