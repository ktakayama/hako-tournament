#!/usr/bin/env perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# �ᥤ�󥹥���ץ�
# $Id: hako-main.cgi,v 1.4 2004/11/06 02:28:45 gaba Exp $

# ���顼�����å���
#use CGI::Carp qw(fatalsToBrowser);

# ����ե������ɤ߹���
require ('hako-ini.cgi');

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------

# ���Υե�����
$HthisFile = "$baseDir/hako-main.cgi";

# �Ϸ��ֹ�
$HlandSea		= 0;  # ��
$HlandWaste		= 1;  # ����
$HlandPlains	= 2;  # ʿ��
$HlandTown		= 3;  # Į��
$HlandForest	= 4;  # ��
$HlandFarm		= 5;  # ����
$HlandFactory	= 6;  # ����
$HlandBase		= 7;  # �ߥ��������
$HlandDefence	= 8;  # �ɱһ���
$HlandMountain	= 9;  # ��
$HlandHaribote	= 14; # �ϥ�ܥ�

# ���ޥ��
$HcommandTotal = 22; # ���ޥ�ɤμ���
					 # ���ޥ�ɤ����䤹���ϡ���°��readme����ս񤭤��ɤ��ɤ��

# �ײ��ֹ������
# ���Ϸ�
$HcomPrepare  = 01; # ����
$HcomPrepare2 = 02; # �Ϥʤ餷
$HcomReclaim  = 03; # ���Ω��
$HcomDestroy  = 04; # ����
$HcomSellTree = 05; # Ȳ��
$HcomPrepRecr = 06; # ��᤿�ơ��Ϥʤ餷

# ����
$HcomPlant		= 11; # ����
$HcomFarm		= 12; # ��������
$HcomFactory	= 13; # �������
$HcomMountain	= 14; # �η�������
$HcomBase		= 15; # �ߥ�������Ϸ���
$HcomDbase		= 16; # �ɱһ��߷���
$HcomHaribote	= 18; # �ϥ�ܥ�����
$HcomFastFarm	= 19; # ��®��������

# ȯ�ͷ�
$HcomMissileNM	= 31; # �ߥ�����ȯ��
$HcomMissilePP	= 32; # PP�ߥ�����ȯ��

# ���ķ�
$HcomDoNothing	= 41; # ��ⷫ��
$HcomSell		= 42; # ����͢��
$HcomGiveup		= 46; # �������

# ��ư���Ϸ�
$HcomAutoPrepare	= 61; # �ե�����
$HcomAutoPrepare2	= 62; # �ե��Ϥʤ餷
$HcomAutoDelete		= 63; # �����ޥ�ɾõ�
$HcomAutoPrepare3	= 45; # ��缫ư�Ϥʤ餷

# ����
@HcomList =
	($HcomPrepare, $HcomPrepare2, $HcomReclaim, $HcomDestroy,
	 $HcomSellTree, $HcomPrepRecr, $HcomPlant, $HcomFarm, $HcomFactory, $HcomMountain, 
	 $HcomFastFarm, $HcomBase, $HcomDbase,
	 $HcomMissileNM, $HcomMissilePP, $HcomDoNothing, $HcomSell, 
	 $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoPrepare3, $HcomAutoDelete, $HcomGiveup);

