#----------------------------------------------------------------------
# 箱庭トーナメント２
# ヘルプモジュール
# $Id$

#----------------------------------------------------------------------
# ヘルプページモード
#----------------------------------------------------------------------
# メイン
sub helpPageMain {
	# 開放
	unlock();

	# テンプレート出力
	tempHelpPage();
}


sub tempHelpPage {

	# データの表示用設定
	my($yosrep,$devrep,$firep);
	my($unit) = $HunitTime / 3600;
	my($deve) = $HdevelopeTime / 3600;
	my($fiunit) = $HfightTime / 3600;
	my($inter) = $HinterTime / 3600;
	$HdisFalldown /= 10;
	$HdisFallBorder++;

	$yosrep = '（' . $HyosenRepCount . 'ターンまとめて更新）' if($HyosenRepCount > 1);
	$devrep = '（' . $HdeveRepCount . 'ターンまとめて更新）'  if($HdeveRepCount > 1);
	$firep  = '（' . $HfightRepCount . 'ターンまとめて更新）' if($HfightRepCount > 1);

	$hide_mon = qw(隠蔽 見える 100の位で四捨五入)[$HhideMoneyMode];
	$hide_twn = qw(見える 規模を隠蔽)[$Hhide_town];
	$hide_frm = qw(見える 森に偽装 森に偽装\(規模も隠蔽\))[$Hhide_farm];
	$hide_fac = qw(見える 森に偽装 森に偽装\(規模も隠蔽\))[$Hhide_factory];
	$hide_mis = qw(見える 森に偽装)[$Hhide_missile];
	$hide_def = qw(見える 森に偽装)[$Hhide_deffence];

	# 報酬金設定を表示
    my $price;
	if($HrewardMode == 1) {
		$price = "(双方のミサイル基地の数 ＋ 双方の防衛施設の数 × 2) ÷ ".
					"2 × 自分の戦闘行為回数 × 15 ＋ 荒地(ミサイル跡のみ) × ".
                    "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} elsif($HrewardMode == 2) {
		$price = "破壊された農場・工場・ミサイル基地・防衛施設の建設費 ＋ 荒地(ミサイル跡のみ) × ".
           "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} else {
		$price = "<FONT COLOR=RED>報酬金設定が正しくありません</FONT>";
	}

    # 対戦相手決定方式
    my $battle;
    if($Htournament == 1) {
       $battle = "トーナメント表に従う";
    } else {
       $battle = "デフォルト設定";
    }

    # 特殊設定
	my $mStr;
	if($HeasyReclaim) {
		$mStr .= "<H3>${HtagTH_}☆埋め立ての簡易化${H_tagTH}</H3>\n";
		$mStr .= "→ 通常、海を埋め立てると浅瀬になりますが、その行程を飛ばして荒地になります。<BR>\n";
		$mStr .= "つまり、陸地に面してる海なら、一回で荒地になります。<BR>\n";
		$mStr .= "入り組んだ島を作るのが容易になりますが、その分村が生え難くもなりますので、<BR>\n";
		$mStr .= "ほどほどに入り組ませましょう。<BR><BR>\n";
		$mStr .= "通常通り浅瀬も発生しますが、性能は同じですので特に気にする必要はありません。<BR>\n";
	}
	$mStr = "<B>なし</B><BR>" if(!$mStr);

	out(<<END);
${HtagTitle_}設定一覧${H_tagTitle}
<BR>
<DIV ALIGN=RIGHT><I>system version ${version}</I></DIV><HR>
<BR>
<H1>${HtagHeader_}報酬金設定${H_tagHeader}</H1>
<B>
$price
</B><BR>
<BR><HR>
<H1>${HtagHeader_}対戦相手決定方式${H_tagHeader}</H1>
<B>
$battle
</B><BR>
<BR><HR>
<H1>${HtagHeader_}特殊設定${H_tagHeader}</H1>
<FONT SIZE=+1>${mStr}</FONT>
<BR><HR>
<H1>${HtagHeader_}各種設定値${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}島数関係${H_tagTH}</TD></TR>
<TR><TD>　${HtagName_}最大登録数${H_tagName}　</TD><TD><B>$HmaxIsland島</b></TD></TR>
<TR><TD>　${HtagName_}予選突破${H_tagName}</TD><TD><B>$HfightMem位以上</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}島の初期値${H_tagTH}</TD></TR>
<TR><TD>　${HtagName_}面積${H_tagName}　</TD><TD><B>${HlandSizeValue}${HunitArea}</b></TD></TR>
<TR><TD>　${HtagName_}荒地の数${H_tagName}</TD><TD><B>9ヶ所</b></TD></TR>
<TR><TD>　${HtagName_}浅瀬の数${H_tagName}</TD><TD><B>${HseaNum}ヶ所</b></TD></TR>
<TR><TD>　${HtagName_}資金${H_tagName}　</TD><TD><B>${HinitialMoney}${HunitMoney}</b></TD></TR>
<TR><TD>　${HtagName_}食料${H_tagName}　</TD><TD><B>${HinitialFood}${HunitFood}</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}偽装設定${H_tagTH}</TD></TR>
<TR><TD>　${HtagName_}資金${H_tagName}　</TD><TD><B>${hide_mon}</b></TD></TR>
<TR><TD>　${HtagName_}都市系${H_tagName}　</TD><TD><B>${hide_twn}</b></TD></TR>
<TR><TD>　${HtagName_}農場${H_tagName}　</TD><TD><B>${hide_frm}</b></TD></TR>
<TR><TD>　${HtagName_}工場${H_tagName}　</TD><TD><B>${hide_fac}</b></TD></TR>
<TR><TD>　${HtagName_}ミサイル基地${H_tagName}　</TD><TD><B>${hide_mis}</b></TD></TR>
<TR><TD>　${HtagName_}防衛施設${H_tagName}　</TD><TD><B>${hide_def}</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}その他設定値${H_tagTH}</TD></TR>
<TR><TD>　${HtagName_}村発生率${H_tagName}</TD><TD><B>${HtownGlow}％</b></TD></TR>
<TR><TD>　${HtagName_}失業者数上限${H_tagName}</TD><TD><B>${Hno_work}${HunitPop}</b></TD></TR>
<TR><TD>　${HtagName_}人口増加幅${H_tagName}</TD><TD><B>100〜${HtownUp}${HunitPop}／ターン</b></TD></TR>
<TR><TD>　${HtagName_}木の増える本数${H_tagName}</TD><TD><B>${HtreeUp}00本／ターン</b></TD></TR>
<TR><TD>　${HtagName_}防衛施設伐採代金${H_tagName}</TD><TD><B>${HdefenceValue}${HunitMoney}</b></TD></TR>
<TR><TD>　${HtagName_}自動放棄ターン${H_tagName}</TD><TD><B>${HgiveupTurn}ターン</b></TD></TR>
<TR><TD>　${HtagName_}最大コマンド入力数${H_tagName}</TD><TD><B>${HcommandMax}個</b></TD></TR>
<TR><TD>　${HtagName_}地盤沈下${H_tagName}</TD><TD><B>${HdisFallBorder}${HunitArea}／${HdisFalldown}％</b></TD></TR>

