#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# JS開発画面モジュール
# $Id: hako-js.cgi,v 1.3 2004/04/27 02:41:23 gaba Exp $

#----------------------------------------------------------------------
# Ｊａｖａスクリプト開発画面
#----------------------------------------------------------------------
# ○○島開発計画
sub tempOwnerJava {

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	# コマンドセット
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# 各要素の取り出し
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg) = 
			(
			$command->{'kind'},
			$command->{'target'},
			$command->{'x'},
			$command->{'y'},
			$command->{'arg'}
			);
		# コマンド登録
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\n";
			$com_max .= "0"
		} else {
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\,\n";
			$com_max .= "0,"
		}
	}

	#コマンドリストセット
	my($l_kind);
	$set_listcom = "";
	for($i = 0; $i < $HcommandTotal; $i++) {
		$l_kind = $HcomList[$i];
		if($l_kind < 46 and $l_kind != $HcomPrepRecr) {
			$set_listcom .= "\[$l_kind\,\'$HcomName[$l_kind]\'\]\,\n";
		}
		if($l_kind == $HcomGiveup) {
			$set_listcom .= "\[46\,\'島の放棄\'\]\n";
		}
	}

	my($set_island, $l_name, $l_id);
	#島リストセット
	$set_island = "";
	for($i = 0; $i < $HislandNumber; $i++) {
		$l_name = $Hislands[$i]->{'name'};
		$l_name =~ s/'/\\'/g;
		$l_id = $Hislands[$i]->{'id'};
		if($i == $HislandNumber-1){
			$set_island .= "\[$l_id\,\'$l_name\'\]\n";
		} else {
			$set_island .= "\[$l_id\,\'$l_name\'\]\,\n";
		}
	}

	$nextTurn = $HunitTime - time() + $HislandLastTime;
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
// ＪＡＶＡスクリプト開発画面配布元
// あっぽー庵箱庭諸島（ http://appoh.execweb.cx/hakoniwa/ ）
// Programmed by Jynichi Sakai(あっぽー)
isIE4 = (navigator.appVersion.charAt(0)>=4 && (navigator.appVersion).indexOf("MSIE") != -1);
isNN4 = (navigator.appVersion.charAt(0)>=4 && (navigator.appName).indexOf("Netscape")!=-1);
isNN6 = (document.getElementById);

var str;

g = [$com_max];
k1 = [$com_max];
k2 = [$com_max];
tmpcom1 = [ [0,0,0,0,0] ];
tmpcom2 = [ [0,0,0,0,0] ];
command = [
$set_com];

comlist = [
$set_listcom];

islname = [
$set_island];

function init(){
	for(i = 0; i < command.length ;i++) {
		for(j = 0; j < comlist.length ; j++) {
			if(command[i][0] == comlist[j][0]) {
				g[i] = comlist[j][1];
			}
		}
	}
	outp();
	str = plchg();
	str = "<NOBR><font color=blue>−−−− <B>送信済み</B> −−−−</font></NOBR><br>"+str;
	disp(str, "#ccffcc");

	/*
	if(isIE4){
		window.document.onmouseup = menuclose;
	} else {
		document.captureEvents(Event.MOUSEDOWN)
		document.onmousedown = getMouseData;
		if(!(isNN6)) {
			window.document.onmouseup = menuclose;
		}
	}
	*/
}