# �ײ��̾��������
$HcomName[$HcomPrepare]		= '����';
$HcomCost[$HcomPrepare]		= 5;
$HcomName[$HcomPrepare2]	= '�Ϥʤ餷';
$HcomCost[$HcomPrepare2]	= 100;
$HcomName[$HcomReclaim]		= '���Ω��';
$HcomCost[$HcomReclaim]		= 100;
$HcomName[$HcomDestroy]		= '����';
$HcomCost[$HcomDestroy]		= 200;
$HcomName[$HcomPrepRecr]	= '���Ω�ơ��Ϥʤ餷';
$HcomCost[$HcomPrepRecr]	= 0;
$HcomName[$HcomSellTree]	= 'Ȳ��';
$HcomCost[$HcomSellTree]	= 0;
$HcomName[$HcomPlant]		= '����';
$HcomCost[$HcomPlant]		= 10;
$HcomName[$HcomFarm]		= '��������';
$HcomCost[$HcomFarm]		= 20;
$HcomName[$HcomFactory]		= '�������';
$HcomCost[$HcomFactory]		= 100;
$HcomName[$HcomMountain]	= '�η�������';
$HcomCost[$HcomMountain]	= 300;
$HcomName[$HcomFastFarm]	= '��®��������';
$HcomCost[$HcomFastFarm]	= 500;
$HcomName[$HcomBase]		= '�ߥ�������Ϸ���';
$HcomCost[$HcomBase]		= 300;
$HcomName[$HcomDbase]		= '�ɱһ��߷���';
$HcomCost[$HcomDbase]		= 600;
$HcomName[$HcomHaribote]	= '�ϥ�ܥ�����';
$HcomCost[$HcomHaribote]	= 1;
$HcomName[$HcomMissileNM]	= '�ߥ�����ȯ��';
$HcomCost[$HcomMissileNM]	= 20;
$HcomName[$HcomMissilePP]	= 'PP�ߥ�����ȯ��';
$HcomCost[$HcomMissilePP]	= 50;
$HcomName[$HcomDoNothing]	= '��ⷫ��';
$HcomCost[$HcomDoNothing]	= 0;
$HcomName[$HcomSell]		= '����͢��';
$HcomCost[$HcomSell]		= -100;
$HcomName[$HcomGiveup]		= '�������';
$HcomCost[$HcomGiveup]		= 0;
$HcomName[$HcomAutoPrepare]	= '���ϼ�ư����';
$HcomCost[$HcomAutoPrepare]	= 0;
$HcomName[$HcomAutoPrepare2]= '�Ϥʤ餷��ư����';
$HcomCost[$HcomAutoPrepare2]= 0;
$HcomName[$HcomAutoPrepare3] = '��缫ư�Ϥʤ餷';
$HcomCost[$HcomAutoPrepare3] = 0;
$HcomName[$HcomAutoDelete]	= '���ײ�����ű��';
$HcomCost[$HcomAutoDelete]	= 0;

#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------

# COOKIE
my($defaultID);		# ���̾��

# ��κ�ɸ��
$HpointNumber = $HislandSize * $HislandSize;

# �ǥХå��⡼����ϡ�������ΤޤȤṹ���Ϥ��ʤ�
if($Hdebug == 1) {
	$HyosenRepCount	= 1;
	$HdeveRepCount	= 1;
	$HfightRepCount	= 1;
}

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------

# jcode.pl��require
require($jcode);

# my $agent=$ENV{'HTTP_USER_AGENT'};
# require('hako-imode.cgi') if($agent=~/DoCoMo/ or $mobile);

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";

$Body = "<BODY $htmlBody>";

mente_mode() if(-e "./mente_lock");

# ��å��򤫤���
if(!hakolock()) {
	# ��å�����
	# �إå�����
	tempHeader();

	# ��å����ԥ�å�����
	tempLockFail();

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}

# ����ν����
srand(time^$$);

# COOKIE�ɤߤ���
cookieInput();

# CGI�ɤߤ���
cgiInput();

# ��ǡ������ɤߤ���
if(readIslandsFile($HcurrentID) == 0) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

# �ƥ�ץ졼�Ȥ�����
tempInitialize();

# COOKIE����
cookieOutput();


if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
   $HmainMode eq 'commandJava' ||						# ���ޥ�����ϥ⡼��
   $HmainMode eq 'comment' && $HjavaMode eq 'java' ||	# ���������ϥ⡼��
   $HmainMode eq 'lbbs' && $HjavaMode eq 'java') {		# ������BBS�⡼��

	$Body = "<BODY onload=\"init()\" $htmlBody>";
	require('hako-js.cgi');
	require('hako-map.cgi');

	# �إå�����
	tempHeader();

	if($HmainMode eq 'commandJava') {
		# ��ȯ�⡼��
		commandJavaMain();
	} elsif($HmainMode eq 'comment') {
		# ���������ϥ⡼��
		commentMain();
	} elsif($HmainMode eq 'lbbs') {
		# ������Ǽ��ĥ⡼��
		localBbsMain();
	} else {
		ownerMain();
	}

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);

} elsif($HmainMode eq 'landmap') {
	require('hako-js.cgi');
	require('hako-map.cgi');
	$Body = "<BODY $htmlBody>";

	# �إå�����
	tempHeader();
	# �Ѹ��⡼��
	printIslandJava();
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
} elsif($HmainMode ne "expView") {
	# �إå�����
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ������ʹ�
	require('hako-turn.cgi');
	require('hako-top.cgi');
	turnMain();

} elsif($HmainMode eq 'new') {
	# ��ο�������
	require('hako-turn.cgi');
	require('hako-map.cgi');
	newIslandMain();

} elsif($HmainMode eq 'print') {
	# �Ѹ��⡼��
	require('hako-map.cgi');
	printIslandMain();

} elsif($HmainMode eq 'owner') {

	# ��ȯ�⡼��
	require('hako-map.cgi');
	ownerMain();

} elsif($HmainMode eq 'command') {
	# ���ޥ�����ϥ⡼��
	require('hako-map.cgi');
	commandMain();

} elsif($HmainMode eq 'comment') {
	# ���������ϥ⡼��
	require('hako-map.cgi');
	commentMain();

} elsif($HmainMode eq 'lbbs') {
	# ������Ǽ��ĥ⡼��
	require('hako-map.cgi');
	localBbsMain();

} elsif($HmainMode eq 'change') {
	# �����ѹ��⡼��
	require('hako-turn.cgi');
	require('hako-top.cgi');
	changeMain();

} elsif($HmainMode eq 'FightView') {
	# LOG�⡼��
	require('hako-map.cgi');
	FightViewMain();

} elsif($HmainMode eq 'FightIsland') {
	# �ԼԤ���ɽ��
	require('hako-map.cgi');
	fight_map();

} elsif($HmainMode eq 'logView') {
	# LOG�⡼��
	require('hako-top.cgi');
	logViewMain();

} elsif($HmainMode eq 'helpView') {
	# HELP�⡼��
	require('hako-help.cgi');
	helpPageMain();

} elsif($HmainMode eq 'chartView') {
	# �ȡ��ʥ���ɽ�⡼��
	require('hako-chart.cgi');
	chartPageMain();

} elsif($HmainMode eq 'expView') {
	# exp�⡼��
	require('hako-help.cgi');
	expPageMain();

} else {
	# ����¾�ξ��ϥȥåץڡ����⡼��
	require('hako-top.cgi');
	topPageMain();
}

