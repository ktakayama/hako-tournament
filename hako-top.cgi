#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# �ȥåץ⥸�塼��
# $Id: hako-top.cgi,v 1.2 2004/02/18 04:42:31 gaba Exp $

#----------------------------------------------------------------------
# �ȥåץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub topPageMain {
	# ����
	unlock();

	# �ƥ�ץ졼�Ƚ���
	tempTopPage();
}

# �ȥåץڡ���
sub tempTopPage {

    # �����ȥ�
    out("${HtagTitle_}$Htitle${H_tagTitle}\n");

	# �������ɽ��
	if($HislandTurn < $HyosenTurn) {
		out("${HtagFico_}��ͽ����${H_tagFico}\n");
	} elsif(($HislandNumber == 2) && ($HislandTurn != 0)) {
		out("${HtagFico_}��辡���${H_tagFico}\n");
	} elsif($HislandNumber == 1 and $HislandTurn != 0) {
		out("${HtagFico_}�㽪λ��${H_tagFico}\n");
	} else {
		out("${HtagFico_}����$HislandFightCount�����${H_tagFico}\n");
	}

	# ���������̤򳫤��⡼�ɤʤ�
	my $blank = ($Htop_blank) ? " TARGET=\"_blank\"" : "";

	# �ǥХå��⡼�ɤʤ�֥������ʤ��ץܥ���
	if($Hdebug == 1) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�������ʤ��" NAME="TurnButton">
</FORM>
END
	}

	my $cmt_ = 7;
	my($mStr1) = '';
	if($HhideMoneyMode != 0) {
		$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
		$cmt_++;
	}

	my $fightmode = "";
	if($HislandFightMode == 1) {
		$fightmode = '<font color=red>��Ʈ����</font>';
		if($HislandChangeTurn == $HislandTurn){
			$fightmode .= '[��������<font color=red>�����Բ�</font>]';
		} else {
			$fightmode .= '[������' . ($HislandChangeTurn + 1) . '�Ϲ����Բ�]';
		}
	} elsif($HislandTurn < $HyosenTurn) {
		$fightmode = '<font color=blue>��ȯ����</font>[������' . ($HyosenTurn) . '�ޤ�ͽ��]';
	} else {
		$fightmode = '<font color=blue>��ȯ����</font>';
		if($HislandChangeTurn == $HislandTurn){
			$fightmode .= '[����������<font color=red>��Ʈ����</font>]';
		} else {
			$fightmode .= '[������' . ($HislandChangeTurn + 1) . '�����Ʈ����]';
		}
	}
	out("<H1>${HtagHeader_}������$HislandTurn${H_tagHeader}��$fightmode</H1>");

	if($HislandNumber > 1 or $HislandTurn == 0) {
		#������ɽ��
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		if ($sec < 0 or $HislandTurnCount > 1){
			out("<B><font size=+1>��${HtagHeader_}�������Ʋ�����${H_tagHeader}��</font></b>");
		} else {
			if(!$Htime_mode) {
				my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
				out("<B><font size=+1>���󹹿����� $mon2��$mday2��$hour2��$min2ʬ�����Ĥ� $hour���� $minʬ $sec��</font></b>");
			} else {
				out("<B><font size=+1>�ʼ��Υ�����ޤǡ����� $hour���� $minʬ $sec�á�</font></b>");
			}
		}
	}

	# ��ȯ�⡼�ɤ�Cookie����ɤ߹���
    if($CjavaMode eq java) {
		$javacheck = 'checked';
    } else {
		$cgicheck = 'checked';
	}

	# �ե�����
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
<H1>${HtagHeader_}��ʬ�����${H_tagHeader}</H1>
<FORM name="Island" action="$HthisFile" method="POST">
���ʤ������̾���ϡ�<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="��ȯ���˹Ԥ�">
<INPUT TYPE="BUTTON" VALUE="���������̤ǳ�ȯ" onClick="develope()"><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $cgicheck>�̾�⡼��
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $javacheck>Java������ץȥ⡼��
<INPUT TYPE="HIDDEN" NAME="OwnerButton">
</FORM>
</TD>
<TD WIDTH=50> </TD>
<TD>
<FONT size=+2><B>
<A HREF="$HthisFile?LogFileView=1" target=_blank STYlE="text-decoration:none">${HtagHeader_}�Ƕ�ν����${H_tagHeader}</A>
<BR><BR><BR>
<A HREF="$HthisFile?FightLog=0" target=_blank STYlE="text-decoration:none">${HtagHeader_}����ε�Ͽ${H_tagHeader}</A>
</TD>
</TR></TABLE>
<HR>

