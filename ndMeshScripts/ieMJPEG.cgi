#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use IO::Socket;

my $host = "localhost";
my $host1 = "172.30.100.41";
my $host2 = "129.74.152.233";
my $snoopy = "snoopy.cse.nd.edu";
my $port = 8081;

die "don't use this file \n";
#########
#this is a test
#my $input = param('command');
#die "you didn't enter a command, try again \n" unless $input;
#print "Content-type: text/html\n\n";
#print "This is what I got: $input\n";

#die "done\n";
##############



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
                                PeerAddr => $host2,
                                PeerPort => $port,
                                Timeout => 5)
        or die "can't connect to port $port on $host2:  $1\n";
        
$handle->autoflush(1);
die "can't fork: $! \n" unless defined($kidpid = fork());

#commented code was used for debugging
my $temp = 0;
my $extra;
my $index;
my @practice;
local $/ = "\n\n\n";

####this is the area of interest
print "\<OBJECT ID=\"Player\" width=320 height=240 CLASSID=\"CLSID:745395C8-D0E1-4227-8586-624CA9A10A8D\" CODEBASE=\"activex/AMC.cab#version=2,0,21,0\" ";
####this is the area of interest
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
    
    print $handle "$host1 $input";
    
    
    
}