# �եå�����
tempFooter() if($HmainMode ne "expView");

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
	my($command, $number) = @_;
	my($i);

	# ���줾�줺�餹
	splice(@$command, $number, 1);

	# �Ǹ�˻�ⷫ��
	$command->[$HcommandMax - 1] = {
		'kind' => $HcomDoNothing,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
		};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
	my($command, $number) = @_;
	my($i);

	# ���줾�줺�餹
	return if $number == $#$command;
	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
	my($num) = @_; # 0�����Ϸ��ɤߤ��ޤ�
				   # -1�������Ϸ����ɤ�
				   # �ֹ���Ȥ�������Ϸ��������ɤߤ���

	# �ǡ����ե�����򳫤�
	if(!open(IN, "${HdirName}/hakojima.dat")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
		if(!open(IN, "${HdirName}/hakojima.dat")) {
			return 0;
		}
	}

	# �ƥѥ�᡼�����ɤߤ���
	$HislandTurn	 = int(<IN>); # �������
	$HislandLastTime = int(<IN>); # �ǽ���������

	if($HislandLastTime == 0) {
		return 0;
	}
	$HislandNumber		= int(<IN>);  # ������
	$HislandNextID		= int(<IN>);  # ���˳�����Ƥ�ID
	$HislandFightMode	= int(<IN>);  # ���ߤ���Ʈ�⡼��
	$HislandChangeTurn	= int(<IN>);  # �ڤ��ؤ�������
	$HislandFightCount	= int(<IN>);  # �������ܤ�
	$HislandTurnCount	= int(<IN>);  # �����󹹿���
	$HislandChart		= <IN>;       # �ȡ��ʥ���ɽ
	chomp($HislandChart);

	# ���������Ƚ��
	my($now) = time;
	if((($Hdebug == 1 and $HmainMode eq 'Hdebugturn') or 
		(($now - $HislandLastTime) >= $HunitTime) or ($HislandTurnCount > 1)) and $HislandNumber > 1) {
		$HmainMode = 'turn';
		$num = -1; # �����ɤߤ���
	}

	# ����ɤߤ���
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		 $Hislands[$i] = readIsland($num);
		 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}

	# �ե�������Ĥ���
	close(IN);

	return 1;
}