function cominput(x, k, z) {
	a = document.myForm.NUMBER.options[document.myForm.NUMBER.selectedIndex].value;
	b = document.myForm.COMMAND.options[document.myForm.COMMAND.selectedIndex].value;
	c = document.myForm.POINTX.options[document.myForm.POINTX.selectedIndex].value;
	d = document.myForm.POINTY.options[document.myForm.POINTY.selectedIndex].value;
	e = document.myForm.AMOUNT.options[document.myForm.AMOUNT.selectedIndex].value;
	f = document.myForm.TARGETID.options[document.myForm.TARGETID.selectedIndex].value;
	if(x == 6){ b = k; }
	if(z) { f = z; }
	if (x == 1 || x == 6)		{
		for(i = $HcommandMax - 1; i > a; i--) {
			command[i] = command[i-1];
				g[i] = g[i-1];
		}
	} else if(x == 3) {
		for(i = Math.floor(a); i < ($HcommandMax - 1); i++) {
			command[i] = command[i + 1];
			g[i] = g[i+1];
		}
		command[$HcommandMax-1] = [41,0,0,0,0];
		g[$HcommandMax-1] = '資金繰り';
		str = plchg();
		str = "<NOBR><font color=red><b>−−−−−未送信−−−−−</b></font></NOBR><br>"+str;
		disp(str,"white");
		outp();
		return true;
	} else if(x == 4) {
		i = Math.floor(a)
		if (i == 0){ return true; }
		i = Math.floor(a)
		tmpcom1[i] = command[i];tmpcom2[i] = command[i - 1];
		command[i] = tmpcom2[i];command[i-1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i - 1];
		g[i] = k2[i];g[i-1] = k1[i];
		ns(--i);
		str = plchg();
		str = "<NOBR><font color=red><b>−−−−−未送信−−−−−</b></font></NOBR><br>"+str;
		disp(str,"white");
		outp();
		return true;
	} else if(x == 5) {
		i = Math.floor(a)
		if (i == $HcommandMax-1){ return true; }
		tmpcom1[i] = command[i];tmpcom2[i] = command[i + 1];
		command[i] = tmpcom2[i];command[i+1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i + 1];
		g[i] = k2[i];g[i+1] = k1[i];
		ns(++i);
		str = plchg();
		str = "<NOBR><font color=red><b>−−−−−未送信−−−−−</b></font></NOBR><br>"+str;
		disp(str,"white");
		outp();
		return true;
	}

	for(i = 0;i < comlist.length; i++){
		if(comlist[i][0] == b){
			g[a] = comlist[i][1];
			break;
		}
	}

	command[a] = [b,c,d,e,f];
	ns(++a);
	str = plchg();
	str = "<NOBR><font color=red><b>−−−−−未送信−−−−−</b></font></NOBR><br>"+str;
	disp(str, "white");
	outp();
	menuclose();
	return true;
}

function plchg(){
	strn1 = "";
	for(i = 0; i < $HcommandMax; i++) {
		c = command[i];
		kind = '<FONT COLOR="#d08000"><B>' + g[i] + '</B></FONT>';
		x = c[1];
		y = c[2];
		tgt = c[4];
		point = '<FONT COLOR="#a06040"><B>' + "(" + x + "," + y + ")" + '</B></FONT>';
		for(j = 0; j < islname.length ; j++) {
			if(tgt == islname[j][0]){
				tgt = '<FONT COLOR="#a06040"><B>' + islname[j][1] + "島" + '</B></FONT>';
			}
		}
		if(c[0] == $HcomDoNothing || c[0] == $HcomAutoPrepare3){ // 資金繰り 一括自動地ならし
			strn2 = kind;
		} else if(c[0] == $HcomMissileNM || // ミサイル関連
			c[0] == $HcomMissilePP){
			if(c[3] == 0){
				arg = "（無制限）";
			} else {
				arg = "（" + c[3] + "発）";
			}
			strn2 = tgt + point + "へ" + kind + arg;
		} else if(c[0] == $HcomSell){ // 食料輸出
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = "（" + arg + "$HunitFood）";
			strn2 = kind + arg;
		} else if(c[0] == $HcomDestroy){ // 掘削
			strn2 = point + "で" + kind;
		} else if(c[0] == $HcomFarm || c[0] == $HcomMountain || // 農場、工場、採掘場整備
			c[0] == $HcomFactory || c[0] == $HcomFastFarm) {
			if(c[3] != 0) {
				arg = "（" + c[3] + "回）";
				strn2 = point + "で" + kind + arg;
			} else {
				strn2 = point + "で" + kind;
			}
		} else {
			strn2 = point + "で" + kind;
		}
		tmpnum = '';
		if(i < 9){ tmpnum = '0'; }
			strn1 += 
			'<A STYLE="text-decoration:none;color:000000" HREF="JavaScript:void(0);" onClick="ns(' + i + ')"><NOBR>' +
			tmpnum + (i + 1) + ':' +
			strn2 + '</NOBR></A><BR>\\n';
		}
	return strn1;
}

function disp(str,bgclr){
	if(str==null)  str = "";

	if(isNN6) {
		el = document.getElementById("LINKMSG1");
		el.innerHTML = str;
		document.getElementById("plan").bgColor = bgclr;
	} else if(isIE4) {
		el = document.all("LINKMSG1");
		el.innerHTML = str;
		document.all.plan.bgColor = bgclr;
	} else if(isNN4) {
		lay = document.layers["PARENT_LINKMSG"].document.layers["LINKMSG1"];
		lay.document.open();
		lay.document.write("<font style='font-size:11pt'>"+str+"</font>");
		lay.document.close(); 
		document.layers["PARENT_LINKMSG"].bgColor = bgclr;
	}
}

