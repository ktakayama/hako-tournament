#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# �إ�ץ⥸�塼��
# $Id: hako-help.cgi,v 1.2 2004/11/03 11:01:20 gaba Exp $

#----------------------------------------------------------------------
# �إ�ץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub helpPageMain {
	# ����
	unlock();

	# �ƥ�ץ졼�Ƚ���
	tempHelpPage();
}


sub tempHelpPage {

	# �ǡ�����ɽ��������
	my($devrep,$firep);
	my($unit) = $HunitTime / 3600;
	my($deve) = $HdevelopeTime / 3600;
	my($fiunit) = $HfightTime / 3600;
	my($inter) = $HinterTime / 3600;
	$HdisFalldown /= 10;
	$HdisFallBorder++;

	$devrep = '��' . $HdeveRepCount . '������ޤȤ�ƹ�����' if($HdeveRepCount > 1);
	$firep  = '��' . $HfightRepCount . '������ޤȤ�ƹ�����' if($HfightRepCount > 1);

	$hide_mon = ($HhideMoneyMode) ? (($HhideMoneyMode == 2) ? "100�ΰ̤ǻͼθ���" : "������") : "����";
	$hide_twn = ($Hhide_town) ? "���Ϥ���" : "������";
	$hide_frm = ($Hhide_farm) ? (($Hhide_farm == 2) ? "���˵���(���ϤⱣ��)" : "���˵���") : "������";
	$hide_fac = ($Hhide_factory) ? (($Hhide_factory == 2) ? "���˵���(���ϤⱣ��)" : "���˵���") : "������";
	$hide_mis = ($Hhide_missile)  ? "���˵���" : "������";
	$hide_def = ($Hhide_deffence) ? "���˵���" : "������";

	# �󽷶������ɽ��
    my $price;
	if($HrewardMode == 1) {
		$price = "(�����Υߥ�������Ϥο� �� �������ɱһ��ߤο� �� 2) �� ".
					"2 �� ��ʬ����Ʈ�԰ٲ�� �� 15 �� ����(�ߥ������פΤ�) �� ".
                    "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} elsif($HrewardMode == 2) {
		$price = "�˲����줿���졦���졦�ߥ�������ϡ��ɱһ��ߤη����� �� ����(�ߥ������פΤ�) �� ".
           "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} else {
		$price = "<FONT COLOR=RED>�󽷶����꤬����������ޤ���</FONT>";
	}

    # ��������������
    my $battle;
    if($Htournament == 1) {
       $battle = "�ȡ��ʥ���ɽ�˽���";
    } else {
       $battle = "�ǥե��������";
    }

    # �ü�����
	my $mStr;
	if($HeasyReclaim) {
		$mStr .= "<H3>${HtagTH_}�����Ω�Ƥδʰײ�${H_tagTH}</H3>\n";
		$mStr .= "�� �̾�������Ω�Ƥ�������ˤʤ�ޤ��������ι��������Ф��ƹ��Ϥˤʤ�ޤ���<BR>\n";
		$mStr .= "�ĤޤꡢΦ�Ϥ��̤��Ƥ볤�ʤ顢���ǹ��Ϥˤʤ�ޤ���<BR>\n";
		$mStr .= "�����Ȥ�������Τ��ưפˤʤ�ޤ���������ʬ¼�������񤯤�ʤ�ޤ��Τǡ�<BR>\n";
		$mStr .= "�ۤɤۤɤ������Ȥޤ��ޤ��礦��<BR><BR>\n";
		$mStr .= "�̾��̤�������ȯ�����ޤ�������ǽ��Ʊ���Ǥ��Τ��ä˵��ˤ���ɬ�פϤ���ޤ���<BR>\n";
	}
	$mStr = "<B>�ʤ�</B><BR>" if(!$mStr);

	out(<<END);
${HtagTitle_}�������${H_tagTitle}
<BR>
<DIV ALIGN=RIGHT><I>system version ${version}</I></DIV><HR>
<BR>
<H1>${HtagHeader_}�󽷶�����${H_tagHeader}</H1>
<B>
$price
</B><BR>
<BR><HR>
<H1>${HtagHeader_}��������������${H_tagHeader}</H1>
<B>
$battle
</B><BR>
<BR><HR>
<H1>${HtagHeader_}�ü�����${H_tagHeader}</H1>
<FONT SIZE=+1>${mStr}</FONT>
<BR><HR>
<H1>${HtagHeader_}�Ƽ�������${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}����ط�${H_tagTH}</TD></TR>
<TR><TD>��${HtagName_}������Ͽ��${H_tagName}��</TD><TD><B>$HmaxIsland��</b></TD></TR>
<TR><TD>��${HtagName_}ͽ������${H_tagName}</TD><TD><B>$HfightMem�̰ʾ�</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}��ν����${H_tagTH}</TD></TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${HlandSizeValue}${HunitArea}</b></TD></TR>
<TR><TD>��${HtagName_}���Ϥο�${H_tagName}</TD><TD><B>9����</b></TD></TR>
<TR><TD>��${HtagName_}�����ο�${H_tagName}</TD><TD><B>${HseaNum}����</b></TD></TR>
<TR><TD>��${HtagName_}���${H_tagName}��</TD><TD><B>${HinitialMoney}${HunitMoney}</b></TD></TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${HinitialFood}${HunitFood}</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}��������${H_tagTH}</TD></TR>
<TR><TD>��${HtagName_}���${H_tagName}��</TD><TD><B>${hide_mon}</b></TD></TR>
<TR><TD>��${HtagName_}�ԻԷ�${H_tagName}��</TD><TD><B>${hide_twn}</b></TD></TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${hide_frm}</b></TD></TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${hide_fac}</b></TD></TR>
<TR><TD>��${HtagName_}�ߥ��������${H_tagName}��</TD><TD><B>${hide_mis}</b></TD></TR>
<TR><TD>��${HtagName_}�ɱһ���${H_tagName}��</TD><TD><B>${hide_def}</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}����¾������${H_tagTH}</TD></TR>
<TR><TD>��${HtagName_}¼ȯ��Ψ${H_tagName}</TD><TD><B>${HtownGlow}��</b></TD></TR>
<TR><TD>��${HtagName_}���ȼԿ����${H_tagName}</TD><TD><B>${Hno_work}${HunitPop}</b></TD></TR>
<TR><TD>��${HtagName_}�͸�������${H_tagName}</TD><TD><B>100��${HtownUp}${HunitPop}��������</b></TD></TR>
<TR><TD>��${HtagName_}�ڤ��������ܿ�${H_tagName}</TD><TD><B>${HtreeUp}00�ܡ�������</b></TD></TR>
<TR><TD>��${HtagName_}�ɱһ���Ȳ�����${H_tagName}</TD><TD><B>${HdefenceValue}${HunitMoney}</b></TD></TR>
<TR><TD>��${HtagName_}��ư����������${H_tagName}</TD><TD><B>${HgiveupTurn}������</b></TD></TR>
<TR><TD>��${HtagName_}���祳�ޥ�����Ͽ�${H_tagName}</TD><TD><B>${HcommandMax}��</b></TD></TR>
<TR><TD>��${HtagName_}��������${H_tagName}</TD><TD><B>${HdisFallBorder}${HunitArea}��${HdisFalldown}��</b></TD></TR>

