#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# �Ͽޥ⡼�ɥ⥸�塼��
# $Id: hako-map.cgi,v 1.8 2004/11/10 13:45:13 gaba Exp $

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMain {
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

	# �Ѹ�����
	tempPrintIslandHead();	# �褦����!!
	islandInfo();			# ��ξ���
	islandMap(0) if(!$easy_mode); # ����Ͽޡ��Ѹ��⡼��

	# �����������Ǽ���
	if($HuseLbbs) {
		tempLbbsHead();		# ������Ǽ���
		tempLbbsInput();	# �񤭹��ߥե�����
		tempLbbsContents();	# �Ǽ�������
	}

	# �ᶷ���ʰ״Ѹ����̿��ξ���ɽ�����ʤ�
	tempRecent(0) if(!$easy_mode);
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub ownerMain {
	# ����
	unlock();

	# �⡼�ɤ�����
	$HmainMode = 'owner';

	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		return;
	}

    # ��ȯ����
    if($HjavaMode eq 'java') {
		write_access_log("JS"); # ����������
		tempOwnerJava();	# ��Java������ץȳ�ȯ�ײ��
    } else {
		write_access_log("NM"); # ����������
		tempOwner();		# ���̾�⡼�ɳ�ȯ�ײ��
    }

    # �����������Ǽ���
    if($HuseLbbs) {
		tempLbbsHead();			# ������Ǽ���
		tempLbbsInputOW();		# �񤭹��ߥե�����
		tempLbbsContents();		# �Ǽ�������
    }

	# �ᶷ
	tempRecent(1);
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commandMain {
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

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# �ե����ϡ��ե��Ϥʤ餷
		# ��ɸ�������
		makeRandomPointArray();
		my($land) = $island->{'land'};

		# ���ޥ�ɤμ������
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
		# ���ä�
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		tempCommandDelete();

	} elsif($HcommandKind == $HcomPrepRecr) {
		# ���Ω�ơ��Ϥʤ餷
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		slideBack($command, $HcommandPlanNumber);
		tempCommandAdd();
		# ���ޥ�ɤ���Ͽ
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
		# ���ޥ�ɤ���Ͽ
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcommandKind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
	}

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();

}

