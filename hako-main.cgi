#!/usr/bin/env perl
# ↑はサーバーに合わせて変更して下さい。
# perl5用です。

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メインスクリプト(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# メインスクリプト
# $Id: hako-main.cgi,v 1.4 2004/11/06 02:28:45 gaba Exp $

# エラーチェック用
#use CGI::Carp qw(fatalsToBrowser);

# 設定ファイル読み込み
require ('hako-ini.cgi');

#----------------------------------------------------------------------
# これ以降のスクリプトは、変更されることを想定していませんが、
# いじってもかまいません。
# コマンドの名前、値段などは解りやすいと思います。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 各種定数
#----------------------------------------------------------------------

# このファイル
$HthisFile = "$baseDir/hako-main.cgi";

# 地形番号
$HlandSea		= 0;  # 海
$HlandWaste		= 1;  # 荒地
$HlandPlains	= 2;  # 平地
$HlandTown		= 3;  # 町系
$HlandForest	= 4;  # 森
$HlandFarm		= 5;  # 農場
$HlandFactory	= 6;  # 工場
$HlandBase		= 7;  # ミサイル基地
$HlandDefence	= 8;  # 防衛施設
$HlandMountain	= 9;  # 山
$HlandHaribote	= 14; # ハリボテ

# コマンド
$HcommandTotal = 22; # コマンドの種類
					 # コマンドを増やす場合は、付属のreadmeの注意書きを良く読む事

# 計画番号の設定
# 整地系
$HcomPrepare  = 01; # 整地
$HcomPrepare2 = 02; # 地ならし
$HcomReclaim  = 03; # 埋め立て
$HcomDestroy  = 04; # 掘削
$HcomSellTree = 05; # 伐採
$HcomPrepRecr = 06; # 埋めたて＋地ならし

# 作る系
$HcomPlant		= 11; # 植林
$HcomFarm		= 12; # 農場整備
$HcomFactory	= 13; # 工場建設
$HcomMountain	= 14; # 採掘場整備
$HcomBase		= 15; # ミサイル基地建設
$HcomDbase		= 16; # 防衛施設建設
$HcomHaribote	= 18; # ハリボテ設置
$HcomFastFarm	= 19; # 高速農場整備

# 発射系
$HcomMissileNM	= 31; # ミサイル発射
$HcomMissilePP	= 32; # PPミサイル発射

# 運営系
$HcomDoNothing	= 41; # 資金繰り
$HcomSell		= 42; # 食料輸出
$HcomGiveup		= 46; # 島の放棄

# 自動入力系
$HcomAutoPrepare	= 61; # フル整地
$HcomAutoPrepare2	= 62; # フル地ならし
$HcomAutoDelete		= 63; # 全コマンド消去
$HcomAutoPrepare3	= 45; # 一括自動地ならし

# 順番
@HcomList =
	($HcomPrepare, $HcomPrepare2, $HcomReclaim, $HcomDestroy,
	 $HcomSellTree, $HcomPrepRecr, $HcomPlant, $HcomFarm, $HcomFactory, $HcomMountain, 
	 $HcomFastFarm, $HcomBase, $HcomDbase,
	 $HcomMissileNM, $HcomMissilePP, $HcomDoNothing, $HcomSell, 
	 $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoPrepare3, $HcomAutoDelete, $HcomGiveup);

# 計画の名前と値段
$HcomName[$HcomPrepare]		= '整地';
$HcomCost[$HcomPrepare]		= 5;
$HcomName[$HcomPrepare2]	= '地ならし';
$HcomCost[$HcomPrepare2]	= 100;
$HcomName[$HcomReclaim]		= '埋め立て';
$HcomCost[$HcomReclaim]		= 100;
$HcomName[$HcomDestroy]		= '掘削';
$HcomCost[$HcomDestroy]		= 200;
$HcomName[$HcomPrepRecr]	= '埋め立て＋地ならし';
$HcomCost[$HcomPrepRecr]	= 0;
$HcomName[$HcomSellTree]	= '伐採';
$HcomCost[$HcomSellTree]	= 0;
$HcomName[$HcomPlant]		= '植林';
$HcomCost[$HcomPlant]		= 10;
$HcomName[$HcomFarm]		= '農場整備';
$HcomCost[$HcomFarm]		= 20;
$HcomName[$HcomFactory]		= '工場建設';
$HcomCost[$HcomFactory]		= 100;
$HcomName[$HcomMountain]	= '採掘場整備';
$HcomCost[$HcomMountain]	= 300;
$HcomName[$HcomFastFarm]	= '高速農場整備';
$HcomCost[$HcomFastFarm]	= 500;
$HcomName[$HcomBase]		= 'ミサイル基地建設';
$HcomCost[$HcomBase]		= 300;
$HcomName[$HcomDbase]		= '防衛施設建設';
$HcomCost[$HcomDbase]		= 600;
$HcomName[$HcomHaribote]	= 'ハリボテ設置';
$HcomCost[$HcomHaribote]	= 1;
$HcomName[$HcomMissileNM]	= 'ミサイル発射';
$HcomCost[$HcomMissileNM]	= 20;
$HcomName[$HcomMissilePP]	= 'PPミサイル発射';
$HcomCost[$HcomMissilePP]	= 50;
$HcomName[$HcomDoNothing]	= '資金繰り';
$HcomCost[$HcomDoNothing]	= 0;
$HcomName[$HcomSell]		= '食料輸出';
$HcomCost[$HcomSell]		= -100;
$HcomName[$HcomGiveup]		= '島の放棄';
$HcomCost[$HcomGiveup]		= 0;
$HcomName[$HcomAutoPrepare]	= '整地自動入力';
$HcomCost[$HcomAutoPrepare]	= 0;
$HcomName[$HcomAutoPrepare2]= '地ならし自動入力';
$HcomCost[$HcomAutoPrepare2]= 0;
$HcomName[$HcomAutoPrepare3] = '一括自動地ならし';
$HcomCost[$HcomAutoPrepare3] = 0;
$HcomName[$HcomAutoDelete]	= '全計画を白紙撤回';
$HcomCost[$HcomAutoDelete]	= 0;

#----------------------------------------------------------------------
# 変数
#----------------------------------------------------------------------

# COOKIE
my($defaultID);		# 島の名前

# 島の座標数
$HpointNumber = $HislandSize * $HislandSize;

# デバックモード中は、ターンのまとめ更新はしない
if($Hdebug == 1) {
	$HyosenRepCount	= 1;
	$HdeveRepCount	= 1;
	$HfightRepCount	= 1;
}

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------

# jcode.plをrequire
require($jcode);

# my $agent=$ENV{'HTTP_USER_AGENT'};
# require('hako-imode.cgi') if($agent=~/DoCoMo/ or $mobile);

# 「戻る」リンク
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}トップへ戻る${H_tagBig}</A>";

