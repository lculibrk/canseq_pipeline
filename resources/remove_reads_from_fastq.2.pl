#!/usr/bin/perl

##########
#a script to remove reads from a fastq file based on an input file of read names
#-inputs : -1 read_names.txt -2 original.fq 
#
# usage: /usr/bin/perl remove_reads_from_fastq.pl -1 read_names.txt -2 original.fq > new.fq
# 
#
#written by greg taylor june 2018
##########

use strict;
use Data::Dumper;

use Getopt::Std;
&getopts('1:2:');
use vars qw($opt_1 $opt_2);

unless ($opt_1 && $opt_2) {
  help();
}


#####
#determine file types
#####

my $f1="undef";    #file1 file-type
my $f2="undef";    #file2 file-type

open(FILE1, "$opt_1") || die "Cannot open the file $opt_1\n";
close (FILE1);
 
open(FILE2, "$opt_2") || die "Cannot open the file $opt_2\n";
close (FILE2);



######
#parse original input files to reduce data
######

open(FILE1, "$opt_1") || die "Cannot open the file $opt_1\n";
open(FILE2, "$opt_2") || die "Cannot open the file $opt_2\n";

my %parsed = ();
my %read;
my %col3;
my %col4;
for (my $x=0; $x <= 2000000; $x++){
  my $line1 = <FILE1>;
  chomp $line1;
  my @line1 = split (/\s+/, $line1);
  $read{$line1[0]} = 1;
}


while (my $line2 = <FILE2>){
  chomp $line2;
  my @line2 = split (/\s+/, $line2);
  if (defined $read{$line2[0]}) {
#    print "$line2". "\n";
    $line2 = <FILE2>;
#    print "$line2";
    $line2 = <FILE2>;
#    print "$line2";
    $line2 = <FILE2>;
#    print "$line2";
    delete $read{$line2[0]};
    my $line1 = <FILE1>;
    chomp $line1;
    my @line1 = split (/\s+/, $line1);
    $read{$line1[0]} = 1;
  } 
  else{
    print "$line2". "\n";
    $line2 = <FILE2>;
    print "$line2";
    $line2 = <FILE2>;
    print "$line2";
    $line2 = <FILE2>;
    print "$line2";
  }


}

close FILE1;
close FILE2;





sub help {
 print "remove_reads_from_fastq.pl\n";
 print "\t-1 read_names.txt \n";
 print "\t-2 original.fq 2\n";
 print "\t > new.fq \n";
 exit();
}