#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commentMain {
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

	# ��å������򹹿�
	$island->{'comment'} = htmlEscape($Hmessage);

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# �����ȹ�����å�����
	tempComment();

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub localBbsMain {
	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($foreignName);

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '' && $HcurrentID != 0) {
		unlock();
		tempProblem();
		return;
	}

	# ����⡼�ɤ���ʤ���̾������å��������ʤ����
	if($HlbbsMode != 2) {
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# ��̵���Ѹ��԰ʳ��ϥѥ���ɥ����å�
	if($HlbbsMode == 0 && $HforID != 0) {
		# ����ԥ⡼��
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
		$foreignName .= "<font size=-1 color=gray>(".$fIsland->{'name'}."��)</font></A>";
	} elsif($HlbbsMode) {
		# ���⡼��
		if(!checkPassword($island->{'password'},$HinputPassword)) {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}

	my($lbbs);
	$lbbs = $island->{'lbbs'};

	# �⡼�ɤ�ʬ��
	if($HlbbsMode == 2) {
		# ����⡼��
		# ��å����������ˤ��餹
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
		tempLbbsDelete();
	} else {
		# ��Ģ�⡼��
		# ��å���������ˤ��餹
		slideLbbsMessage($lbbs);

		if($HforID == 0 and $HlbbsMode == 0){
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '3';
		} elsif (($HlbbsMode == 0) && ($HforID != $island->{'id'})){
			$HlbbsMessage = htmlEscape($HlbbsMessage) . "����".$foreignName;
			$message = '0';
		} else {
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '1';
		}
		$HlbbsName = "$HislandTurn��" . htmlEscape($HlbbsName);
		my $now = time;
		$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage&$now";

		tempLbbsAdd();
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);

	# ��ȤΥ⡼�ɤ�
	if($HlbbsMode == 0) {
		printIslandMain();
	} else {
		ownerMain();
	}
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
	my($island) = $Hislands[$HcurrentNumber];
	# ����ɽ��
	my($rank) = $HcurrentNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	my($mountain) = $island->{'mountain'};
	my($mStr3) = '';
	my($cmt_) = 7;

	# ͽ�����֡����ȼԤ���¤���äƤ�����ٹ�
	if($HislandTurn < $HyosenTurn) {
		my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
		$tmp = 0 if($tmp < 0);
		$mStr3 = "<FONT COLOR=RED><B>���ȼԤ�".$Hno_work.$HunitPop.
					"�ʾ�ФƤ���Τǡ��͸����ä����ȥåפ��ޤ����������ߤ���ƤƲ�������</B></FONT>" if($tmp >= $Hno_work);
		$cmt_++;
	}
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";

	my($mStr1) = '';
	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# ̵���ޤ���owner�⡼��
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
		$cmt_++;
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		# 1000��ñ�̥⡼��
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
		$cmt_++;

		$farm 	  = "��̩" if($Hhide_farm == 2);
		$factory  = "��̩" if($Hhide_factory == 2);

	}

	my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
		$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
	}

	# ��������ɽ��
	my $fight_name = '';
	if($island->{'fight_id'} > 0 and $island->{'pop'} > 0) {
		my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
		if($HcurrentNumber ne '') {
			my $tIsland = $Hislands[$HcurrentNumber];
			my $name = '<A HREF="'.$HthisFile."?Sight=".$tIsland->{'id'}."\" TARGET=_blank>$tIsland->{'name'}��</A>";
			$fight_name = "<TR><TD $HbgCommentCell COLSPAN=".$cmt_." align=CENTER nowrap=nowrap><NOBR><B>��������$name�Ǥ�</B></NOBR></TD></TR>";
		}
	}

	# ��ȯ��ߤ�ɽ��
	my $rest_msg = '';
	if($island->{'rest'} > 0 and $HislandNumber > 1 and $island->{'pop'} > 0) {
		$rest_msg  = "<TR><TH $HbgCommentCell COLSPAN=".$cmt_." nowrap=nowrap><NOBR>\n";
		$rest_msg .= "���ﾡ�ˤ�곫ȯ����桡";
		$rest_msg .= "�Ĥ�<FONT COLOR=RED>".$island->{'rest'}."</FONT>������</NOBR></TH></TR>";
	}

	my $time;
	if($HislandNumber > 1) {
		#������ɽ��
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		$time = "<BR><B>������${HislandTurn}</B> �ʼ��Υ�����ޤǡ�$hour���� $minʬ $sec�á�";
	}

	# �͸���ɽ��
	$pop = (!$Hhide_town or $HmainMode eq 'owner') ? $island->{'pop'}.$HunitPop : aboutPop($island->{'pop'});

	out(<<END);
<CENTER>
${time}
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�η��쵬��${H_tagTH}</NOBR></TH>
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

# �Ͽޤ�ɽ��
# ������1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
sub islandMap {
	my($mode, $js) = @_;
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
			if($com->{'kind'} < 20) {
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
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], $js);
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