function outp(){
	comary = "";

	for(k = 0; k < command.length; k++){
		comary = comary + command[k][0]
		+" "+command[k][1]
		+" "+command[k][2]
		+" "+command[k][3]
		+" "+command[k][4]
		+" ";
	}
	document.myForm.COMARY.value = comary;
}

function ps(x, y) {
	document.forms[0].elements[4].options[x].selected = true;
	document.forms[0].elements[5].options[y].selected = true;
	showMenu();
	return true;
}

function ns(x) {
	if (x == $HcommandMax){ return true; }
	document.forms[0].elements[2].options[x].selected = true;
	return true;
}

function set_com(x, y, land) {
	com_str = land + "\\n";
	for(i = 0; i < $HcommandMax; i++) {
		c = command[i];
		x2 = c[1];
		y2 = c[2];
		if(x == x2 && y == y2 && c[0] < 30) {
			com_str += "[" + (i + 1) +"]" ;
			kind = g[i];
			if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory) {
				if(c[3] != 0) {
					arg = "（" + c[3] + "回）";
					com_str += kind + arg;
				} else {
					com_str += kind;
				}
			} else {
				com_str += kind;
			}
			com_str += " ";
		}
	}
	window.status = com_str;
	document.myForm.COMSTATUS.value= com_str;
}

function jump(theForm) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = theForm.TARGETID.options[sIndex].value;
	if (url != "" ) window.open("$HthisFile?IslandMap=" +url,"", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=450,height=630");
}

function showMenu() {
	if((isNN6) && !(isIE4)){
		document.getElementById("menu").style.left = mouseX;
		document.getElementById("menu").style.top = mouseY - 50;
		document.getElementById("menu").style.display = "block";
		document.getElementById("menu").style.visibility = "visible";
	} else if(isNN4) {
		var def = 0;
		var y_ = window.pageYOffset;
		var left_def = (mouseY - y_) - (innerHeight - 169);
		if((mouseY - y_) < 28) { def = 28 - (mouseY - y_); }
		if(left_def > 0) { def = - left_def; }
		document.menu.left = mouseX; // 横
		document.menu.top  = mouseY - 30 + def; // 縦
		document.menu.visibility = "show";
	} else if(isIE4) {
		var def = 0;
		var left_def = event.clientY - (document.body.clientHeight - 138);
		if(event.clientY < 80) { def = 80 - event.clientY; }
		if(left_def > 0) { def = - left_def; }
		menu.style.left= event.clientX + document.body.scrollLeft;
		menu.style.top = event.clientY + document.body.scrollTop - 80 + def;
		menu.style.display = "block";
		menu.style.visibility = "visible";
	}
}

function menuclose() {
	if(isNN6) {
		document.getElementById("menu").style.display = "none";
	} else if(isNN4) {
		document.menu.visibility = "hide";
	} else {
		window["menu"].style.display = "none";
	}
}

function getMouseData(e) {
	mouseX = e.pageX;
	mouseY = e.pageY;
}

//-->
</SCRIPT>
<DIV ID="menu" STYLE="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR=#ccffcc>
<TR><TD NOWRAP>

END
	local($kind, $cost, $s, $tak);
	$tak = $HcommandTotal - 3;
	for($i = 0; $i < $tak; $i++) {
		$kind = $HcomList[$i];
		if($kind > 30 || $kind == 6){ next; }
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '無料'
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		if($i == 7){ out("<HR SIZE=1>"); }
		out("<a href=\"javascript:void(0);\" onClick=\"cominput(6,${kind})\" STYlE=\"text-decoration:none\">$HcomName[$kind]($cost)<BR></A>\n");
	}

	out(<<END);
<HR SIZE=1>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
END
	islandInfo();

	out(<<END);
<CENTER>
<TABLE BORDER>
<TR valign=top>
<TD $HbgInputCell >
<CENTER>
<FORM name="myForm" action="$HthisFile" method=POST>
<BR><nobr><center>ミサイル発射上限数[<b> $island->{'fire'} </b>]発</center></nobr><BR>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>動 作<BR>
<A HREF=JavaScript:void(0); onClick="cominput(1)">挿入</A>　
<A HREF=JavaScript:void(0); onClick="cominput(2)">上書き</A>　
<A HREF=JavaScript:void(0); onClick="cominput(3)">削除</A></B>
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
	my($kind, $cost);
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
		if(($kind < 60 && $kind != $HcomPrepRecr) || ($kind == $HcomAutoPrepare3)){
			$set_cost = "($cost)";
			out("<OPTION VALUE=$kind>$HcomName[$kind]$set_cost\n");
		}
	}

	out(<<END);
