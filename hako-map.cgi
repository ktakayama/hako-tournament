#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# 地図モードモジュール
# $Id: hako-map.cgi,v 1.8 2004/11/10 13:45:13 gaba Exp $

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン
sub printIslandMain {
	# 開放
	unlock();

	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# 名前の取得
	$HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

	# 観光画面
	tempPrintIslandHead();	# ようこそ!!
	islandInfo();			# 島の情報
	islandMap(0) if(!$easy_mode); # 島の地図、観光モード

	# ○○島ローカル掲示板
	if($HuseLbbs) {
		tempLbbsHead();		# ローカル掲示板
		tempLbbsInput();	# 書き込みフォーム
		tempLbbsContents();	# 掲示板内容
	}

	# 近況　簡易観光者通信の場合は表示しない
	tempRecent(0) if(!$easy_mode);
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン
sub ownerMain {
	# 開放
	unlock();

	# モードを明示
	$HmainMode = 'owner';

	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		return;
	}

    # 開発画面
    if($HjavaMode eq 'java') {
		write_access_log("JS"); # アクセスログ
		tempOwnerJava();	# 「Javaスクリプト開発計画」
    } else {
		write_access_log("NM"); # アクセスログ
		tempOwner();		# 「通常モード開発計画」
    }

    # ○○島ローカル掲示板
    if($HuseLbbs) {
		tempLbbsHead();			# ローカル掲示板
		tempLbbsInputOW();		# 書き込みフォーム
		tempLbbsContents();		# 掲示板内容
    }

	# 近況
	tempRecent(1);
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン
sub commandMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# モードで分岐
	my($command) = $island->{'command'};

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# フル整地、フル地ならし
		# 座標配列を作る
		makeRandomPointArray();
		my($land) = $island->{'land'};

		# コマンドの種類決定
		my($kind) = $HcomPrepare;
		if($HcommandKind == $HcomAutoPrepare2) {
			$kind = $HcomPrepare2;
		}

		my($i) = 0;
		my($j) = 0;
		while(($j < $HpointNumber) && ($i < $HcommandMax)) {
			my($x) = $Hrpx[$j];
			my($y) = $Hrpy[$j];
			if($land->[$x][$y] == $HlandWaste) {
				slideBack($command, $HcommandPlanNumber);
				$command->[$HcommandPlanNumber] = {
					'kind' => $kind,
					'target' => 0,
					'x' => $x,
					'y' => $y,
					'arg' => 0
					};
				$i++;
			}
			$j++;
		}
		tempCommandAdd();
	} elsif($HcommandKind == $HcomAutoDelete) {
		# 全消し
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		tempCommandDelete();

	} elsif($HcommandKind == $HcomPrepRecr) {
		# 埋め立て＋地ならし
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		slideBack($command, $HcommandPlanNumber);
		tempCommandAdd();
		# コマンドを登録
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcomReclaim,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
		$command->[$HcommandPlanNumber + 1] = {
			'kind' => $HcomPrepare2,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
		};

	} else {
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		tempCommandAdd();
		# コマンドを登録
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcommandKind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
	}

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();

}

#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン
sub commentMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# メッセージを更新
	$island->{'comment'} = htmlEscape($Hmessage);

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# コメント更新メッセージ
	tempComment();

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン

