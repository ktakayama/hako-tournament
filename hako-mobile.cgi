#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# ����ü���⥸�塼��
# $Id$

McgiInput();

tempHeader();

if($HmainMode eq 'turn') {
   # �����󹹿��Ԥ�
   MturnPageMain();
} elsif($HmainMode eq 0) {
   # �Ѹ�����
   MprintMain(0);
} elsif($HmainMode eq 1) {
   # �����
   MlogMain();
} elsif($HmainMode eq 2) {
   # ��ȯ����
   MprintMain(1);
} elsif($HmainMode eq 3) {
   # �ײ����
   McmdMain(0);
} elsif($HmainMode eq 4) {
   # �ײ�����
   McmdMain(1);
} elsif($HmainMode eq 'command') {
   # �ײ�����
   McmdInputMain();
} elsif($HmainMode eq 'chartView') {
   # ���ֹ����
   MlistPageMain();
} elsif($HmainMode eq 'helpView') {
   # ���ֹ����
   MhelpPageMain();
} elsif($HmainMode eq 'expView') {
   # ���ֹ����
   MlinkPageMain();
} else {
   MtopPageMain();
}

tempFooter();

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------

# CGI �ɤ߹���
sub McgiInput {
   my $getLine = $ENV{'QUERY_STRING'};

   if($getLine =~ /ID=([0-9]+)/){
      $HcurrentID = $1;
   }
   if($getLine =~ /PS=([^\&]*)/){
      $HinputPassword = $1;
   }
   if($getLine =~ /MP=([0-9]+)/){
      $HlbbsName = $1;
   }

   if($HmainMode eq 'print') {
      $HmainMode = 0;
   }

   $HlbbsName =~ tr/0-9//cd;
}

# ���¸�߳�ǧ
sub MexistCheck {
   my $mode = shift;
   unlock() if(!$mode);

   $HcurrentNumber = $HidToNumber{$HcurrentID};

   # �ʤ��������礬�ʤ����
   if($HcurrentNumber eq '') {
      tempProblem();
      return 1;
   }

   return 0;
}

# �ѥ���ɥ����å�
sub MpassCheck {
   my $island = $Hislands[$HcurrentNumber];

   # �ѥ����
   if(!checkPassword($island->{'password'},$HinputPassword)) {
      # password�ְ㤤
      tempWrongPassword();
      return 1;
   }

   return 0;
}

# �Ͽޥ⡼��
sub MprintMain {
   my $mode = shift;

   if(MexistCheck()) {
      return;
   }
   if($mode) {
      if(MpassCheck()) {
         return;
      }
   }

   MislandInfo($mode); # ��ξ���
   MislandMap($mode); # ����Ͽ�
}

# �����
sub MlogMain {
   my $mode = 0;

   if(MexistCheck()) {
      return;
   }

   if($HinputPassword) {
      if(MpassCheck()) {
         return;
      }

      $mode = 1;
   }

   MtoMapLink($mode);

   my $i;
   for($i = 0; $i < $HlogMax/2; $i++) {
      logFilePrint($i, $HcurrentID, $mode, 2);
   }
}

# ��ȯ�ײ�
sub McmdMain {
   my $mode = shift;

   if(MexistCheck() or MpassCheck()) {
      return;
   }

   MtoMapLink(1);
   if($mode == 0) {
      McmdListPageMain($HcommandMax);
   } else {
      McmdInputPageMain();
   }
}

# ��ȯ�ײ����Ͻ���
sub McmdInputMain {
   if(MexistCheck(1) or MpassCheck()) {
      unlock();
      return;
   }

   require('hako-map.cgi');

   my $island  = $Hislands[$HcurrentNumber];

   $HcommandPlanNumber--;

   commandAdd($island);

   unlock();

   $HcommandPlanNumber++;
   MtoMapLink(1);
   McmdInputPageMain();
}

