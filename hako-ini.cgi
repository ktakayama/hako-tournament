#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# ����ե�����
# $Id$

#----------------------------------------------------------------------
# �Ƽ�������
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ���ɬ�����ꤹ����ʬ
#----------------------------------------------------------------------

# ���Υե�������֤��ǥ��쥯�ȥ�  �Ǹ�˥���å���(/)���դ��ʤ���
$baseDir = 'http://www.hako.com';

# �����ե�������֤��ǥ��쥯�ȥ�
$imageDir	= 'http://www.hako.com/img';

$toppage 	= 'http://www.hako.com/';			# �ۡ���ڡ����Υ��ɥ쥹
$bbsname 	= '�Ǽ���';							# �Ǽ��Ĥ�̾��
$bbs		= 'http://www.hako.com/bbs/';		# �Ǽ��ĥ��ɥ쥹
$bbsLog		= './bbs/log.dat';					# �Ǽ��ĤΥ��ե�����̾
$imageExp	= 'http://www.hako.com/imgexp/';	# �����Υ���������������ڡ���

$jcode				= './jcode.pl';				# jcode.pl�ΰ���
$masterPassword		= 'master';					# �ޥ������ѥ����
$HspecialPassword	= 'special';				# �ü�ѥ����
$adminName			= '�����Ԥ�̾��';			# ������̾
$email				= '������@�ɤ�.�ɤ�.�ɤ�';	# �����ԤΥ᡼�륢�ɥ쥹
$version			= "0.97";					# �С������ɽ���ѡʴ���Ū���ѹ����ʤ��褦�ˡ���

$HdirMode			= 0755;						# �ǡ����ǥ��쥯�ȥ�Υѡ��ߥå����
$HdirName			= 'data';					# �ǡ����ǥ��쥯�ȥ��̾��
$Hdirfdata			= 'fdata';					# ����ε�Ͽ�ݻ��ǥ��쥯�ȥ�
$Hdirmdata			= 'mdata';					# ��Ʈ���ϻ�����ǡ���
$Hdiraccess			= 'access_log';				# �����������ݻ��ǥ��쥯�ȥ�

# �ǡ����ν񤭹�����
# ��å�������
# 1 �ե������͡�������
# 2 �����ƥॳ����(��ǽ�ʤ�кǤ�˾�ޤ���)
$lockMode = 1;

# (��)
# 1�����򤹤���ˤϡ�'lockfile'�Ȥ������ѡ��ߥ����666�ζ��Υե������
# ���Υե������Ʊ���֤��֤��Ʋ�������

#----------------------------------------------------------------------
# ɬ�����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ������ߤˤ�ä����ꤹ����ʬ
#----------------------------------------------------------------------
#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
$unlockTime		= 90;		# �۾ｪλ������(��å��岿�äǡ�����������뤫)
$HlogMax		= 8;		# ���ե������ݻ��������
$HhistoryMax	= 10;		# ȯ�����ݻ��Կ�
$HbackupTurn	= 3;		# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTimes	= 3;		# �Хå����åפ򲿲�ʬ�Ĥ���
$HgiveupTurn	= 15;		# �������ޥ�ɼ�ư���ϥ������
$HcommandMax	= 30;		# ���ޥ�����ϸ³���
$HislandSize	= 12;		# ����礭��
$HuseLbbs		= 1;		# ������Ǽ��Ĥ���Ѥ��뤫�ɤ���(0:���Ѥ��ʤ�)
$HlbbsMax		= 10;		# ������Ǽ�����¸�Կ�
$HlbbsView		= 5;		# ������Ǽ��ġ��̾�Ѹ����̤�ɽ������Կ���HlbbsMax��꾮�����������
$Htop_blank		= 0;		# �ȥåפ�����̾����å��ǿ��������̤�ɽ��(0:Ʊ�����̡�1:����������)
$cryptOn		= 1;		# �ѥ���ɤΰŹ沽(1���ȰŹ沽����)
$Hdebug			= 0;		# �ǥХå��⡼��(1���ȡ��֥������ʤ��ץܥ��󤬻��ѤǤ���)
$Hmobile		= 0;		# ���Ӳ��̥ƥ�����(1���ȡ�����Ū�˷����Ѥβ���ɽ��)
$Htime_mode		= 0;		# ���󹹿��ޤǤ�������ɽ������ʤ����Ϥ�����1�ˤ��Ʋ�����
$Hmissile_log	= 0;		# �ߥ�����ȯ�ͤΥ����ά��ɽ�������0:���ʤ� 1:���ꤹ���

