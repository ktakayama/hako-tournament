#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# JS��ȯ���̥⥸�塼��
# $Id: hako-js.cgi,v 1.3 2004/04/27 02:41:23 gaba Exp $

#----------------------------------------------------------------------
# �ʣ���᥹����ץȳ�ȯ����
#----------------------------------------------------------------------
# �����糫ȯ�ײ�
sub tempOwnerJava {

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	# ���ޥ�ɥ��å�
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# �����Ǥμ��Ф�
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg) = 
			(
			$command->{'kind'},
			$command->{'target'},
			$command->{'x'},
			$command->{'y'},
			$command->{'arg'}
			);
		# ���ޥ����Ͽ
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\n";
			$com_max .= "0"
		} else {
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\,\n";
			$com_max .= "0,"
		}
	}

	#���ޥ�ɥꥹ�ȥ��å�
	my($l_kind);
	$set_listcom = "";
	for($i = 0; $i < $HcommandTotal; $i++) {
		$l_kind = $HcomList[$i];
		if($l_kind < 46 and $l_kind != $HcomPrepRecr) {
			$set_listcom .= "\[$l_kind\,\'$HcomName[$l_kind]\'\]\,\n";
		}
		if($l_kind == $HcomGiveup) {
			$set_listcom .= "\[46\,\'�������\'\]\n";
		}
	}

	my($set_island, $l_name, $l_id);
	#��ꥹ�ȥ��å�
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
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
// �ʣ��֣�������ץȳ�ȯ�������۸�
// ���äݡ���Ȣ������ http://appoh.execweb.cx/hakoniwa/ ��
// Programmed by Jynichi Sakai(���äݡ�)
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
	str = "<NOBR><font color=blue>�ݡݡݡ� <B>�����Ѥ�</B> �ݡݡݡ�</font></NOBR><br>"+str;
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
		g[$HcommandMax-1] = '��ⷫ��';
		str = plchg();
		str = "<NOBR><font color=red><b>�ݡݡݡݡ�̤�����ݡݡݡݡ�</b></font></NOBR><br>"+str;
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
		str = "<NOBR><font color=red><b>�ݡݡݡݡ�̤�����ݡݡݡݡ�</b></font></NOBR><br>"+str;
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
		str = "<NOBR><font color=red><b>�ݡݡݡݡ�̤�����ݡݡݡݡ�</b></font></NOBR><br>"+str;
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
	str = "<NOBR><font color=red><b>�ݡݡݡݡ�̤�����ݡݡݡݡ�</b></font></NOBR><br>"+str;
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
				tgt = '<FONT COLOR="#a06040"><B>' + islname[j][1] + "��" + '</B></FONT>';
			}
		}
		if(c[0] == $HcomDoNothing || c[0] == $HcomAutoPrepare3){ // ��ⷫ�� ��缫ư�Ϥʤ餷
			strn2 = kind;
		} else if(c[0] == $HcomMissileNM || // �ߥ������Ϣ
			c[0] == $HcomMissilePP){
			if(c[3] == 0){
				arg = "��̵���¡�";
			} else {
				arg = "��" + c[3] + "ȯ��";
			}
			strn2 = tgt + point + "��" + kind + arg;
		} else if(c[0] == $HcomSell){ // ����͢��
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = "��" + arg + "$HunitFood��";
			strn2 = kind + arg;
		} else if(c[0] == $HcomDestroy){ // ����
			strn2 = point + "��" + kind;
		} else if(c[0] == $HcomFarm || c[0] == $HcomMountain || // ���졢���졢�η�������
			c[0] == $HcomFactory || c[0] == $HcomFastFarm) {
			if(c[3] != 0) {
				arg = "��" + c[3] + "���";
				strn2 = point + "��" + kind + arg;
			} else {
				strn2 = point + "��" + kind;
			}
		} else {
			strn2 = point + "��" + kind;
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
					arg = "��" + c[3] + "���";
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
		document.menu.left = mouseX; // ��
		document.menu.top  = mouseY - 30 + def; // ��
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
			$cost = '̵��'
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
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
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
<BR><nobr><center>�ߥ�����ȯ�;�¿�[<b> $island->{'fire'} </b>]ȯ</center></nobr><BR>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>ư ��<BR>
<A HREF=JavaScript:void(0); onClick="cominput(1)">����</A>��
<A HREF=JavaScript:void(0); onClick="cominput(2)">���</A>��
<A HREF=JavaScript:void(0); onClick="cominput(3)">���</A></B>
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
	# �ײ��ֹ�
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
<SELECT NAME=COMMAND>
END

	#���ޥ��
	my($kind, $cost);
	for($i = 0; $i < $HcommandTotal; $i++) {
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
		if(($kind < 60 && $kind != $HcomPrepRecr) || ($kind == $HcomAutoPrepare3)){
			$set_cost = "($cost)";
			out("<OPTION VALUE=$kind>$HcomName[$kind]$set_cost\n");
		}
	}

	out(<<END);
</SELECT>
<HR>
<B>��ɸ(</B>
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
<B>����</B><SELECT NAME=AMOUNT>
END

	# ����
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>��ɸ����</B>��
<B><BIG><A HREF=JavaScript:void(0); onClick="jump(myForm)" STYlE="text-decoration:none"> ɽ\�� </A></BIG></B><BR>
<SELECT NAME=TARGETID>
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>���ޥ�ɰ�ư</B><br>
<BIG><A HREF=JavaScript:void(0); onClick="cominput(4)" STYlE="text-decoration:none"> �� </A> ����
<A HREF=JavaScript:void(0); onClick="cominput(5)" STYlE="text-decoration:none"> �� </A></BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<p><font size=2>�Ǹ��<font color=red>�ײ������ܥ���</font>��<br>�����Τ�˺��ʤ��褦�ˡ�</font>
</CENTER><BR>
</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2">
�Ǹ�˷ײ���������Τ�˺��ʤ��ǲ�������
��������񤭡�����Ƿײ�����Ϥ�����ޤ���
</TEXTAREA></center>
END
	islandMapJava(1);	# ����Ͽޡ���ͭ�ԥ⡼��
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
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
������<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
�ѥ����<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
sub commandJavaMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# �⡼�ɤ�ʬ��
	my($command) = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
		# ���ޥ����Ͽ
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
	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# �Ͽޤ�ɽ��
#----------------------------------------------------------------------
sub islandMapJava {
	my($mode) = @_;
	my($island);
	$island = $Hislands[$HcurrentNumber];

	# �Ϸ����Ϸ��ͤ����
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);

	out("<CENTER><TABLE BORDER><TR><TD>");

	# ���ޥ�ɼ���
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

	# ��ɸ(��)�����
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# ���Ϸ�����Ӳ��Ԥ����
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# �������ܤʤ��ֹ�����
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ϸ������
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], 1);
		}

		# ������ܤʤ��ֹ�����
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ԥ����
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
sub printIslandJava {
	# ����
	unlock();

	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# ̾���μ���
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
		document.menu.left = mouseX; // ��
		document.menu.top  = mouseY - 15; // ��
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
			$cost = '̵��'
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
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
</TD></TR>
</TABLE>
</DIV>
<center>${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}${H_tagBig}
</center>
END
	islandMapJava(0);  # ����Ͽޡ��Ѹ��⡼��
	landStringFlash(); # �����ͣ��Хǡ���ɽ��

	# �ᶷ
	tempRecent(0);

}

