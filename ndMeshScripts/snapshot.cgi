#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use IO::Socket;

#this script pulls a snapshot from a specified camera/gw

my $host = "localhost";
my $host1 = "172.30.100.41";
my $host2 = "129.74.152.233";
my $snoopy = "snoopy.cse.nd.edu";
my $port = 8081;


#########

my $resolution = param('resolution');
die "you didn't choose a resolution, try again \n" unless $resolution;


my $gwAddress = param('gwaddress');
die "you didn't enter an ip address for GW, try again \n" unless $gwAddress;
my $ngwAddress = param('ngwaddress');
die "you didn't enter an ip address for NGW, try again\n" unless $ngwAddress;


#print "Content-type: text/html\n\n";
#print "This is what I got: $input\n";

#die "done\n";
#die "command: $input  gw: $gwAddress ngw: $ngwAddress\n";
##############

my $snapCommand = "/SnapshotJPEG?Resolution=320x240";

my $input;

if($resolution == 1){
    $input = "/SnapshotJPEG?Resolution=192x144";
}
elsif($resolution == 2){
    $input = "/SnapshotJPEG?Resolution=320x240";
}
elsif($resolution == 3){
    $input = "/SnapshotJPEG?Resolution=640x480";
}
else{
    die "Incorrect value for resolution\n";
}


###########
#below was for debugging:

#print "Content-type: text/html\n\n";
#print $move;
#die "all doone!\n";
#if(@params){
#    print "here you go:\n";
#    #my $name=$query->param('Direction');
#    print @params;
#}
###################


my ($mainHost, $kidpid, $handle, $line);
my @array;

$handle = IO::Socket::INET->new(Proto => "tcp",
                                PeerAddr => $gwAddress,
                                PeerPort => $port,
                                Timeout => 5)
        or die "can't connect to port $port on $gwAddress:  $!\n";
        
$handle->autoflush(1);
die "can't fork: $! \n" unless defined($kidpid = fork());

#commented code was used for debugging
my $temp = 0;
my $extra;
my $index;
my @practice;
local $/ = "\n\n\n";

if($kidpid){
    #print STDOUT "Content-type: text/html\n\n";
    while ($line = <$handle>){
        
        #chomp($line);
        #chop($line);
        #chop($line);
        #chop($line);
        if($temp < 2){
            if($line =~ /Content-type:/){
                #print $line;
                #@practice=$line;
                chomp($line);
                $index = index($line,"Content-type:");
                #print "the index is $index\n";
                print substr($line,$index);
                
                #kill("TERM",$kidpid);
                #die "we are done for now\n";
            }
            $temp++;
        }
        else{
            kill("TERM",$kidpid);
            #chomp;
            #$extra = $line;
            #chomp($line);
            #$line .= "\n";
            #if($line eq "Content-type")
            #NEED TO PROCESS THE STRING HERE!!!
            chomp($line);
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
    #this is the child process
    
    print $handle "$ngwAddress $input";
    
}