# ��ξ���
sub MislandInfo {
   my $mode = shift;
   my $island = $Hislands[$HcurrentNumber];

   # ����ɽ��
   my $rank = $HcurrentNumber + 1;
   my $farm = $island->{'farm'};
   my $factory  = $island->{'factory'};
   my $mountain = $island->{'mountain'};
   my $name;

   # ͽ�����֡����ȼԤ���¤���äƤ�����ٹ�
   my $mStr1 = '';
   if($HislandTurn < $HyosenTurn) {
      my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
      $tmp = 0 if($tmp < 0);
      $mStr1 = "<FONT COLOR=RED>���ȼԤ�".$Hno_work.$HunitPop.
      "�ʾ�ФƤ���Τǡ��͸����ä����ȥåפ��ޤ����������ߤ���ƤƲ�������</FONT><br>" if($tmp >= $Hno_work);
   }

   $farm     = ($farm == 0) ? "-" : "${farm}0$HunitPop";
   $factory  = ($factory == 0) ? "-" : "${factory}0$HunitPop";
   $mountain = ($mountain == 0) ? "-" : "${mountain}0$HunitPop";
   $farm     = "��̩" if($Hhide_farm == 2);
   $factory  = "��̩" if($Hhide_factory == 2);

   my($mStr2) = '';
   if(($HhideMoneyMode == 1) || ($mode == 1)) {
      # ̵���ޤ���owner�⡼��
      $mStr2 = "$island->{'money'}$HunitMoney";
   } elsif($HhideMoneyMode == 2) {
      $mStr2 = aboutMoney($island->{'money'});
   }

   # ��������ɽ��
   my $fight_name = '';
   if($island->{'fight_id'} > 0 and $island->{'pop'} > 0) {
      my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
      if($HcurrentNumber ne '') {
         my $tIsland = $Hislands[$HcurrentNumber];
         my $name = '<A HREF="'.$HthisFile."?Sight=$tIsland->{'id'}&MP=$HlbbsName\">$tIsland->{'name'}��</A>";
         $fight_name = "���: $name<br>";
      }
   }

   # ��ȯ��ߤ�ɽ��
   my $rest_msg = '';
   if($island->{'rest'} > 0 and $HislandNumber > 1 and $island->{'pop'} > 0) {
      $rest_msg = "���ﾡ�ˤ�곫ȯ����桡";
      $rest_msg .= "�Ĥ�<FONT COLOR=RED>".$island->{'rest'}."</FONT>������<br>";
   }

   # �͸���ɽ��
   $pop = (!$Hhide_town or $mode == 1) ? $island->{'pop'}.$HunitPop : aboutPop($island->{'pop'});

   my $cmd;
   if($mode) {
      $name = "$island->{'name'}�糫ȯ����";
      $cmd  = '<br><input type="submit" name="Mobile3" value="�ײ����">';
      $cmd  .= '<input type="submit" name="Mobile4" value="�ײ�����">';
   } else {
      $name = "$island->{'name'}��Ѹ�����";
   }

   out(<<END);
$name<br>
<hr>
���: $rank<br>
�͸�: $pop<br>
���: $mStr2<br>
����: $island->{'food'}$HunitFood<br>
����: $island->{'area'}$HunitArea<br>
����: $farm<br>
����: $factory<br>
�η�: $mountain<br>
$rest_msg
$fight_name
$mStr1
<hr>
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$island->{'id'}">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" name="Mobile1" value="�����">
$cmd
</form>
<hr>
END
}