</table>
<BR><HR>
<H1>${HtagHeader_}������ʹԥإ��${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}�����󹹿�����${H_tagTH}</TD></TR>
<TR><TD><NOBR>��${HtagName_}ͽ������${H_tagName}</NOBR></TD><TD NOWRAP><B>$unit����</b>��${devrep}</TD></TR>
<TR><td WIDTH=100><NOBR>��${HtagName_}��ȯ����${H_tagName}</NOBR></TD><TD NOWRAP><B>$deve����</b>��${devrep}</TD></TR>
<TR><TD><NOBR>��${HtagName_}��Ʈ����${H_tagName}</NOBR></TD><TD NOWRAP><B>$fiunit����</b>��${firep}</TD></TR>
<TR><TD><NOBR>��${HtagName_}��Ʈ���鳫ȯ�ܹ�${H_tagName}</NOBR></TD><TD NOWRAP><B>$inter���ָ�</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}�ƴ��֤Υ������${H_tagTH}</TD></TR>
<TR><TD>��${HtagName_}ͽ��${H_tagName}��</TD><TD><B>$HyosenTurn������ޤ�</b></TD></TR>
<TR><TD>��${HtagName_}��ȯ����${H_tagName}</TD><TD><B><NOBR>$HdevelopeTurn������</NOBR></b></TD></TR>
<TR><TD NOWRAP>��${HtagName_}��Ʈ����${H_tagName}</TD><TD NOWRAP><B>$HfightTurn������</b></TD></TR>
<TR><TD NOWRAP>��${HtagName_}���ﾡ���γ�ȯ��ߡ�${H_tagName}</TD><TD NOWRAP><B>��$HnofightUp	�� ����� �� $HnofightTurn�˥�����</b></TD></TR>

