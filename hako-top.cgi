#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# トップモジュール
# $Id: hako-top.cgi,v 1.2 2004/02/18 04:42:31 gaba Exp $

#----------------------------------------------------------------------
# トップページモード
#----------------------------------------------------------------------
# メイン
sub topPageMain {
	# 開放
	unlock();

	# テンプレート出力
	tempTopPage();
}

# トップページ
sub tempTopPage {

    # タイトル
    out("${HtagTitle_}$Htitle${H_tagTitle}\n");

	# 回戦数の表示
	if($HislandTurn < $HyosenTurn) {
		out("${HtagFico_}≪予選≫${H_tagFico}\n");
	} elsif(($HislandNumber == 2) && ($HislandTurn != 0)) {
		out("${HtagFico_}≪決勝戦≫${H_tagFico}\n");
	} elsif($HislandNumber == 1 and $HislandTurn != 0) {
		out("${HtagFico_}≪終了≫${H_tagFico}\n");
	} else {
		out("${HtagFico_}≪第$HislandFightCount回戦≫${H_tagFico}\n");
	}

	# 新しい画面を開くモードなら
	my $blank = ($Htop_blank) ? " TARGET=\"_blank\"" : "";

	# デバッグモードなら「ターンを進める」ボタン
	if($Hdebug == 1) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
	}

	my $cmt_ = 7;
	my($mStr1) = '';
	if($HhideMoneyMode != 0) {
		$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
		$cmt_++;
	}

	my $fightmode = "";
	if($HislandFightMode == 1) {
		$fightmode = '<font color=red>戦闘期間</font>';
		if($HislandChangeTurn == $HislandTurn){
			$fightmode .= '[次ターン<font color=red>攻撃不可</font>]';
		} else {
			$fightmode .= '[ターン' . ($HislandChangeTurn + 1) . 'は攻撃不可]';
		}
	} elsif($HislandTurn < $HyosenTurn) {
		$fightmode = '<font color=blue>開発期間</font>[ターン' . ($HyosenTurn) . 'まで予選]';
	} else {
		$fightmode = '<font color=blue>開発期間</font>';
		if($HislandChangeTurn == $HislandTurn){
			$fightmode .= '[次ターンより<font color=red>戦闘開始</font>]';
		} else {
			$fightmode .= '[ターン' . ($HislandChangeTurn + 1) . 'より戦闘開始]';
		}
	}
	out("<H1>${HtagHeader_}ターン$HislandTurn${H_tagHeader}　$fightmode</H1>");

	if($HislandNumber > 1 or $HislandTurn == 0) {
		#　時間表示
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		if ($sec < 0 or $HislandTurnCount > 1){
			out("<B><font size=+1>（${HtagHeader_}更新して下さい${H_tagHeader}）</font></b>");
		} else {
			if(!$Htime_mode) {
				my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
				out("<B><font size=+1>次回更新日時 $mon2月$mday2日$hour2時$min2分　　残り $hour時間 $min分 $sec秒</font></b>");
			} else {
				out("<B><font size=+1>（次のターンまで、あと $hour時間 $min分 $sec秒）</font></b>");
			}
		}
	}

	# 開発モードをCookieより読み込み
    if($CjavaMode eq java) {
		$javacheck = 'checked';
    } else {
		$cgicheck = 'checked';
	}

	# フォーム
	out(<<END);
<SCRIPT language="JavaScript">
<!--
function develope(){
	//window.open("", "newWinTyotouA","menubar=no,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=800,height=640");
	document.Island.target = "newWinTyotouA";
	document.Island.submit();
	document.Island.target = "";
	return true;
}

//-->
</SCRIPT>
<HR>

<TABLE>
<TR>
<TD>
<H1>${HtagHeader_}自分の島へ${H_tagHeader}</H1>
<FORM name="Island" action="$HthisFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