# ��ҤȤ��ɤߤ���
sub readIsland {
	my($num) = @_;
	my($name, $id, $prize, $absent, $comment, $password, $money, $food,
	   $pop, $area, $farm, $factory, $mountain, $score, $fire, $ownername, 
	   $fight_id, $reward, $missile, $log, $fly, $rest);
	$name = <IN>; # ���̾��
	chomp($name);
	if($name =~ s/,(.*)$//g) {
		$score = int($1);
	} else {
		$score = 0;
	}
	$id = int(<IN>);		# ID�ֹ�
	$prize = int(<IN>);		# ����
	$absent = int(<IN>);	# Ϣ³��ⷫ���
	$comment = <IN>;		# ������
	chomp($comment);
	$password = <IN>;		# �Ź沽�ѥ����
	chomp($password);
	$money = int(<IN>);		# ���
	$food = int(<IN>);		# ����
	$pop = int(<IN>);		# �͸�
	$area = int(<IN>);		# ����
	$farm = int(<IN>);		# ����
	$factory = int(<IN>);	# ����
	$mountain = int(<IN>);	# �η���
	$fire = int(<IN>);		# �ߥ�����ȯ�Ϳ�
	$ownername = <IN>;		# �����ʡ��͡���
	chomp($ownername);
	$fight_id = int(<IN>);	# �������ID
	$reward = int(<IN>);	# �󽷶��ѥե饰
	$missile = int(<IN>);	# �󽷶��ѥե饰��
	$log = int(<IN>);		# �����˲���
	$fly = int(<IN>);		# �ߥ����������
	$rest = int(<IN>);		# ���٤ߴ���

	# HidToName�ơ��֥����¸
	$HidToName{$id} = $name;

	# �Ϸ�
	my(@land, @landValue, $line, @command, @lbbs);

	if(($num == -1) || ($num == $id)) {
		if(!open(IIN, "${HdirName}/island.$id")) {
			rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
			if(!open(IIN, "${HdirName}/island.$id")) {
				exit(0);
			}
		}
		my($x, $y);
		for($y = 0; $y < $HislandSize; $y++) {
			$line = <IIN>;
			for($x = 0; $x < $HislandSize; $x++) {
				$line =~ s/^(.)(..)//;
				$land[$x][$y] = hex($1);
				$landValue[$x][$y] = hex($2);
			}
		}

		# ���ޥ��
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			$line = <IIN>;
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
			$command[$i] = {
				'kind' => int($1),
				'target' => int($2),
				'x' => int($3),
				'y' => int($4),
				'arg' => int($5)
				}
		}

		# ������Ǽ���
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}

		close(IIN);
	}

	# �緿�ˤ����֤�
	return {
		 'name' => $name,
		 'id' => $id,
		 'score' => $score,
		 'prize' => $prize,
		 'absent' => $absent,
		 'comment' => $comment,
		 'password' => $password,
		 'money' => $money,
		 'food' => $food,
		 'pop' => $pop,
		 'area' => $area,
		 'farm' => $farm,
		 'factory' => $factory,
		 'mountain' => $mountain,
		 'fire' => $fire,
		 'ownername' => $ownername,
		 'fight_id' => $fight_id,
		 'reward' => $reward,
		 'missile' => $missile,
		 'log' => $log,
		 'fly' => $fly,
		 'rest' => $rest,
		 'land' => \@land,
		 'landValue' => \@landValue,
		 'command' => \@command,
		 'lbbs' => \@lbbs,
	};
}

# ����ǡ����񤭹���
sub writeIslandsFile {
	my($num) = @_;

	# �ե�����򳫤�
	open(OUT, ">${HdirName}/hakojima.tmp");

	# �ƥѥ�᡼���񤭹���
	print OUT "$HislandTurn\n";
	print OUT "$HislandLastTime\n";
	print OUT "$HislandNumber\n";
	print OUT "$HislandNextID\n";
	print OUT "$HislandFightMode\n";
	print OUT "$HislandChangeTurn\n";
	print OUT "$HislandFightCount\n";
	print OUT "$HislandTurnCount\n";
	print OUT "$HislandChart\n";

	# ��ν񤭤���
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		 writeIsland($Hislands[$i], $num);
	}

	# �ե�������Ĥ���
	close(OUT);

	# �����̾���ˤ���
	unlink("${HdirName}/hakojima.dat");
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}