$Body = "<BODY $htmlBody>";

mente_mode() if(-e "./mente_lock");

# ロックをかける
if(!hakolock()) {
	# ロック失敗
	# ヘッダ出力
	tempHeader();

	# ロック失敗メッセージ
	tempLockFail();

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}

# 乱数の初期化
srand(time^$$);

# COOKIE読みこみ
cookieInput();

# CGI読みこみ
cgiInput();

# 島データの読みこみ
if(readIslandsFile($HcurrentID) == 0) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

# テンプレートを初期化
tempInitialize();

# COOKIE出力
cookieOutput();


if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
   $HmainMode eq 'commandJava' ||						# コマンド入力モード
   $HmainMode eq 'comment' && $HjavaMode eq 'java' ||	# コメント入力モード
   $HmainMode eq 'lbbs' && $HjavaMode eq 'java') {		# ローカルBBSモード

	$Body = "<BODY onload=\"init()\" $htmlBody>";
	require('hako-js.cgi');
	require('hako-map.cgi');

	# ヘッダ出力
	tempHeader();

	if($HmainMode eq 'commandJava') {
		# 開発モード
		commandJavaMain();
	} elsif($HmainMode eq 'comment') {
		# コメント入力モード
		commentMain();
	} elsif($HmainMode eq 'lbbs') {
		# ローカル掲示板モード
		localBbsMain();
	} else {
		ownerMain();
	}

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);

} elsif($HmainMode eq 'landmap') {
	require('hako-js.cgi');
	require('hako-map.cgi');
	$Body = "<BODY $htmlBody>";

	# ヘッダ出力
	tempHeader();
	# 観光モード
	printIslandJava();
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
} elsif($HmainMode ne "expView") {
	# ヘッダ出力
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ターン進行
	require('hako-turn.cgi');
	require('hako-top.cgi');
	turnMain();

} elsif($HmainMode eq 'new') {
	# 島の新規作成
	require('hako-turn.cgi');
	require('hako-map.cgi');
	newIslandMain();

} elsif($HmainMode eq 'print') {
	# 観光モード
	require('hako-map.cgi');
	printIslandMain();

} elsif($HmainMode eq 'owner') {

	# 開発モード
	require('hako-map.cgi');
	ownerMain();

} elsif($HmainMode eq 'command') {
	# コマンド入力モード
	require('hako-map.cgi');
	commandMain();

} elsif($HmainMode eq 'comment') {
	# コメント入力モード
	require('hako-map.cgi');
	commentMain();

} elsif($HmainMode eq 'lbbs') {
	# ローカル掲示板モード
	require('hako-map.cgi');
	localBbsMain();

} elsif($HmainMode eq 'change') {
	# 情報変更モード
	require('hako-turn.cgi');
	require('hako-top.cgi');
	changeMain();

} elsif($HmainMode eq 'FightView') {
	# LOGモード
	require('hako-map.cgi');
	FightViewMain();

} elsif($HmainMode eq 'FightIsland') {
	# 敗者の島表示
	require('hako-map.cgi');
	fight_map();

} elsif($HmainMode eq 'logView') {
	# LOGモード
	require('hako-top.cgi');
	logViewMain();

} elsif($HmainMode eq 'helpView') {
	# HELPモード
	require('hako-help.cgi');
	helpPageMain();

} elsif($HmainMode eq 'chartView') {
	# トーナメント表モード
	require('hako-chart.cgi');
	chartPageMain();

} elsif($HmainMode eq 'expView') {
	# expモード
	require('hako-help.cgi');
	expPageMain();

} else {
	# その他の場合はトップページモード
	require('hako-top.cgi');
	topPageMain();
}