パスワードをどうぞ！！<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="開発しに行く">
<INPUT TYPE="BUTTON" VALUE="新しい画面で開発" onClick="develope()"><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $cgicheck>通常モード
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $javacheck>Javaスクリプトモード
<INPUT TYPE="HIDDEN" NAME="OwnerButton">
</FORM>
</TD>
<TD WIDTH=50> </TD>
<TD>
<FONT size=+2><B>
<A HREF="$HthisFile?LogFileView=1" target=_blank STYlE="text-decoration:none">${HtagHeader_}最近の出来事${H_tagHeader}</A>
<BR><BR><BR>
<A HREF="$HthisFile?FightLog=0" target=_blank STYlE="text-decoration:none">${HtagHeader_}対戦の記録${H_tagHeader}</A>
</TD>
</TR></TABLE>
<HR>

<H1>${HtagHeader_}諸島の状況${H_tagHeader}</H1>
<P>
島の名前をクリックすると、<B>観光</B>することができます。<BR>
順位をクリックすると<B>簡易観光者通信</B>を表示します。 
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}対戦相手${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}採掘場規模${H_tagTH}</NOBR></TH>
</TR>
END

	my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
	for($ii = 0; $ii < $HislandNumber; $ii++) {
		# レッドライン用
		if($ii == $HfightMem){
			$HbgInfoCell	= $YbgInfoCell;
			$HbgCommentCell	= $YbgCommentCell;
			$HbgNameCell	= $YbgNameCell;
			$HbgNumberCell	= $YbgNumberCell;
			out ("<TR><TH colspan=".($cmt_+2)."><FONT SIZE=+1 COLOR=#C00000><i>−　予選通過ライン　−</I></FONT></TH></TR>");
		}
		$j = $ii + 1;
		$island = $Hislands[$ii];

		$id = $island->{'id'};
		$farm = $island->{'farm'};
		$factory = $island->{'factory'};
		$mountain = $island->{'mountain'};
		$farm	  = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
		$factory  = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
		$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
		$farm 	  = "機密" if($Hhide_farm == 2);
		$factory  = "機密" if($Hhide_factory == 2);

		if($island->{'absent'}  == 0) {
			$name = "${HtagName_}$island->{'name'}島${H_tagName}";
		} else {
			$name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
		}

		my($flags);
		$flags = $island->{'prize'};
		$prize = '';

		# 名前に賞の文字を追加
		my($f) = 1;
		my($i);
		for($i = 1; $i < 10; $i++) {
			if($flags & $f) {
				$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
			}
			$f *= 2;
		}

		my($mStr1) = '';
		if($HhideMoneyMode == 1) {
			$mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
		} elsif($HhideMoneyMode == 2) {
			my($mTmp) = aboutMoney($island->{'money'});
			$mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
		}

		my($comname) ="${HtagTH_}コメント：${H_tagTH}";
		if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
			$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
		}
		my $fight_name = '<CENTER>−−−</CENTER>';

		if($island->{'pop'} == 0) {
			$fight_name = "敗退";
		} elsif($island->{'fight_id'} > 0) {
			my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
			if($HcurrentNumber ne '') {
				my $tIsland = $Hislands[$HcurrentNumber];
				$fight_name = $tIsland->{'name'}."島";
			}
		} elsif($HislandNumber == 1 and $HislandTurn > 0) {
			$fight_name = "<CENTER>優勝！</CENTER>";
		} elsif($island->{'fight_id'} == -1) {
			$fight_name = "<CENTER>不戦勝</CENTER>";
		}
		$pop = ($Hhide_town) ? aboutPop($island->{'pop'}) : $island->{'pop'}.$HunitPop;

		out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?BBS=${id}"${blank}>${HtagNumber_}$j${H_tagNumber}</A></NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}"${blank}>
$name
</A>
</NOBR><BR>
$prize
</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$fight_name</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$pop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mountain</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=$cmt_ align=left nowrap=nowrap><NOBR>$comname$island->{'comment'}</NOBR></TD>
</TR>
END
	}

	out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}新しい島を探す${H_tagHeader}</H1>
