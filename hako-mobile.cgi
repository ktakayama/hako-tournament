#----------------------------------------------------------------------
# 箱庭トーナメント２
# 携帯端末モジュール
# $Id$

McgiInput();

tempHeader();

if($HmainMode eq 'turn') {
   # ターン更新待ち
   MturnPageMain();
} elsif($HmainMode eq 0) {
   # 観光画面
   MprintMain(0);
} elsif($HmainMode eq 1) {
   # 出来事
   MlogMain();
} elsif($HmainMode eq 2) {
   # 開発画面
   MprintMain(1);
} elsif($HmainMode eq 3) {
   # 計画一覧
   McmdMain(0);
} elsif($HmainMode eq 4) {
   # 計画入力
   McmdMain(1);
} elsif($HmainMode eq 'command') {
   # 計画入力
   McmdInputMain();
} elsif($HmainMode eq 'chartView') {
   # 島番号一覧
   MlistPageMain();
} elsif($HmainMode eq 'helpView') {
   # 島番号一覧
   MhelpPageMain();
} elsif($HmainMode eq 'expView') {
   # 島番号一覧
   MlinkPageMain();
} else {
   MtopPageMain();
}

tempFooter();

#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------

# CGI 読み込み
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

# 島の存在確認
sub MexistCheck {
   my $mode = shift;
   unlock() if(!$mode);

   $HcurrentNumber = $HidToNumber{$HcurrentID};

   # なぜかその島がない場合
   if($HcurrentNumber eq '') {
      tempProblem();
      return 1;
   }

   return 0;
}

# パスワードチェック
sub MpassCheck {
   my $island = $Hislands[$HcurrentNumber];

   # パスワード
   if(!checkPassword($island->{'password'},$HinputPassword)) {
      # password間違い
      tempWrongPassword();
      return 1;
   }

   return 0;
}

# 地図モード
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

   MislandInfo($mode); # 島の情報
   MislandMap($mode); # 島の地図
}

# 出来事
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

# 開発計画
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

# 開発計画入力処理
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

# 島の情報
sub MislandInfo {
   my $mode = shift;
   my $island = $Hislands[$HcurrentNumber];

   # 情報表示
   my $rank = $HcurrentNumber + 1;
   my $farm = $island->{'farm'};
   my $factory  = $island->{'factory'};
   my $mountain = $island->{'mountain'};
   my $name;

   # 予選期間、失業者が上限を上回っていたら警告
   my $mStr1 = '';
   if($HislandTurn < $HyosenTurn) {
      my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
      $tmp = 0 if($tmp < 0);
      $mStr1 = "<FONT COLOR=RED>失業者が".$Hno_work.$HunitPop.
      "以上出ているので、人口増加がストップします。生産施設を建てて下さい。</FONT><br>" if($tmp >= $Hno_work);
   }

   $farm     = ($farm == 0) ? "-" : "${farm}0$HunitPop";
   $factory  = ($factory == 0) ? "-" : "${factory}0$HunitPop";
   $mountain = ($mountain == 0) ? "-" : "${mountain}0$HunitPop";
   $farm     = "機密" if($Hhide_farm == 2);
   $factory  = "機密" if($Hhide_factory == 2);

   my($mStr2) = '';
   if(($HhideMoneyMode == 1) || ($mode == 1)) {
      # 無条件またはownerモード
      $mStr2 = "$island->{'money'}$HunitMoney";
   } elsif($HhideMoneyMode == 2) {
      $mStr2 = aboutMoney($island->{'money'});
   }

   # 対戦相手の表示
   my $fight_name = '';
   if($island->{'fight_id'} > 0 and $island->{'pop'} > 0) {
      my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
      if($HcurrentNumber ne '') {
         my $tIsland = $Hislands[$HcurrentNumber];
         my $name = '<A HREF="'.$HthisFile."?Sight=$tIsland->{'id'}&MP=$HlbbsName\">$tIsland->{'name'}島</A>";
         $fight_name = "相手: $name<br>";
      }
   }

   # 開発停止の表示
   my $rest_msg = '';
   if($island->{'rest'} > 0 and $HislandNumber > 1 and $island->{'pop'} > 0) {
      $rest_msg = "不戦勝により開発停止中　";
      $rest_msg .= "残り<FONT COLOR=RED>".$island->{'rest'}."</FONT>ターン<br>";
   }

   # 人口の表示
   $pop = (!$Hhide_town or $mode == 1) ? $island->{'pop'}.$HunitPop : aboutPop($island->{'pop'});

   my $cmd;
   if($mode) {
      $name = "$island->{'name'}島開発画面";
      $cmd  = '<br><input type="submit" name="Mobile3" value="計画一覧">';
      $cmd  .= '<input type="submit" name="Mobile4" value="計画入力">';
   } else {
      $name = "$island->{'name'}島観光画面";
   }

   out(<<END);
$name<br>
<hr>
順位: $rank<br>
人口: $pop<br>
資金: $mStr2<br>
食料: $island->{'food'}$HunitFood<br>
面積: $island->{'area'}$HunitArea<br>
農場: $farm<br>
工場: $factory<br>
採掘: $mountain<br>
$rest_msg
$fight_name
$mStr1
<hr>
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$island->{'id'}">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" name="Mobile1" value="出来事">
$cmd
</form>
<hr>
END
}

