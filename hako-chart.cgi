#----------------------------------------------------------------------
# 箱庭トーナメント２
# トーナメント表モジュール
# $Id: hako-chart.cgi,v 1.1 2004/11/03 11:01:20 gaba Exp $

#----------------------------------------------------------------------
# トーナメント表モード
#----------------------------------------------------------------------
# メイン
sub chartPageMain {
   # 開放
   unlock();

   # テンプレート出力
   tempChartPage();
}

sub tempChartPage {

   out(<<END);
${HtagTitle_}トーナメント表${H_tagTitle}
<BR>
<BR>
<HR>
<BR>
END

   open(CRT, "${Hdirfdata}/chart");
   while(<CRT>) {
      out($_);
   }
   close(CRT);

   out(<<END);
<BR><BR>
※不戦勝が多数発生した場合は、正しく表示されません。<BR>
END
}


sub makeChartPage {
   # 新しい画面を開くモードなら
   my $blank = ($Htop_blank) ? " TARGET=\"_blank\"" : "";

   my @cell = ();

   my $mTeams = $HfightMem * 2;
   my $start  = 0;
   my $end    = 0;
   my $sep    = 1;
   my $win    = 1;

   my @lines = ('', '┘', '┐', '│', '├', '─', '<b>┣</b>', '<b>━</b>', '<b>┛</b>', '<b>┓</b>', '<b>┃</b>');
   my $Charts = $HislandChart;

   my @island1 = split(/"/, $Charts);
   my @island2 = split(/"/, $Charts);

   for($f = 0;2**$f <= $HfightMem;$f++) {
      $sep += 2**$f;
      $start += 2**($f-1);
      my $x;
      $Charts = '';
      for($i = $start;$i <= $mTeams;$i++) {
         if(($i - $start) % $sep  == 0) {
            if($f == 0) {
               my ($win, $id, $name) = split(/,/, $island2[$x]);
               $win = $HislandFightCount if($win eq '-');
               $Charts .= $win.",";
               $x++;
            } else {
               $cell[$i][$f] = 4;

               my $wFlag;
               my $win  = $island2[$x];
               my $win2 = $island2[$x+1];
               $x+=2;
               if(($win >= $f or $win2 >= $f) and $win != $win2) {
                  $cell[$i][$f] = 6;
                  if($win > $win2) {
                     $Charts .= "$win,";
                     $wFlag = 1;
                  } else {
                     $Charts .= "$win2,";
                     $wFlag = 2;
                  }
               }

               for($z = 1;$z < $end;$z++) {
                  $cell[$i-$z][$f] = ($wFlag == 1) ? 10 : 3;
                  $cell[$i+$z][$f] = ($wFlag == 2) ? 10 : 3;
               }

               $cell[$i-$z][$f] = ($wFlag == 1) ? 9 : 2;
               $cell[$i+$z][$f] = ($wFlag == 2) ? 8 : 1;

            }
         }
      }
      @island2 = split(/,/, $Charts);

      $end += 2**($f-1);
   }

   open(CRT, ">${Hdirfdata}/chart.bak");
   print CRT "<TABLE border=0 cellspacing=0 cellpadding=0>\n";
   for($i = 0;$i < $mTeams;$i++) {
      print CRT "<tr>";
      if($i % 2 == 0) {
         my ($win, $id, $name) = split(/,/, $island1[$i/2]);
         my $num = $HidToNumber{$id};
         if($num ne '') {
            $name  = "<a style=\"text-decoration:none\" href='${HthisFile}?Sight=${id}'${blank}>";
            $name .= "${HtagName_}$Hislands[$num]->{'name'}島${H_tagName}";
            $name .= "</a>";
         } else {
            $name = "${HtagName2_}${name}${H_tagName2}";
         }
         print CRT "<td>${name}&nbsp;</td>";
      } else {
         print CRT "<td>&nbsp;</td>";
      }
      for($f = 0;2**$f <= $mTeams;$f++) {
         print CRT "<td>";
         print CRT $lines[$cell[$i][$f]];
         print CRT "</td>";
         foreach (1..3) {
            print CRT "<td>";
            if($cell[$i][$f+1] == 8 or $cell[$i][$f+1] == 9) {
               print CRT $lines[7];
            } elsif(2**$f == $mTeams/2 and $i+1 == 2**$f) {
               if($_ == 3) {
                  print CRT "&nbsp;優勝";
               }
            } elsif($cell[$i][$f] == 4 or $cell[$i][$f] == 6) {
               print CRT $lines[5];
            } elsif($f == 0 and $i % 2 == 0) {
               print CRT $lines[5];
            }
            print CRT "</td>";
         }
      }
      print CRT "</tr>";
   }
   print CRT "</TABLE>\n";
   close(CRT);

   rename("${Hdirfdata}/chart.bak", "${Hdirfdata}/chart");
}
1;

