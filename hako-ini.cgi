#----------------------------------------------------------------------
# 箱庭トーナメント２
# 設定ファイル
# $Id$

#----------------------------------------------------------------------
# 各種設定値
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下、必ず設定する部分
#----------------------------------------------------------------------

# このファイルを置くディレクトリ  最後にスラッシュ(/)は付けない。
$baseDir = 'http://www.hako.com';

# 画像ファイルを置くディレクトリ
$imageDir	= 'http://www.hako.com/img';

$toppage 	= 'http://www.hako.com/';			# ホームページのアドレス
$bbsname 	= '掲示板';							# 掲示板の名称
$bbs		= 'http://www.hako.com/bbs/';		# 掲示板アドレス
$bbsLog		= './bbs/log.dat';					# 掲示板のログファイル名
$imageExp	= 'http://www.hako.com/imgexp/';	# 画像のローカル設定の説明ページ

$jcode				= './jcode.pl';				# jcode.plの位置
$masterPassword		= 'master';					# マスターパスワード
$HspecialPassword	= 'special';				# 特殊パスワード
$adminName			= '管理者の名前';			# 管理者名
$email				= '管理者@どこ.どこ.どこ';	# 管理者のメールアドレス
$version			= "0.97";					# バージョン表記用（基本的に変更しないように！）

$HdirMode			= 0755;						# データディレクトリのパーミッション
$HdirName			= 'data';					# データディレクトリの名前
$Hdirfdata			= 'fdata';					# 対戦の記録保持ディレクトリ
$Hdirmdata			= 'mdata';					# 戦闘開始時の島データ
$Hdiraccess			= 'access_log';				# アクセスログ保持ディレクトリ

# データの書き込み方
# ロックの方式
# 1 ファイルリネーム（注）
# 2 システムコール(可能ならば最も望ましい)
$lockMode = 1;

# (注)
# 1を選択する場合には、'lockfile'という、パーミション666の空のファイルを、
# このファイルと同位置に置いて下さい。

#----------------------------------------------------------------------
# 必ず設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下、好みによって設定する部分
#----------------------------------------------------------------------
#----------------------------------------
# ゲームの進行やファイルなど
#----------------------------------------
$unlockTime		= 90;		# 異常終了基準時間(ロック後何秒で、強制解除するか)
$HlogMax		= 8;		# ログファイル保持ターン数
$HhistoryMax	= 10;		# 発見ログ保持行数
$HbackupTurn	= 3;		# バックアップを何ターンおきに取るか
$HbackupTimes	= 3;		# バックアップを何回分残すか
$HgiveupTurn	= 15;		# 放棄コマンド自動入力ターン数
$HcommandMax	= 30;		# コマンド入力限界数
$HislandSize	= 12;		# 島の大きさ
$HuseLbbs		= 1;		# ローカル掲示板を使用するかどうか(0:使用しない)
$HlbbsMax		= 10;		# ローカル掲示板保存行数
$HlbbsView		= 5;		# ローカル掲示板、通常観光画面で表示する行数（HlbbsMaxより小さくする事）
$Htop_blank		= 0;		# トップから島名クリックで新しい画面で表示(0:同じ画面　1:新しい画面)
$cryptOn		= 1;		# パスワードの暗号化(1だと暗号化する)
$Hdebug			= 0;		# デバッグモード(1だと、「ターンを進める」ボタンが使用できる)
$Hmobile		= 0;		# 携帯画面テスト用(1だと、強制的に携帯用の画面表示)
$Htime_mode		= 0;		# 次回更新までの日時が表示されない場合はここを1にして下さい
$Hmissile_log	= 0;		# ミサイル発射のログを簡略化表示する（0:しない 1:設定する）

# 報酬金設定　（最後に荒地(ミサイル跡)代を足すのは全て共通）
# ここに書いてある数字以外にするとわけわからん事になります
# 1: (双方のミサイル基地の数 + 双方の防衛施設の数 * 2) / 2 * 自分の戦闘行為回数 * 15
# 2: 壊された施設の代金（農場・工場・ミサイル基地・防衛施設）完全回収型
# 相手の強さにより ＊予定　設定しないで下さい
# 相対的な強さ　　 ＊予定　設定しないで下さい
$HrewardMode	= 1;

# 対戦相手決定方式
# 0: (デフォルト) 島力と言う島の強さを判定する方式
# 1: トーナメント表を使った方式 最初の対戦相手決定のみ島力を計算 (不戦勝が出ると、正しく動作しません)
# 完全なランダム   ＊予定 設定しないで下さい
$Htournament	= 0;