END
	if($HislandTurn > 0) {
        out("途中参加は出来ません。次回登録開始まで、今しばらくお待ち下さいませ。<BR>\n");
	} elsif($HislandNumber < $HmaxIsland) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
どんな名前をつける予定？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="探しに行く" NAME="NewIslandButton"><BR><BR>
<font color=red>※他の方と同一のIPアドレスになってしまう恐れのある方は、事前にメールでお知らせ下さい。
（家族・会社等）<BR>
　重複登録と間違えられる可能性が有ります。<br>
途中参加は出来ません。登録希望の方はお早めにどうぞ。
</font>
</FORM>
END
	} else {
		out("島の数が最大数です・・・現在登録できません。\n");
	}

	my($Himfflag);
	if($HimgLine eq '' || $HimgLine eq $imageDir){
		$Himfflag = '<FONT COLOR=RED>未設定</FONT>';
	} else {
		$Himfflag = $baseIMG;
	}

	out(<<END);
<HR><P>
<TABLE>
<TR><TD WIDTH=420 ROWSPAN=2 VALIGN=TOP>
<H1>${HtagHeader_}島の名前とパスワードの変更${H_tagHeader}</H1>
<P>
(注意)名前の変更には$HcostChangeName${HunitMoney}かかります。
</P>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
どんな名前に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
</FORM>

</TD>

<TD VALIGN=TOP WIDTH=350>
<H1>${HtagHeader_}画像のローカル設定${H_tagHeader}</H1>
<NOBR>現在の設定<B>[</b> ${Himfflag} <B>]</B></NOBR>
<BR><A HREF=${imageExp} target=_blank><FONT SIZE=+1> 説 明 </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Macユーザー用<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET><BR>
<FONT SIZE=-1>Macの方は、こちらを使用して下さい。</FONT>
</form>
</TD></TR>

<TR HEIGHT=100><TD ALIGN=CENTER>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="設定を解除する" name=IMGSET>
</form>
</TD></TR>
</TABLE>
<HR>
<H1>${HtagHeader_}オーナーの名前決定！${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
あなたの島は？
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>　　名前入力
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=16 MAXLENGTH=32>
　　パスワード
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="これにする" NAME="ChangeOwnerName">
</form>
<HR>
<H1>${HtagHeader_}発見の記録${H_tagHeader}</H1>
END
	historyPrint();
}

# 記録ファイル表示
sub historyPrint {
	open(HIN, "${HdirName}/hakojima.his");
	my(@line, $l);
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
	}
	@line = reverse(@line);

	foreach $l (@line) {
		$l =~ /^([0-9]*),(.*)$/;
		out("<NOBR>${HtagNumber_}ターン${1}${H_tagNumber}：${2}</NOBR><BR>\n");
	}
	close(HIN);
}

#----------------------------------------------------------------------
# ログ表示モード
#----------------------------------------------------------------------
# メイン
sub logViewMain {

	# 開放
	unlock();

	# テンプレート出力
	tempLogPage();
}

sub tempLogPage {

	out(<<END);

<font size=+3><b>${HtagHeader_}最近の出来事${H_tagHeader}</b></font>　
　<FONT COLOR="blue" size=2><B><a href="$HthisFile?LogFileView=1">現ターン</a>
　<a href="$HthisFile?LogFileView=2">2ターン分表示</a>
END
	for($i = 3; $i -1 < $HlogMax; $i++) {
		out("　<a href=\"$HthisFile?LogFileView=${i}\">${i}ターン分</a>\n");
	}
	out(<<END);
</b></font><br>
END
	logPrintTop();

}

# ログ表示
sub logPrintTop {
	my($i);
	for($i = 0; $i < $Hlogturn; $i++) {
		out("<hr>\n");
		logFilePrint($i, 0, 0);

	}
}



1;