# 島の地図
sub MislandMap {
   my $mode = shift;
   my $island = $Hislands[$HcurrentNumber];

   # 地形、地形値を取得
   my($x, $y);
   my $land = $island->{'land'};
   my $landValue = $island->{'landValue'};

   # 座標(上)を出力
   for($x = 0; $x < $HislandSize; $x++) {
      out(qw(０ １ ２ ３ ４ ５ ６ ７ ８ ９)[($x%10)]);
   }
   out("<br>\n");

   # 各地形および改行を出力
   for($y = 0; $y < $HislandSize; $y++) {
      # 偶数行目なら番号を出力
      if(($y % 2) == 0) {
         my $line = ($y >= 10) ? $y-10 : $y;
         out($line);
      }

      # 各地形を出力
      for($x = 0; $x < $HislandSize; $x++) {
         my $l = $land->[$x][$y];
         my $lv = $landValue->[$x][$y];
         MlandString($l, $lv, $x, $y, $mode);
      }

      # 奇数行目なら番号を出力
      if(($y % 2) == 1) {
         my $line = ($y >= 10) ? $y-10 : $y;
         out($line);
      }

      # 改行を出力
      out("<br>\n");
   }

   out("&nbsp;");
   for($x = 0; $x < $HislandSize; $x++) {
      out(qw(０ １ ２ ３ ４ ５ ６ ７ ８ ９)[($x%10)]);
   }
   out("<br>\n");
}