# ��ҤȤĽ񤭹���
sub writeIsland {
	my($island, $num) = @_;
	my($score);
	$score = int($island->{'score'});
	print OUT $island->{'name'} . ",$score\n";
	print OUT $island->{'id'} . "\n";
	print OUT $island->{'prize'} . "\n";
	print OUT $island->{'absent'} . "\n";
	print OUT $island->{'comment'} . "\n";
	print OUT $island->{'password'} . "\n";
	print OUT $island->{'money'} . "\n";
	print OUT $island->{'food'} . "\n";
	print OUT $island->{'pop'} . "\n";
	print OUT $island->{'area'} . "\n";
	print OUT $island->{'farm'} . "\n";
	print OUT $island->{'factory'} . "\n";
	print OUT $island->{'mountain'} . "\n";
	print OUT $island->{'fire'} . "\n";
	print OUT $island->{'ownername'} . "\n";
	print OUT $island->{'fight_id'} . "\n";
	print OUT $island->{'reward'} . "\n";
	print OUT $island->{'missile'} . "\n";
	print OUT $island->{'log'} . "\n";
	print OUT $island->{'fly'} . "\n";
	print OUT $island->{'rest'} . "\n";

	# �Ϸ�
	if(($num <= -1) || ($num == $island->{'id'})) {
		open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}");

		my($land, $landValue);
		$land = $island->{'land'};
		$landValue = $island->{'landValue'};
		my($x, $y);
		for($y = 0; $y < $HislandSize; $y++) {
			for($x = 0; $x < $HislandSize; $x++) {
				printf IOUT ("%x%02x", $land->[$x][$y], $landValue->[$x][$y]);
			}
			print IOUT "\n";
		}

		# ���ޥ��
		my($command, $cur, $i);
		$command = $island->{'command'};
		for($i = 0; $i < $HcommandMax; $i++) {
			printf IOUT ("%d,%d,%d,%d,%d\n", 
						 $command->[$i]->{'kind'},
						 $command->[$i]->{'target'},
						 $command->[$i]->{'x'},
						 $command->[$i]->{'y'},
						 $command->[$i]->{'arg'}
						 );
		}

		# ������Ǽ���
		my($lbbs);
		$lbbs = $island->{'lbbs'};
		for($i = 0; $i < $HlbbsMax; $i++) {
			print IOUT $lbbs->[$i] . "\n";
		}

		close(IOUT);
		unlink("${HdirName}/island.$island->{'id'}");
		rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
	}
}

#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------

# ɸ����Ϥؤν���
sub out {
	print STDOUT jcode::sjis($_[0]);
}

# ����ε�Ͽ��
sub Hfihgt_log {
	my $fight;

	# �����������
	my $fTurn = $HislandFightCount;
	# �辡��ξ��99�ˤ���
	$fTurn = 99 if($HislandNumber == 1);

	open(DOUT, ">$HdirName/fight.log.bak");
	print DOUT "<${fTurn}>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<tr><TH colspan=4></th><th $HbgTitleCell colspan=4>${HtagTH_}����${H_tagTH}</th><TH colspan=1></th>\n";
	print DOUT "<TH $HbgTitleCell colspan=3>${HtagTH_}�Լ�${H_tagTH}</th></tr>\n";
	print DOUT "<TR>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�Լ�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����߿�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>��</TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�󽷶�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ߴ��${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ɻܿ�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>��</TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ߴ��${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ɻܿ�${H_tagTH}</NOBR></TH>\n";
	print DOUT "</tr>\n";

	foreach $fight (@fight_log_flag) {
		my ($name,$tName,$reward,$log,$pop,$tLog,$tPop,$fly,$id) = split(",",$fight);
		$logD	= int($log / 1000)."��";
		$logM	= ($log - $logD * 1000)."��";
		$tLogD	= int($tLog / 1000)."��";
		$tLogM	= ($tLog - $tLogD * 1000)."��";
		$tName	= "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
					$HtagName2_.$tName."��".$H_tagName2."</A>";
		$tPop	.= ${HunitPop};
		if($id == -1) {
			$tName = "${HtagName2_}���ﾡ${H_tagName2}";
			$tPop  = "��";
			$tLogM = "��";
			$tLogD = "��";
		}
		print DOUT "<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}��${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR>${tName}</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${fly}ȯ</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>��</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${reward}${HunitMoney}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${pop}${HunitPop}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${logM}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${logD}</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>��</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${tPop}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${tLogM}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${tLogD}</nobr></TH>\n";
		print DOUT "</tr>\n";
	}
	print DOUT "</TABLE>\n";
	print DOUT @offset;
	close(DOUT);
	rename("${HdirName}/fight.log.bak","${HdirName}/fight.log");
}

# ͽ�������
sub Hlog_yosen {
	my $yosen;
	open(DOUT, ">$HdirName/fight.log");
	print DOUT "<0>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<TR>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH></tr>";
	foreach $yosen (@yosen_log) {
		my ($pop,$name) = split(",",$yosen);
		print DOUT "<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}��${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td></tr>\n";
	}
	print DOUT "</TABLE>\n";
	close(DOUT);
}

