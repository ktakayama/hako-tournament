#!/usr/bin/perl
# ↑はサーバーに合わせて変更して下さい。

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メンテナンスツール(ver1.01)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# メンテナンスツール
# $Id: hako-mente.cgi,v 1.1 2003/05/15 02:08:55 gaba Exp $

require ('hako-ini.cgi');

# このファイル
my($thisFile) = './hako-mente.cgi';

# use Time::Localが使えない環境では、'use Time::Local'の行を消して下さい。
# ただし、更新時間の変更が'秒指定で変更'しかできなくなります。
use Time::Local;

# ――――――――――――――――――――――――――――――
# 設定項目は以上
# ――――――――――――――――――――――――――――――

# 各種変数
my($mainMode);
my($inputPass);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

print <<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>箱島２ メンテナンスツール</TITLE>
</HEAD>
<BODY>
END

cgiInput();

if($mainMode eq 'delete') {
	deleteMode() if(passCheck());
} elsif($mainMode eq 'current') {
	currentMode() if(passCheck());
} elsif($mainMode eq 'time') {
	timeMode() if(passCheck());
} elsif($mainMode eq 'stime') {
	stimeMode() if(passCheck());
} elsif($mainMode eq 'new') {
	newMode() if(passCheck());
} elsif($mainMode eq 'mente') {
	menteMode() if(passCheck());
} elsif($mainMode eq 'unmente') {
	unmenteMode() if(passCheck());
}
mainMode();

print <<END;
</FORM>
</BODY>
</HTML>
END

sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	} 
	closedir(DIN);
	rmdir($dn);
}

sub currentMode {
	myrmtree "${HdirName}";
	mkdir("${HdirName}", $HdirMode);
	opendir(DIN, "${HdirName}.bak$currentID/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
	} 
	closedir(DIN);
}

sub deleteMode {
	if($deleteID eq '') {
		myrmtree "${HdirName}";
	} else {
		myrmtree "${HdirName}.bak$deleteID";
	}
	unlink "hakojimalockflock";
}

sub newMode {
	mkdir($HdirName, $HdirMode);
    mkdir($Hdirfdata, $HdirMode);
    mkdir($Hdirmdata, $HdirMode);
    mkdir($Hdiraccess, $HdirMode);

	# 現在の時間を取得
	my($now) = time;
	$now = $now - ($now % ($HunitTime));

	open(OUT, ">$HdirName/hakojima.dat"); # ファイルを開く
	print OUT "0\n";		 # ターン数1
	print OUT "$now\n";	 	 # 開始時間
	print OUT "0\n";		 # 島の数
	print OUT "1\n";		 # 次に割り当てるID
	print OUT "0\n";		 # 現在の戦闘モード
	print OUT ($HyosenTurn+$HdevelopeTurn)."\n";		 # 切り替えターン
	print OUT "1\n";		 # 何回戦目か
	print OUT "1\n";		 # ターン更新数

	# ファイルを閉じる
	close(OUT);
}

sub timeMode {
	$ctMon--;
	$ctYear -= 1900;
	$ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
	stimeMode();
}

sub stimeMode {
	my($t) = $ctSec;
	open(IN, "${HdirName}/hakojima.dat");
	my(@lines);
	@lines = <IN>;
	close(IN);

	$lines[1] = "$t\n";

	open(OUT, ">${HdirName}/hakojima.dat");
	print OUT @lines;
	close(OUT);
}

sub mainMode {
	opendir(DIN, "./");

	print <<END;
<FORM action="$thisFile" method="POST">
<H1>箱島２ メンテナンスツール</H1>
<B>パスワード:</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD>
<BR><BR>
END

	# 現役データ
	if(-d "${HdirName}") {
		if(-e "./mente_lock") {
			print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード解除" NAME="UNMENTE">\n#;
		} else {
			print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード" NAME="MENTE">\n#;
		}
		dataPrint("");
	} else {
		print <<END;
	<HR>
	<INPUT TYPE="submit" VALUE="新しいデータを作る" NAME="NEW">
END
	}

	# バックアップデータ
	my($dn);
	while($dn = readdir(DIN)) {
		if($dn =~ /^${HdirName}.bak(.*)/) {
			dataPrint($1);
		}
	} 
	closedir(DIN);
}