# フッタ出力
tempFooter() if($HmainMode ne "expView");

# 終了
exit(0);

# コマンドを前にずらす
sub slideFront {
	my($command, $number) = @_;
	my($i);

	# それぞれずらす
	splice(@$command, $number, 1);

	# 最後に資金繰り
	$command->[$HcommandMax - 1] = {
		'kind' => $HcomDoNothing,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
		};
}

# コマンドを後にずらす
sub slideBack {
	my($command, $number) = @_;
	my($i);

	# それぞれずらす
	return if $number == $#$command;
	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# 島データ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readIslandsFile {
	my($num) = @_; # 0だと地形読みこまず
				   # -1だと全地形を読む
				   # 番号だとその島の地形だけは読みこむ

	# データファイルを開く
	if(!open(IN, "${HdirName}/hakojima.dat")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
		if(!open(IN, "${HdirName}/hakojima.dat")) {
			return 0;
		}
	}

	# 各パラメータの読みこみ
	$HislandTurn	 = int(<IN>); # ターン数
	$HislandLastTime = int(<IN>); # 最終更新時間

	if($HislandLastTime == 0) {
		return 0;
	}
	$HislandNumber		= int(<IN>);  # 島の総数
	$HislandNextID		= int(<IN>);  # 次に割り当てるID
	$HislandFightMode	= int(<IN>);  # 現在の戦闘モード
	$HislandChangeTurn	= int(<IN>);  # 切り替えターン
	$HislandFightCount	= int(<IN>);  # 何回戦目か
	$HislandTurnCount	= int(<IN>);  # ターン更新数
	$HislandChart		= <IN>;       # トーナメント表
	chomp($HislandChart);

	# ターン処理判定
	my($now) = time;
	if((($Hdebug == 1 and $HmainMode eq 'Hdebugturn') or 
		(($now - $HislandLastTime) >= $HunitTime) or ($HislandTurnCount > 1)) and $HislandNumber > 1) {
		$HmainMode = 'turn';
		$num = -1; # 全島読みこむ
	}

	# 島の読みこみ
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		 $Hislands[$i] = readIsland($num);
		 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}

	# ファイルを閉じる
	close(IN);

	return 1;
}