</table>
<BR><HR>
<H1>${HtagHeader_}ターン進行ヘルプ${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}ターン更新時間${H_tagTH}</TD></TR>
<TR><TD><NOBR>　${HtagName_}予選期間${H_tagName}</NOBR></TD><TD NOWRAP><B>$unit時間</b>　${yosrep}</TD></TR>
<TR><td WIDTH=100><NOBR>　${HtagName_}開発期間${H_tagName}</NOBR></TD><TD NOWRAP><B>$deve時間</b>　${devrep}</TD></TR>
<TR><TD><NOBR>　${HtagName_}戦闘期間${H_tagName}</NOBR></TD><TD NOWRAP><B>$fiunit時間</b>　${firep}</TD></TR>
<TR><TD><NOBR>　${HtagName_}戦闘から開発移行${H_tagName}</NOBR></TD><TD NOWRAP><B>$inter時間後</b></TD></TR>

<TR><TD colspan=2 $HbgTitleCell>${HtagTH_}各期間のターン数${H_tagTH}</TD></TR>
<TR><TD>　${HtagName_}予選${H_tagName}　</TD><TD><B>$HyosenTurnターンまで</b></TD></TR>
<TR><TD>　${HtagName_}開発期間${H_tagName}</TD><TD><B><NOBR>$HdevelopeTurnターン</NOBR></b></TD></TR>
<TR><TD NOWRAP>　${HtagName_}戦闘期間${H_tagName}</TD><TD NOWRAP><B>$HfightTurnターン</b></TD></TR>
<TR><TD NOWRAP>　${HtagName_}不戦勝時の開発停止　${H_tagName}</TD><TD NOWRAP><B>（$HnofightUp	× 回戦数 ＋ $HnofightTurn）ターン</b></TD></TR>

