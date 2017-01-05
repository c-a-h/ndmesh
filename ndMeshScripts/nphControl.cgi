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



#######
#this section receives and stores the command set by the link from the webpage
my $query=CGI->new;
my @params = $query->param();


#this araa takes input from the link and adds it to the command that will be sent to the camera
my $input = $query->param('Direction');
die "no command was sent " unless $input;
my $move = "/nphControlCamera?Direction=" . $input;

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

#MAKE CALLBACK FUNCTION?
my $temp = 0;
my $extra;
local $/ = "\n\n\n";

if($kidpid){
    print STDOUT "Content-type: text/html\n\n";
    while ($line = <$handle>){
        chomp($line);
        if($temp < 2){
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
    #this is the child process
    
    print $handle "$host1 $move";
    
    
    
}