# 島ひとつ読みこみ
sub readIsland {
	my($num) = @_;
	my($name, $id, $prize, $absent, $comment, $password, $money, $food,
	   $pop, $area, $farm, $factory, $mountain, $score, $fire, $ownername, 
	   $fight_id, $reward, $missile, $log, $fly, $rest);
	$name = <IN>; # 島の名前
	chomp($name);
	if($name =~ s/,(.*)$//g) {
		$score = int($1);
	} else {
		$score = 0;
	}
	$id = int(<IN>);		# ID番号
	$prize = int(<IN>);		# 受賞
	$absent = int(<IN>);	# 連続資金繰り数
	$comment = <IN>;		# コメント
	chomp($comment);
	$password = <IN>;		# 暗号化パスワード
	chomp($password);
	$money = int(<IN>);		# 資金
	$food = int(<IN>);		# 食料
	$pop = int(<IN>);		# 人口
	$area = int(<IN>);		# 広さ
	$farm = int(<IN>);		# 農場
	$factory = int(<IN>);	# 工場
	$mountain = int(<IN>);	# 採掘場
	$fire = int(<IN>);		# ミサイル発射数
	$ownername = <IN>;		# オーナーネーム
	chomp($ownername);
	$fight_id = int(<IN>);	# 対戦相手ID
	$reward = int(<IN>);	# 報酬金用フラグ
	$missile = int(<IN>);	# 報酬金用フラグ２
	$log = int(<IN>);		# 施設破壊数
	$fly = int(<IN>);		# ミサイル飛来数
	$rest = int(<IN>);		# お休み期間

	# HidToNameテーブルへ保存
	$HidToName{$id} = $name;

	# 地形
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

		# コマンド
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

		# ローカル掲示板
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}

		close(IIN);
	}

	# 島型にして返す
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

# 全島データ書き込み
sub writeIslandsFile {
	my($num) = @_;

	# ファイルを開く
	open(OUT, ">${HdirName}/hakojima.tmp");

	# 各パラメータ書き込み
	print OUT "$HislandTurn\n";
	print OUT "$HislandLastTime\n";
	print OUT "$HislandNumber\n";
	print OUT "$HislandNextID\n";
	print OUT "$HislandFightMode\n";
	print OUT "$HislandChangeTurn\n";
	print OUT "$HislandFightCount\n";
	print OUT "$HislandTurnCount\n";
	print OUT "$HislandChart\n";

	# 島の書きこみ
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		 writeIsland($Hislands[$i], $num);
	}

	# ファイルを閉じる
	close(OUT);

	# 本来の名前にする
	unlink("${HdirName}/hakojima.dat");
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}

# 島ひとつ書き込み
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

	# 地形
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

		# コマンド
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

		# ローカル掲示板
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
# 入出力
#----------------------------------------------------------------------

# 標準出力への出力
sub out {
	print STDOUT jcode::sjis($_[0]);
}