</table>
END

	my($fitone) = $HdevelopeTurn + $HyosenTurn;
	my($fittwo) = $fitone + $HfightTurn;
	my($fitNum) = 1;
	my($v_mode,$v_time,$v_turn,$v_text);
	$v_text = "　";

	# ターン行程の日程表示用
	if(!$Htime_mode and $HislandTurn < $HyosenTurn) {
		$v_time = (($HyosenTurn - $HislandTurn) / $HyosenRepCount - 1) * $HunitTime + $HislandLastTime + $HunitTime;
		my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
		$v_text = "　〜　".$mon."月".$mday."日".$hour."時".$min."分";
		$v_mode = 1;
		$v_time -= $HinterTime;
	}
	out(<<END);
<BR><HR>
<H1>${HtagHeader_}ターン進行行程 早見表${H_tagHeader}</H1>
※この表が誤っている可能性が少しばかりあるので、参考程度に留めて下さい。
<table height=125 border $HbgNameCell>
<TR>
<td>${HtagName_}予選${H_tagName}</td>
<TD $HbgCommentCell><B>0　〜　$HyosenTurn</B></td>
<TD>$v_text</TD>
</tr>
END

	$HyosenTurn++;
	$v_time += $HunitTime;

	for($i = 2;$i <= $HfightMem;$i*=2) {
		my $kaisen = ($i*2 > $HfightMem) ? "決勝" : "第$fitNum回";
		# ターン行程の日程表示用
		if(!$Htime_mode and !$v_mode and $HislandTurn + 1 >= $HyosenTurn and $HislandTurn + 1 <= $fitone) {
			$v_time += (($fitone - $HislandTurn) / $HdeveRepCount - 1) * $HdevelopeTime + $HislandLastTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_text = "　〜　".$mon."月".$mday."日".$hour."時".$min."分";
			$v_mode = 1;
		} elsif(!$Htime_mode and $v_mode) {
			$v_time += $HinterTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_time = $v_time + (($HdevelopeTurn - $HdeveRepCount) / $HdeveRepCount * $HdevelopeTime);
			my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($v_time);
			$v_text = $mon."月".$mday."日".$hour."時".$min."分 〜 ". $mon2."月".$mday2."日".$hour2."時".$min2."分";
		}
	out(<<END);
<TR>
<TD ALIGN=RIGHT>${HtagName_}${kaisen}戦開発期間${H_tagName}</td>
<TD $HbgCommentCell><B>$HyosenTurn　〜　$fitone</b></td>
<TD>$v_text</TD>
</TR>
<TR>
<TD align=right>${HtagName_}戦闘期間${H_tagName}</TD><TD $HbgCommentCell><B>
END
		# ターン行程の日程表示用
		if(!$Htime_mode and !$v_mode and $HislandTurn + 1 >= $fitone and $HislandTurn + 1 <= $fittwo) {
			$v_time += (($fittwo - $HislandTurn) / $HfightRepCount - 1) * $HfightTime + $HislandLastTime;
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time);
			$v_text = "　〜　".$mon."月".$mday."日".$hour."時".$min."分";
			$v_mode = 1;
		} elsif(!$Htime_mode and $v_mode) {
			my($sec,$min,$hour,$mday,$mon) = get_time($v_time + $HfightTime);
			$v_time = $v_time + ($HfightTurn / $HfightRepCount * $HfightTime);
			my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($v_time);
			$v_text = $mon."月".$mday."日".$hour."時".$min."分 〜 ". $mon2."月".$mday2."日".$hour2."時".$min2."分";
		}
		out (($fitone + 1) . "　〜　$fittwo</b></td><TD>$v_text</TD></tr>\n");
		$fitNum++;
		$HyosenTurn = $fittwo + 1;
		$fitone = $HyosenTurn + $HdevelopeTurn - 1;
		$fittwo = $fitone + $HfightTurn;
	}
	out("</table>\n<BR></hr>\n");
	out("<HR>${HtempBack}");
}

#----------------------------------------------------------------------
# マニュアルページモード
#----------------------------------------------------------------------
# メイン
sub expPageMain {
	# 開放
	unlock();

	# テンプレート出力
	tempexpPage();
}