sub landString {
	my($l, $lv, $x, $y, $mode, $comStr, $j_mode) = @_;
	my($point) = "($x,$y)";
	my($image, $alt);

	if($l == $HlandSea) {
		if($lv == 1) {
			# ����
			$image = 'land14.gif';
			$alt = '��(����)';
		} else {
			# ��
			$image = 'land0.gif';
			$alt = '��';
		}
	} elsif($l == $HlandWaste) {
		# ����
		if($lv == 1) {
			$image = 'land13.gif'; # ������
			$alt = '����';
		} else {
			$image = 'land1.gif';
			$alt = '����';
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$image = 'land2.gif';
		$alt = 'ʿ��';
	} elsif($l == $HlandForest) {
		# ��
		if($mode == 1) {
			$image = 'land6.gif';
			$alt = "��(${lv}$HunitTree)";
		} else {
			# �Ѹ��Ԥξ����ڤ��ܿ�����
			$image = 'land6.gif';
			$alt = '��';
		}
	} elsif($l == $HlandTown) {
		# Į
		my($p, $n);
		if($lv < 30) {
			$p = 3;
			$n = '¼';
		} elsif($lv < 100) {
			$p = 4;
			$n = 'Į';
		} else {
			$p = 5;
			$n = '�Ի�';
		}

		$image = "land${p}.gif";
		$alt = "$n(${lv}$HunitPop)";
		$alt = $n if($Hhide_town and $mode == 0);
	} elsif($l == $HlandFarm) {
		# ����
		$image = 'land7.gif';
		$alt = "����(${lv}0${HunitPop}����)";
		($image,$alt) =  ('land6.gif','��') if($Hhide_farm and $mode == 0)
	} elsif($l == $HlandFactory) {
		# ����
		$image = 'land8.gif';
		$alt = "����(${lv}0${HunitPop}����)";
		($image,$alt) =  ('land6.gif','��') if($Hhide_factory and $mode == 0)
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# �Ѹ��Ԥξ��
			($image,$alt) = ($Hhide_missile) ? ('land6.gif','��') : ('land9.gif','�ߥ��������');
		} else {
			# �ߥ��������
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "�ߥ�������� (��٥� ${level}/�и��� $lv)";
		}
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		$image = 'land10.gif';
		$alt = '�ɱһ���';
		($image,$alt) =  ('land6.gif','��') if($Hhide_deffence and $mode == 0)
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		$image = 'land10.gif';
		if($mode == 0) {
			# �Ѹ��Ԥξ����ɱһ��ߤΤդ�
			$alt = '�ɱһ���';
		} else {
			$alt = '�ϥ�ܥ�';
		}
	} elsif($l == $HlandMountain) {
		# ��
		my($str);
		$str = '';
		if($lv > 0) {
			$image = 'land15.gif';
			$alt = "��(�η���${lv}0${HunitPop}����)";
		} else {
			$image = 'land11.gif';
			$alt = '��';
		}
	}


	# ��ȯ���̤ξ��ϡ���ɸ����
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

// �ߥ������ϰϤΥޡ����󥰤򥻥å�
function set_mark(x, y) {
   if(!document.mark_form.mark.checked) return false;
   if(!document.getElementById) {
      alert("���ѿ���������ޤ��󤬡����Ȥ��Υ֥饦���Ϥ��ε�ǽ�򥵥ݡ��Ȥ��Ƥ��ޤ���");
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

      // �Ԥˤ�����Ĵ��
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

// ������ޡ����󥰲�
function set_highlight(x, y, color) {
   if(document.getElementById) {
      document.getElementById(x+"x"+y).width  = "30";
      document.getElementById(x+"x"+y).height = "30";
      document.getElementById(x+"x"+y).border = "1";
      document.getElementById(x+"x"+y).style.borderColor = "#"+color;
   }
}

// �ޡ����󥰲��
function unset_highlight(x, y) {
   if(document.getElementById) {
      document.getElementById(x+"x"+y).width  = "32";
      document.getElementById(x+"x"+y).height = "32";
      document.getElementById(x+"x"+y).border = "0";
   }
}

// ���ƤΥޡ����󥰤���
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
�ޡ�����<INPUT TYPE=CHECKBOX NAME="mark">
����
<SELECT NAME="kind_mark">
<OPTION VALUE="">ɸ��
<OPTION VALUE="FFFF00">Yellow
<OPTION VALUE="FF0000">Red
<OPTION VALUE="0000FF">Blue
<OPTION VALUE="00FF00">Green
<OPTION VALUE="FF00FF">Purple
<OPTION VALUE="CCCCBB">Gray
<OPTION VALUE="-">None
</SELECT>
�ϰ�
<SELECT NAME="number_mark">
<OPTION VALUE="1">0HEX
<OPTION VALUE="7">1HEX
<OPTION VALUE="19" SELECTED>2HEX
</SELECT>
��<INPUT TYPE="BUTTON" VALUE="���" onClick="unset_all_highlight();">
</FORM>
END
}


#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ���̥�ɽ��
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode, 1);
	}
}

# ������ؤ褦��������
sub tempPrintIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}�ؤ褦��������${H_tagBig}<BR>
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