# 対戦の記録ログ
sub Hfihgt_log {
	my $fight;

	# 回戦数数代入
	my $fTurn = $HislandFightCount;
	# 決勝戦の場合99にする
	$fTurn = 99 if($HislandNumber == 1);

	open(DOUT, ">$HdirName/fight.log.bak");
	print DOUT "<${fTurn}>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<tr><TH colspan=4></th><th $HbgTitleCell colspan=4>${HtagTH_}勝者${H_tagTH}</th><TH colspan=1></th>\n";
	print DOUT "<TH $HbgTitleCell colspan=3>${HtagTH_}敗者${H_tagTH}</th></tr>\n";
	print DOUT "<TR>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}勝者${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}敗者${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}飛来ミ数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>　</TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}報酬金${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊ミ基数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊防施数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>　</TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊ミ基数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊防施数${H_tagTH}</NOBR></TH>\n";
	print DOUT "</tr>\n";

	foreach $fight (@fight_log_flag) {
		my ($name,$tName,$reward,$log,$pop,$tLog,$tPop,$fly,$id) = split(",",$fight);
		$logD	= int($log / 1000)."機";
		$logM	= ($log - $logD * 1000)."機";
		$tLogD	= int($tLog / 1000)."機";
		$tLogM	= ($tLog - $tLogD * 1000)."機";
		$tName	= "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
					$HtagName2_.$tName."島".$H_tagName2."</A>";
		$tPop	.= ${HunitPop};
		if($id == -1) {
			$tName = "${HtagName2_}不戦勝${H_tagName2}";
			$tPop  = "−";
			$tLogM = "−";
			$tLogD = "−";
		}
		print DOUT "<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}島${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR>${tName}</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${fly}発</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>　</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${reward}${HunitMoney}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${pop}${HunitPop}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${logM}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${logD}</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>　</nobr></td>\n";
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

# 予選落ちログ
sub Hlog_yosen {
	my $yosen;
	open(DOUT, ">$HdirName/fight.log");
	print DOUT "<0>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<TR>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH></tr>";
	foreach $yosen (@yosen_log) {
		my ($pop,$name) = split(",",$yosen);
		print DOUT "<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}島${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td></tr>\n";
	}
	print DOUT "</TABLE>\n";
	close(DOUT);
}

# CGIの読みこみ
sub cgiInput {
	my($line, $getLine);

	# 入力を受け取って日本語コードをEUCに
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line = jcode::euc($line);
	$line =~ s/[\x00-\x1f\,]//g;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	# 対象の島
	if($line =~ /CommandButton([0-9]+)=/) {
		# コマンド送信ボタンの場合
		$HcurrentID = $1;
		$defaultID = $1;
	}

	if($line =~ /ISLANDNAME=([^\&]*)\&/){
		# 名前指定の場合
		$HcurrentName = cutColumn($1, 32);
	}

	if($line =~ /ISLANDID=([0-9]+)\&/){
		# その他の場合
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# パスワード
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

	# メッセージ
	if($line =~ /MESSAGE=([^\&]*)\&/) {
		$Hmessage = cutColumn($1, 80);
	}

	# ローカル掲示板
	if($line =~ /LBBSNAME=([^\&]*)\&/) {
		$HlbbsName = $1;
		$HdefaultName = $1;
	}
	if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
		$HlbbsMessage = cutColumn($1, 80);
	}

	# 画像のローカル設定MAC用
	if($line =~ /IMGLINEMAC=([^&]*)\&/){
		my($flag) = 'file:///' . $1;
		$HimgLine = $flag;
	}

	# 画像のローカル設定
	if($line =~ /IMGLINE=([^&]*)\&/){
		my($flag) = substr($1, 0 , -10);
		$flag =~ tr/\\/\//;
		if($flag eq 'del'){ $flag = $imageDir; } else { $flag = 'file:///' . $flag; }
		$HimgLine = $flag;
	}

	if($line =~ /OWNERNAME=([^\&]*)\&/){
		# オーナー名指定の場合
		$HownerName = cutColumn($1, 22);
	}

	if($line =~ /CommandJavaButton([0-9]+)=/) {
		# コマンド送信ボタンの場合（Ｊａｖａスクリプト）
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# 簡易観光者通信の場合
	if($line =~ /BBSMODE/) {
		$easy_mode = 1;
	}

	# main modeの取得
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
			# 観光者
			$HlbbsMode = 0;
			$HforID = $HcurrentID;
		} elsif($1 eq 'OW') {
			# 島主
			$HlbbsMode = 1;
		} else {
			# 削除
			$HlbbsMode = 2;
		}
		$HcurrentID = $2;

		# 削除かもしれないので、番号を取得
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

		# コマンドモードの場合、コマンドの取得
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


#cookie入力
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
		$HimgLine =~ s/筑集眺餅/デスクトップ/g;
	}
	if($cookie =~ /${HthisFile}JAVAMODE=\(([^\)]*)\)/) {
		$CjavaMode = $1;
	}

}