sub tempexpPage {

	# 表示用設定
	$HunitTime /= 3600;
	$HdevelopeTime /= 3600;
	$HfightTime /= 3600;
	$HinterTime /= 3600;
	$HdisFalldown /= 10;
	$HdisFallBorder++;
	$precheap++;
	$precheap2 = $HcomCost[$HcomPrepare2] * $precheap2 / 10;
	$HfightTurnH = $HfightTurn / 2;

	# 報酬金設定
	if($HrewardMode == 1) {
		$reward_msg = "(双方のミサイル基地の数 ＋ 双方の防衛施設の数 × 2) ÷ ".
					"2 × 自分の戦闘行為回数<SMALL>*</SMALL> × 15 ＋ 荒地(ミサイル跡のみ) × ".
                    "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} elsif($HrewardMode == 2) {
		$reward_msg = "破壊された農場・工場・ミサイル基地・防衛施設の建設費 ＋ 荒地(ミサイル跡のみ) × ".
        "$HcomCost[$HcomPrepare2] ".$HunitMoney;
	} else {
		$reward_msg = "<FONT COLOR=RED>報酬金設定が正しくありません</FONT>";
	}

	# 丸々1ページ分のHTML
	out("Content-type: text/html\n\n");
	out(<<END);
<html>
<head>
<title>箱庭トーナメント２マニュアル</title>
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
<span><font color=#00cc99>箱庭トーナメント２</font></span>
<BR><BR>
基本は、オリジナルの箱庭２と同じです。
<BR>オリジナルの箱庭2のルールは<a href=http://www.nn.iij4u.or.jp/~flora/>この辺</a>をご覧下さい。 <BR>
<BR>
このマニュアルに書いていない事は、基本的に上記のオリジナル版と同様の設定です。<BR>
わからない事、疑問に思った事は、お気軽に掲示板にてご質問下さい。

<BR><BR><HR><BR>
<h2>■どんなゲームか？</h2>
<B>１対１</b>のトーナメント戦です。
<BR>決められた対戦相手を、戦闘期間中に撃破すれば次に進めます。<BR>
これを数回繰り返し、最終的に残った<B>１島</b>が優勝です。<BR><BR><BR>

<h2>■まず予選…</h2>
登録して最初の<B>第${HyosenTurn}ターン</b>までは、予選期間です。<BR>
第${HyosenTurn}ターンの時点で、<B>合計${HfightMem}島</b>になるように<u>人口の少ない</u>島が<B>予選落ち</B>となります。<BR>
この期間は、他島へのミサイル発射コマンドは全て<B>キャンセル</b>されます。<BR><BR>
さらに、この後第一回戦の対戦相手が決定。開発期間へと以降します。<BR><BR>
放っておいても勝手に人口は増えていっていまいますので、<B>資金繰り${HstopAddPop}回目からは、</b><BR>
それ以降人口の<B>自然増加はストップ</b>します。<BR>
コマンド入力を行えば元通り自然増加します。<BR><BR>
また、同様に<B>失業者</B>の数が<B>${Hno_work}${HunitPop}以上</B>になると人口の<B>自然増加はストップ</b>します。<BR>
失業者とは、全く働いてない島民の事です。
<BR><BR>
これら二つの人口の自然増加ストップは、<B>予選期間のみ</B>です。<BR>
<BR><BR>
<h2>■開発期間、戦闘期間について</h2>

その後<B>${HdevelopeTurn}ターン</b>は、開発期間です。<BR>
この期間も、<B>ミサイルは撃てない</b>ので、開発に専念して下さい。<BR>
開発期間が終わると、戦闘期間に入ります。（戦闘期間は${HfightTurn}ターン）<BR>
戦闘期間中は、自分の<B>対戦相手にのみ</b>ミサイルの発射が許可されます。<BR>
生き残る為には、相手を潰さないといけません。<BR>
戦闘期間終了時に、<B>人口が多い</b>方が勝利になります。<BR>
敗者の島は、即座に放棄されます。頑張って下さい。<BR>
<BR>
その後、開発期間＞戦闘期間＞開発期間・・・と続いていき、最後の１島になるまで、続きます。<BR>
<B>開発期間</b>の最初のターンに、対戦相手が決定します。<BR>
<BR><BR>

<h2>■ターン更新について</h2>
予選期間中は、<B>${HunitTime}時間で${HyosenRepCount}ターン</b>進みます。<BR>
開発期間中は、<B>${HdevelopeTime}時間で${HdeveRepCount}ターン</b>進みます。<BR>
戦闘期間中は、<B>${HfightTime}時間で${HfightRepCount}ターン</B>進みます。<BR><BR>
開発期間の最後のターンの次のターン更新は、その<B>${HfightTime}時間後</b>になります。（わかりづらいですが・・・）<BR>
つまり、戦闘期間に入るまでに、${HfightTime}時間空くということです。<BR>
また、戦闘期間終了時点の次のターンは、${HinterTime}時間後に更新されます。<BR>
<B>設定一覧</b>というのもありますので、ご確認下さい。
<BR><BR><BR>
<h2>■勝敗</h2>
勝敗は、人口で決定します。<BR>
もし、人口が全くの<B>同数</b>であれば、前ターンで上位に居た方が、勝者となります。<BR>
島の総数が２で割れない場合は、どこか１島が、不戦勝ということになります。<BR>
また、勝利島は、<B>報酬金</b>を受け取れます。当然不戦勝の島は報酬金は貰えません。<BR><BR>
<B>報酬金</b>は、<BR>
$reward_msg
　です。<BR><BR>
また、戦闘期間の半分（${HfightTurnH}ターン）が経過するまでに、戦闘行為回数<SMALL>*</SMALL>が${do_fight}ターンに満たなかった場合は敗北となります。<BR>
<BR><BR>

<h2>■不戦勝</h2>
対戦相手がいない場合・開発期間終了時までに、対戦相手がいなくなった場合（放棄等で）は、<B>不戦勝</b>となります。<BR>
不戦勝となった場合は、<B>数ターン</b>の間<B>開発が停止</b>します。<BR>
つまり、コマンドの進行も無ければ、災害も発生しません。<BR>
開発画面（又は観光画面）にて、残り停止ターンが表示されますので、０になるまで一時停止となります。<BR><BR>
開発停止期間は、<B>回戦数×${HnofightUp}＋${HnofightTurn}</b> です。<BR>
つまり、第1回戦での停止期間は、16ターンとなります。<BR><BR>
また、戦闘期間の半分（${HfightTurnH}ターン）が経過するまでに、「相手がいなくなった場合」及び「相手の戦闘行為回数<SMALL>*</SMALL>が${do_fight}ターンに満たなかった場合」は不戦勝扱いとなります。<BR>
この場合は、戦闘開始時の島の状態に戻され、開発停止になります。<BR>
停止期間は、<B>（回戦数×${HnofightUp}＋${HnofightTurn}）− 経過ターン数</B>です。
<BR><BR>
尚、不戦勝は下位付近の島がなる確率が高いです。
<BR><BR>
注:
戦闘行為→ミサイル基地建設・防衛施設建設・各種ミサイル発射<BR>
<BR><BR>
<h2>■対戦相手決定方式</h2>
ちょっと複雑ですが、対戦相手の決定方法です。<BR><BR>
END
   if($Htournament == 1) {
      out(<<END);
まず、予選期間終了と同時に島別に<b>「島力」</b>を割り出します。<BR>
島力は以下の計算式に基づいて割り出されます。<BR><BR>
250 × (人口 + 農場 + 工場 + 採掘場規模) + 面積 × 700 + 軍事施設数 × 1000 + 推定資金 + 木の本数 × $HtreeValue - 荒地 × $HcomCost[$HcomPrepare2]<BR><BR>
次に0〜割り出された数値の間で数字を一つ、ランダムに取り出します。<BR>
仮に島力が5000の場合、最終的な島力は、0〜5000の間のどれかとなるわけです。<BR><BR>
この最終的に割り出された島力を、上位から並べて行き、上から順番にトーナメント表に割り振っていきます。
END
   } else {
      out(<<END);
まず、戦闘(予選)期間終了と同時に島別に<b>「島力」</b>を割り出します。<BR>
島力は以下の計算式に基づいて割り出されます。<BR><BR>
250 × (人口 + 農場 + 工場 + 採掘場規模) + 面積 × 700 + 軍事施設数 × 1000 + 推定資金 + 木の本数 × $HtreeValue - 荒地 × $HcomCost[$HcomPrepare2]<BR><BR>
次に0〜割り出された数値の間で数字を一つ、ランダムに取り出します。<BR>
仮に島力が5000の場合、最終的な島力は、0〜5000の間のどれかとなるわけです。<BR><BR>
この最終的に割り出された島力を、上位から並べて行き、上から順番に対戦相手としていきます。
END
   }

   out(<<END);
<BR><BR><BR>
<h2>■廃止・変更・新コマンド一覧</h2>
<B>以下のコマンドは使用出来ません。</b><BR>
・食料援助<BR>
・資金援助<BR>
・誘致活動<BR>
・海底基地建設<BR>
・ＳＴミサイル発射<BR>
・陸地破壊弾発射<br>
・怪獣派遣<BR>
・記念碑建造(発射)<BR><BR>
<B>以下のコマンドは変更がありました。</b><BR>
・各種ミサイル発射　−＞　予選・開発期間中は、発射できません。戦闘期間中は、対戦相手にしか発射できません。<BR>
・掘削　−＞　油田を掘る事が出来なくなりました。　海に対して行うと、キャンセルされます。<BR>
・植林　−＞　${HcomCost[$HcomPlant]}${HunitMoney}。<BR>
・伐採　−＞　ターン消費無し。防衛施設に対して行うと、${HdefenceValue}${HunitMoney}で売却出来る。もちろんターン消費なし。<BR>
・防衛施設　−＞　${HcomCost[$HcomDbase]}${HunitMoney}　観光者からは森に見える。　売却する事が出来る。<BR><BR>
<B>以下は新コマンドです</b><BR>
・高速農場整備<BR>　−＞　${HcomCost[$HcomFastFarm]}${HunitMoney}　ターン消費しない農場整備　戦闘期間中は使用出来ません。<BR>
・一括自動地ならし<BR>　−＞　このコマンド一つで、全ての荒地を地ならししてくれる。${precheap}箇所目の荒地からは、費用が${precheap2}${HunitMoney}と割引される。　同じく戦闘期間中は使用不可。<BR>
<BR><BR>

<h2>■災害</h2>

自然災害は発生しません。<BR>
発生する災害は以下の通りです。<BR><BR>

地盤沈下　−＞　${HdisFallBorder}ヘックス以上にて${HdisFalldown}％<BR>

<BR><BR>

<h2>■島の初期値・設定等</h2>
設定一覧をご確認下さい。<BR>
<B>*重要な設定がある場合がありますので、必ず確認して下さい。</B><BR>
<BR><BR>

<!--
<h2>■登録方法</h2>
登録は<a href=mail.html>こちら</a>で受け付けております。<BR>
その他の登録方法は受け付けておりません。<BR>
ただし、ゲーム途中での参加は出来ません。<BR>
<B>先着順</b>ですので、空きがあっても参加できない場合もございます。ご了承下さいませ。<BR>

<BR><BR>
-->
END

   my $log = int($HlogMax / 2);
   my $cmd = int($HcommandMax / 2);

   out(<<END);
<h2>■携帯電話対応</h2>
あくまでも補助的な機能ですが、携帯電話からの開発計画の入力に対応しています。<BR>
<BR>

以下に携帯電話からの操作についての説明がありますが、ある程度は携帯電話と箱庭諸島に慣れている事を前提として書いています。<BR>
その為、理解しにくい点も多々あるかと思いますが、あらかじめご承知下さい。<BR>
<BR>

まず最も重要な点は、横幅が25バイト以上表示出来ない端末では地図が正常に表示されません。<BR>
何の事だか意味のわからない人は、以下に記したやり方で開発画面まで行ってみて下さい。<BR>
地図の横幅が画面内に収まっていれば問題ありません。<BR>
この点は今後も変わらないので、残念ですが正常に表示されない人は諦めて下さい。<BR>
<BR>

携帯電話からのアクセスには自分の島の<B>島番号</B>が必要になります。<BR>
対戦相手が居る場合は、その島の<B>島番号</B>も控えておいた方が安心です。<BR>
<B>島番号</B>は、観光に行く事で調べる事が出来ます。<BR>
観光に行くと、アドレスが「$HthisFile?Sight=12」のような形になるかと思いますが、この末尾の<B>12</B>と言う数字の部分がその島の<B>島番号</B>を表わしています。<BR>
自分の島へ観光に行き、番号を調べておきましょう。<BR>
<BR>

ここまで調べたら、早速携帯電話でアクセスしてみましょう。<BR>
携帯電話専用のアドレスとかは無いので、パソコンと同じアドレスにアクセスして下さい。<BR>
アクセスすると、入力フォームが現れるので、IDと書いてある箇所へさっき調べた<B>島番号</B>を、
PSの欄には<B>パスワード</B>を入力してその下にあるボタンを押しましょう。<BR>
カラーモードと言うのは今は気にしないで標準のままでいいです。<BR>
<BR>

「開発」をクリックすると、簡易的な開発画面が表示されます。<BR>
ここから計画を入力したり、出来事を確認したり出来ます。<BR>
地図の読み方については、「ヘルプ」を見るとわかるので省略します。<BR>
<BR>

「出来事」をクリックすると、最近の出来事が表示されます。<BR>
パソコン上で見るのとは違い、${log}ターン分のログしか表示されません。<BR><BR>

「計画一覧」をクリックすると、入力済みの開発計画が表示されます。<BR>
<B>数量</B>は、x0 のように簡略化した形で表示されます。<BR>
<BR>

「計画入力」をクリックすると、開発計画の入力が行なえます。<BR>
画面の下部には入力済みの計画が${cmd}件表示されています。<BR>
この画面では、いわゆる「通常モード」と同じ間隔で計画の入力をします。<BR>
パソコンとの違いは、計画番号、座標、数量に対して数値を直接入力する必要がある事くらいです。<BR>
[]内の数値に対応したキーを入力すると、その入力欄に直接飛ぶ事が出来ます。<BR>
例えば、1を入力すると計画番号の入力が始まります。(もしかしたらこの機能に対応していない端末があるかもしれません。)<BR>
<BR>

島番号とパスワードは保存されないので、毎回毎回入力しなければなりません。<BR>
そこで、ブックマークへの登録を工夫する事により、入力の手間を省く事が可能です。<BR>
具体的には「$HthisFile?ID=12&PS=0123」というアドレスにアクセスすると、自動的に島番号12、パスワード0123と入力済みの状態でアクセス出来ます。<BR>
IDとPSの部分には自分の島番号とパスワードを設定しておきましょう。<BR>
他人にブックマークを覗かれるとパスワードがばれてしまうので、ばれると危険なパスワードの場合はパスワードの部分は空欄にしておく事をお薦めします。<BR>
<BR>

最後に<B>カラーモード</B>とは、各ヘックスの色付けの状態を表わしています。<BR>
「標準」の場合は、森、ミサイル基地、防衛施設以外のヘックスには色が付きません。<BR>
「フルカラー」では海以外の全てのヘックスに色が付きます。<BR>
<B>フルカラー</B>では容量も大きくなってしまうので、いわゆるパケット代も多くなってしまいます。<BR>
<B>標準</B>だと容量も小さいので、環境によって好きな方を選んで下さい。<BR>
<BR>

<B>カラーモード</B>の選択状態も島番号やパスワードと同じようにブックマークへのアドレスに含める事で保存する事が出来ます。<BR>
アドレス欄の末尾に「&MP=1」と追加するだけで自動的にフルカラーが選択されます。<BR>
<BR>

尚、観光者通信やコメント欄などの機能は利用できません。<BR>
<BR><BR>

<h2>■注意事項</h2>
生き残り戦ですので、ミサイルを撃つ事を前提としております。<BR>
ミサイルを撃たれたくない、撃ちたくない平和的な方は、参加しない事をお勧めします。<BR><BR>
また、途中でアクセスが出来なくなる恐れがある方の参加はお断り致します。<BR>
途中で放棄されると、その時の対戦相手が有利になってしまいます。<BR><BR>
戦闘期間に入ったら、全力で相手を攻撃して下さい。<BR>
故意に海に向けて撃ったり、対戦相手が有利になるように画策した場合は、<B>永久追放</B>致します。<BR><BR>
当然の事ながら、重複登録・複数島管理・他サイトでの、闇取引は禁止です。<BR>
発覚次第、問答無用で削除します。<BR>
こちらは、厳しくいかせて頂きます。<BR><BR>
さらに、ターン更新時間でのブラウザの読みこみ中止は<B>絶対に</b>しないで下さい。<BR>
<B>データファイルが壊れてしまう</b>可能性があります！<BR><BR>
<HR>
<BR>
</body>
</htML>

END

}

1;
