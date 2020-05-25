#!/bin/usr/perl

$i=0;
$wav=undef;
$txt="";

while(<STDIN>){
  chomp();
  if(m/\/([^\/]*.wav)/){
    if($i>0){
      print "$wav $txt\n";
      $wav=undef;
      $txt="";
    }
    $wav = $1;
    $i+=1;
  }elsif(m/ret":"([^\"]*)"/){
    $txt = $txt." $1";
  }
}
if($i>0){
      print "$wav $txt\n";
      $wav=undef;
      $txt="";
}