# 1ヘックス
sub MlandString {
   my($l, $lv, $x, $y, $mode, $comStr) = @_;
   my($point) = "($x,$y)";
   my($alt, $color, $img);

   if($l == $HlandSea) {
      if($lv == 1) {
         # 浅瀬
         $alt = '−';
         $color = '#6666FF';
      } else {
         # 海
         $alt = '・';
      }
   } elsif($l == $HlandWaste) {
      # 荒地
      $alt = '■';
      $color = '#800000';
   } elsif($l == $HlandPlains) {
      # 平地
      $alt = '□';
      $color = '#00F000';
   } elsif($l == $HlandForest) {
      # 森
      $alt = "森";
      $color = '#008800';
   } elsif($l == $HlandTown) {
      if($lv < 30) {
         $alt = '村';
         $color = '#999900';
      } elsif($lv < 100) {
         $alt = '町';
         $color = '#996600';
      } elsif($lv < 200) {
         $alt = '都';
         $color = '#666600';
      } else {
         $alt = '巨';
         $color = '#660000';
      }
   } elsif($l == $HlandFarm) {
      # 農場
      if($Hhide_farm and $mode == 0) {
         $alt = '森';
         $color = '#008800';
      } else {
         $alt = "農";
         $color = '#0000FF';
      }
   } elsif($l == $HlandFactory) {
      # 工場
      if($Hhide_factory and $mode == 0) {
         $alt = '森';
         $color = '#008800';
      } else {
         $alt = "工";
         $color = '#606060';
      }
   } elsif($l == $HlandBase) {
      if($mode == 0) {
         # 観光者の場合
         $alt = ($Hhide_missile) ? '森' : 'ミ';
      } else {
         # ミサイル基地
         $alt = "ミ";
      }
      $color = '#008800';
   } elsif($l == $HlandDefence) {
      # 防衛施設
      if($Hhide_deffence and $mode == 0) {
         $alt = '森';
         $color = '#008800';
      } else {
         $alt = '防';
         $color = '#FF0000';
      }
   } elsif($l == $HlandHaribote) {
      # ハリボテ
      if($mode == 0) {
         # 観光者の場合は防衛施設のふり
         $alt = '防';
      } else {
         $alt = 'ハ';
      }
      $color = '#FF0000';
   } elsif($l == $HlandMountain) {
      # 山
      if($lv > 0) {
         $alt = "採";
      } else {
         $alt = '山';
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
# HTML 出力
#----------------------------------------------------------------------
# ターン更新待ち
sub MturnPageMain {
   unlock();

   out("ターン更新待ちです。暫く待ってからアクセスして下さい。");
}

# 島番号一覧
sub MlistPageMain {
   unlock();

   out("[順位] 島番号: 島名<hr>");
   for($i = 0; $i < $HislandNumber; $i++) {
      my $j = $i + 1;
      my $island = $Hislands[$i];
      out("[$j] $island->{'id'}: $island->{'name'}島<br>\n");
   }
}

# 計画入力
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
計画番号(1〜$HcommandMax)<br>
[1]<input type="text" name="NUMBER" value="$HcommandPlanNumber" size="2" accesskey="1" istyle="4"><br>
<br>

計画<br>
<select name="COMMAND" accesskey="2">
END

   #コマンド
   my($kind, $cost);
   for($i = 0; $i < $HcommandTotal; $i++) {
      my $s;
      $kind = $HcomList[$i];
      $cost = $HcomCost[$kind];
      if($cost == 0) {
         $cost = '無料'
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
座標(横,縦)<br>
[2]<input type="text" name="POINTX" value="$HcommandX" size="2" accesskey="2" istyle="4"> , 
[3]<input type="text" NAME="POINTY" value="$HcommandY" size="2" accesskey="3" istyle="4"><br>
<br>

数量(0〜49)<br>
[4]<input type="text" name="AMOUNT" value="$HcommandArg" size="2" accesskey="4" istyle="4"><br>
<br>

目標<br>
<select name="TARGETID" accesskey="6">
END
   out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
   out(<<END);
<br>
</select><br>
<br>
動作<br>
<input type="radio" name="COMMANDMODE" value="insert" accesskey="5" checked>[5]挿入<br>
<input type="radio" name="COMMANDMODE" value="write" accesskey="6">[6] 上書き<br>
<input type="radio" name="COMMANDMODE" value="delete" accesskey="7">[7] 削除<br>
<br>
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" value="計画送信" name="CommandButton$island->{'id'}">
</form>
<hr>
END
   McmdListPageMain($HcommandMax/2);
}

# 計画一覧
sub McmdListPageMain {
   my $max = shift;

   for($i = 0; $i < $max; $i++) {
      MtempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
   }
}

# 計画表示
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
      # ミサイル系
      $target = $HidToName{$target};
      $target =  ($target eq '') ? "無人島" : "${target}島";

      $name =~ s/発射//;
      out("$target$pointへ${name}x$arg");
   } elsif($kind == $HcomSell) {
      # 食料輸出
      out("${name}x$arg");
   } elsif(($kind == $HcomFarm) || ($kind == $HcomFactory) || ($kind == $HcomMountain)) {
      # 回数付き
      if($arg == 0) {
         out("$pointで$name");
      } else {
         out("$pointで$name($arg回)");
      }
   } else {
      # 座標付き
      out("$pointで$name");
   }

   out("<br>\n");
}

# 各種リンク
sub MlinkPageMain {
   my $bbTime = get_time((stat($bbsLog))[9], 1, 1);
   unlock();

   out(<<END);
- <A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">箱庭諸島スクリプト配布元</A><br>
<BR>
- <A HREF="$toppage">ホーム</A><br>
- <A HREF="$bbs">$bbsname</A>$bbTime<br>
END
}

# マップヘルプ
sub MhelpPageMain {
   unlock();

   out(<<END);
<font color="#6666FF">−</font> → 浅瀬<br>
・ → 海<br>
<font color="#800000">■</font> → 荒地<br>
<font color="#00F000">□</font> → 平地<br>
<font color="#008800">森</font> → 森<br>

<font color="#999900">村</font> → 村<br>
<font color="#996600">町</font> → 町<br>
<font color="#666600">都</font> → 都市<br>
<font color="#660000">巨</font> → 2万人規模の都市<br>

<font color="#0000FF">農</font> → 農場<br>
<font color="#606060">工</font> → 工場<br>
<font color="#C03030">採</font> → 採掘場<br>
<font color="#C03030">山</font> → 山<br>

<font color="#008800">ミ</font> → ミサイル基地<br>
<font color="#FF0000">防</font> → 防衛施設<br>
<font color="#FF0000">ハ</font> → ハリボテ<br>
END
}

# トップページ
sub MtopPageMain {
   unlock();

   if($HlbbsName ne '') {
      $sL[$HlbbsName] = ' selected';
   } else {
      $sL[0] = ' selected';
   }

   if($HislandNumber > 1 or $HislandTurn == 0) {
      #　時間表示
      my($hour, $min, $sec);
      my($now) = time;
      my($showTIME) = ($HislandLastTime + $HunitTime - $now);
      $hour = int($showTIME / 3600);
      $min  = int(($showTIME - ($hour * 3600)) / 60);
      $sec  = $showTIME - ($hour * 3600) - ($min * 60);
      if ($sec < 0 or $HislandTurnCount > 1){
         out("(ターン更新待ちです。暫く待ってからアクセスして下さい。)");
      } else {
         if(!$Htime_mode) {
            my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
            out("次回更新日時 $mon2月$mday2日$hour2時$min2分<br>残り $hour時間 $min分 $sec秒");
         } else {
            out("（次のターンまで、あと $hour時間 $min分 $sec秒）");
         }
      }
   }

   out(<<END);
<hr>
<form action="./hako-main.cgi" method="POST">
ID:<input type="text" name="ISLANDID" size="3" value="$HcurrentID" istyle="4"><br>
PS:<input type="text" name="PASSWORD" size="6" value="$HinputPassword" istyle="3"><br>
カラーモード:<br>
<select name="LBBSNAME">
<option$sL[0] value="0">標準
<option$sL[1] value="1">フルカラー
</select><br>
<input type="submit" name="Mobile2" value="開発">
<input type="submit" name="Mobile0" value="観光">
<input type="submit" name="Mobile1" value="出来事">
</form>

<br>
<a href="./hako-main.cgi?chart=1">島番号一覧</a>
END
}

# 地図画面へのフォームリンク
sub MtoMapLink {
   my $mode = shift;

   my $name = ($mode) ? '開発' : '観光';
   my $num  = ($mode) ? 2 : 0;

   out(<<END);
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$HcurrentID">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="LBBSNAME" value="$HlbbsName">
<input type="submit" name="Mobile${num}" value="${name}画面">
</form>
<hr>
END
}

1;