# ����Ͽ�
sub MislandMap {
   my $mode = shift;
   my $island = $Hislands[$HcurrentNumber];

   # �Ϸ����Ϸ��ͤ����
   my($x, $y);
   my $land = $island->{'land'};
   my $landValue = $island->{'landValue'};

   # ��ɸ(��)�����
   for($x = 0; $x < $HislandSize; $x++) {
      out(qw(�� �� �� �� �� �� �� �� �� ��)[($x%10)]);
   }
   out("<br>\n");

   # ���Ϸ�����Ӳ��Ԥ����
   for($y = 0; $y < $HislandSize; $y++) {
      # �������ܤʤ��ֹ�����
      if(($y % 2) == 0) {
         my $line = ($y >= 10) ? $y-10 : $y;
         out($line);
      }

      # ���Ϸ������
      for($x = 0; $x < $HislandSize; $x++) {
         my $l = $land->[$x][$y];
         my $lv = $landValue->[$x][$y];
         MlandString($l, $lv, $x, $y, $mode);
      }

      # ������ܤʤ��ֹ�����
      if(($y % 2) == 1) {
         my $line = ($y >= 10) ? $y-10 : $y;
         out($line);
      }

      # ���Ԥ����
      out("<br>\n");
   }

   out("&nbsp;");
   for($x = 0; $x < $HislandSize; $x++) {
      out(qw(�� �� �� �� �� �� �� �� �� ��)[($x%10)]);
   }
   out("<br>\n");
}

# 1�إå���
sub MlandString {
   my($l, $lv, $x, $y, $mode, $comStr) = @_;
   my($point) = "($x,$y)";
   my($alt, $color, $img);

   if($l == $HlandSea) {
      if($lv == 1) {
         # ����
         $alt = '��';
         $color = '#6666FF';
      } else {
         # ��
         $alt = '��';
      }
   } elsif($l == $HlandWaste) {
      # ����
      $alt = '��';
      $color = '#800000';
   } elsif($l == $HlandPlains) {
      # ʿ��
      $alt = '��';
      $color = '#00F000';
   } elsif($l == $HlandForest) {
      # ��
      $alt = "��";
      $color = '#008800';
   } elsif($l == $HlandTown) {
      if($lv < 30) {
         $alt = '¼';
         $color = '#999900';
      } elsif($lv < 100) {
         $alt = 'Į';
         $color = '#996600';
      } elsif($lv < 200) {
         $alt = '��';
         $color = '#666600';
      } else {
         $alt = '��';
         $color = '#660000';
      }
   } elsif($l == $HlandFarm) {
      # ����
      if($Hhide_farm and $mode == 0) {
         $alt = '��';
         $color = '#008800';
      } else {
         $alt = "��";
         $color = '#0000FF';
      }
   } elsif($l == $HlandFactory) {
      # ����
      if($Hhide_factory and $mode == 0) {
         $alt = '��';
         $color = '#008800';
      } else {
         $alt = "��";
         $color = '#606060';
      }
   } elsif($l == $HlandBase) {
      if($mode == 0) {
         # �Ѹ��Ԥξ��
         $alt = ($Hhide_missile) ? '��' : '��';
      } else {
         # �ߥ��������
         $alt = "��";
      }
      $color = '#008800';
   } elsif($l == $HlandDefence) {
      # �ɱһ���
      if($Hhide_deffence and $mode == 0) {
         $alt = '��';
         $color = '#008800';
      } else {
         $alt = '��';
         $color = '#FF0000';
      }
   } elsif($l == $HlandHaribote) {
      # �ϥ�ܥ�
      if($mode == 0) {
         # �Ѹ��Ԥξ����ɱһ��ߤΤդ�
         $alt = '��';
      } else {
         $alt = '��';
      }
      $color = '#FF0000';
   } elsif($l == $HlandMountain) {
      # ��
      if($lv > 0) {
         $alt = "��";
      } else {
         $alt = '��';
      }
      $color = '#C03030';
   }

   if($color and $HlbbsName == 1) {
      $alt = "<font color='$color'>$alt</font>";
   } elsif($color eq '#008800' or $colore eq '#FF0000') {
      $alt = "<font color='$color'>$alt</font>";
   }

   out $alt;
}

#----------------------------------------------------------------------
# HTML ����
#----------------------------------------------------------------------
# �����󹹿��Ԥ�
sub MturnPageMain {
   unlock();

   out("�����󹹿��Ԥ��Ǥ����ä��ԤäƤ��饢���������Ʋ�������");
}