# CGI���ɤߤ���
sub cgiInput {
	my($line, $getLine);

	# ���Ϥ������ä����ܸ쥳���ɤ�EUC��
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line = jcode::euc($line);
	$line =~ s/[\x00-\x1f\,]//g;

	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};

	# �оݤ���
	if($line =~ /CommandButton([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��
		$HcurrentID = $1;
		$defaultID = $1;
	}

	if($line =~ /ISLANDNAME=([^\&]*)\&/){
		# ̾������ξ��
		$HcurrentName = cutColumn($1, 32);
	}

	if($line =~ /ISLANDID=([0-9]+)\&/){
		# ����¾�ξ��
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# �ѥ����
	if($line =~ /OLDPASS=([^\&]*)\&/) {
		$HoldPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD2=([^\&]*)\&/) {
		$HinputPassword2 = $1;
	}

	if($line =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}

	# ��å�����
	if($line =~ /MESSAGE=([^\&]*)\&/) {
		$Hmessage = cutColumn($1, 80);
	}

	# ������Ǽ���
	if($line =~ /LBBSNAME=([^\&]*)\&/) {
		$HlbbsName = $1;
		$HdefaultName = $1;
	}
	if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
		$HlbbsMessage = cutColumn($1, 80);
	}

	# �����Υ���������MAC��
	if($line =~ /IMGLINEMAC=([^&]*)\&/){
		my($flag) = 'file:///' . $1;
		$HimgLine = $flag;
	}

	# �����Υ���������
	if($line =~ /IMGLINE=([^&]*)\&/){
		my($flag) = substr($1, 0 , -10);
		$flag =~ tr/\\/\//;
		if($flag eq 'del'){ $flag = $imageDir; } else { $flag = 'file:///' . $flag; }
		$HimgLine = $flag;
	}

	if($line =~ /OWNERNAME=([^\&]*)\&/){
		# �����ʡ�̾����ξ��
		$HownerName = cutColumn($1, 22);
	}

	if($line =~ /CommandJavaButton([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��ʣʣ���᥹����ץȡ�
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# �ʰ״Ѹ����̿��ξ��
	if($line =~ /BBSMODE/) {
		$easy_mode = 1;
	}

	# main mode�μ���
	if($line =~ /TurnButton/) {
		if($Hdebug == 1) {
			$HmainMode = 'Hdebugturn';
		}
	} elsif($line =~ /OwnerButton/) {
		$HmainMode = 'owner';
	} elsif($getLine =~ /Sight=([0-9]*)/) {
		$HmainMode = 'print';
		$HcurrentID = $1;
	} elsif($getLine =~ /BBS=([0-9]*)/) {
		$HmainMode  = 'print';
		$HcurrentID = $1;
		$easy_mode  = 1;
	} elsif($line =~ /ChangeOwnerName/) {
		$HmainMode = 'change';
	} elsif($getLine =~ /LogFileView=([0-9]*)/) {
		$HmainMode = 'logView';
		$Hlogturn = ($1 > $HlogMax) ? $HlogMax : $1;
	} elsif($getLine =~ /help/) {
		$HmainMode = 'helpView';
	} elsif($getLine =~ /chart/) {
		$HmainMode = 'chartView';
	} elsif($getLine =~ /exp/) {
		$HmainMode = 'expView';
	} elsif($getLine =~ /LoseMap=([0-9]*)/) {
		$HmainMode = 'FightIsland';
		$HcurrentID = $1;
	} elsif($getLine =~ /FightLog/) {
		$HmainMode = 'FightView';
	} elsif($getLine =~ /IslandMap=([0-9]*)/) {
		$HmainMode = 'landmap';
		$HcurrentID = $1;
	} elsif($line =~ /NewIslandButton/) {
		$HmainMode = 'new';
	} elsif($line =~ /LbbsButton(..)([0-9]*)/) {
		$HmainMode = 'lbbs';
		if($1 eq 'FO') {
			# �Ѹ���
			$HlbbsMode = 0;
			$HforID = $HcurrentID;
		} elsif($1 eq 'OW') {
			# ���
			$HlbbsMode = 1;
		} else {
			# ���
			$HlbbsMode = 2;
		}
		$HcurrentID = $2;

		# ������⤷��ʤ��Τǡ��ֹ�����
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;

	} elsif($line =~ /ChangeInfoButton/) {
		$HmainMode = 'change';
	} elsif($line =~ /MessageButton([0-9]*)/) {
		$HmainMode = 'comment';
		$HcurrentID = $1;
	} elsif($line =~ /CommandJavaButton/) {
		$HmainMode = 'commandJava';
		$line =~ /COMARY=([^\&]*)\&/;
		$HcommandComary = $1;
	} elsif($line =~ /CommandButton/) {
		$HmainMode = 'command';

		# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /COMMANDMODE=(write|insert|delete)/;
		$HcommandMode = $1;
	} else {
		$HmainMode = 'top';
	}

}


#cookie����
sub cookieInput {
	my($cookie);

	$cookie = jcode::euc($ENV{'HTTP_COOKIE'});

	if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
		$defaultID = $1;
	}
	if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
		$HdefaultPassword = $1;
	}
	if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
		$HdefaultName = $1;
	}
	if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
		$HdefaultX = $1;
	}
	if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
		$HdefaultY = $1;
	}
	if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
		$HdefaultKind = $1;
	}
	if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
		$HimgLine = $1;
		$HimgLine =~ s/�޽�į��/�ǥ����ȥå�/g;
	}
	if($cookie =~ /${HthisFile}JAVAMODE=\(([^\)]*)\)/) {
		$CjavaMode = $1;
	}

}