<H1>${HtagHeader_}����ξ���${H_tagHeader}</H1>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���<BR>
��̤򥯥�å������<B>�ʰ״Ѹ����̿�</B>��ɽ�����ޤ��� 
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�η��쵬��${H_tagTH}</NOBR></TH>
</TR>
END

	my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
	for($ii = 0; $ii < $HislandNumber; $ii++) {
		# ��åɥ饤����
		if($ii == $HfightMem){
			$HbgInfoCell	= $YbgInfoCell;
			$HbgCommentCell	= $YbgCommentCell;
			$HbgNameCell	= $YbgNameCell;
			$HbgNumberCell	= $YbgNumberCell;
			out ("<TR><TH colspan=".($cmt_+2)."><FONT SIZE=+1 COLOR=#C00000><i>�ݡ�ͽ���̲�饤�󡡡�</I></FONT></TH></TR>");
		}
		$j = $ii + 1;
		$island = $Hislands[$ii];

		$id = $island->{'id'};
		$farm = $island->{'farm'};
		$factory = $island->{'factory'};
		$mountain = $island->{'mountain'};
		$farm	  = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
		$factory  = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
		$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
		$farm 	  = "��̩" if($Hhide_farm == 2);
		$factory  = "��̩" if($Hhide_factory == 2);

		if($island->{'absent'}  == 0) {
			$name = "${HtagName_}$island->{'name'}��${H_tagName}";
		} else {
			$name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
		}

		my($flags);
		$flags = $island->{'prize'};
		$prize = '';

		# ̾���˾ޤ�ʸ�����ɲ�
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

		my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
		if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
			$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
		}
		my $fight_name = '<CENTER>�ݡݡ�</CENTER>';

		if($island->{'pop'} == 0) {
			$fight_name = "����";
		} elsif($island->{'fight_id'} > 0) {
			my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
			if($HcurrentNumber ne '') {
				my $tIsland = $Hislands[$HcurrentNumber];
				$fight_name = $tIsland->{'name'}."��";
			}
		} elsif($HislandNumber == 1 and $HislandTurn > 0) {
			$fight_name = "<CENTER>ͥ����</CENTER>";
		} elsif($island->{'fight_id'} == -1) {
			$fight_name = "<CENTER>���ﾡ</CENTER>";
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
<H1>${HtagHeader_}���������õ��${H_tagHeader}</H1>
END
	if($HislandTurn > 0) {
        out("���滲�äϽ���ޤ��󡣼�����Ͽ���Ϥޤǡ������Ф餯���Ԥ��������ޤ���<BR>\n");
	} elsif($HislandNumber < $HmaxIsland) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
�ɤ��̾����Ĥ���ͽ�ꡩ<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="õ���˹Ԥ�" NAME="NewIslandButton"><BR><BR>
<font color=red>��¾������Ʊ���IP���ɥ쥹�ˤʤäƤ��ޤ�����Τ������ϡ������˥᡼��Ǥ��Τ餻��������
�ʲ�²���������<BR>
����ʣ��Ͽ�ȴְ㤨�����ǽ����ͭ��ޤ���<br>
���滲�äϽ���ޤ�����Ͽ��˾�����Ϥ����ˤɤ�����
</font>
</FORM>
END
	} else {
		out("��ο���������Ǥ�������������Ͽ�Ǥ��ޤ���\n");
	}

	my($Himfflag);
	if($HimgLine eq '' || $HimgLine eq $imageDir){
		$Himfflag = '<FONT COLOR=RED>̤����</FONT>';
	} else {
		$Himfflag = $baseIMG;
	}

	out(<<END);
<HR><P>
<TABLE>
<TR><TD WIDTH=420 ROWSPAN=2 VALIGN=TOP>
<H1>${HtagHeader_}���̾���ȥѥ���ɤ��ѹ�${H_tagHeader}</H1>
<P>
(���)̾�����ѹ��ˤ�$HcostChangeName${HunitMoney}������ޤ���
</P>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM>

</TD>

<TD VALIGN=TOP WIDTH=350>
<H1>${HtagHeader_}�����Υ���������${H_tagHeader}</H1>
<NOBR>���ߤ�����<B>[</b> ${Himfflag} <B>]</B></NOBR>
<BR><A HREF=${imageExp} target=_blank><FONT SIZE=+1> �� �� </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="����" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Mac�桼������<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="����" name=IMGSET><BR>
<FONT SIZE=-1>Mac�����ϡ����������Ѥ��Ʋ�������</FONT>
</form>
</TD></TR>

<TR HEIGHT=100><TD ALIGN=CENTER>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="�����������" name=IMGSET>
</form>
</TD></TR>
</TABLE>
<HR>
<H1>${HtagHeader_}�����ʡ���̾�����ꡪ${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
���ʤ�����ϡ�
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>����̾������
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=16 MAXLENGTH=32>
�����ѥ����
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="����ˤ���" NAME="ChangeOwnerName">
</form>
<HR>
<H1>${HtagHeader_}ȯ���ε�Ͽ${H_tagHeader}</H1>
END
	historyPrint();
}

# ��Ͽ�ե�����ɽ��
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
		out("<NOBR>${HtagNumber_}������${1}${H_tagNumber}��${2}</NOBR><BR>\n");
	}
	close(HIN);
}

#----------------------------------------------------------------------
# ��ɽ���⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub logViewMain {

	# ����
	unlock();

	# �ƥ�ץ졼�Ƚ���
	tempLogPage();
}

sub tempLogPage {

	out(<<END);

<font size=+3><b>${HtagHeader_}�Ƕ�ν����${H_tagHeader}</b></font>��
��<FONT COLOR="blue" size=2><B><a href="$HthisFile?LogFileView=1">��������</a>
��<a href="$HthisFile?LogFileView=2">2������ʬɽ��</a>
END
	for($i = 3; $i -1 < $HlogMax; $i++) {
		out("��<a href=\"$HthisFile?LogFileView=${i}\">${i}������ʬ</a>\n");
	}
	out(<<END);
</b></font><br>
END
	logPrintTop();

}

# ��ɽ��
sub logPrintTop {
	my($i);
	for($i = 0; $i < $Hlogturn; $i++) {
		out("<hr>\n");
		logFilePrint($i, 0, 0);

	}
}



1;