#----------------------------------------
# 更新時間や、島数
#----------------------------------------
$HmaxIsland		= 100;		# 島の最大数
$HfightMem 		= 32;		# 予選後通過島数（2のべき乗にするべき）
$HyosenTurn		= 48;		# 予選期間ターン数（0にしないで下さい）
$HdevelopeTurn	= 24;		# 開発期間ターン数
$HfightTurn		= 12;		# 戦闘期間ターン数
$HunitTime		= 43200;	# 予選期間更新時間(3600秒＝1時間)
$HdevelopeTime	= 7200;		# 開発期間更新時間 # 2時間
$HfightTime		= 86400;	# 戦闘期間更新時間 # 24時間
$HinterTime		= 93600;	# 戦闘期間終了後の開発期間への移行までの時間
$HyosenRepCount	= 3;		# 予選期間一回に更新するターン数(例えば３にするとまとめて３ターン進む)
$HdeveRepCount	= 1;		# 開発期間一回に更新するターン数
$HfightRepCount	= 3;		# 戦闘期間一回に更新するターン数
$HstopAddPop	= 3;		# 人口増加ストップする資金繰り回数
$do_fight		= 3;		# 不戦勝にならないための、必要戦闘行為回数

# 不戦勝の開発停止ターン数
$HnofightTurn	= 12;		# 基本値
$HnofightUp		= 4;		# 上の数値　＋ この数値×回戦数となります

#----------------------------------------
# 資金、食料などの設定値と単位
#----------------------------------------
$HinitialMoney		= 2000;		# 初期資金
$HinitialFood		= 1000;		# 初期食料
$HlandSizeValue		= 32;		# 初期面積
$HseaNum			= 20;		# 初期浅瀬の数
$HunitMoney			= '億円';	# お金の単位
$HunitFood			= '00トン';	# 食料の単位
$HunitPop			= '00人';	# 人口の単位
$HunitArea			= '00万坪';	# 広さの単位
$HunitTree			= '00本';	# 木の数の単位
$HtreeValue			= 5;		# 木の単位当たりの売値
$HtreeUp			= 2;		# １ターンで木の増える本数
$HtownUp			= 10;		# 人口の増加幅（10だと最大1000人）
$HeatenFood			= 0.2;		# 人口1単位あたりの食料消費料
$HtownGlow			= 25;		# 村の発生率（％）
$Hno_work			= 500;		# 失業者数のボーダーライン（10だと1000人）
								# この数値を超えると、人口増加がストップします（予選のみ）
$HcostChangeName	= 0;		# 名前変更のコスト
$HdefenceValue		= 400;		# 防衛施設の売却値

# 一括自動地ならし用
$precheap			= 10;		# 何個目の荒地から割り引きか（この数の次の荒地から）
$precheap2			= 8;		# その際の割引率（8にしたら、2割引ということになります）

#----------------------------------------
# 偽装設定（都市以外は森で偽装）
#----------------------------------------
$HhideMoneyMode		= 2;		# 資金の表示(0:見えない　1: 見える　2:100の位で四捨五入)
$Hhide_missile		= 1;		# ミサイル基地　0:しない　1:する
$Hhide_deffence		= 1;		# 防衛施設　0:しない　1:する
$Hhide_town			= 0;		# 都市系　0:しない　1:する
$Hhide_farm			= 0;		# 農場　0:しない　1:する　2:規模も隠蔽
$Hhide_factory		= 0;		# 工場　0:しない　1:する　2:規模も隠蔽

#----------------------------------------
# 特殊設定（詳しい説明はreadmeで）
#----------------------------------------
# 0:設定しない　1:設定する
$HeasyReclaim		= 0;		# 埋め立ての簡易化

#----------------------------------------
# 基地の経験値
#----------------------------------------
$HmaxExpPoint	= 200;		# 経験値の最大値(最大255)
$maxBaseLevel	= 5;		# ミサイル基地　レベルの最大値
@baseLevelUp	= (20, 60, 120, 200);	# 経験値

#----------------------------------------
# 災害
#----------------------------------------
# 地盤沈下発生率(確率は0.1%単位)
$HdisFallBorder	= 90;	# 安全限界の広さ(Hex数)
$HdisFalldown	= 30;	# その広さを超えた場合の確率

#----------------------------------------
# 賞関係
#----------------------------------------
# 賞の名前
$Hprize[0] = 'ターン杯';
$Hprize[1] = '繁栄賞';
$Hprize[2] = '超繁栄賞';
$Hprize[3] = '究極繁栄賞';
$Hprize[4] = '平和賞';
$Hprize[5] = '超平和賞';
$Hprize[6] = '究極平和賞';
$Hprize[7] = '災難賞';
$Hprize[8] = '超災難賞';
$Hprize[9] = '究極災難賞';