</table>
END

	my($fitone) = $HdevelopeTurn + $HyosenTurn;
	my($fittwo) = $fitone + $HfightTurn;
	my($fitNum) = 1;
	my($v_mode,$v_time,$v_turn,$v_text);
	$v_text = "��";

	# ���������������ɽ����
	if(!$Htime_mode and $HislandTurn < $HyosenTurn) {
		$v_time = (($HyosenTurn - $HislandTurn) / $HdeveRepCount - 1) * $HunitTime + $HislandLastTime + $HunitTime;
		my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
		$v_text = "������".$mon."��".$mday."��".$hour."��".$min."ʬ";
		$v_mode = 1;
		$v_time -= $HinterTime;
	}
	out(<<END);
<BR><HR>
<H1>${HtagHeader_}������ʹԹ��� �ḫɽ${H_tagHeader}</H1>
������ɽ����äƤ����ǽ���������Ф��ꤢ��Τǡ��������٤�α��Ʋ�������
<table height=125 border $HbgNameCell>
<TR>
<td>${HtagName_}ͽ��${H_tagName}</td>
<TD $HbgCommentCell><B>0������$HyosenTurn</B></td>
<TD>$v_text</TD>
</tr>
END

	$v_yosenTime = ($HyosenTurn / $HdeveRepCount) * $HunitTime;
	$HyosenTurn++;
	$v_time += $HdevelopeTime;

	for($i = 2;$i <= $HfightMem;$i*=2) {
		my $kaisen = ($i*2 > $HfightMem) ? "�辡" : "��$fitNum��";
		# ���������������ɽ����
		if(!$Htime_mode and !$v_mode and $HislandTurn + 1 >= $HyosenTurn and $HislandTurn + 1 <= $fitone) {
			$v_time = (($fitone - $HislandTurn) / $HdeveRepCount) * $HdevelopeTime + $HislandLastTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_text = "������".$mon."��".$mday."��".$hour."��".$min."ʬ";
			$v_mode = 1;
		} elsif(!$Htime_mode and $v_mode) {
			$v_time += $HinterTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_time = $v_time + (($HdevelopeTurn - $HdeveRepCount) / $HdeveRepCount * $HdevelopeTime);
			my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($v_time);
			$v_text = $mon."��".$mday."��".$hour."��".$min."ʬ �� ". $mon2."��".$mday2."��".$hour2."��".$min2."ʬ";
		}
	out(<<END);
<TR>
<TD ALIGN=RIGHT>${HtagName_}${kaisen}�ﳫȯ����${H_tagName}</td>
<TD $HbgCommentCell><B>$HyosenTurn������$fitone</b></td>
<TD>$v_text</TD>
</TR>
<TR>
<TD align=right>${HtagName_}��Ʈ����${H_tagName}</TD><TD $HbgCommentCell><B>
END
		# ���������������ɽ����
		if(!$Htime_mode and !$v_mode and $HislandTurn + 1 >= $fitone and $HislandTurn + 1 <= $fittwo) {
			$v_time = (($fittwo - $HislandTurn) / $HfightRepCount - 1) * $HfightTime + $HislandLastTime + $HunitTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_text = "������".$mon."��".$mday."��".$hour."��".$min."ʬ";
			$v_mode = 1;
		} elsif(!$Htime_mode and $v_mode) {
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time + $HfightTime);
			$v_time = $v_time + ($HfightTurn / $HfightRepCount * $HfightTime);
			my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($v_time);
			$v_text = $mon."��".$mday."��".$hour."��".$min."ʬ �� ". $mon2."��".$mday2."��".$hour2."��".$min2."ʬ";
		}
		out (($fitone + 1) . "������$fittwo</b></td><TD>$v_text</TD></tr>\n");
		$fitNum++;
		$HyosenTurn = $fittwo + 1;
		$fitone = $HyosenTurn + $HdevelopeTurn - 1;
		$fittwo = $fitone + $HfightTurn;
	}
	out("</table>\n<BR></hr>\n");
	out("<HR>${HtempBack}");
}