#----------------------------------------------------------------------
# �����ͣ��Хǡ�������
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

	# ���Ϸ������
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {

		# ���Ϸ������
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

	# ���Ϸ������
	my($Compjs) = "";
	for($x = 0; $x < $HislandSize; $x++) {
		# ���Ϸ������
		for($y = 0; $y < $HislandSize; $y++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$code = landFlashData($l, $lv);
			$Compjs .= $code;
		}
 	}

	out(<<END);
<CENTER><FORM>
�����ͣ��к����ġ����ѥǡ���(FLASH��)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="3">$Comp</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/flash/hako-map.html" target="_blank">
�����ͣ��к����ġ���(FLASH��)�򥪥�饤��ǵ�ư</a><P>
�����ͣ��к����ġ����ѥǡ���(Java������ץ���)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="4">$Compjs</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/javascript/map.html" target="_blank">
�����ͣ��к����ġ���(Java������ץ���)�򥪥�饤��ǵ�ư</a><BR><BR><BR>
<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">
�����ͣ��к����ġ���(JAVA��FLASH��)���������ɤ���</a><p>
</FORM>
</CENTER>
END

}

sub landFlashData {
	my($l, $lv) = @_;
	my($flash_data);

	if($l == $HlandSea) {
		# ����
		if($lv == 1) {
			$flash_data = "o";
		} else {
			# ��
			$flash_data = "a";
		}
	} elsif($l == $HlandWaste) {
		# ����
		if($lv == 1) {
			# ������
			$flash_data = "n";
		} else {
			$flash_data = "b";
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$flash_data = "c";
	} elsif($l == $HlandForest) {
		# ��
		$flash_data = "g";
	} elsif($l == $HlandMountain) {
		# ��
		$flash_data = "l";
	} elsif($l == $HlandTown) {
		if($lv < 30) {
			# ¼
			$flash_data = "d";
		} elsif($lv < 100) {
			# Į
			$flash_data = "e";
		} else {
			# �Ի�
			$flash_data = "f";
		}
	} elsif($l == $HlandFarm) {
		# ����
		$flash_data = ($Hhide_farm) ? "g" : "h";;
	} elsif($l == $HlandFactory) {
		# ����
		$flash_data = ($Hhide_factory) ? "g" : "i";
	} elsif($l == $HlandBase) {
		# �ߥ��������
		$flash_data = ($Hhide_missile) ? "g" : "j";
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		#$flash_data = "k";
		# �ɱһ��ߤϿ��ˤʤ�
		$flash_data = ($Hhide_deffence) ? "g" : "k";
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		$flash_data = "k";
	} else {
		# ����¾
		$flash_data = "b";
	}
	return $flash_data;
}




1;