# ���ֹ����
sub MlistPageMain {
   unlock();

   out("[���] ���ֹ�: ��̾<hr>");
   for($i = 0; $i < $HislandNumber; $i++) {
      my $j = $i + 1;
      my $island = $Hislands[$i];
      out("[$j] $island->{'id'}: $island->{'name'}��<br>\n");
   }
}

# �ײ�����
sub McmdInputPageMain {
   my $island = $Hislands[$HcurrentNumber];

   $HcommandPlanNumber++;
   $HcommandKind       = 0 if($HcommandKind eq '');
   $HcommandArg        = 0 if($HcommandArg eq '');
   $HcommandX          = 0 if($HcommandX eq '');
   $HcommandY          = 0 if($HcommandY eq '');
   $HcommandMode       = 'insert' if($HcommandMode eq '');

   out(<<END);
<form action="./hako-main.cgi" method="POST">
�ײ��ֹ�(1��$HcommandMax)<br>
[1]<input type="text" name="NUMBER" value="$HcommandPlanNumber" size="2" accesskey="1" istyle="4"><br>
<br>

�ײ�<br>
<select name="COMMAND" accesskey="2">
END

   #���ޥ��
   my($kind, $cost);
   for($i = 0; $i < $HcommandTotal; $i++) {
      my $s;
      $kind = $HcomList[$i];
      $cost = $HcomCost[$kind];
      if($cost == 0) {
         $cost = '̵��'
      } elsif($cost < 0) {
         $cost = - $cost;
         $cost .= $HunitFood;
      } else {
         $cost .= $HunitMoney;
      }
      $s = ' selected' if($kind == $HcommandKind);

      out("<option value='$kind'$s>$HcomName[$kind]($cost)\n");
   }

   out(<<END);
</select><br>
<br>
��ɸ(��,��)<br>
[2]<input type="text" name="POINTX" value="$HcommandX" size="2" accesskey="2" istyle="4"> , 
[3]<input type="text" NAME="POINTY" value="$HcommandY" size="2" accesskey="3" istyle="4"><br>
<br>

����(0��49)<br>
[4]<input type="text" name="AMOUNT" value="$HcommandArg" size="2" accesskey="4" istyle="4"><br>
<br>

��ɸ<br>
<select name="TARGETID" accesskey="6">
END
   out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
   out(<<END);
<br>
</select><br>
<br>
ư��<br>
<input type="radio" name="COMMANDMODE" value="insert" accesskey="5" checked>[5]����<br>
<input type="radio" name="COMMANDMODE" value="write" accesskey="6">[6] ���<br>
<input type="radio" name="COMMANDMODE" value="delete" accesskey="7">[7] ���<br>
<br>
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" value="�ײ�����" name="CommandButton$island->{'id'}">
</form>
<hr>
END
   McmdListPageMain($HcommandMax/2);
}

# �ײ����
sub McmdListPageMain {
   my $max = shift;

   for($i = 0; $i < $max; $i++) {
      MtempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
   }
}

# �ײ�ɽ��
sub MtempCommand {
   my($number, $command) = @_;
   my($kind, $target, $x, $y, $arg) =
   (
      $command->{'kind'},
      $command->{'target'},
      $command->{'x'},
      $command->{'y'},
      $command->{'arg'}
   );
   my $name  = "${HcomName[$kind]}";
   my $point = "($x,$y)";

   my($j) = sprintf("[%02d] ", $number + 1);

   out("$j");

   if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) || ($kind == $HcomGiveup)) {
      out($name);
   } elsif(($kind == $HcomMissileNM) || ($kind == $HcomMissilePP)) {
      # �ߥ������
      $target = $HidToName{$target};
      $target =  ($target eq '') ? "̵����" : "${target}��";

      $name =~ s/ȯ��//;
      out("$target$point��${name}x$arg");
   } elsif($kind == $HcomSell) {
      # ����͢��
      out("${name}x$arg");
   } elsif(($kind == $HcomFarm) || ($kind == $HcomFactory) || ($kind == $HcomMountain)) {
      # ����դ�
      if($arg == 0) {
         out("$point��$name");
      } else {
         out("$point��$name($arg��)");
      }
   } else {
      # ��ɸ�դ�
      out("$point��$name");
   }

   out("<br>\n");
}