#cookie����
sub cookieOutput {
	my($cookie, $info);

	# �ä�����¤�����
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
		gmtime(time + 30 * 86400); # ���� + 30��

	# 2������
	$year += 1900;
	if ($date < 10) { $date = "0$date"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min < 10) { $min  = "0$min"; }
	if ($sec < 10) { $sec  = "0$sec"; }

	# ������ʸ����
	$day = ("Sunday", "Monday", "Tuesday", "Wednesday",
			"Thursday", "Friday", "Saturday")[$day];

	# ���ʸ����
	$mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

	# �ѥ��ȴ��¤Υ��å�
	$info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
	$cookie = '';
	
	if(($HcurrentID) && ($HmainMode eq 'owner')){
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
	}
	if($HinputPassword) {
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
	}
	if($HcommandTarget) {
		$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
	}
	if($HlbbsName) {
		$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
	}
	if($HcommandX) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
	}
	if($HcommandY) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
	}
	if($HcommandKind) {
		# ��ư�ϰʳ�
		$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
	}
	if($HimgLine) {
		$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
	}
	if($HjavaMode) {
		$cookie .= "Set-Cookie: ${HthisFile}JAVAMODE=($HjavaMode) $info";
	}
	out($cookie);
}

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# rename����å�
		return hakolock1();

	} elsif($lockMode == 2) {
		# flock����å�
		return hakolock2();
	}
}

sub hakolock1 {
	# ��å���
	$lfh = file_lock() or die return 0;
	return 1;
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# ����
		return 1;
	} else {
		# ����
		return 0;
	}
}

# ��å��򳰤�
sub unlock {
	if($lockMode == 1) {
		# rename����å�
		rename($lfh->{current}, $lfh->{path});
	} elsif($lockMode == 2) {
		# flock����å�
		close(LOCKID);

	}
}

# ����å�����
sub file_lock {
	my %lfh = (dir => "./", basename => "lockfile", timeout => $unlockTime, trytime => 3, @_);
	$lfh{path} = $lfh{dir}.$lfh{basename};

	for (my $i = 0; $i < $lfh{trytime}; $i++, sleep 1) {
		return \%lfh if (rename($lfh{path}, $lfh{current} = $lfh{path} . time));
	}

	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);

	foreach (@filelist) {
		if (/^$lfh{basename}(\d+)/) {
			return \%lfh if (time - $1 > $lfh{timeout} and
			rename($lfh{dir} . $_, $lfh{current} = $lfh{path} . time));
			last;
		}
	}
	undef;
}

# �����������֤�
sub min {
	return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# �ѥ���ɥ��󥳡���
sub encode {
	if($cryptOn == 1) {
		return crypt($_[0], 'h2');
	} else {
		return $_[0];
	}
}

# �ѥ���ɥ����å�
sub checkPassword {
	my($p1, $p2) = @_;
	$p1 =~ s/\r|\n//;

	# null�����å�
	if($p2 eq '') {
		return 0;
	}

	# �ޥ������ѥ���ɥ����å�
	if($masterPassword eq $p2) {
		return 1;
	}

	# ����Υ����å�
	if($p1 eq encode($p2)) {
		return 1;
	}

	return 0;
}

# 1000��ñ�̴ݤ�롼����
sub aboutPop {
	my($p) = @_;
	if($p < 500) {
		return "����5���Ͱʲ�";
	} else {
		$p = int(($p + 250) / 500) * 5;
		return "����".$p."����";
	}
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "����500${HunitMoney}̤��";
	} else {
		$m = int(($m + 500) / 1000);
		return "����${m}000${HunitMoney}";
	}
}

# 1000��ñ�̴ݤ�롼�������Ϸ׻���
sub aboutMoney2 {
	my($m) = @_;
	if($m < 500) {
		return 500;
	} else {
		$m = int(($m + 500) / 1000);
		return $m;
	}
}

# ����������ʸ���ν���
sub htmlEscape {
	my($s) = @_;
	$s =~ s/&/&amp;/g;
	$s =~ s/</&lt;/g;
	$s =~ s/>/&gt;/g;
	$s =~ s/\"/&quot;/g; #"
	return $s;
}