sub localBbsMain {
	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($foreignName);

	# なぜかその島がない場合
	if($HcurrentNumber eq '' && $HcurrentID != 0) {
		unlock();
		tempProblem();
		return;
	}

	# 削除モードじゃなくて名前かメッセージがない場合
	if($HlbbsMode != 2) {
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# 島無し観光者以外はパスワードチェック
	if($HlbbsMode == 0 && $HforID != 0) {
		# 外国者モード
		my($foreignNumber) = $HidToNumber{$HforID};
		if($foreignNumber eq ''){
			unlock();
			tempProblem();
			return;
		}
		my($fIsland) = $Hislands[$foreignNumber];
		if(!checkPassword($fIsland->{'password'},$HinputPassword)) {
			unlock();
			tempWrongPassword();
			return;
		}
		$foreignName  = "<A HREF=\"".$HthisFile."?BBS=".$fIsland->{'id'}."\" STYlE=\"text-decoration:none\" TARGET=_blank>";
		$foreignName .= "<font size=-1 color=gray>(".$fIsland->{'name'}."島)</font></A>";
	} elsif($HlbbsMode) {
		# 島主モード
		if(!checkPassword($island->{'password'},$HinputPassword)) {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}

	my($lbbs);
	$lbbs = $island->{'lbbs'};

	# モードで分岐
	if($HlbbsMode == 2) {
		# 削除モード
		# メッセージを前にずらす
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
		tempLbbsDelete();
	} else {
		# 記帳モード
		# メッセージを後ろにずらす
		slideLbbsMessage($lbbs);

		if($HforID == 0 and $HlbbsMode == 0){
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '3';
		} elsif (($HlbbsMode == 0) && ($HforID != $island->{'id'})){
			$HlbbsMessage = htmlEscape($HlbbsMessage) . "　　".$foreignName;
			$message = '0';
		} else {
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '1';
		}
		$HlbbsName = "$HislandTurn：" . htmlEscape($HlbbsName);
		my $now = time;
		$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage&$now";

		tempLbbsAdd();
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);

	# もとのモードへ
	if($HlbbsMode == 0) {
		printIslandMain();
	} else {
		ownerMain();
	}
}

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
	my($island) = $Hislands[$HcurrentNumber];
	# 情報表示
	my($rank) = $HcurrentNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	my($mountain) = $island->{'mountain'};
	my($mStr3) = '';
	my($cmt_) = 7;

	# 予選期間、失業者が上限を上回っていたら警告
	if($HislandTurn < $HyosenTurn) {
		my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
		$tmp = 0 if($tmp < 0);
		$mStr3 = "<FONT COLOR=RED><B>失業者が".$Hno_work.$HunitPop.
					"以上出ているので、人口増加がストップします。生産施設を建てて下さい。</B></FONT>" if($tmp >= $Hno_work);
		$cmt_++;
	}
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";

	my($mStr1) = '';
	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# 無条件またはownerモード
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
		$cmt_++;
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		# 1000億単位モード
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
		$cmt_++;

		$farm 	  = "機密" if($Hhide_farm == 2);
		$factory  = "機密" if($Hhide_factory == 2);

	}

	my($comname) ="${HtagTH_}コメント：${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
		$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
	}

	# 対戦相手の表示
	my $fight_name = '';
	if($island->{'fight_id'} > 0 and $island->{'pop'} > 0) {
		my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
		if($HcurrentNumber ne '') {
			my $tIsland = $Hislands[$HcurrentNumber];
			my $name = '<A HREF="'.$HthisFile."?Sight=".$tIsland->{'id'}."\" TARGET=_blank>$tIsland->{'name'}島</A>";
			$fight_name = "<TR><TD $HbgCommentCell COLSPAN=".$cmt_." align=CENTER nowrap=nowrap><NOBR><B>対戦相手は$nameです</B></NOBR></TD></TR>";
		}
	}

	# 開発停止の表示
	my $rest_msg = '';
	if($island->{'rest'} > 0 and $HislandNumber > 1 and $island->{'pop'} > 0) {
		$rest_msg  = "<TR><TH $HbgCommentCell COLSPAN=".$cmt_." nowrap=nowrap><NOBR>\n";
		$rest_msg .= "不戦勝により開発停止中　";
		$rest_msg .= "残り<FONT COLOR=RED>".$island->{'rest'}."</FONT>ターン</NOBR></TH></TR>";
	}

	my $time;
	if($HislandNumber > 1) {
		#　時間表示
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		$time = "<BR><B>ターン${HislandTurn}</B> （次のターンまで、$hour時間 $min分 $sec秒）";
	}

	# 人口の表示
	$pop = (!$Hhide_town or $HmainMode eq 'owner') ? $island->{'pop'}.$HunitPop : aboutPop($island->{'pop'});

	out(<<END);
<CENTER>
${time}
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}採掘場規模${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$pop</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${mountain}</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=${cmt_} align=left nowrap=nowrap><NOBR>$comname$island->{'comment'}</NOBR></TD>
</TR>
$rest_msg
$fight_name
</TABLE>
$mStr3</CENTER>
END
}