# 表示モード
sub dataPrint {
	my($suf) = @_;

	print "<HR>";
	if($suf eq "") {
		open(IN, "${HdirName}/hakojima.dat");
		print "<H1>現役データ</H1>";
	} else {
		open(IN, "${HdirName}.bak$suf/hakojima.dat");
		print "<H1>バックアップ$suf</H1>";
	}

	my($lastTurn);
	$lastTurn = <IN>;
	my($lastTime);
	$lastTime = <IN>;

	my($timeString) = timeToString($lastTime);

	print <<END;
	<B>ターン$lastTurn</B><BR>
	<B>最終更新時間</B>:$timeString<BR>
	<B>最終更新時間(秒数表示)</B>:1970年1月1日から$lastTime 秒<BR>
	<INPUT TYPE="submit" VALUE="このデータを削除" NAME="DELETE$suf">
END

	if($suf eq "") {
		my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
			localtime($lastTime);
		$mon++;
		$year += 1900;

		print <<END;
	<H2>最終更新時間の変更</H2>
	<INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">年
	<INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">月
	<INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">日
	<INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">時
	<INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">分
	<INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">秒
	<INPUT TYPE="submit" VALUE="変更" NAME="NTIME"><BR>
	1970年1月1日から<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">秒
	<INPUT TYPE="submit" VALUE="秒指定で変更" NAME="STIME">

END
	} else {
		print <<END;
		<INPUT TYPE="submit" VALUE="このデータを現役に" NAME="CURRENT$suf">
END
	}
}

sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
		localtime($_[0]);
	$mon++;
	$year += 1900;

	return "${year}年 ${mon}月 ${date}日 ${hour}時 ${min}分 ${sec}秒";
}

# CGIの読みこみ
sub cgiInput {
	my($line);

	# 入力を受け取る
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	if($line =~ /DELETE([0-9]*)/) {
		$mainMode = 'delete';
		$deleteID = $1;
	} elsif($line =~ /CURRENT([0-9]*)/) {
		$mainMode = 'current';
		$currentID = $1;
	} elsif($line =~ /NEW/) {
		$mainMode = 'new';
	} elsif($line =~ /UNMENTE/) {
		$mainMode = 'unmente';
	} elsif($line =~ /MENTE/) {
		$mainMode = 'mente';
	} elsif($line =~ /NTIME/) {
		$mainMode = 'time';
		if($line =~ /YEAR=([0-9]*)/) {
			$ctYear = $1; 
		}
		if($line =~ /MON=([0-9]*)/) {
			$ctMon = $1; 
		}
		if($line =~ /DATE=([0-9]*)/) {
			$ctDate = $1; 
		}
		if($line =~ /HOUR=([0-9]*)/) {
			$ctHour = $1; 
		}
		if($line =~ /MIN=([0-9]*)/) {
			$ctMin = $1; 
		}
		if($line =~ /NSEC=([0-9]*)/) {
			$ctSec = $1; 
		}
	} elsif($line =~ /STIME/) {
		$mainMode = 'stime';
		if($line =~ /SSEC=([0-9]*)/) {
			$ctSec = $1; 
		}
	}

	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$inputPass = $1;
	}
}

# ファイルのコピー
sub fileCopy {
	my($src, $dist) = @_;
	open(IN, $src);
	open(OUT, ">$dist");
	while(<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);
}

# パスチェック
sub passCheck {
	if($inputPass eq $masterPassword) {
		return 1;
	} else {
		print <<END;
   <FONT SIZE=7>パスワードが違います。</FONT>
END
		return 0;
	}
}

# メンテナンスモード
sub menteMode {
    mkdir("./mente_lock", $HdirMode);
}

# メンテモード解除
sub unmenteMode {
	rmdir("./mente_lock");
}

1;
