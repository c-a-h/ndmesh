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

my $command = "/nphMotionJpeg?Resolution=320x240&Quality=Motion&Framerate=20";
my $command2 = "/SnapshotJPEG?Resolution=640x480&Quality=Standard";
my $command3 = "/nphVideo?Mode=0&Resolution=320x240&Quality=Standard";

my ($mainHost, $kidpid, $handle, $line);
my @array;

$handle = IO::Socket::INET->new(Proto => "tcp",
                                PeerAddr => $host2,
                                PeerPort => $port,
                                Timeout => 5)
        or die "can't connect to port $port on $host2:  $1\n";
        
$handle->autoflush(1);
die "can't fork: $! \n" unless defined($kidpid = fork());

#MAKE CALLBACK FUNCTION?
my $temp = 0;
my $extra;
local $/ = "\n\n\n";

if($kidpid){
    print STDOUT "Content-type: multipart/x-mixed-replace; boundary=--myboundary\n\n";
    while ($line = <$handle>){
        chomp($line);
        if($temp < 4){
            $temp++;
        }
        else{
            #chomp;
            #$extra = $line;
            #chomp($line);
            #$line .= "\n";
            #if($line eq "Content-type")
            #NEED TO PROCESS THE STRING HERE!!!
            #chop($line);
            #chop($line);
            #chop($line);
            print STDOUT $line;
        }
        #print STDOUT $line;
        #push(@array, $line);
        #print STDOUT "I'M in the loop\n";
        #print STDOUT $line;
        
    }
    #shift(@array);
    #shift(@array);
    #print STDOUT "Content-type: multipart/x-mixed-replace;boundary=--myboundary\n\n";
    #print STDOUT @array;
    kill("TERM",$kidpid);
}

else{
    
    
    print $handle "$host1 $command";
    
    
    
}
