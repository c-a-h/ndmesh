#!/usr/bin/perl
use warnings;
use strict;
use CGI qw( :standard );
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;
use strict;
use DBI;
use DBD::mysql;
#this script creates the map page from the meshcam database

my $user = "webuser";
my $password = "webpassword";

my $dsn = "DBI:mysql:meshcam:localhost";
my $dbh = DBI->connect($dsn, $user, $password) or die $DBI::errstr;



my $sth = $dbh->prepare("SELECT * FROM ROUTER_INFO");

$sth->execute() || die $sth->errstr;
my @row;
my @ngw;
my @gw;
#print "Content-type: text/plain\n\n";

#


while($_ = $sth->fetchrow_hashref){
    if($_->{Type} =~ m/NGW/){
        push @ngw, $_;
    }
    else{
        push @gw, $_;
    }
    push @row, $_;
    
}





#print "@row[0]->{has_camera}";

#print "\n\n";

#print "<br>";
#
#print @row[0]->{Name};
#print "\n new section\n\n";



#push(@row,$sth->fetchrow_array);
#push(@row,$sth->fetchrow_array);
#my $info = $sth->fetchrow->hashref;


#print $info;
  #while ( @row = $sth->fetchrow_array ) {
  #  print "@row\n";
  #}
  
  #print "this should be the last entry: \n";
  #
  #print @row[8];
  


$dbh->disconnect || die "Failed to disconnect\n";


#
my $template = HTML::Template->new(filename => "/usr/local/apache2/htdocs/ndmesh/map.tmpl");
#$template->param(test => @row[0]->{Name});
$template->param(first => \@row);
$template->param(ngw => \@ngw);
$template->param(gw => \@gw);
#$template->param(\@row => \@row);
#
#$template->param(gwaddr => $gwAddress);
#$template->param(ngwaddr    => $ngwAddress);
#
print "Content-type: text/html\n\n";
print $template->output();
#
##print "Content-type: text/html\n\n";