#----------------------------------------------------------------------
# �ޥ˥奢��ڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub expPageMain {
	# ����
	unlock();

	# �ƥ�ץ졼�Ƚ���
	tempexpPage();
}

sub tempexpPage {

	# ɽ��������
	$HunitTime /= 3600;
	$HdevelopeTime /= 3600;
	$HfightTime /= 3600;
	$HinterTime /= 3600;
	$HdisFalldown /= 10;
	$HdisFallBorder++;
	$precheap++;
	$precheap2 = $HcomCost[$HcomPrepare2] * $precheap2 / 10;
	$HfightTurnH = $HfightTurn / 2;

	# �󽷶�����
	if($HrewardMode == 1) {
		$reward_msg = "(�����Υߥ�������Ϥο� �� �������ɱһ��ߤο� �� 2) �� ".
					"2 �� ��ʬ����Ʈ�԰ٲ��<SMALL>*</SMALL> �� 15 �� ����(�ߥ������פΤ�) �� ".
                    "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} elsif($HrewardMode == 2) {
		$reward_msg = "�˲����줿���졦���졦�ߥ�������ϡ��ɱһ��ߤη����� �� ����(�ߥ������פΤ�) �� ".
        "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} else {
		$reward_msg = "<FONT COLOR=RED>�󽷶����꤬����������ޤ���</FONT>";
	}

	# �ݡ�1�ڡ���ʬ��HTML
	out("Content-type: text/html\n\n");
	out(<<END);
<html>
<head>
<title>Ȣ��ȡ��ʥ��ȣ��ޥ˥奢��</title>
<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">

<STYLE type="text/css">
<!--
body	      { font-size: 13pt}
tr,td,th      { font-size: 11pt}
a:link        { font-size: 13pt; color:#000066  }
a:alink       { font-size: 13pt; color:#000066  }
a:visited     { font-size: 13pt; color:#000066  }
a:hover       { font-size: 13pt; color:#FF0000 }
span          { font-size: 25pt }
big           { font-size: 15pt }
small         { font-size: 11pt }
b             { color:#ff3333 }
h2             { color:#006600 }
-->
</STYLE>
</head>
<body bgcolor="#ccccff">
<span><font color=#00cc99>Ȣ��ȡ��ʥ��ȣ�</font></span>
<BR><BR>
���ܤϡ����ꥸ�ʥ��Ȣ����Ʊ���Ǥ���
<BR>���ꥸ�ʥ��Ȣ��2�Υ롼���<a href=http://www.nn.iij4u.or.jp/~flora/>������</a>������������ <BR>
�����˽񤤤Ƥ��ʤ����ϡ�����Ū�ˡ����ꥸ�ʥ��Ʊ�ͤ�����Ǥ���<BR>
�狼��ʤ���������˻פä����ϡ������ڤ˷Ǽ��ĤˤƤ����䲼������

<BR><BR><HR><BR>
<h2>���ɤ�ʥ����फ��</h2>
<B>���У�</b>�Υȡ��ʥ�����Ǥ���
<BR>����줿����������Ʈ������˷��ˤ���м��˿ʤ�ޤ���<BR>
�������󷫤��֤����ǽ�Ū�˻Ĥä�<B>����</b>��ͥ���Ǥ���<BR><BR><BR>

<h2>���ޤ�ͽ����</h2>
��Ͽ���ƺǽ��<B>��${HyosenTurn}������</b>�ޤǤϡ�ͽ�����֤Ǥ���<BR>
��${HyosenTurn}������λ����ǡ�<B>���${HfightMem}��</b>�ˤʤ�褦��<u>�͸��ξ��ʤ�</u>�礬<B>ͽ�����</B>�Ȥʤ�ޤ���<BR>
���δ��֤ϡ�¾��ؤΥߥ�����ȯ�ͥ��ޥ�ɤ�����<B>����󥻥�</b>����ޤ���<BR><BR>
����ˡ����θ��������������꤬���ꡣ��ȯ���֤ؤȰʹߤ��ޤ���<BR><BR>
�ۤäƤ����Ƥ⾡��˿͸��������Ƥ��äƤ��ޤ��ޤ��Τǡ�<B>��ⷫ��${HstopAddPop}���ܤ���ϡ�</b><BR>
����ʹ߿͸���<B>�������äϥ��ȥå�</b>���ޤ���<BR>
���ޥ�����Ϥ�Ԥ��и��̤꼫�����ä��ޤ���<BR><BR>
�ޤ���Ʊ�ͤ�<B>���ȼ�</B>�ο���${Hno_work}${HunitPop}�ʾ�ˤʤ�ȿ͸���<B>�������äϥ��ȥå�</b>���ޤ���<BR>
���ȼԤȤϡ�����Ư���Ƥʤ���̱�λ��Ǥ���
<BR><BR>
�������Ĥο͸��μ������å��ȥåפϡ�<B>ͽ�����֤Τ�</B>�Ǥ���<BR>
<BR><BR>
<h2>����ȯ���֡���Ʈ���֤ˤĤ���</h2>

���θ�<B>${HdevelopeTurn}������</b>�ϡ���ȯ���֤Ǥ���<BR>
���δ��֤⡢<B>�ߥ�����Ϸ�Ƥʤ�</b>�Τǡ���ȯ����ǰ���Ʋ�������<BR>
��ȯ���֤������ȡ���Ʈ���֤�����ޤ�������Ʈ���֤�${HfightTurn}�������<BR>
��Ʈ������ϡ���ʬ��<B>�������ˤΤ�</b>�ߥ������ȯ�ͤ����Ĥ���ޤ���<BR>
�����Ĥ�٤ˤϡ������٤��ʤ��Ȥ����ޤ���<BR>
��Ʈ���ֽ�λ���ˡ�<B>�͸���¿��</b>���������ˤʤ�ޤ���<BR>
�ԼԤ���ϡ�¨�¤���������ޤ�����ĥ�äƲ�������<BR>
<BR>
���θ塢��ȯ���֡���Ʈ���֡䳫ȯ���֡�������³���Ƥ������Ǹ�Σ���ˤʤ�ޤǡ�³���ޤ���<BR>
<B>��ȯ����</b>�κǽ�Υ�����ˡ�������꤬���ꤷ�ޤ���<BR>
<BR><BR>

<h2>�������󹹿��ˤĤ���</h2>
ͽ��������ϡ�<B>${HunitTime}���֤�${HdeveRepCount}������</b>�ʤߤޤ���<BR>
��ȯ������ϡ�<B>${HdevelopeTime}���֤�${HdeveRepCount}������</b>�ʤߤޤ���<BR>
��Ʈ������ϡ�<B>${HfightTime}���֤�${HfightRepCount}������</B>�ʤߤޤ���<BR><BR>
��ȯ���֤κǸ�Υ�����μ��Υ����󹹿��ϡ�����<B>${HfightTime}���ָ�</b>�ˤʤ�ޤ����ʤ狼�ꤺ�餤�Ǥ�����������<BR>
�Ĥޤꡢ��Ʈ���֤�����ޤǤˡ�${HfightTime}���ֶ����Ȥ������ȤǤ���<BR>
�ޤ�����Ʈ���ֽ�λ�����μ��Υ�����ϡ�${HinterTime}���ָ�˹�������ޤ���<BR>
<B>�������</b>�Ȥ����Τ⤢��ޤ��Τǡ�����ǧ��������
<BR><BR><BR>
<h2>������</h2>
���Ԥϡ��͸��Ƿ��ꤷ�ޤ���<BR>
�⤷���͸���������<B>Ʊ��</b>�Ǥ���С���������Ǿ�̤˵錄���������ԤȤʤ�ޤ���<BR>
�����������ǳ��ʤ����ϡ��ɤ������礬�����ﾡ�Ȥ������Ȥˤʤ�ޤ���<BR>
�ޤ���������ϡ�<B>�󽷶�</b>��������ޤ����������ﾡ������󽷶���㤨�ޤ���<BR><BR>
<B>�󽷶�</b>�ϡ�<BR>
$reward_msg
���Ǥ���<BR><BR>
�ޤ�����Ʈ���֤�Ⱦʬ��${HfightTurnH}������ˤ��в᤹��ޤǤˡ���Ʈ�԰ٲ��<SMALL>*</SMALL>��${do_fight}������������ʤ��ä��������̤Ȥʤ�ޤ���<BR>
<BR><BR>

<h2>�����ﾡ</h2>
������꤬���ʤ���硦��ȯ���ֽ�λ���ޤǤˡ�������꤬���ʤ��ʤä������������ǡˤϡ�<B>���ﾡ</b>�Ȥʤ�ޤ���<BR>
���ﾡ�Ȥʤä����ϡ�<B>��������</b>�δ�<B>��ȯ�����</b>���ޤ���<BR>
�Ĥޤꡢ���ޥ�ɤοʹԤ�̵����С��ҳ���ȯ�����ޤ���<BR>
��ȯ���̡����ϴѸ����̡ˤˤơ��Ĥ���ߥ�����ɽ������ޤ��Τǡ����ˤʤ�ޤǰ����ߤȤʤ�ޤ���<BR><BR>
��ȯ��ߴ��֤ϡ�<B>�������${HnofightUp}��${HnofightTurn}</b> �Ǥ���<BR>
�Ĥޤꡢ��1����Ǥ���ߴ��֤ϡ�16������Ȥʤ�ޤ���<BR><BR>
�ޤ�����Ʈ���֤�Ⱦʬ��${HfightTurnH}������ˤ��в᤹��ޤǤˡ�����꤬���ʤ��ʤä����׵ڤӡ�������Ʈ�԰ٲ��<SMALL>*</SMALL>��${do_fight}������������ʤ��ä����פ����ﾡ�����Ȥʤ�ޤ���<BR>
���ξ��ϡ���Ʈ���ϻ�����ξ��֤��ᤵ�졢��ȯ��ߤˤʤ�ޤ���<BR>
��ߴ��֤ϡ�<B>�ʲ������${HnofightUp}��${HnofightTurn}�ˡ� �в᥿�����</B>�Ǥ���
<BR><BR>
�������ﾡ�ϲ����ն���礬�ʤ��Ψ���⤤�Ǥ���
<BR><BR>
��:
��Ʈ�԰٢��ߥ�������Ϸ��ߡ��ɱһ��߷��ߡ��Ƽ�ߥ�����ȯ��<BR>
<BR><BR>
<h2>����������������</h2>
����ä�ʣ���Ǥ������������η�����ˡ�Ǥ���<BR><BR>
END
   if($Htournament == 1) {
      out(<<END);
�ޤ���ͽ�����ֽ�λ��Ʊ�������̤�<b>�����ϡ�</b>����Ф��ޤ���<BR>
���Ϥϰʲ��η׻����˴�Ť��Ƴ��Ф���ޤ���<BR><BR>
250 �� (�͸� + ���� + ���� + �η��쵬��) + ���� �� 700 + �������߿� �� 1000 + ������ + �ڤ��ܿ� �� $HtreeValue - ���� �� $HcomCost[$HcomPrepare2]<BR><BR>
����0�����Ф��줿���ͤδ֤ǿ������ġ�������˼��Ф��ޤ���<BR>
�������Ϥ�5000�ξ�硢�ǽ�Ū�����Ϥϡ�0��5000�δ֤Τɤ줫�Ȥʤ�櫓�Ǥ���<BR><BR>
���κǽ�Ū�˳��Ф��줿���Ϥ򡢾�̤����¤٤ƹԤ����夫����֤˥ȡ��ʥ���ɽ�˳�꿶�äƤ����ޤ���
END
   } else {
      out(<<END);
�ޤ�����Ʈ(ͽ��)���ֽ�λ��Ʊ�������̤�<b>�����ϡ�</b>����Ф��ޤ���<BR>
���Ϥϰʲ��η׻����˴�Ť��Ƴ��Ф���ޤ���<BR><BR>
250 �� (�͸� + ���� + ���� + �η��쵬��) + ���� �� 700 + �������߿� �� 1000 + ������ + �ڤ��ܿ� �� $HtreeValue - ���� �� $HcomCost[$HcomPrepare2]<BR><BR>
����0�����Ф��줿���ͤδ֤ǿ������ġ�������˼��Ф��ޤ���<BR>
�������Ϥ�5000�ξ�硢�ǽ�Ū�����Ϥϡ�0��5000�δ֤Τɤ줫�Ȥʤ�櫓�Ǥ���<BR><BR>
���κǽ�Ū�˳��Ф��줿���Ϥ򡢾�̤����¤٤ƹԤ����夫����֤��������Ȥ��Ƥ����ޤ���
END
   }

   out(<<END);
<BR><BR><BR>
<h2>���ѻߡ��ѹ��������ޥ�ɰ���</h2>
<B>�ʲ��Υ��ޥ�ɤϻ��ѽ���ޤ���</b><BR>
���������<BR>
�������<BR>
��Ͷ�׳�ư<BR>
��������Ϸ���<BR>
���ӣԥߥ�����ȯ��<BR>
��Φ���˲���ȯ��<br>
�������ɸ�<BR>
����ǰ���¤(ȯ��)<BR><BR>
<B>�ʲ��Υ��ޥ�ɤ��ѹ�������ޤ�����</b><BR>
���Ƽ�ߥ�����ȯ�͡��ݡ䡡ͽ������ȯ������ϡ�ȯ�ͤǤ��ޤ�����Ʈ������ϡ��������ˤ���ȯ�ͤǤ��ޤ���<BR>
������ݡ䡡���Ĥ򷡤��������ʤ��ʤ�ޤ������������Ф��ƹԤ��ȡ�����󥻥뤵��ޤ���<BR>
�����ӡ��ݡ䡡${HcomCost[$HcomPlant]}${HunitMoney}��<BR>
��Ȳ�Ρ��ݡ䡡���������̵�����ɱһ��ߤ��Ф��ƹԤ��ȡ�${HdefenceValue}${HunitMoney}����ѽ���롣�����󥿡������ʤ���<BR>
���ɱһ��ߡ��ݡ䡡${HcomCost[$HcomDbase]}${HunitMoney}���Ѹ��Ԥ���Ͽ��˸����롣����Ѥ����������롣<BR><BR>
<B>�ʲ��Ͽ����ޥ�ɤǤ�</b><BR>
����®��������<BR>���ݡ䡡${HcomCost[$HcomFastFarm]}${HunitMoney}����������񤷤ʤ�������������Ʈ������ϻ��ѽ���ޤ���<BR>
����缫ư�Ϥʤ餷<BR>���ݡ䡡���Υ��ޥ�ɰ�Ĥǡ����Ƥι��Ϥ��Ϥʤ餷���Ƥ���롣${precheap}�ս��ܤι��Ϥ���ϡ����Ѥ�${precheap2}${HunitMoney}�ȳ������롣��Ʊ������Ʈ������ϻ����Բġ�<BR>
<BR><BR>

<h2>���ҳ�</h2>

�����ҳ���ȯ�����ޤ���<BR>
ȯ������ҳ��ϰʲ����̤�Ǥ���<BR><BR>

�����������ݡ䡡${HdisFallBorder}�إå����ʾ�ˤ�${HdisFalldown}��<BR>

<BR><BR>
<h2>����ν���͡�������</h2>
��������򤴳�ǧ��������<BR>
<B>*���פ����꤬�����礬����ޤ��Τǡ�ɬ����ǧ���Ʋ�������</B><BR>
<BR><BR>
<!--<h2>����Ͽ��ˡ</h2>
��Ͽ��<a href=mail.html>������</a>�Ǽ����դ��Ƥ���ޤ���<BR>
����¾����Ͽ��ˡ�ϼ����դ��Ƥ���ޤ���<BR>
������������������Ǥλ��äϽ���ޤ���<BR>
<B>�����</b>�Ǥ��Τǡ����������äƤ⻲�äǤ��ʤ����⤴�����ޤ�����λ���������ޤ���<BR>

<BR><BR>-->
<h2>����ջ���</h2>
�����Ĥ���Ǥ��Τǡ��ߥ�������Ļ�������Ȥ��Ƥ���ޤ���<BR>
�ߥ������⤿�줿���ʤ�����������ʤ�ʿ��Ū�����ϡ����ä��ʤ����򤪴��ᤷ�ޤ���<BR><BR>
�ޤ�������ǥ�������������ʤ��ʤ붲�줬�������λ��äϤ��Ǥ��פ��ޤ���<BR>
��������������ȡ����λ���������꤬ͭ���ˤʤäƤ��ޤ��ޤ���<BR><BR>
��Ʈ���֤����ä��顢���Ϥ����򹶷⤷�Ʋ�������<BR>
�ΰդ˳��˸����Ʒ�ä��ꡢ������꤬ͭ���ˤʤ�褦�˲���������ϡ�<B>�ʵ�����</B>�פ��ޤ���<BR><BR>
�����λ��ʤ��顢��ʣ��Ͽ��ʣ���������¾�����ȤǤΡ��Ǽ���϶ػߤǤ���<BR>
ȯ�м��衢����̵�ѤǺ�����ޤ���<BR>
������ϡ���������������ĺ���ޤ���<BR><BR>
����ˡ������󹹿����֤ǤΥ֥饦�����ɤߤ�����ߤ�<B>���Ф�</b>���ʤ��ǲ�������<BR>
<B>�ǡ����ե����뤬����Ƥ��ޤ�</b>��ǽ��������ޤ���<BR><BR>
<HR>
<BR>
</body>
</htML>

END

}

1;