#cookie出力
sub cookieOutput {
	my($cookie, $info);

	# 消える期限の設定
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
		gmtime(time + 30 * 86400); # 現在 + 30日

	# 2ケタ化
	$year += 1900;
	if ($date < 10) { $date = "0$date"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min < 10) { $min  = "0$min"; }
	if ($sec < 10) { $sec  = "0$sec"; }

	# 曜日を文字に
	$day = ("Sunday", "Monday", "Tuesday", "Wednesday",
			"Thursday", "Friday", "Saturday")[$day];

	# 月を文字に
	$mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

	# パスと期限のセット
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
		# 自動系以外
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
# ユーティリティ
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# rename式ロック
		return hakolock1();

	} elsif($lockMode == 2) {
		# flock式ロック
		return hakolock2();
	}
}

sub hakolock1 {
	# ロックを試す
	$lfh = file_lock() or die return 0;
	return 1;
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# 成功
		return 1;
	} else {
		# 失敗
		return 0;
	}
}

# ロックを外す
sub unlock {
	if($lockMode == 1) {
		# rename式ロック
		rename($lfh->{current}, $lfh->{path});
	} elsif($lockMode == 2) {
		# flock式ロック
		close(LOCKID);

	}
}

# 新ロック方式
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

# 小さい方を返す
sub min {
	return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# パスワードエンコード
sub encode {
	if($cryptOn == 1) {
		return crypt($_[0], 'h2');
	} else {
		return $_[0];
	}
}

# パスワードチェック
sub checkPassword {
	my($p1, $p2) = @_;
	$p1 =~ s/\r|\n//;

	# nullチェック
	if($p2 eq '') {
		return 0;
	}

	# マスターパスワードチェック
	if($masterPassword eq $p2) {
		return 1;
	}

	# 本来のチェック
	if($p1 eq encode($p2)) {
		return 1;
	}

	return 0;
}

# 1000人単位丸めルーチン
sub aboutPop {
	my($p) = @_;
	if($p < 500) {
		return "推定5万人以下";
	} else {
		$p = int(($p + 250) / 500) * 5;
		return "推定".$p."万人";
	}
}

# 1000億単位丸めルーチン
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "推定500${HunitMoney}未満";
	} else {
		$m = int(($m + 500) / 1000);
		return "推定${m}000${HunitMoney}";
	}
}

# 1000億単位丸めルーチン　島力計算用
sub aboutMoney2 {
	my($m) = @_;
	if($m < 500) {
		return 500;
	} else {
		$m = int(($m + 500) / 1000);
		return $m;
	}
}

# エスケープ文字の処理
sub htmlEscape {
	my($s) = @_;
	$s =~ s/&/&amp;/g;
	$s =~ s/</&lt;/g;
	$s =~ s/>/&gt;/g;
	$s =~ s/\"/&quot;/g; #"
	return $s;
}

# 80ケタに切り揃え
sub cutColumn {
	my($s, $c) = @_;
	if(length($s) <= $c) {
		return $s;
	} else {
		# 合計80ケタになるまで切り取り
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

# 島の名前から番号を得る(IDじゃなくて番号)
sub nameToNumber {
	my($name) = @_;

	# 全島から探す
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'name'} eq $name) {
			return $i;
		}
	}

	# 見つからなかった場合
	return -1;
}