</SELECT>
<HR>
<B>座標(</B>
<SELECT NAME=POINTX>

END
	for($i = 0; $i < $HislandSize; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

	for($i = 0; $i < $HislandSize; $i++) {
		out("<OPTION VALUE=$i>$i\n");
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
<B>目標の島</B>：
<B><BIG><A HREF=JavaScript:void(0); onClick="jump(myForm)" STYlE="text-decoration:none"> 表\示 </A></BIG></B><BR>
<SELECT NAME=TARGETID>
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>コマンド移動</B><br>
<BIG><A HREF=JavaScript:void(0); onClick="cominput(4)" STYlE="text-decoration:none"> ▲ </A> ・・
<A HREF=JavaScript:void(0); onClick="cominput(5)" STYlE="text-decoration:none"> ▼ </A></BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<p><font size=2>最後に<font color=red>計画送信ボタン</font>を<br>押すのを忘れないように。</font>
</CENTER><BR>
</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2">
最後に計画送信するのを忘れないで下さい。
挿入・上書き・削除で計画の入力が出来ます。
</TEXTAREA></center>
END
	islandMapJava(1);	# 島の地図、所有者モード
	my $comment = $Hislands[$HcurrentNumber]->{'comment'};
	out(<<END);
</FORM>
</TD>
<TD $HbgCommandCell id="plan">
<ilayer name="PARENT_LINKMSG" width="100%" height="100%">
   <layer name="LINKMSG1" width="200"></layer>
   <span id="LINKMSG1"></span>
</ilayer>
<BR>
</TD>
</TR>
</TABLE>
</CENTER>
<HR>
<CENTER>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
sub commandJavaMain {
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
	for($i = 0; $i < $HcommandMax; $i++) {
		# コマンド登録
		$HcommandComary =~ s/([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) //;
		if($1 == 0) {
			$1 = 41;
		}
		$command->[$i] = {
			'kind' => $1,
			'x' => $2,
			'y' => $3,
			'arg' => $4,
			'target' => $5
		};
	}
	tempCommandAdd();
	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# 地図の表示
#----------------------------------------------------------------------
sub islandMapJava {
	my($mode) = @_;
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
			if($com->{'kind'} < 21) {
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
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], 1);
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

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
sub printIslandJava {
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

out(<<END);
<SCRIPT Language="JavaScript">
<!--

isIE4 = (navigator.appVersion.charAt(0)>=4 && (navigator.appVersion).indexOf("MSIE") != -1);
isNN4 = (navigator.appVersion.charAt(0)>=4 && (navigator.appName).indexOf("Netscape")!=-1);
isNN6 = (document.getElementById);

	if(isIE4){
		window.document.onmouseup = menuclose;
	} else {
		document.captureEvents(Event.MOUSEDOWN)
		document.onmousedown = getMouseData;
		if(!(isNN6)) {
			window.document.onmouseup = menuclose;
		}
	}

function ps(x, y) {
	window.opener.document.myForm.POINTX.options[x].selected = true;
	window.opener.document.myForm.POINTY.options[y].selected = true;
	showMenu();
	return true;
}

function showMenu() {
	if((isNN6) && !(isIE4)){
		document.getElementById("menu").style.left = mouseX;
		document.getElementById("menu").style.top = mouseY - 20;
		document.getElementById("menu").style.visibility = "visible";
		document.getElementById("menu").style.display = "block";
	} else if(isNN4) {
		document.menu.left = mouseX; // 横
		document.menu.top  = mouseY - 15; // 縦
		document.menu.visibility = "show";
	} else if(isIE4) {
		menu.style.visibility = 'visible';
		menu.style.display = 'block';
		menu.style.left= event.clientX + document.body.scrollLeft;
		menu.style.top = event.clientY + document.body.scrollTop - 20;
	}
}

function menuclose() {
	if(isNN6) {
		document.getElementById("menu").style.display = "none";
	} else if(isNN4) {
		document.menu.visibility = "hide";
	} else {
		window["menu"].style.display = "none";
	}
}

function getMouseData(e) {
	mouseX = e.pageX;
	mouseY = e.pageY;
}
function cominput(kind) {
	window.opener.cominput(6, kind, $HcurrentID);
	menuclose();
}

function ShowMsg(n){
	window.status = n;
}
//-->
</SCRIPT>

<DIV ID="menu" STYLE="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR=#ccffcc>
<TR><TD NOWRAP>

END
	local($kind, $cost, $s, $tak);
	$tak = $HcommandTotal - 3;
	for($i = 0; $i < $tak; $i++) {
		$kind = $HcomList[$i];
		if(!($kind >= 30 and $kind <= 35)){ next; }
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '無料'
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		if($i == 7){ out("<HR>"); }
		out("<a href=\"javascript:void(0);\" onClick=\"cominput(${kind})\" STYlE=\"text-decoration:none\">$HcomName[$kind]($cost)<BR></A>\n");
	}

	out(<<END);
<HR>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
<center>${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}${H_tagBig}
</center>
END
	islandMapJava(0);  # 島の地図、観光モード
	landStringFlash(); # 擬似ＭＡＰデータ表示

	# 近況
	tempRecent(0);

}

#----------------------------------------------------------------------
# 擬似ＭＡＰデータ生成
#----------------------------------------------------------------------
sub landStringFlash {
	my($island);
	$island = $Hislands[$HcurrentNumber];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);
	my($code) = "";
	my($befor) = "a";
	my($Count) = 0;
	my($Comp) = "";
	my($ret) = "";

	# 各地形を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$code = landFlashData($l, $lv);

				if ($code eq $befor) {
					$Count++;
				} else {
					$Comp .= $befor;
					if( $Count != 0){
						$Comp .= ($Count - 1);
					}
					$Count = 0;
					$befor = $code;
				}
		}
 	}

	if($befor ne "a"){
		$Comp .= $befor;
		if( $Count != 0) {
			$Comp .= ($Count - 1);
		}
	}
	$Comp .= "\@";
	$Comp = substr($Comp,1);

	# 各地形を出力
	my($Compjs) = "";
	for($x = 0; $x < $HislandSize; $x++) {
		# 各地形を出力
		for($y = 0; $y < $HislandSize; $y++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$code = landFlashData($l, $lv);
			$Compjs .= $code;
		}
 	}

	out(<<END);
<CENTER><FORM>
擬似ＭＡＰ作成ツール用データ(FLASH版)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="3">$Comp</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/flash/hako-map.html" target="_blank">
擬似ＭＡＰ作成ツール(FLASH版)をオンラインで起動</a><P>
擬似ＭＡＰ作成ツール用データ(Javaスクリプト版)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="4">$Compjs</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/javascript/map.html" target="_blank">
擬似ＭＡＰ作成ツール(Javaスクリプト版)をオンラインで起動</a><BR><BR><BR>
<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">
擬似ＭＡＰ作成ツール(JAVA・FLASH版)をダウンロードする</a><p>
</FORM>
</CENTER>
END

}

sub landFlashData {
	my($l, $lv) = @_;
	my($flash_data);

	if($l == $HlandSea) {
		# 浅瀬
		if($lv == 1) {
			$flash_data = "o";
		} else {
			# 海
			$flash_data = "a";
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		if($lv == 1) {
			# 着弾点
			$flash_data = "n";
		} else {
			$flash_data = "b";
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$flash_data = "c";
	} elsif($l == $HlandForest) {
		# 森
		$flash_data = "g";
	} elsif($l == $HlandMountain) {
		# 山
		$flash_data = "l";
	} elsif($l == $HlandTown) {
		if($lv < 30) {
			# 村
			$flash_data = "d";
		} elsif($lv < 100) {
			# 町
			$flash_data = "e";
		} else {
			# 都市
			$flash_data = "f";
		}
	} elsif($l == $HlandFarm) {
		# 農場
		$flash_data = ($Hhide_farm) ? "g" : "h";;
	} elsif($l == $HlandFactory) {
		# 工場
		$flash_data = ($Hhide_factory) ? "g" : "i";
	} elsif($l == $HlandBase) {
		# ミサイル基地
		$flash_data = ($Hhide_missile) ? "g" : "j";
	} elsif($l == $HlandDefence) {
		# 防衛施設
		#$flash_data = "k";
		# 防衛施設は森になる
		$flash_data = ($Hhide_deffence) ? "g" : "k";
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		$flash_data = "k";
	} else {
		# その他
		$flash_data = "b";
	}
	return $flash_data;
}




1;