# 80�������ڤ�·��
sub cutColumn {
	my($s, $c) = @_;
	if(length($s) <= $c) {
		return $s;
	} else {
		# ���80�����ˤʤ�ޤ��ڤ���
		my($ss) = '';
		my($count) = 0;
		while($count < $c) {
			$s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
			if($1) {
				$ss .= $1;
				$count ++;
			} else {
				$ss .= $2;
			}
			$count ++;
		}
		return $ss;
	}
}

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
	my($name) = @_;

	# ���礫��õ��
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'name'} eq $name) {
			return $i;
		}
	}

	# ���Ĥ���ʤ��ä����
	return -1;
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if($kind == $HlandBase) {
		# �ߥ��������
		for($i = $maxBaseLevel; $i > 1; $i--) {
			if($exp >= $baseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	}
}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# (@Hrpx, @Hrpy)������
sub makeRandomPointArray {
	# �����
	my($y);
	@Hrpx = (0..$HislandSize-1) x $HislandSize;
	for($y = 0; $y < $HislandSize; $y++) {
		push(@Hrpy, ($y) x $HislandSize);
	}

	# ����åե�
	my ($i);
	for ($i = $HpointNumber; --$i; ) {
		my($j) = int(rand($i+1)); 
		if($i == $j) { next; }
		@Hrpx[$i,$j] = @Hrpx[$j,$i];
		@Hrpy[$i,$j] = @Hrpy[$j,$i];
	}
}

# 0����(n - 1)�����
sub random {
	return int(rand(1) * $_[0]);
}

# 
sub get_time {
	my $time = $_[0];
	my($sec,$min,$hour,$mday,$mon) = localtime($time);
	$mon  = "0".$mon if($mon++ < 9);
	$mday = "0".$mday if($mday < 10);
	$hour = "0".$hour if($hour < 10);
	$min  = "0".$min if($min < 10);
	return ($sec,$min,$hour,$mday,$mon);
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
	my($fileNumber, $id, $mode, $kankou) = @_;
	open(LIN, "${HdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	my($fi) = 0;

	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# ��̩�ط�
		if($m == 1) {
			if(($mode == 0) || ($id1 != $id)) {
				# ��̩ɽ�������ʤ�
				next;
			}
			$m = '<B>(��̩)</B>';
		} elsif($m == 2 and !$id) {
			next;
		} else {
			$m = '';
		}

		# ɽ��Ū�Τ�
		if($id != 0) {
			if(($id != $id1) &&
			   ($id != $id2)) {
				next;
			}
		}
		next if($id and $id2 and $id != $id2 and $Hmissile_log);

		# ɽ��
		if($kankou == 1) {
			out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
		} elsif(($fi == 0) && ($mode == 0)) {
			out("<NOBR><BR><B><I><FONT COLOR='#000000' SIZE=+2>������$turn$m��</FONT></I></B><BR><HR width=50% align=left>\n");
			out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
			$fi++;
		} else {
			out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
		}
	}

	close(LIN);
}

#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �����
sub tempInitialize {
	# �祻�쥯��(�ǥե���ȼ�ʬ)
	$HislandList = getIslandList($defaultID);
}

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
	my($select,$mode,$target) = @_;
	my($list, $name, $id, $s, $i);

	#��ꥹ�ȤΥ�˥塼
	$list = '';
	for($i = 0; $i < $HislandNumber; $i++) {
		$name = $Hislands[$i]->{'name'};
		$id = $Hislands[$i]->{'id'};
		if($mode and $id != $select and $id != $target) {
			next;
		}
		if(($id eq $select and !$mode) or ($id eq $target and $mode)) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		$list .=
			"<OPTION VALUE=\"$id\" $s>${name}��\n";
	}
	return $list;
}

# ��å�����
sub tempLockFail {
	# �����ȥ�
	out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
	# �����ȥ�
	out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack
END
}

# hakojima.dat���ʤ�
sub tempNoDataFile {
	out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���<BR>
�����Ԥ������դ��ޤǻä����Ԥ���������${H_tagBig}$HtempBack
END
}

# �ѥ���ɴְ㤤
sub tempWrongPassword {
	out(<<END);
${HtagBig_}�ѥ���ɤ��㤤�ޤ���${H_tagBig}$HtempBack
<SCRIPT LANGUAGE="JavaScript">
<!--
function init() {}
//-->
</SCRIPT>
END
}

# ��������ȯ��
sub tempProblem {
	out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}

# ���ƥʥ���
sub mente_mode {
	# �إå�����
	tempHeader();

	# ��å�����
	out("${HtagBig_}�������ƥʥ���Ǥ���<BR>�ä����Ԥ���������${H_tagBig}");

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}
