#! /usr/bin/perl

# ============================================================= #
#                                                               #
#   アクセスログ解析ツール                                      #
#   鷹の島 (http://espion.just-size.jp/)                        #
#   Kyosuke Takayama (support@mc.neweb.ne.jp)                   #
#                                                               #
#                                                               #
# ============================================================= #
# $Id: access.cgi,v 1.3 2004/06/03 01:59:14 gaba Exp $

use strict;

# スクリプト名
my $script = "access.cgi";

# パスワード
my $passwd = "pass";

# アクセスログディレクトリ名
my $data_dir = "./access_log";

# 観光画面表示用のリンク
my $hako_link = "./hako-main.cgi?Sight=";

# -- 設定ここまで --------------------------------------------- #

my (@log, @dir_list);
my %Q;
my $dir_flag;
my $i = 0;

my($sec, $min, $hour, $day, $month, $Year, $wday, $isdst) = localtime;
$month ++;
$Q{file} = "${month}-${day}.cgi";

decode();

if(pass_check()) {
	html_header();
	read_data_dir();
	read_data_file();
	data_sort();

	html_form();
	html_data();
	html_footer();
}


# -- フォームからのデータ処理 --------------------------------- #
sub decode {
	my ($buffer, $i);

	return if($ENV{'CONTENT_LENGTH'} > 51200);
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

	foreach (split(/&/,$buffer)) {
		my($name, $value) = split(/=/);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;

		$Q{$name} = $value;
		last if($i > 200 and $i++);
	}
}

# -- パスワードチェック --------------------------------------- #
sub pass_check {

	return 1 if($Q{pass} eq $passwd);

	html_pass_form();
	return 0;
}

# -- アクセスログデータ読み込み ------------------------------- #
sub read_data_file {
	my $file;
	$file = $Q{file} if($Q{file} and $dir_flag);

	open(IN, "${data_dir}/${file}");
	foreach (<IN>) {
		($log[$i]->{time},
		 $log[$i]->{ip2},
		 $log[$i]->{xip},
		 $log[$i]->{id},
		 $log[$i]->{name},
		 $log[$i]->{type},
		 $log[$i]->{agent}
		) = split(/,/);

		$log[$i]->{ip} = $log[$i]->{ip2};
		$log[$i]->{ip2} =~ s/([\d\.]*)(\.[\d]*)/$1/g if($Q{last});
		$log[$i]->{ip2} =~ s/\.//g unless($Q{last});
		$i++;
	}
	close(IN);

}

# -- データディレクトリ読み込み ------------------------------- #
sub read_data_dir {
	my $dir;

	opendir(DIR, "${data_dir}");
	while ($dir = readdir(DIR)) {
		push (@dir_list, $dir) if($dir =~ /[\d]*-[\d]*\.cgi/);
		$dir_flag = 1 if($dir eq $Q{file});
	}
	closedir(DIR);

}

# -- データソート---------------------------------------------- #
sub data_sort {
	my @idx = (0..$#log);

	if($Q{type} == 0) {
		@idx = sort { $log[$a]->{ip2} <=> $log[$b]->{ip2} || $log[$a]->{time} <=> $log[$b]->{time} } @idx;
	} elsif($Q{type} == 1) {
		@idx = sort { $log[$a]->{time} <=> $log[$b]->{time} || $log[$a]->{id} <=> $log[$b]->{id} } @idx;
	}
	@log = @log[@idx];
}

# -- HTMLヘッダ ----------------------------------------------- #
sub html_header {

	print "Content-type: text/html\n\n";
	print <<_HTML_;
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="ja">
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=euc-jp">
<TITLE>アクセスログ</TITLE>
</HEAD>
<BODY ALINK="#000000" VLINK="#000000" LINK="#000000">
_HTML_

}

# -- HTMLフッタ ----------------------------------------------- #
sub html_footer {

	print <<_HTML_;
<HR>
<DIV ALIGN="RIGHT">
<A HREF="http://espion.just-size.jp/">鷹の島</A></DIV>
</BODY>
</HTML>
_HTML_

}

# -- パスワード入力フォーム ----------------------------------- #
sub html_pass_form {

	print "Content-type: text/html\n\n";
	print <<_HTML_;
<FORM ACTION="${script}" METHOD="POST">
<INPUT TYPE="PASSWORD" NAME="pass">
<INPUT TYPE="SUBMIT" VALUE="入室">
</FORM>
_HTML_

}

# -- HTMLフォーム --------------------------------------------- #
sub html_form {
	@dir_list = reverse (@dir_list);
	my @type;
	my $ch_all = ($Q{all}) ? " CHECKED" : "";
	my $ch_last = ($Q{last}) ? " CHECKED" : "";
	$type[$Q{type}] = " CHECKED";

	print <<_HTML_;
<FORM ACTION="${script}" METHOD="POST">
<SELECT NAME="file">
_HTML_

	foreach (@dir_list) {
		print "<OPTION VALUE='";
		print;
		print "'";
		print " selected" if($Q{file} eq $_);
		print ">";
		print;
		print "\n";
	}

	print <<_HTML_;
</SELECT>
<INPUT TYPE="CHECKBOX" NAME="all"${ch_all}>全て表示
<INPUT TYPE="CHECKBOX" NAME="last"${ch_last}>IPカット
<BR>
<INPUT TYPE="RADIO" NAME="type" VALUE="0"$type[0]>標準
<INPUT TYPE="RADIO" NAME="type" VALUE="1"$type[1]>時間順　　　　　
<INPUT TYPE="HIDDEN" NAME="pass" VALUE="$Q{pass}">
<INPUT TYPE="SUBMIT" VALUE="送信">
</FORM>
<HR>
_HTML_

}

# -- アクセスログデータ表示 ----------------------------------- #
sub html_data {
	my ($id_flag, $ip_flag);
	my $flag = 1;

	print <<_HTML_;
<TABLE BORDER>
<TR BGCOLOR="#999999">
<TH>TIME</TH>
<TH>IP</TH>
<TH>XIP</TH>
<TH>NAME</TH>
<TH>TYPE</TH>
<TH>AGENT</TH>
</TR>
_HTML_

	foreach (0..$#log) {
		my $tmp;
		my $as = $log[$_];
		if($ip_flag ne $as->{ip2} and $id_flag ne $as->{id}) {
			$flag = ($flag) ? 0 : 1;
		} elsif ($id_flag ne $as->{id}) {
			$tmp = 1;
		} elsif(!$Q{all} and $ip_flag eq $as->{ip2} and $id_flag eq $as->{id}) {
			next;
		}
		$id_flag = $as->{id};
		$ip_flag = $as->{ip2};
		if($tmp) {
			print "<TR bgcolor=#9999FF>";
		} elsif($flag) {
			print "<TR bgcolor=#BBBBBB>";
		} else {
			print "<TR>";
		}

		my($sec,$min,$hou,$day,$mon,$year,$wday) = localtime($as->{time});
		$hou = "0$hou" if($hou < 10);
		$min = "0$min" if($min < 10);
		$sec = "0$sec" if($sec < 10);

		$as->{id} =~ s/ //;
		my $link = qq|<A HREF="${hako_link}$as->{id}" target="_blank">$as->{name}</A>|;

		print <<_HTML_;
<TD> $hou:$min:$sec
<TD> $as->{ip}
<TD> $as->{xip}
<TD> $link
<TD> $as->{type}
<TD> $as->{agent}
</TR>
_HTML_

	}

	print "</TABLE>";
}