# �󽷶����ꡡ�ʺǸ�˹���(�ߥ�������)���­���Τ����ƶ��̡�
# �����˽񤤤Ƥ�������ʳ��ˤ���Ȥ櫓�狼�����ˤʤ�ޤ�
# 1: (�����Υߥ�������Ϥο� + �������ɱһ��ߤο� * 2) / 2 * ��ʬ����Ʈ�԰ٲ�� * 15
# 2: �����줿���ߤ��������졦���졦�ߥ�������ϡ��ɱһ��ߡ˴��������
# ���ζ����ˤ�� ��ͽ�ꡡ���ꤷ�ʤ��ǲ�����
# ����Ū�ʶ������� ��ͽ�ꡡ���ꤷ�ʤ��ǲ�����
$HrewardMode	= 1;

# ��������������
# 0: (�ǥե����) ���Ϥȸ�����ζ�����Ƚ�ꤹ������
# 1: �ȡ��ʥ���ɽ��Ȥä����� �ǽ������������Τ����Ϥ�׻� (���ﾡ���Ф�ȡ�������ư��ޤ���)
# �����ʥ�����   ��ͽ�� ���ꤷ�ʤ��ǲ�����
$Htournament	= 0;

#----------------------------------------
# �������֤䡢���
#----------------------------------------
$HmaxIsland		= 100;		# ��κ����
$HfightMem 		= 32;		# ͽ�����̲������2�Τ٤���ˤ���٤���
$HyosenTurn		= 48;		# ͽ�����֥��������0�ˤ��ʤ��ǲ�������
$HdevelopeTurn	= 24;		# ��ȯ���֥������
$HfightTurn		= 12;		# ��Ʈ���֥������
$HunitTime		= 43200;	# ͽ�����ֹ�������(3600�á�1����)
$HdevelopeTime	= 7200;		# ��ȯ���ֹ������� # 2����
$HfightTime		= 86400;	# ��Ʈ���ֹ������� # 24����
$HinterTime		= 93600;	# ��Ʈ���ֽ�λ��γ�ȯ���֤ؤΰܹԤޤǤλ���
$HyosenRepCount	= 3;		# ͽ�����ְ��˹������륿�����(�㤨�У��ˤ���ȤޤȤ�ƣ�������ʤ�)
$HdeveRepCount	= 1;		# ��ȯ���ְ��˹������륿�����
$HfightRepCount	= 3;		# ��Ʈ���ְ��˹������륿�����
$HstopAddPop	= 3;		# �͸����å��ȥåפ����ⷫ����
$do_fight		= 3;		# ���ﾡ�ˤʤ�ʤ�����Ρ�ɬ����Ʈ�԰ٲ��

# ���ﾡ�γ�ȯ��ߥ������
$HnofightTurn	= 12;		# ������
$HnofightUp		= 4;		# ��ο��͡��� ���ο��߲͡�����Ȥʤ�ޤ�

#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
$HinitialMoney		= 2000;		# ������
$HinitialFood		= 1000;		# �������
$HlandSizeValue		= 32;		# �������
$HseaNum			= 20;		# ��������ο�
$HunitMoney			= '����';	# �����ñ��
$HunitFood			= '00�ȥ�';	# ������ñ��
$HunitPop			= '00��';	# �͸���ñ��
$HunitArea			= '00����';	# ������ñ��
$HunitTree			= '00��';	# �ڤο���ñ��
$HtreeValue			= 5;		# �ڤ�ñ�������������
$HtreeUp			= 2;		# ����������ڤ��������ܿ�
$HtownUp			= 10;		# �͸�����������10���Ⱥ���1000�͡�
$HeatenFood			= 0.2;		# �͸�1ñ�̤�����ο���������
$HtownGlow			= 25;		# ¼��ȯ��Ψ�ʡ��
$Hno_work			= 500;		# ���ȼԿ��Υܡ������饤���10����1000�͡�
								# ���ο��ͤ�Ķ����ȡ��͸����ä����ȥåפ��ޤ���ͽ���Τߡ�
$HcostChangeName	= 0;		# ̾���ѹ��Υ�����
$HdefenceValue		= 400;		# �ɱһ��ߤ������

# ��缫ư�Ϥʤ餷��
$precheap			= 10;		# �����ܤι��Ϥ�����������ʤ��ο��μ��ι��Ϥ����
$precheap2			= 8;		# ���κݤγ��Ψ��8�ˤ����顢2����Ȥ������Ȥˤʤ�ޤ���

#----------------------------------------
# ����������Ի԰ʳ��Ͽ��ǵ�����
#----------------------------------------
$HhideMoneyMode		= 2;		# ����ɽ��(0:�����ʤ���1: �����롡2:100�ΰ̤ǻͼθ���)
$Hhide_missile		= 1;		# �ߥ�������ϡ�0:���ʤ���1:����
$Hhide_deffence		= 1;		# �ɱһ��ߡ�0:���ʤ���1:����
$Hhide_town			= 0;		# �ԻԷϡ�0:���ʤ���1:����
$Hhide_farm			= 0;		# ���졡0:���ʤ���1:���롡2:���ϤⱣ��
$Hhide_factory		= 0;		# ���졡0:���ʤ���1:���롡2:���ϤⱣ��

#----------------------------------------
# �ü�����ʾܤ���������readme�ǡ�
#----------------------------------------
# 0:���ꤷ�ʤ���1:���ꤹ��
$HeasyReclaim		= 0;		# ���Ω�Ƥδʰײ�

#----------------------------------------
# ���Ϥηи���
#----------------------------------------
$HmaxExpPoint	= 200;		# �и��ͤκ�����(����255)
$maxBaseLevel	= 5;		# �ߥ�������ϡ���٥�κ�����
@baseLevelUp	= (20, 60, 120, 200);	# �и���

#----------------------------------------
# �ҳ�
#----------------------------------------
# ��������ȯ��Ψ(��Ψ��0.1%ñ��)
$HdisFallBorder	= 90;	# �����³��ι���(Hex��)
$HdisFalldown	= 30;	# ���ι�����Ķ�������γ�Ψ

#----------------------------------------
# �޴ط�
#----------------------------------------
# �ޤ�̾��
$Hprize[0] = '��������';
$Hprize[1] = '�˱ɾ�';
$Hprize[2] = 'Ķ�˱ɾ�';
$Hprize[3] = '����˱ɾ�';
$Hprize[4] = 'ʿ�¾�';
$Hprize[5] = 'Ķʿ�¾�';
$Hprize[6] = '���ʿ�¾�';
$Hprize[7] = '�����';
$Hprize[8] = 'Ķ�����';
$Hprize[9] = '��˺����';

#----------------------------------------
# �����ط���
#----------------------------------------
$htmlBody	= 'BGCOLOR="#EEFFFF"';		# <BODY>�����Υ��ץ����
$Htitle		= 'Ȣ��ȡ��ʥ��ȣ�';		# ������Υ����ȥ�ʸ��

# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# ��������
$HtagFico_ = '<FONT SIZE="7" COLOR="#4444ff">';
$H_tagFico = '</FONT>';

# H1������
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# �礭��ʸ��
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# ���̾���ʤ�
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# �����ʤä����̾��
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# �ҳ�
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';

# ������Ǽ��ġ���̵���Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSK_ = '<FONT COLOR="#003333"><B>';
$H_tagLbbsSK = '</B></FONT>';

# �̾��ʸ����(��������Ǥʤ���BODY�����Υ��ץ�����������ѹ����٤�
$HnormalColor = '#000000';

