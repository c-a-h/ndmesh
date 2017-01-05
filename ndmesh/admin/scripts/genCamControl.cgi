#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;
#this script will make the links relevant to a specific camera on the cam.html page




#my $host = "localhost";
#my $host1 = "172.30.100.41";
#my $host2 = "129.74.152.233";
#my $snoopy = "snoopy.cse.nd.edu";
#my $port = 8081;


#########
#this is a test
#my $input = param('command');
#die "you didn't enter a command, try again \n" unless $input;
#my $snap = param('snapshot');
#
my $gwAddress = param('gwaddress');
die "you didn't enter an ip address for GW, try again \n" unless $gwAddress;
my $ngwAddress = param('ngwaddress');
die "you didn't enter an ip address for NGW, try again \n" unless $ngwAddress;
my $tempPage = param('page');
die "you didn't choose which page to display to\n" unless $tempPage;
my $camname = param('camname');


my $template;
if($tempPage == 23){
    $template = HTML::Template->new(filename => "/usr/local/apache2/htdocs/ndmesh/admin/backup/old/cam.tmpl");
}
elsif($tempPage == 3){
    $template = HTML::Template->new(filename => "/usr/local/apache2/htdocs/ndmesh/test1.tmpl");
    $template->param(confirm => 1);
    #this link is probably broken
}
elsif($tempPage == 9){
    $template = HTML::Template->new(filename => "/usr/local/apache2/htdocs/ndmesh/admin/cam.tmpl");
    $template->param(camname => $camname);
}
elsif($tempPage == 8){
    $template = HTML::Template->new(filename => "/usr/local/apache2/htdocs/ndmesh/admin/camstream.tmpl");
    $template->param(camname => $camname);
}
else{
    die "incorrect page number parameter\n";
}


$template->param(gwaddr => $gwAddress);
$template->param(ngwaddr    => $ngwAddress);

print "Content-type: text/html\n\n";
print $template->output();

#print "Content-type: text/html\n\n";