# �����糫ȯ�ײ�
sub tempOwner {

	my($island) = $Hislands[$HcurrentNumber];
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
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
<nobr><BR>�ߥ�����ȯ�;�¿�[<b> $island->{'fire'} </b>]ȯ</nobr>
<FORM action="$HthisFile" method=POST>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="$HdefaultPassword">
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
	my($kind, $cost, $s);
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
<B>��ɸ(</B>
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
<B>����</B><SELECT NAME=AMOUNT>
END

	# ����
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>��ɸ����</B><BR>
<SELECT NAME=TARGETID>
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
</CENTER>
</TD>
<TD $HbgMapCell VALIGN=TOP><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA></center>
END
	islandMap(1);	# ����Ͽޡ���ͭ�ԥ⡼��
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
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
������<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
�ѥ����<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

# ���ϺѤߥ��ޥ��ɽ��
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
		$target = "̵��";
	}
	$target = "$HtagName_${target}��$H_tagName";
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

	my($j) = sprintf("%02d��", $number + 1);

	out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

	if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) || 
	   ($kind == $HcomGiveup)) {
		out("$name");
	} elsif(($kind == $HcomMissileNM) ||
			($kind == $HcomMissilePP)) {
		# �ߥ������
		my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
		out("$target$point��$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomSell) {
		# ����͢��
		out("$name$value");
	} elsif($kind == $HcomDestroy) {
		# ����
		out("$point��$name");
	} elsif(($kind == $HcomFarm) || ($kind == $HcomFactory) ||
			 ($kind == $HcomMountain)) {
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

	out("</FONT></NOBR></A><BR>");
}

# ������Ǽ���
sub tempLbbsHead {
	out(<<END);
<HR>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
</CENTER>
END
}

# ������Ǽ������ϥե�����
sub tempLbbsInput {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<font color=red>�礬̵�����⵭Ģ�Ǥ��ޤ����������������Ƥ˴ط���̵��ȯ���ϡ�����������${bbsname}�ؤ��ꤤ���ޤ���</font>
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD colspan="2">��ʬ���硧
<SELECT NAME="ISLANDID">
<OPTION value="0">��̵���Ѹ���
$HislandList</SELECT>
���ѥ���ɡ�<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonFO$HcurrentID"></TD>
</TR>
</TABLE>
END
	out("<INPUT TYPE=HIDDEN NAME='BBSMODE'>") if($easy_mode);
	my $msg = ($easy_mode) ? "Sight=$HcurrentID>�ݡ��̾�Ѹ����̤�..." : "BBS=$HcurrentID>�ݡ�ʰ״Ѹ����̿���...";
	out("<B><A STYlE=\"text-decoration:none\" HREF=".$HthisFile."?".$msg."</A></B>");
	out("</FORM>\n</CENTER>\n");
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH COLSPAN=2>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ֹ�
<SELECT NAME=NUMBER>
END
	# ȯ���ֹ�
	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonDL$HcurrentID">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ�������
sub tempLbbsContents {
	my($lbbs, $line);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	out(<<END);
<CENTER>
<font color=red><b>��̾�򥯥�å�����ȡ��ʰ״Ѹ����̿������Ӥޤ�</b></font>
<TABLE BORDER>
<TR>
<TH>�ֹ�</TH>
<TH>��Ģ����</TH>
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
				# �Ѹ���
				out("<TD>$HtagLbbsSS_$2 > $mes$H_tagLbbsSS</TD></TR>");
			} elsif($1 == 3) {
				# ��̵���Ѹ���
				out("<TD>$HtagLbbsSK_$2 > $mes$H_tagLbbsSK</TD></TR>");
			} else {
				# ���
				out("<TD>$HtagLbbsOW_$2 > $mes$H_tagLbbsOW</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE></CENTER>
END

}

# ����ε�Ͽ
sub FightViewMain {

	open(IN, "$HdirName/fight.log");
	my @lines = <IN>;
	close(IN);
	unlock();

	out ("${HtagTitle_}����ε�Ͽ${H_tagTitle}<BR><DIV ALIGN=right>*�ԼԤ���̾�򥯥�å������������ξ���������ޤ�</DIV>\n");

	foreach $line(@lines) {
		chop($line);
		if($line =~ /<[0-9]*>/) {
			out("</blockquote>\n");
			out("<hr><blockquote>\n<H1>����");
			$line =~ s/<|>//g;
			my $msg = ($line == 0) ? "ͽ�����" : ($line == 99) ? "�辡��" : $line."����";
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
${HtagBig_}${HtagName_}��${islandName}���${H_tagName}��������ͻ�${H_tagBig}<BR>
<a href=${HthisFile}?FightLog=0>${HtagBig_}���${H_tagBig}</a><BR>
<BR>
<TABLE BORDER><TR><TD>
END
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
			landString($l, $lv, $x, $y, 1, $comStr[$x][$y]);
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

# ������������¸
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
	print  ACS time() . ", ${ip}, ${xip}, ${HcurrentID}, ${HcurrentName}��, ${view}, ${agent},\n";
	close(ACS);
}

# ������Ǽ��Ĥ�̾������å��������ʤ����
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ���${H_tagBig}<HR>
END
}

# ���ޥ�ɺ��
sub tempCommandDelete {
	out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
	out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ���${H_tagBig}<HR>
END
}

# �������ѹ�����
sub tempComment {
	out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ���${H_tagBig}<HR>
END
}

# �ᶷ
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�ζᶷ${H_tagBig}<BR>
END
	logPrintLocal($mode);
}

1;