# ���ɽ�������°��
$HbgTitleCell   = 'BGCOLOR="#ccffcc"';	# ���ɽ���Ф�
$HbgNumberCell  = 'BGCOLOR="#ccffcc"';	# ���ɽ���
$HbgNameCell	= 'BGCOLOR="#ccffff"';	# ���ɽ���̾��
$HbgInfoCell	= 'BGCOLOR="#ccffff"';	# ���ɽ��ξ���
$HbgCommentCell = 'BGCOLOR="#ccffcc"';	# ���ɽ��������
$HbgInputCell   = 'BGCOLOR="#ccffcc"';	# ��ȯ�ײ�ե�����
$HbgMapCell		= 'BGCOLOR="#ccffcc"';	# ��ȯ�ײ��Ͽ�
$HbgCommandCell = 'BGCOLOR="#ccffcc"';	# ��ȯ�ײ����ϺѤ߷ײ�

# ͽ���������åɥ饤��
$YbgNumberCell  = 'BGCOLOR="#F0BBDA"'; # ���ɽ���
$YbgNameCell    = 'BGCOLOR="#E4CCF5"'; # ���ɽ���̾��
$YbgInfoCell    = 'BGCOLOR="#E4CCF5"'; # ���ɽ��ξ���
$YbgCommentCell = 'BGCOLOR="#F0BBDA"'; # ���ɽ��������

#----------------------------------------
# �إå������եå���
#----------------------------------------
# �إå�
sub tempHeader {

	my($HimgFlag) = 0;
	if($HimgLine eq '' || $HimgLine eq $imageDir){
		$baseIMG = $imageDir;
		$HimgFlag = 1;
	} else {
		$baseIMG = $HimgLine;
	}
	$baseIMG =~ s/�޽�į��/�ǥ����ȥå�/g;

	out("Content-type: text/html\n\n");
	return if($Hasync);

	if($Hmobile == 0) {
		my $bbTime = get_time((stat($bbsLog))[9], 1, 1);
		out(<<END);
<HTML>
<HEAD>
<TITLE>$Htitle</TITLE>
<BASE HREF="$baseIMG/">
</HEAD>
$Body
��<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A>
 / <A HREF="http://appoh.execweb.cx/hakoniwa/" target=_blank>Ȣ��Java������ץ��� ���۸�</A>
 / <A HREF="http://espion.just-size.jp/archives/dist_hako/" target=_blank>Ȣ��ȡ��ʥ��ȣ� ���۸�</A>
 / <A HREF="http://espion.just-size.jp/files/link/link.cgi" target=_blank>Ȣ��ȡ��ʥ��ȥ�󥯽�</A>
<B><BR>
<A HREF="$toppage">�ȥåץڡ���</A>
 / <A HREF="$bbs">$bbsname</A>$bbTime
 / <A HREF="$HthisFile?LogFileView=1" target=_blank>�Ƕ�ν����</A>
 / <A HREF="$HthisFile?help=1">�������</A>
 / <A HREF="$HthisFile?exp=1" target=_blank>�ޥ˥奢��</A>
 / <A HREF="$baseDir/hako-main.cgi">���</A>
</B>
</nobr>
<HR>
END
		if($HimgFlag) {
			out("<FONT COLOR=RED>�����С���ٷڸ��ΰ٤ˡ������Υ����������ԤäƲ�����褦�ˤ��ꤤ�פ��ޤ���</FONT><HR>");
		}
	} else {
       out(<<END);
<HTML>
<HEAD>
<TITLE>$Htitle</TITLE>
</HEAD>
<BODY bgcolor="#ffffff">
<a href="./hako-main.cgi">�ȥå�</a> <a href="./hako-main.cgi?help=1">�إ��</a> <a href="./hako-main.cgi?exp=1">���</a>
<hr>
END
    }
}

# �եå�
sub tempFooter {
	if($Hmobile == 0) {
		out(<<END);
<HR>
<P align=right>
<NOBR>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html" target=_blank>Ȣ����祹����ץ����۸�</A>
����<A HREF="$toppage">�ȥåץڡ���</A>
����<A HREF="$bbs">$bbsname</A>
����<A HREF="$HthisFile?LogFileView=1" target=_blank>�Ƕ�ν����</A>
</nobr><BR><BR>
������:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
</P>
END
	}
	out(<<END);
</BODY>
</HTML>
END
}

require('local-ini.cgi') if(-e 'local-ini.cgi');

1;