# 地図の表示
# 引数が1なら、ミサイル基地等をそのまま表示
sub islandMap {
	my($mode, $js) = @_;
	my($island);
	$island = $Hislands[$HcurrentNumber];

	# 地形、地形値を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);

	out("<CENTER><TABLE BORDER><TR><TD>");

	# コマンド取得
	my($command) = $island->{'command'};
	my($com, @comStr, $i);
	if($HmainMode eq 'owner') {
		for($i = 0; $i < $HcommandMax; $i++) {
			my($j) = $i + 1;
			$com = $command->[$i];
			if($com->{'kind'} < 20) {
				$comStr[$com->{'x'}][$com->{'y'}] .=
					" [${j}]$HcomName[$com->{'kind'}]";
			}
		}
	}

	# 座標(上)を出力
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# 各地形および改行を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# 偶数行目なら番号を出力
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], $js);
		}

		# 奇数行目なら番号を出力
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 改行を出力
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

sub landString {
	my($l, $lv, $x, $y, $mode, $comStr, $j_mode) = @_;
	my($point) = "($x,$y)";
	my($image, $alt);

	if($l == $HlandSea) {
		if($lv == 1) {
			# 浅瀬
			$image = 'land14.gif';
			$alt = '海(浅瀬)';
		} else {
			# 海
			$image = 'land0.gif';
			$alt = '海';
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		if($lv == 1) {
			$image = 'land13.gif'; # 着弾点
			$alt = '荒地';
		} else {
			$image = 'land1.gif';
			$alt = '荒地';
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$image = 'land2.gif';
		$alt = '平地';
	} elsif($l == $HlandForest) {
		# 森
		if($mode == 1) {
			$image = 'land6.gif';
			$alt = "森(${lv}$HunitTree)";
		} else {
			# 観光者の場合は木の本数隠す
			$image = 'land6.gif';
			$alt = '森';
		}
	} elsif($l == $HlandTown) {
		# 町
		my($p, $n);
		if($lv < 30) {
			$p = 3;
			$n = '村';
		} elsif($lv < 100) {
			$p = 4;
			$n = '町';
		} else {
			$p = 5;
			$n = '都市';
		}

		$image = "land${p}.gif";
		$alt = "$n(${lv}$HunitPop)";
		$alt = $n if($Hhide_town and $mode == 0);
	} elsif($l == $HlandFarm) {
		# 農場
		$image = 'land7.gif';
		$alt = "農場(${lv}0${HunitPop}規模)";
		($image,$alt) =  ('land6.gif','森') if($Hhide_farm and $mode == 0)
	} elsif($l == $HlandFactory) {
		# 工場
		$image = 'land8.gif';
		$alt = "工場(${lv}0${HunitPop}規模)";
		($image,$alt) =  ('land6.gif','森') if($Hhide_factory and $mode == 0)
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# 観光者の場合
			($image,$alt) = ($Hhide_missile) ? ('land6.gif','森') : ('land9.gif','ミサイル基地');
		} else {
			# ミサイル基地
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "ミサイル基地 (レベル ${level}/経験値 $lv)";
		}
	} elsif($l == $HlandDefence) {
		# 防衛施設
		$image = 'land10.gif';
		$alt = '防衛施設';
		($image,$alt) =  ('land6.gif','森') if($Hhide_deffence and $mode == 0)
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		$image = 'land10.gif';
		if($mode == 0) {
			# 観光者の場合は防衛施設のふり
			$alt = '防衛施設';
		} else {
			$alt = 'ハリボテ';
		}
	} elsif($l == $HlandMountain) {
		# 山
		my($str);
		$str = '';
		if($lv > 0) {
			$image = 'land15.gif';
			$alt = "山(採掘場${lv}0${HunitPop}規模)";
		} else {
			$image = 'land11.gif';
			$alt = '山';
		}
	}


	# 開発画面の場合は、座標設定
	if($j_mode) {
		if($mode == 1) {
			out(qq#<A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
			out(qq#onMouseOver="set_com($x, $y, '$point $alt'); return true;" onMouseOut="window.status = '';">#);
			$comStr = '';
		} else {
			out(qq#<A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
			out(qq#onMouseOver="window.status='$point $alt $comStr'; return true;" onMouseOut="window.status = '';">#);
		}
	} elsif($mode == 1) {
		out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	} else {
		out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	}

	out("<IMG SRC=\"$image\" TITLE=\"$point $alt $comStr\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0  ID='${x}x${y}'></A>");

}

sub islandMarking {
   out(<<END);
<script type="text/javascript">
<!--
var mArray = new Array();
var lastX = 0;
var lastY = 0;
var lastN = 19;

// ミサイル範囲のマーキングをセット
function set_mark(x, y) {
   if(!document.mark_form.mark.checked) return false;
   if(!document.getElementById) {
      alert("大変申し訳ありませんが、お使いのブラウザはこの機能をサポートしていません。");
      return false;
   }

   var num  = document.mark_form.number_mark.value;
   var kind = document.mark_form.kind_mark.value;

   if(kind == '') {
      do_mark(lastX, lastY, lastN, '-');

      if(lastX == x && lastY == y) {
         lastX = 0;
         lastY = 0;
         return;
      }
      lastX = x;
      lastY = y;
      kind = 'FFFF00';
   }

   do_mark(x, y, num, kind);
}

function do_mark(x, y, num, kind) {
   var xArray = new Array(0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
   var yArray = new Array(0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

   for (i = 0; i < num; i++) {
      var targetX = x + xArray[i];
      var targetY = y + yArray[i];

      // 行による位置調整
      if(((targetY % 2) == 0) && ((y % 2) == 1)) {
         targetX = targetX - 1;
      }
      if(!(targetX < 0 || targetX >= $HislandSize || targetY < 0 || targetY >= $HislandSize)) {
         if(kind == '-') {
            unset_highlight(targetX, targetY);
            mArray[targetX+"x"+targetY] = 0;
         } else {
            set_highlight(targetX, targetY, kind);
            mArray[targetX+"x"+targetY] = 1;
         }
      }
   }
}

// 画像をマーキング化
function set_highlight(x, y, color) {
   if(document.getElementById) {
      document.getElementById(x+"x"+y).width  = "30";
      document.getElementById(x+"x"+y).height = "30";
      document.getElementById(x+"x"+y).border = "1";
      document.getElementById(x+"x"+y).style.borderColor = "#"+color;
   }
}

// マーキング解除
function unset_highlight(x, y) {
   if(document.getElementById) {
      document.getElementById(x+"x"+y).width  = "32";
      document.getElementById(x+"x"+y).height = "32";
      document.getElementById(x+"x"+y).border = "0";
   }
}

// 全てのマーキングを解除
function unset_all_highlight() {
   for (f=0;f<$HislandSize;f++) {
      for (i=0;i<$HislandSize;i++) {
         if(mArray[i+"x"+f] == 1) {
            unset_highlight(i, f);
         }
      }
   }
}
                                                                                                                            //-->
</script>

<FORM NAME="mark_form">
マーキング<INPUT TYPE=CHECKBOX NAME="mark">
種類
<SELECT NAME="kind_mark">
<OPTION VALUE="">標準
<OPTION VALUE="FFFF00">Yellow
<OPTION VALUE="FF0000">Red
<OPTION VALUE="0000FF">Blue
<OPTION VALUE="00FF00">Green
<OPTION VALUE="FF00FF">Purple
<OPTION VALUE="CCCCBB">Gray
<OPTION VALUE="-">None
</SELECT>
範囲
<SELECT NAME="number_mark">
<OPTION VALUE="1">0HEX
<OPTION VALUE="7">1HEX
<OPTION VALUE="19" SELECTED>2HEX
</SELECT>
　<INPUT TYPE="BUTTON" VALUE="解除" onClick="unset_all_highlight();">
</FORM>
END
}


#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# 個別ログ表示
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode, 1);
	}
}

# ○○島へようこそ！！
sub tempPrintIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}へようこそ！！${H_tagBig}<BR>
END
	out($HtempBack."<BR>") if(!$Htop_blank);
	out(<<END);
</CENTER>
<SCRIPT Language="JavaScript">
<!--
function ShowMsg(n){
		window.status = n;
}
//-->
</SCRIPT>
END
}

# ○○島開発計画
sub tempOwner {

	my($island) = $Hislands[$HcurrentNumber];
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
   if(document.mark_form.mark.checked) {
      set_mark(x, y);
   } else {
      document.forms[0].elements[4].options[x].selected = true;
      document.forms[0].elements[5].options[y].selected = true;
   }
   return true;
}

function ns(x) {
	document.forms[0].elements[2].options[x].selected = true;
	return true;
}
function ShowMsg(n){
		window.status = n;
		document.forms[0].COMSTATUS.value= n;
}
//-->
</SCRIPT>
END

	islandInfo();

	out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TD $HbgInputCell VALIGN=TOP>
<CENTER>
<nobr><BR>ミサイル発射上限数[<b> $island->{'fire'} </b>]発</nobr>
<FORM action="$HthisFile" method=POST>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
	# 計画番号
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
<SELECT NAME=COMMAND>
END

	#コマンド
	my($kind, $cost, $s);
	for($i = 0; $i < $HcommandTotal; $i++) {
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
		if($kind == $HdefaultKind) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>座標(</B>
<SELECT NAME=POINTX>

END
	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out(<<END);
</SELECT><B>)</B>
<HR>
<B>数量</B><SELECT NAME=AMOUNT>
END

	# 数量
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>目標の島</B><BR>
<SELECT NAME=TARGETID>
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
</CENTER>
</TD>
<TD $HbgMapCell VALIGN=TOP><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA></center>
END
	islandMap(1);	# 島の地図、所有者モード
    out("</FORM>");
    islandMarking();
	out(<<END);
</TD>
<TD $HbgCommandCell>
END
	for($i = 0; $i < $HcommandMax; $i++) {
		tempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
	}

	out(<<END);
</TD>
</TR>
</TABLE>
</CENTER>
<HR>
<CENTER>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

# 入力済みコマンド表示
sub tempCommand {
	my($number, $command) = @_;
	my($kind, $target, $x, $y, $arg) =
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );
	my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
	my($point) = "$HtagName_($x,$y)$H_tagName";
	$target = $HidToName{$target};
	if($target eq '') {
		$target = "無人";
	}
	$target = "$HtagName_${target}島$H_tagName";
	my($value) = $arg * $HcomCost[$kind];
	if($value == 0) {
		$value = $HcomCost[$kind];
	}
	if($value < 0) {
		$value = -$value;
		$value = "$value$HunitFood";
	} else {
		$value = "$value$HunitMoney";
	}
	$value = "$HtagName_$value$H_tagName";

	my($j) = sprintf("%02d：", $number + 1);

	out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

	if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) || 
	   ($kind == $HcomGiveup)) {
		out("$name");
	} elsif(($kind == $HcomMissileNM) ||
			($kind == $HcomMissilePP)) {
		# ミサイル系
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		out("$target$pointへ$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomSell) {
		# 食料輸出
		out("$name$value");
	} elsif($kind == $HcomDestroy) {
		# 掘削
		out("$pointで$name");
	} elsif(($kind == $HcomFarm) || ($kind == $HcomFactory) ||
			 ($kind == $HcomMountain)) {
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

	out("</FONT></NOBR></A><BR>");
}

# ローカル掲示板
sub tempLbbsHead {
	out(<<END);
<HR>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}観光者通信${H_tagBig}<BR>
</CENTER>
END
}

# ローカル掲示板入力フォーム
sub tempLbbsInput {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<font color=red>島が無い方も記帳できます。又、ゲーム内容に関係の無い発言は、出来るだけ、${bbsname}へお願いします。</font>
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD colspan="2">自分の島：
<SELECT NAME="ISLANDID">
<OPTION value="0">島無い観光者
$HislandList</SELECT>
　パスワード：<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonFO$HcurrentID"></TD>
</TR>
</TABLE>
END
	out("<INPUT TYPE=HIDDEN NAME='BBSMODE'>") if($easy_mode);
	my $msg = ($easy_mode) ? "Sight=$HcurrentID>−＞通常観光画面へ..." : "BBS=$HcurrentID>−＞簡易観光者通信へ...";
	out("<B><A STYlE=\"text-decoration:none\" HREF=".$HthisFile."?".$msg."</A></B>");
	out("</FORM>\n</CENTER>\n");
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH COLSPAN=2>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
番号
<SELECT NAME=NUMBER>
END
	# 発言番号
	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
	my($lbbs, $line);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	out(<<END);
<CENTER>
<font color=red><b>島名をクリックすると、簡易観光者通信へ飛びます</b></font>
<TABLE BORDER>
<TR>
<TH>番号</TH>
<TH>記帳内容</TH>
</TR>
END

	my($i);
	$HlbbsView = $HlbbsMax if($easy_mode);
	for($i = 0; $i < $HlbbsView; $i++) {
		$line = $lbbs->[$i];
		if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
			my($j) = $i + 1;
			my ($mes) = split(/&/,$3);
			out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
			if($1 == 0) {
				# 観光者
				out("<TD>$HtagLbbsSS_$2 > $mes$H_tagLbbsSS</TD></TR>");
			} elsif($1 == 3) {
				# 島無し観光者
				out("<TD>$HtagLbbsSK_$2 > $mes$H_tagLbbsSK</TD></TR>");
			} else {
				# 島主
				out("<TD>$HtagLbbsOW_$2 > $mes$H_tagLbbsOW</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE></CENTER>
END

}

# 対戦の記録
sub FightViewMain {

	open(IN, "$HdirName/fight.log");
	my @lines = <IN>;
	close(IN);
	unlock();

	out ("${HtagTitle_}対戦の記録${H_tagTitle}<BR><DIV ALIGN=right>*敗者の島名をクリックすると敗戦時の状況が見れます</DIV>\n");

	foreach $line(@lines) {
		chop($line);
		if($line =~ /<[0-9]*>/) {
			out("</blockquote>\n");
			out("<hr><blockquote>\n<H1>　　");
			$line =~ s/<|>//g;
			my $msg = ($line == 0) ? "予選落ち" : ($line == 99) ? "決勝戦" : $line."回戦";
			out(${HtagHeader_}.$msg.${H_tagHeader}."</H1>");
		} else {
			out($line);
		}
	}
	out("</blockquote>\n");
}

sub fight_map {
    my($l, $lv);
    my($land, $landValue, $line);

	open(LIN, "${Hdirfdata}/island.${HcurrentID}");
	$islandName = <LIN>;
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		$line = <LIN>;
		for($x = 0; $x < $HislandSize; $x++) {
			$line =~ s/^(.)(..)//;
			$land->[$x][$y] = hex($1);
			$landValue->[$x][$y] = hex($2);
		}
	}
    close(LIN);
	unlock();
    out (<<END);
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
    return true;
}

function ns(x) {
    return true;
}

function ShowMsg(n){
	window.status = n;
}
//-->
</SCRIPT>
<CENTER>
${HtagBig_}${HtagName_}「${islandName}島」${H_tagName}敗戦時の様子${H_tagBig}<BR>
<a href=${HthisFile}?FightLog=0>${HtagBig_}戻る${H_tagBig}</a><BR>
<BR>
<TABLE BORDER><TR><TD>
END
	# 座標(上)を出力
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# 各地形および改行を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# 偶数行目なら番号を出力
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, 1, $comStr[$x][$y]);
		}

		# 奇数行目なら番号を出力
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 改行を出力
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

# アクセスログ保存
sub write_access_log {
	my $i;
	my $view = $_[0];

	foreach (%ENV) {
		s/&(?!(?:amp|quot|lt|gt);)/&amp;/g;
		s/"/&quot;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		last if($i > 200 and $i++);
	}
	my $xip = $ENV{'HTTP_X_FORWARDED_FOR'};
	my $ip  = $ENV{'REMOTE_ADDR'};

	my($sec, $min, $hour, $day, $month, $Year, $wday, $isdst) = localtime;
	$month ++;

	my($log_file) = $Hdiraccess."/" . $month . "-" . $day . ".cgi";
	my($agent) = $ENV{'HTTP_USER_AGENT'};
	open(ACS, ">>${log_file}");
	print  ACS time() . ", ${ip}, ${xip}, ${HcurrentID}, ${HcurrentName}島, ${view}, ${agent},\n";
	close(ACS);
}

# ローカル掲示板で名前かメッセージがない場合
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}記帳内容を削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}記帳を行いました${H_tagBig}<HR>
END
}

# コマンド削除
sub tempCommandDelete {
	out(<<END);
${HtagBig_}コマンドを削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
	out(<<END);
${HtagBig_}コマンドを登録しました${H_tagBig}<HR>
END
}

# コメント変更成功
sub tempComment {
	out(<<END);
${HtagBig_}コメントを更新しました${H_tagBig}<HR>
END
}

# 近況
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}の近況${H_tagBig}<BR>
END
	logPrintLocal($mode);
}

1;