# �Ƽ���
sub MlinkPageMain {
   my $bbTime = get_time((stat($bbsLog))[9], 1, 1);
   unlock();

   out(<<END);
- <A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A><br>
<BR>
- <A HREF="$toppage">�ۡ���</A><br>
- <A HREF="$bbs">$bbsname</A>$bbTime<br>
END
}

# �ޥåץإ��
sub MhelpPageMain {
   unlock();

   out(<<END);
<font color="#6666FF">��</font> �� ����<br>
�� �� ��<br>
<font color="#800000">��</font> �� ����<br>
<font color="#00F000">��</font> �� ʿ��<br>
<font color="#008800">��</font> �� ��<br>

<font color="#999900">¼</font> �� ¼<br>
<font color="#996600">Į</font> �� Į<br>
<font color="#666600">��</font> �� �Ի�<br>
<font color="#660000">��</font> �� 2���͵��Ϥ��Ի�<br>

<font color="#0000FF">��</font> �� ����<br>
<font color="#606060">��</font> �� ����<br>
<font color="#C03030">��</font> �� �η���<br>
<font color="#C03030">��</font> �� ��<br>

<font color="#008800">��</font> �� �ߥ��������<br>
<font color="#FF0000">��</font> �� �ɱһ���<br>
<font color="#FF0000">��</font> �� �ϥ�ܥ�<br>
END
}

# �ȥåץڡ���
sub MtopPageMain {
   unlock();

   if($HlbbsName ne '') {
      $sL[$HlbbsName] = ' selected';
   } else {
      $sL[0] = ' selected';
   }

   if($HislandNumber > 1 or $HislandTurn == 0) {
      #������ɽ��
      my($hour, $min, $sec);
      my($now) = time;
      my($showTIME) = ($HislandLastTime + $HunitTime - $now);
      $hour = int($showTIME / 3600);
      $min  = int(($showTIME - ($hour * 3600)) / 60);
      $sec  = $showTIME - ($hour * 3600) - ($min * 60);
      if ($sec < 0 or $HislandTurnCount > 1){
         out("(�����󹹿��Ԥ��Ǥ����ä��ԤäƤ��饢���������Ʋ�������)");
      } else {
         if(!$Htime_mode) {
            my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
            out("���󹹿����� $mon2��$mday2��$hour2��$min2ʬ<br>�Ĥ� $hour���� $minʬ $sec��");
         } else {
            out("�ʼ��Υ�����ޤǡ����� $hour���� $minʬ $sec�á�");
         }
      }
   }

   out(<<END);
<hr>
<form action="./hako-main.cgi" method="POST">
ID:<input type="text" name="ISLANDID" size="3" value="$HcurrentID" istyle="4"><br>
PS:<input type="text" name="PASSWORD" size="6" value="$HinputPassword" istyle="3"><br>
���顼�⡼��:<br>
<select name="LBBSNAME">
<option$sL[0] value="0">ɸ��
<option$sL[1] value="1">�ե륫�顼
</select><br>
<input type="submit" name="Mobile2" value="��ȯ">
<input type="submit" name="Mobile0" value="�Ѹ�">
<input type="submit" name="Mobile1" value="�����">
</form>

<br>
<a href="./hako-main.cgi?chart=1">���ֹ����</a>
END
}

# �Ͽ޲��̤ؤΥե�������
sub MtoMapLink {
   my $mode = shift;

   my $name = ($mode) ? '��ȯ' : '�Ѹ�';
   my $num  = ($mode) ? 2 : 0;

   out(<<END);
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$HcurrentID">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" name="Mobile${num}" value="${name}����">
</form>
<hr>
END
}

1;