# 経験地からレベルを算出
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if($kind == $HlandBase) {
		# ミサイル基地
		for($i = $maxBaseLevel; $i > 1; $i--) {
			if($exp >= $baseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	}
}

# (0,0)から(size - 1, size - 1)までの数字が一回づつ出てくるように
# (@Hrpx, @Hrpy)を設定
sub makeRandomPointArray {
	# 初期値
	my($y);
	@Hrpx = (0..$HislandSize-1) x $HislandSize;
	for($y = 0; $y < $HislandSize; $y++) {
		push(@Hrpy, ($y) x $HislandSize);
	}

	# シャッフル
	my ($i);
	for ($i = $HpointNumber; --$i; ) {
		my($j) = int(rand($i+1)); 
		if($i == $j) { next; }
		@Hrpx[$i,$j] = @Hrpx[$j,$i];
		@Hrpy[$i,$j] = @Hrpy[$j,$i];
	}
}

# 0から(n - 1)の乱数
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
# ログ表示
#----------------------------------------------------------------------
# ファイル番号指定でログ表示
sub logFilePrint {
	my($fileNumber, $id, $mode, $kankou) = @_;
	open(LIN, "${HdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	my($fi) = 0;

	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# 機密関係
		if($m == 1) {
			if(($mode == 0) || ($id1 != $id)) {
				# 機密表示権利なし
				next;
			}
			$m = '<B>(機密)</B>';
		} elsif($m == 2 and !$id) {
			next;
		} else {
			$m = '';
		}

		# 表示的確か
		if($id != 0) {
			if(($id != $id1) &&
			   ($id != $id2)) {
				next;
			}
		}
		next if($id and $id2 and $id != $id2 and $Hmissile_log);

		# 表示
		if($kankou == 1) {
			out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
		} elsif(($fi == 0) && ($mode == 0)) {
			out("<NOBR><BR><B><I><FONT COLOR='#000000' SIZE=+2>ターン$turn$m：</FONT></I></B><BR><HR width=50% align=left>\n");
			out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
			$fi++;
		} else {
			out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
		}
	}

	close(LIN);
}

#----------------------------------------------------------------------
# テンプレート
#----------------------------------------------------------------------
# 初期化
sub tempInitialize {
	# 島セレクト(デフォルト自分)
	$HislandList = getIslandList($defaultID);
}

# 島データのプルダウンメニュー用
sub getIslandList {
	my($select,$mode,$target) = @_;
	my($list, $name, $id, $s, $i);

	#島リストのメニュー
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
			"<OPTION VALUE=\"$id\" $s>${name}島\n";
	}
	return $list;
}

# ロック失敗
sub tempLockFail {
	# タイトル
	out(<<END);
${HtagBig_}同時アクセスエラーです。<BR>
ブラウザの「戻る」ボタンを押し、<BR>
しばらく待ってから再度お試し下さい。${H_tagBig}$HtempBack
END
}

# 強制解除
sub tempUnlock {
	# タイトル
	out(<<END);
${HtagBig_}前回のアクセスが異常終了だったようです。<BR>
ロックを強制解除しました。${H_tagBig}$HtempBack
END
}

# hakojima.datがない
sub tempNoDataFile {
	out(<<END);
${HtagBig_}データファイルが開けません。<BR>
管理者が気が付くまで暫くお待ち下さい。${H_tagBig}$HtempBack
END
}

# パスワード間違い
sub tempWrongPassword {
	out(<<END);
${HtagBig_}パスワードが違います。${H_tagBig}$HtempBack
<SCRIPT LANGUAGE="JavaScript">
<!--
function init() {}
//-->
</SCRIPT>
END
}

# 何か問題発生
sub tempProblem {
	out(<<END);
${HtagBig_}問題発生、とりあえず戻ってください。${H_tagBig}$HtempBack
END
}

# メンテナンス中
sub mente_mode {
	# ヘッダ出力
	tempHeader();

	# メッセージ
	out("${HtagBig_}只今メンテナンス中です。<BR>暫くお待ち下さい。${H_tagBig}");

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}
