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

my $incoming = new IO::Socket::INET (
        LocalHost => '129.74.154.171',
        LocalPort => '7022',
        Proto => 'tcp',
        Listen => 10,
        Reuse => 1,    
    );


print $sock "5\n";

#ADD SHIT HERE


close($sock);


die "Could not create LISTENING SOCKET  $!  \n" unless $incoming;


my $new_incoming = $incoming->accept();
#print "before\n";
#print "Content-type: text/html\n\n";
my @image;
#$/="--myboundary\r\n";
while(<$new_incoming>){
    #print "this is a joke";
    #print $_;
    push(@image,$_);
    
    
}
#shift(@image);
#shift(@image);
#shift(@image);
my $indexer;
#print "Content-Type: image/jpeg\n\n";
print @image;

#for($indexer=0; $indexer<(947); $indexer++){
#    print $image[$indexer];
#}


#
#
#
#print "Content-type: text/html\n\n";
#print "you made it this far\n";
#
##for($index=0; $index<10; $index++){
#
##}
##close($incoming);
##die "oops\n";
#
##this is where to change the command to do
##whatever you like
#print "you're trying to connect\n";
#
##view image????
#
#
#
##print "Content-type: text/html\n\n";
##for ($in=0; $in<1000; $in++){
##print "listening socket has been made, waiting for incoming...\n";
#
#    while(<$new_incoming>){
#        
#        print $_;
#        
#    }
##}
#
close($incoming);
#
#



#print "your script ran perfectly \n";