#----------------------------------------
# 外見関係等
#----------------------------------------
$htmlBody	= 'BGCOLOR="#EEFFFF"';		# <BODY>タグのオプション
$Htitle		= '箱庭トーナメント２';		# ゲームのタイトル文字

# タグ
# タイトル文字
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# 何回戦目
$HtagFico_ = '<FONT SIZE="7" COLOR="#4444ff">';
$H_tagFico = '</FONT>';

# H1タグ用
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# 大きい文字
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# 島の名前など
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# 薄くなった島の名前
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# 順位の番号など
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# 順位表における見だし
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# 開発計画の名前
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# 災害
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';

# ローカル掲示板、島無し観光者の書いた文字
$HtagLbbsSK_ = '<FONT COLOR="#003333"><B>';
$H_tagLbbsSK = '</B></FONT>';

# 通常の文字色(これだけでなく、BODYタグのオプションもちゃんと変更すべし
$HnormalColor = '#000000';

# 順位表、セルの属性
$HbgTitleCell   = 'BGCOLOR="#ccffcc"';	# 順位表見出し
$HbgNumberCell  = 'BGCOLOR="#ccffcc"';	# 順位表順位
$HbgNameCell	= 'BGCOLOR="#ccffff"';	# 順位表島の名前
$HbgInfoCell	= 'BGCOLOR="#ccffff"';	# 順位表島の情報
$HbgCommentCell = 'BGCOLOR="#ccffcc"';	# 順位表コメント欄
$HbgInputCell   = 'BGCOLOR="#ccffcc"';	# 開発計画フォーム
$HbgMapCell		= 'BGCOLOR="#ccffcc"';	# 開発計画地図
$HbgCommandCell = 'BGCOLOR="#ccffcc"';	# 開発計画入力済み計画

# 予選用落ちレッドライン
$YbgNumberCell  = 'BGCOLOR="#F0BBDA"'; # 順位表順位
$YbgNameCell    = 'BGCOLOR="#E4CCF5"'; # 順位表島の名前
$YbgInfoCell    = 'BGCOLOR="#E4CCF5"'; # 順位表島の情報
$YbgCommentCell = 'BGCOLOR="#F0BBDA"'; # 順位表コメント欄

#----------------------------------------
# ヘッダー　フッター
#----------------------------------------
# ヘッダ
sub tempHeader {

	my($HimgFlag) = 0;
	if($HimgLine eq '' || $HimgLine eq $imageDir){
		$baseIMG = $imageDir;
		$HimgFlag = 1;
	} else {
		$baseIMG = $HimgLine;
	}
	$baseIMG =~ s/筑集眺餅/デスクトップ/g;

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
　<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">箱庭諸島スクリプト配布元</A>
 / <A HREF="http://appoh.execweb.cx/hakoniwa/" target=_blank>箱庭Javaスクリプト版 配布元</A>
 / <A HREF="http://espion.just-size.jp/archives/dist_hako/" target=_blank>箱庭トーナメント２ 配布元</A>
 / <A HREF="http://espion.just-size.jp/files/link/link.cgi" target=_blank>箱庭トーナメントリンク集</A>
<B><BR>
<A HREF="$toppage">トップページ</A>
 / <A HREF="$bbs">$bbsname</A>$bbTime
 / <A HREF="$HthisFile?LogFileView=1" target=_blank>最近の出来事</A>
 / <A HREF="$HthisFile?help=1">設定一覧</A>
 / <A HREF="$HthisFile?exp=1" target=_blank>マニュアル</A>
 / <A HREF="$baseDir/hako-main.cgi">戻る</A>
</B>
</nobr>
<HR>
END
		if($HimgFlag) {
			out("<FONT COLOR=RED>サーバー負荷軽減の為に、画像のローカル設定を行って下さるようにお願い致します。</FONT><HR>");
		}
	} else {
       out(<<END);
<HTML>
<HEAD>
<TITLE>$Htitle</TITLE>
</HEAD>
<BODY bgcolor="#ffffff">
<a href="./hako-main.cgi">トップ</a> <a href="./hako-main.cgi?help=1">ヘルプ</a> <a href="./hako-main.cgi?exp=1">リンク</a>
<hr>
END
    }
}

# フッタ
sub tempFooter {
	if($Hmobile == 0) {
		out(<<END);
<HR>
<P align=right>
<NOBR>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html" target=_blank>箱庭諸島スクリプト配布元</A>
　　<A HREF="$toppage">トップページ</A>
　　<A HREF="$bbs">$bbsname</A>
　　<A HREF="$HthisFile?LogFileView=1" target=_blank>最近の出来事</A>
</nobr><BR><BR>
管理者:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
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
