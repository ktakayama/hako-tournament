#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭トーナメント２
# ターン進行モジュール
# $Id: hako-turn.cgi,v 1.6 2004/11/10 13:01:25 gaba Exp $

# 周囲2ヘックスの座標
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

#----------------------------------------------------------------------
# 島の新規作成モード
#----------------------------------------------------------------------
# メイン
sub newIslandMain {
	# 島がいっぱいでないかチェック
	if($HislandNumber >= $HmaxIsland or $HislandTurn > 0) {
		unlock();
		tempNewIslandFull();
		return;
	}

	# 名前があるかチェック
	if($HcurrentName eq '') {
		unlock();
		tempNewIslandNoName();
		return;
	}

	# 名前が正当かチェック
	if($HcurrentName =~ /[,\"\?\(\)\<\>\$]|^無人$/) {
		# 使えない名前
		unlock();
		tempNewIslandBadName();
		return;
	}

	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
		# すでに発見ずみ
		unlock();
		tempNewIslandAlready();
		return;
	}

	# passwordの存在判定
	if($HinputPassword eq '') {
		# password無し
		unlock();
		tempNewIslandNoPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 簡易重複チェック
	if(registCheck()) {
		unlock();
		tempRegistFailed();
		return;
	}

	# 新しい島の番号を決める
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland();
	my($island) = $Hislands[$HcurrentNumber];

	# 各種の値を設定
	$island->{'name'} = $HcurrentName;
	$island->{'id'} = $HislandNextID;
	$HislandNextID ++;
	$island->{'absent'} = 1;
	$island->{'comment'} = '(未登録)';
	$island->{'password'} = encode($HinputPassword);
	
	# 人口その他算出
	estimate($HcurrentNumber);

	# データ書き出し
	writeIslandsFile($island->{'id'});
	logDiscover($HcurrentName); # ログ

	# 開放
	unlock();

	# 発見画面
	tempNewIslandHead($HcurrentName); # 発見しました!!
	islandInfo(); # 島の情報
	islandMap(1); # 島の地図、ownerモード
}

# 新しい島を作成する
sub makeNewIsland {
	# 地形を作る
	my($land, $landValue) = makeNewLand();

	# 初期コマンドを生成
	my(@command, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		 $command[$i] = {
			 'kind' => $HcomDoNothing,
			 'target' => 0,
			 'x' => 0,
			 'y' => 0,
			 'arg' => 0
		 };
	}

	# 初期掲示板を作成
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		 $lbbs[$i] = "0>>";
	}

	# 島にして返す
	return {
		'land' => $land,
		'landValue' => $landValue,
		'command' => \@command,
		'lbbs' => \@lbbs,
		'money' => $HinitialMoney,
		'food' => $HinitialFood,
		'prize' => 0,
		'ownername' => '0'
	};
}

# 簡易重複チェック
sub registCheck {
	return 0 if($Hdebug == 1);
    my($ip) = $ENV{'HTTP_X_FORWARDED_FOR'};
    $ip = $ENV{'REMOTE_ADDR'} if(!$ip);

	open(IN, "${HdirName}/hakojima.his");
	while(<IN>) {
		chomp();
		next unless(/\(([\d\.]+)\)$/);
		return 1 if($1 eq $ip);
	}
	close(IN);

	return 0;
}

# 新しい島の地形を作成する
sub makeNewLand {
	# 基本形を作成
	my(@land, @landValue, $x, $y, $i);

	# 海に初期化
	for($y = 0; $y < $HislandSize; $y++) {
		 for($x = 0; $x < $HislandSize; $x++) {
			 $land[$x][$y] = $HlandSea;
			 $landValue[$x][$y] = 0;
		 }
	}

	# 中央の4*4に荒地を配置
	my($center) = int($HislandSize / 2 - 1);
	for($y = $center - 1; $y < $center + 3; $y++) {
		 for($x = $center - 1; $x < $center + 3; $x++) {
			 $land[$x][$y] = $HlandWaste;
		 }
	}

	# ☆初期の島の面積固定ルール
	my($size,$seacon) = (16,0);

	# 8*8範囲内に陸地を増殖
	while($size < $HlandSizeValue){
		# ランダム座標
		$x = random(8) + $center - 3;
		$y = random(8) + $center - 3;
		if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
			# 周りに陸地がある場合、浅瀬にする
			# 浅瀬は荒地にする
			# 荒地は平地にする
			if($land[$x][$y] == $HlandSea) {
				if($landValue[$x][$y] == 1) {
					$land[$x][$y] = $HlandPlains;
					$landValue[$x][$y] = 0;
					$size++;
					$seacon--;
				} else {
			 		$landValue[$x][$y] = 1;
					$seacon++;
				}
			}
		}
	}

	my $sea_flag = ($seacon > $HseaNum) ? 1 : 0;

	makeRandomPointArray();
	for($i = 0; $i < $HpointNumber; $i++) {
		last if($seacon == $HseaNum);
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		if(countAround(\@land, $x, $y, $HlandPlains, 7) and $land[$x][$y] == $HlandSea and $landValue[$x][$y] == $sea_flag){
			$landValue[$x][$y] = ($landValue[$x][$y] == 1) ? 0 : 1;
			$seacon += $sea_flag ? -1: 1;
		}
	}

	# 森を作る
	my($count) = 0;
	while($count < 4) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこがすでに森でなければ、森を作る
		 if($land[$x][$y] != $HlandForest) {
			 $land[$x][$y] = $HlandForest;
			 $landValue[$x][$y] = 5; # 最初は500本
			 $count++;
		 }
	}

	# 町を作る
	$count = 0;
	while($count < 2) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこが森か町でなければ、町を作る
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandTown;
			 $landValue[$x][$y] = 5; # 最初は500人
			 $count++;
		 }
	}

	# 山を作る
	$count = 0;
	while($count < 1) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこが森か町でなければ、町を作る
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandMountain;
			 $landValue[$x][$y] = 0; # 最初は採掘場なし
			 $count++;
		 }
	}

	return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# パスワードチェック
	if($HoldPassword eq $HspecialPassword) {
		# 特殊パスワード
		$island->{'money'} = 9999;
		$island->{'food'} = 9999;
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# 名前変更の場合		
		# 名前が正当かチェック
		if($HcurrentName =~ /[,\"\?\(\)\<\>]|^無人$/) {
			# 使えない名前
			unlock();
			tempNewIslandBadName();
			return;
		}

		# 名前の重複チェック
		if(nameToNumber($HcurrentName) != -1) {
			# すでに発見ずみ
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($island->{'money'} < $HcostChangeName) {
			# 金が足りない
			unlock();
			tempChangeNoMoney();
			return;
		}

		# 代金
		if($HoldPassword ne $HspecialPassword) {
			$island->{'money'} -= $HcostChangeName;
		}

		# 名前を変更
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;

        if($Htournament == 1) {
           require('hako-chart.cgi');
           makeChartPage();
        }
	}

	# password変更の場合
	if($HinputPassword ne '') {
		# パスワードを変更
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if($HownerName ne '') {
		# オーナー名を変更
		$island->{'ownername'} = $HownerName;
		$flag = 1;
	}

	if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
		# どちらも変更されていない
		unlock();
		tempChangeNothing();
		return;
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);
	unlock();

	# 変更成功
	tempChange();
}

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {

	# ログファイルを後ろにずらす
	my($i, $j, $s, $d);
	for($i = ($HlogMax - 1); $i >= 0; $i--) {
		$j = $i + 1;
		my($s) = "${HdirName}/hakojima.log$i";
		my($d) = "${HdirName}/hakojima.log$j";
		unlink($d);
		rename($s, $d);
	}

	# まとめ更新初期値
	$HislandTurnCount = $HyosenRepCount if($HislandTurn == 0);

	# 座標配列を作る
	makeRandomPointArray();

	# ターン番号
	$HislandTurn++;

	# 戦闘期間への以降等
	$winlose = 0;
	my $fight_check = 0;

	if($HislandTurn == $HislandChangeTurn && $HislandFightMode == 1) {
		$winlose = 1; # 戦闘期間最終ターン
		$fight_check = 1;
	} elsif($HislandTurn > $HislandChangeTurn) {
		if($HislandFightMode) {
			# 戦闘終了後、開発期間へ
			$HislandFightMode = 0;
			$HislandFightCount++;
			$HislandChangeTurn += $HdevelopeTurn;
		} else {
			# 開発終了後、戦闘期間へ
			$HislandFightMode = 1;
			$HislandChangeTurn += $HfightTurn;
			$winlose = 2;
			# 島の状態を保存
			for($i = 0; $i < $HislandNumber; $i++) {
				island_save($Hislands[$i]);
			}
		}
	}

	# 最終更新時間を更新
	if($HislandTurnCount > 1) {
		$HislandTurnCount--;
	} elsif(($HislandTurn + $HfightRepCount - 1) == $HislandChangeTurn and $HislandFightMode) {
		# 戦闘期間終了時
		$HislandLastTime += $HinterTime;
		$HislandTurnCount = $HfightRepCount;
	} elsif($HislandFightMode) {
		# 戦闘期間
		$HislandLastTime += $HfightTime;
		$HislandTurnCount = $HfightRepCount;
	} elsif(($HislandTurn + $HdeveRepCount - 1) == $HislandChangeTurn) {
		# 開発期間終了時
		$HislandLastTime += $HfightTime;
		$HislandTurnCount = $HdeveRepCount;
	} elsif($HislandTurn <= $HyosenTurn) {
		# 予選期間
		$HislandLastTime += $HunitTime;
		$HislandTurnCount = $HyosenRepCount if($HislandTurn != $HyosenRepCount);
	} else {
		# 開発期間
		$HislandLastTime += $HdevelopeTime;
		$HislandTurnCount = $HdeveRepCount;
	}

	# 順番決め
	my(@order) = randomArray($HislandNumber);

	# 収入、消費フェイズ
	for($i = 0; $i < $HislandNumber; $i++) {
		estimate($order[$i]);
		next if($Hislands[$order[$i]]->{'rest'} > 0); # 不戦勝開発停止中
		income($Hislands[$order[$i]]);

		# ターン開始前の人口をメモる
		$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	}

	# コマンド処理
	for($i = 0; $i < $HislandNumber; $i++) {
		next if($Hislands[$order[$i]]->{'rest'} > 0); # 不戦勝開発停止中
		# 戻り値1になるまで繰り返し
		while(doCommand($Hislands[$order[$i]]) == 0){};
	}

	# 成長および単ヘックス災害
	for($i = 0; $i < $HislandNumber; $i++) {
		# 不戦勝開発停止中
		if($Hislands[$order[$i]]->{'rest'} > 0) {
			$Hislands[$order[$i]]->{'rest'}--;
			next;
		}
		doEachHex($Hislands[$order[$i]]);
	}


	# 島全体処理
	my($remainNumber) = $HislandNumber;
	my($island);
	for($i = 0; $i < $HislandNumber; $i++) {
		$island = $Hislands[$order[$i]];

		doIslandProcess($order[$i], $island); 
		next if($island->{'rest'} > 0);
		# 死滅判定
		my($tmpid) = $island->{'id'};
		if($island->{'dead'} == 1) {
			$island->{'pop'} = 0;
			if($HislandFightMode == 0) {
				unlink("island.$tmpid");
				$remainNumber--;
			} elsif(int($HfightTurn / 2) <= ($HislandChangeTurn - $HislandTurn)) {
				fight_no_fight($island->{'fight_id'});
				unlink("island.$tmpid");
				$remainNumber--;
			} else {
				# 村や町などを全部消し去る
				my($land) = $island->{'land'};
				my($landValue) = $island->{'landValue'};
				for($f = 0; $f < $HpointNumber; $f++) {
					$bx = $Hrpx[$f];
					$by = $Hrpy[$f];
					if($land->[$bx][$by] == $HlandTown) {
						$land->[$bx][$by] = $HlandPlains;
						$landValue->[$bx][$by] = 0;
					}
				}
				$island->{'password'} = random(9999);
				$island->{'rest'} = $HfightTurn * 2;
			}
		} elsif($island->{'pop'} == 0) {
			$island->{'dead'} = 1;
			# 死滅メッセージ
			logDead($tmpid, $island->{'name'});
			if($HislandFightMode == 0) {
				unlink("island.$tmpid");
				$remainNumber--;
			} elsif(int($HfightTurn / 2) <= ($HislandChangeTurn - $HislandTurn)) {
				fight_no_fight($island->{'fight_id'});
				unlink("island.$tmpid");
				$remainNumber--;
			} else {
				$island->{'password'} = random(9999);
				$island->{'rest'} = $HfightTurn * 2;
			}
		}

		if($island->{'pop'} == 0 and $HislandFightMode == 0 and $island->{'fight_id'} > 0) {
			# 開発期間中に島がなくなった場合は、相手の島が不戦勝になる
			my $HcurrentNumber	= $HidToNumber{$island->{'fight_id'}};
			my $tIsland = $Hislands[$HcurrentNumber];
			if($HcurrentNumber ne '') {
				$tIsland->{'rest'}	+= $HnofightTurn + $HislandFightCount * $HnofightUp;
				$tIsland->{'fight_id'} = -1;
			}

		}
	}


	# 勝敗処理
	if($winlose > 0) {

		$remainNumber = $HislandNumber;
		for($i = 0; $i < $HislandNumber; $i++) {
			$island = $Hislands[$i];

			my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
			my $tIsland = $Hislands[$HcurrentNumber];
			if($winlose == 1) {
				# 戦闘後の勝敗・報酬金
                my $id = $island->{'id'};
				if(($HcurrentNumber ne '' and $island->{'pop'} >= $tIsland->{'pop'}) or ($island->{'fight_id'} == -1)) {
					# 勝ち

					my $reward = $island->{'waste'};
					my $tPop = 0;
					if($island->{'fight_id'} > 0) { # 不戦勝は報酬金なし
						# 報酬金設定により分岐
						if($HrewardMode == 1) {
							$reward += int($island->{'reward'} / 2) * $island->{'missile'} * 15 if $island->{'reward'} > 0;
						} elsif($HrewardMode == 2) {
							$reward += $island->{'reward'};
						} elsif($HrewardMode == 3) {

						} elsif($HrewardMode == 4) {

						}
						logWin($island->{'id'}, $island->{'name'}, $reward);
						$island->{'money'}  += $reward;
						$tPop = $tIsland->{'pop'};
						$tIsland->{'pop'} = 0;
						$remainNumber--;
					} else { logWin($island->{'id'}, $island->{'name'}); }

					push(@fight_log_flag, "$island->{'name'},$tIsland->{'name'},$reward,$island->{'log'},$island->{'pop'},$tIsland->{'log'},$tPop,$island->{'fly'},$island->{'fight_id'}");

					$island->{'log'}	 = 0;
					$island->{'fight_id'} = 0;
                    $HislandChart =~ s/[0-9]+,$id,[^"]+"/$HislandFightCount,$id,$island->{'name'}島"/;
				} elsif($HcurrentNumber ne '' and $island->{'pop'} < $tIsland->{'pop'}) {
                   #$island->{'pop'} = 0;
					logLose($island->{'id'}, $island->{'name'});
					save_lose_island($island);
                    my $turn = $HislandFightCount - 1;
                    $HislandChart =~ s/[0-9]+,$id,[^"]+"/$turn,$id,$island->{'name'}島"/;
				}
				$island->{'reward'}	 = 0;
				$island->{'fly'}	 = 0;
				$island->{'missile'} = 0;
			} else {
				# 報酬金フラグ設定
				if($HcurrentNumber ne '') {
					if($island->{'reward_flag'} == 0 and $HrewardMode == 1) {
						my $my_reward = $island->{'reward'} + $tIsland->{'reward'};
						$island->{'reward'}		  = $my_reward;
						$tIsland->{'reward'}	  = $my_reward;
						$tIsland->{'reward_flag'} = 1;
					}
				} else {
					# 対戦相手がいない場合
					$island->{'reward'} = 0;
				}
			}
		}
	}

	# 人口順にソート
	islandSort();

	# 予選落ち判定
	if($HislandTurn == $HyosenTurn) {
		$fight_check = 1;
		if($HislandNumber > $HfightMem) {
			$remainNumber = $HislandNumber;

			for($i = $HfightMem; $i < $HislandNumber; $i++) {
				# 予選落ち
				$island = $Hislands[$i];
				push(@yosen_log, "$island->{'pop'},$island->{'name'}");
				$island->{'pop'} = 0;
				$remainNumber--;
				logLoseOut($island->{'id'},$island->{'name'});
			}
		}
	}

	# 島数カット
	$HislandNumber = $remainNumber;

	# 対戦相手決定
	if($fight_check == 1) {
       if($Htournament == 1) {
          undef %HidToNumber;
          # HidToNumber の作成 (すぐ上で islandSort してるので)
          for($i = 0; $i < $HislandNumber; $i++) {
             my $island = $Hislands[$i];
             $HidToNumber{$Hislands[$i]->{'id'}} = $i;
          }
       }

       if($Htournament == 1 and $HislandChart) {
          # トーナメント表形式

          # 上から順番に割り振り
          my $chart  = $HislandChart;
          while($chart =~ s/$HislandFightCount,([0-9]+),//) {
             my $num = $HidToNumber{$1};
             my $island  = $Hislands[$num];

             if($chart =~ s/$HislandFightCount,([0-9]+),//) {
                my $num2 = $HidToNumber{$1};
                my $tIsland = $Hislands[$num2];
                $island->{'fight_id'}  = $tIsland->{'id'};
                $tIsland->{'fight_id'} = $island->{'id'};
             } else {
                # 不戦勝
                $island->{'fight_id'} = -1;
                $island->{'rest'}    += $HnofightTurn + $HislandFightCount * $HnofightUp;
             }
          }
       } else {
          # 島力順

          # 島力計算
          for($i = 0; $i < $HislandNumber; $i++) {
             doIslandPower($Hislands[$i]);
          }

          # 島力順にソート
          islandPowerSort();

          # 対戦相手決定
          for($i = 0; $i < $HislandNumber; $i++) {
             $island = $HislandPower[$i];
             next if($island->{'fight_id'} > 0);

             if($i + 1 == $HislandNumber) {
                # 不戦勝 開発停止
                $island->{'fight_id'} = -1;
                $island->{'rest'}	  += $HnofightTurn + $HislandFightCount * $HnofightUp;
                $HislandChart .= "0,$island->{'id'},$island->{'name'}島\"0,-\"";
             } else {
                $tIsland = $HislandPower[$i+1];
                $island->{'fight_id'} = $tIsland->{'id'};
                $tIsland->{'fight_id'} = $island->{'id'};
                $HislandChart .= "0,$island->{'id'},$island->{'name'}島\"0,$tIsland->{'id'},$tIsland->{'name'}島\"";
             }
          }
       }

       if($Htournament == 1) {
          require('hako-chart.cgi');
          makeChartPage();
       }
	}

	# 対戦の記録バックアップ用
	if(($winlose == 1) or (($HislandTurn % $HbackupTurn) == 0)){
		open(FOUT, "${HdirName}/fight.log");
		while($f = <FOUT>){
			chomp($f);
			push(@offset,"$f\n");
		}
		close(FOUT);
	}

	# バックアップターンであれば、書く前にrename
	if(($HislandTurn % $HbackupTurn) == 0) {
		my($i);
		my($tmp) = $HbackupTimes - 1;
		myrmtree("${HdirName}.bak$tmp");
		for($i = ($HbackupTimes - 1); $i > 0; $i--) {
			my($j) = $i - 1;
			rename("${HdirName}.bak$j", "${HdirName}.bak$i");
		}
		rename("${HdirName}", "${HdirName}.bak0");
		mkdir("${HdirName}", $HdirMode);

		# ログファイルだけ戻す
		for($i = 0; $i <= $HlogMax; $i++) {
			rename("${HdirName}.bak0/hakojima.log$i",
				   "${HdirName}/hakojima.log$i");
		}
		rename("${HdirName}.bak0/hakojima.his",
			   "${HdirName}/hakojima.his");

		# 対戦の記録保存
		open(BDOUT, ">${HdirName}/fight.log.bak");
		print BDOUT @offset;
		close(BDOUT);
		rename("${HdirName}/fight.log.bak","${HdirName}/fight.log");
	}

	Hlog_yosen() if($HislandTurn == $HyosenTurn);

	Hfihgt_log() if($winlose == 1);

	# ファイルに書き出し
	writeIslandsFile(-1);

	# ファイル読み込み
	readIslandsFile();

	# ログ書き出し
	logFlush();

	# ログ削除
	log_delete() if(@delete_log);

	# 記録ログ調整
	logHistoryTrim();

	# トップへ
	topPageMain();
}

# ディレクトリ消し
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

# 収入、消費フェイズ
sub income {
	my($island) = @_;
	my($pop, $farm, $factory, $mountain) = 
		(	  
		 $island->{'pop'},
		 $island->{'farm'} * 10,
		 $island->{'factory'},
		 $island->{'mountain'}
		 );

	# 収入
	if($pop > $farm) {
		# 農業だけじゃ手が余る場合
		$island->{'food'} += $farm; # 農場フル稼働
		$island->{'money'} +=
			min(int(($pop - $farm) / 10), $factory + $mountain);
	} else {
		# 農業だけで手一杯の場合
		$island->{'food'} += $pop; # 全員野良仕事
	}

	# 食料消費
	$island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
	$island->{'down'} = 1 if($pop - ($farm + $factory * 10 + $mountain * 10) >= $Hno_work);
}


# コマンドフェイズ
sub doCommand {
	my($island) = @_;

	# コマンド取り出し
	my($comArray, $command);
	$comArray = $island->{'command'};
	$command = $comArray->[0];		# 最初のを取り出し
	slideFront($comArray, 0);		# 以降を詰める

	# 各要素の取り出し
	my($kind, $target, $x, $y, $arg) = 
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];
	my($cost) = $HcomCost[$kind];
	my($comName) = $HcomName[$kind];
	my($point) = "($x, $y)";
	my($landName) = landName($landKind, $lv);

	if($kind == $HcomDoNothing) {
		# 資金繰り
		logDoNothing($id, $name, $comName);
		$island->{'money'} += 10;
		$island->{'absent'} ++;
		
		# 自動放棄
		if($island->{'absent'} >= $HgiveupTurn) {
			$comArray->[0] = {
				'kind' => $HcomGiveup,
				'target' => 0,
				'x' => 0,
				'y' => 0,
				'arg' => 0
			}
		}
		return 1;
	}

	$island->{'absent'} = 0;

	# コストチェック
	if($cost > 0) {
		# 金の場合
		if($island->{'money'} < $cost) {
			logNoMoney($id, $name, $comName);
			return 0;
		}
	} elsif($cost < 0) {
		# 食料の場合
		if($island->{'food'} < (-$cost)) {
			logNoFood($id, $name, $comName);
			return 0;
		}
	}

	if(($kind == $HcomAutoPrepare3 or $kind == $HcomFastFarm) and ($HislandFightMode == 1)){
		logLandNG($id, $name, $comName, '現在戦闘期間中のため');
		return 0;
	}

	# コマンドで分岐
	if(($kind == $HcomPrepare) ||
	   ($kind == $HcomPrepare2)) {
		# 整地、地ならし
		if(($landKind == $HlandSea) || 
		   ($landKind == $HlandMountain)) {
			# 海、山、怪獣は整地できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, '整地', $point);

		# 金を差し引く
		$island->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# 地ならし
			# ターン消費せず
			return 0;
		} else {
			# 整地
			return 1;
		}
	} elsif($kind == $HcomAutoPrepare3) {
		# 一括自動地ならし
		my($prepareM, $preFlag) = ($HcomCost[$HcomPrepare2], 0);
		for($i = 0; $i < $HpointNumber; $i++) {
			$bx = $Hrpx[$i];
			$by = $Hrpy[$i];
			if(($land->[$bx][$by] == $HlandWaste) && ($island->{'money'} >= $prepareM)){
				# 目的の場所を平地にする
				$land->[$bx][$by] = $HlandPlains;
				$landValue->[$bx][$by] = 0;
				logLandSuc($id, $name, '整地', "($bx, $by)");
				# 金を差し引く
				$island->{'money'} -= $prepareM;
				$island->{'prepare2'}++;
				$preFlag++;
				if($preFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
		# ターン消費せず
		return 0;
	} elsif($kind == $HcomReclaim) {
		# 埋め立て
		if($landKind != $HlandSea) {
			# 海、しか埋め立てできない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 周りに陸があるかチェック
		my($seaCount) =	(countAround($land, $x, $y, $HlandSea, 7));

		if($seaCount == 7) {
			# 全部海だから埋め立て不能
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if(($landKind == $HlandSea and $lv == 1) or $HeasyReclaim) {
			# 浅瀬の場合
			# 目的の場所を荒地にする
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, $comName, $point);
			$island->{'area'}++;

			if($seaCount <= 4) {
				# 周りの海が3ヘックス以内なので、浅瀬にする
				my($i, $sx, $sy);

				for($i = 1; $i < 7; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];

					# 行による位置調整
					if((($sy % 2) == 0) && (($y % 2) == 1)) {
						$sx--;
					}

					if(($sx < 0) || ($sx >= $HislandSize) ||
					   ($sy < 0) || ($sy >= $HislandSize)) {
					} else {
						# 範囲内の場合
						if($land->[$sx][$sy] == $HlandSea) {
							$landValue->[$sx][$sy] = 1;
						}
					}
				}
			}
		} else {
			# 海なら、目的の場所を浅瀬にする
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			logLandSuc($id, $name, $comName, $point);
		}
		
		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomDestroy) {
		# 掘削
		if($landKind == $HlandSea and $lv == 0) {
			# 海は掘削できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
		if($landKind == $HlandMountain) {
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
		} elsif($landKind == $HlandSea) {
			$landValue->[$x][$y] = 0;
		} else {
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'area'}--;
		}
		logLandSuc($id, $name, $comName, $point);

		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomSellTree) {
		# 伐採
		if(!(($landKind == $HlandForest) || ($landKind == $HlandDefence))) {
			# 森、防衛施設以外は伐採できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);

		# 売却金を得る
		if($landKind == $HlandDefence){
			$island->{'money'} += $HdefenceValue;
			logSecretSell($id, $name, $landName, $point);
		} else {
			$island->{'money'} += $HtreeValue * $lv;
		}

		return 0;
	} elsif(($kind == $HcomPlant) ||
			($kind == $HcomFarm) ||
			($kind == $HcomFactory) ||
			($kind == $HcomBase) ||
			($kind == $HcomHaribote) ||
			($kind == $HcomFastFarm) ||
			($kind == $HcomDbase)) {

		# 地上建設系
		if(!
		   (($landKind == $HlandPlains) ||
			($landKind == $HlandTown) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFastFarm)) ||
			(($landKind == $HlandFactory) && ($kind == $HcomFactory)))) {
			# 不適当な地形
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 種類で分岐
		if($kind == $HcomPlant) {
			# 目的の場所を森にする。
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # 木は最低単位
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			# 目的の場所をミサイル基地にする。
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # 経験値0
			logPBSuc($id, $name, $comName, $point) if($Hhide_missile);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_missile);
			$island->{'missile'}++ if($HislandFightMode == 1);
		} elsif($kind == $HcomHaribote) {
			# 目的の場所をハリボテにする
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
			logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
		} elsif($kind == $HcomFarm or $kind == $HcomFastFarm) {
			# 農場
			if($landKind == $HlandFarm) {
				# すでに農場の場合
				$landValue->[$x][$y] += 2; # 規模 + 2000人
				if($landValue->[$x][$y] > 50) {
					$landValue->[$x][$y] = 50; # 最大 50000人
				}
			} else {
				# 目的の場所を農場に
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10; # 規模 = 10000人
			}
			logPBSuc($id, $name, $comName, $point) if($Hhide_farm);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_farm);
			if($kind == $HcomFastFarm){
				$island->{'money'} -= $cost;
				return 0;
			}
		} elsif($kind == $HcomFactory) {
			# 工場
			if($landKind == $HlandFactory) {
				# すでに工場の場合
				$landValue->[$x][$y] += 10; # 規模 + 10000人
				if($landValue->[$x][$y] > 100) {
					$landValue->[$x][$y] = 100; # 最大 100000人
				}
			} else {
				# 目的の場所を工場に
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30; # 規模 = 10000人
			}
			logPBSuc($id, $name, $comName, $point) if($Hhide_factory);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_factory);
		} elsif($kind == $HcomDbase) {
			# 防衛施設
			# 目的の場所を防衛施設に
			$land->[$x][$y] = $HlandDefence;
			$landValue->[$x][$y] = 0;
			logPBSuc($id, $name, $comName, $point) if($Hhide_deffence);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_deffence);
			$island->{'missile'}++ if($HislandFightMode == 1);
		}

		# 金を差し引く
		$island->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
		if(($kind == $HcomFarm) ||
		   ($kind == $HcomFactory)) {
			if($arg > 1) {
				my($command);
				$arg--;
				slideBack($comArray, 0);
				$comArray->[0] = {
					'kind' => $kind,
					'target' => $target,
					'x' => $x,
					'y' => $y,
					'arg' => $arg
					};
			}
		}

		return 1;
	} elsif($kind == $HcomMountain) {
		# 採掘場
		if($landKind != $HlandMountain) {
			# 山以外には作れない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		$landValue->[$x][$y] += 5; # 規模 + 5000人
		if($landValue->[$x][$y] > 200) {
			$landValue->[$x][$y] = 200; # 最大 200000人
		}
		logLandSuc($id, $name, $comName, $point);

		# 金を差し引く
		$island->{'money'} -= $cost;
		if($arg > 1) {
			my($command);
			$arg--;
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg
				};
		}
		return 1;
	} elsif($kind == $HcomMissileNM || $kind == $HcomMissilePP) {
		# ミサイル系
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		my($flag) = 0;
		if($arg == 0) {
			# 0の場合は撃てるだけ
			$arg = 10000;
		}

		# 事前準備
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tx, $ty, $err);

		# 発射可否確認
		if($HislandFightMode == 0) {
			# 開発期間なので中止
			logLandNG($id, $name, $comName, '現在開発期間中のため');
			return 0;
		} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
			# 対戦相手じゃない場合は中止
			logLandNG($id, $name, $comName, '目標が対戦相手でないため');
			return 0;
		}

		# 難民の数
		my($boat) = 0;

		# 誤差
		if($kind == $HcomMissilePP) {
			$err = 7;
		} else {
			$err = 19;
		}

		# 戦闘行為回数カウント
		$island->{'missile'}++ if($HislandFightMode == 1);

		# 金が尽きるか指定数に足りるか基地全部が撃つまでループ
		my($bx, $by, $count, $ms_count) = (0,0,0,0);
		while(($arg > 0) &&
			  ($island->{'money'} >= $cost)) {
			# 基地を見つけるまでループ
			while($count < $HpointNumber) {
				$bx = $Hrpx[$count];
				$by = $Hrpy[$count];
				if($land->[$bx][$by] == $HlandBase) {
					last;
				}
				$count++;
			}
			if($count >= $HpointNumber) {
				# 見つからなかったらそこまで
				last;
			}
			# 最低一つ基地があったので、flagを立てる
#			$flag++;

			# 基地のレベルを算出
			my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
			# 基地内でループ
			while(($level > 0) &&
				  ($arg > 0) &&
				  ($island->{'money'} > $cost)) {
				# 撃ったのが確定なので、各値を消耗させる
				$level--;
				$arg--;
				$island->{'money'} -= $cost;

				# ミサイル発射数カウント
				$island->{'fly'}++;
				$tIsland->{'fly'}++;
				$flag++;

				# 着弾点算出
				my($r) = random($err);
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				if((($ty % 2) == 0) && (($y % 2) == 1)) {
					$tx--;
				}

				# 着弾点範囲内外チェック
				if(($tx < 0) || ($tx >= $HislandSize) ||
				   ($ty < 0) || ($ty >= $HislandSize)) {
					# 範囲外
					logMsOut($id, $target, $name, $tName,  $comName, $point);
					next;
				}

				# 着弾点の地形等算出
				my($tL) = $tLand->[$tx][$ty];
				my($tLv) = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# 防衛施設判定
				my($defence) = 0;
				if($HdefenceHex[$id][$tx][$ty] == 1) {
					$defence = 1;
				} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
					$defence = 0;
				} else {
					if($tL == $HlandDefence) {
						# 防衛施設に命中
						# フラグをクリア
						my($i, $count, $sx, $sy);
						for($i = 0; $i < 19; $i++) {
							$sx = $tx + $ax[$i];
							$sy = $ty + $ay[$i];

							# 行による位置調整
							if((($sy % 2) == 0) && (($ty % 2) == 1)) {
								$sx--;
							}

							if(($sx < 0) || ($sx >= $HislandSize) ||
							   ($sy < 0) || ($sy >= $HislandSize)) {
								# 範囲外の場合何もしない
							} else {
								# 範囲内の場合
								$HdefenceHex[$id][$sx][$sy] = 0;
							}
						}
					} elsif(countAround($tLand, $tx, $ty, $HlandDefence, 19)) {
						$HdefenceHex[$id][$tx][$ty] = 1;
						$defence = 1;
					} else {
						$HdefenceHex[$id][$tx][$ty] = -1;
						$defence = 0;
					}
				}

				if($defence == 1) {
					# 空中爆破
					logMsCaught($id, $target, $name, $tName, $comName, $point, $tPoint);
					next;
				}

				# 「効果なし」hexを最初に判定  海または山
				if($tL == $HlandSea || $tL == $HlandMountain) {
					$tLname = landName($tL, $tLv);

					# 無効化
					logMsNoDamage($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
					next;
				}

				# ミサイル
				if($tL == $HlandWaste) {
					# 荒地(被害なし)
					logMsWaste($id, $target, $name, $tName,	$comName, $tLname, $point, $tPoint);
				} else {
					# 通常地形
					logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
				}

				# 経験値
				if($tL == $HlandTown) {
					if($land->[$bx][$by] == $HlandBase) {
						$landValue->[$bx][$by] += int($tLv / 20);
						$boat += $tLv; # 通常ミサイルなので難民にプラス
						if($landValue->[$bx][$by] > $HmaxExpPoint) {
							$landValue->[$bx][$by] = $HmaxExpPoint;
						}
					}
				} elsif($tL == $HlandDefence){
					# 対戦の記録用保持
					$island->{'log'} += 1000;
					$tIsland->{'reward'} += $HcomCost[$HcomDbase] if($HrewardMode == 2);
				} elsif($tL == $HlandBase){
					$island->{'log'} ++;
					$tIsland->{'reward'} += $HcomCost[$HcomBase] if($HrewardMode == 2);
				} elsif($tL == $HlandFarm and $HrewardMode == 2){
					$tIsland->{'reward'} += $HcomCost[$HcomFarm];
				} elsif($tL == $HlandFactory and $HrewardMode == 2){
					$tIsland->{'reward'} += $HcomCost[$HcomFactory];
				}

				
				# 荒地になる
				$tLand->[$tx][$ty] = $HlandWaste;
				$tLandValue->[$tx][$ty] = 1; # 着弾点

			}

			# カウント増やしとく
			$count++;
		}


		if($flag > 0) {
			# ミサイル発射数
			logComMissle($id, $name, $tName, $comName, $point, $flag) if($Hmissile_log);
		} else {
			# 基地が一つも無かった場合
			logMsNoBase($id, $name, $comName);
			return 0;
		}

		# 難民判定
		$boat = int($boat / 2);
		if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
			# 難民漂着
			my($achive); # 到達難民
			my($i);
			for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if($land->[$bx][$by] == $HlandTown) {
					# 町の場合
					my($lv) = $landValue->[$bx][$by];
					if($boat > 50) {
						$lv += 50;
						$boat -= 50;
						$achive += 50;
					} else {
						$lv += $boat;
						$achive += $boat;
						$boat = 0;
					}
					if($lv > 200) {
						$boat += ($lv - 200);
						$achive -= ($lv - 200);
						$lv = 200;
					}
					$landValue->[$bx][$by] = $lv;
				} elsif($land->[$bx][$by] == $HlandPlains) {
					# 平地の場合
					$land->[$bx][$by] = $HlandTown;;
					if($boat > 10) {
						$landValue->[$bx][$by] = 5;
						$boat -= 10;
						$achive += 10;
					} elsif($boat > 5) {
						$landValue->[$bx][$by] = $boat - 5;
						$achive += $boat;
						$boat = 0;
					}
				}
				if($boat <= 0) {
					last;
				}
			}
			if($achive > 0) {
				# 少しでも到着した場合、ログを吐く
				logMsBoatPeople($id, $name, $achive);

				# 難民の数が一定数以上なら、平和賞の可能性あり
				if($achive >= 200) {
					my($flags) = $island->{'prize'};

					if((!($flags & 8)) &&  $achive >= 200){
						$flags |= 8;
						logPrize($id, $name, $Hprize[4]);
					} elsif((!($flags & 16)) &&  $achive > 500){
						$flags |= 16;
						logPrize($id, $name, $Hprize[5]);
					} elsif((!($flags & 32)) &&  $achive > 800){
						$flags |= 32;
						logPrize($id, $name, $Hprize[6]);
					}
					$island->{'prize'} = $flags;
				}
			}
		}
		return 1;
	} elsif($kind == $HcomSell) {
		# 輸出量決定
		if($arg == 0) { $arg = 1; }
		my($value) = min($arg * (-$cost), $island->{'food'});

		# 輸出ログ
		logSell($id, $name, $comName, $value);
		$island->{'food'} -=  $value;
		$island->{'money'} += ($value / 10);
		return 0;
	} elsif($kind == $HcomGiveup) {
		# 放棄
		logGiveup($id, $name);
		$island->{'dead'} = 1;
		return 1;
	}

	return 1;
}


# 成長および単ヘックス災害
sub doEachHex {
	my($island) = @_;

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# 増える人口のタネ値
	my($addpop)  = $HtownUp;  # 村、町
	$addpop = 0 if(($HislandTurn <= $HyosenTurn) and 	# 連続資金繰りか、生産施設足りない場合ストップ
				($island->{'absent'} >= $HstopAddPop or $island->{'down'}));
	$addpop = -30 if($island->{'food'} < 0);	# 食料不足

	# ループ
	my($x, $y, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];

		if($landKind == $HlandTown) {
			# 町系
			if($addpop < 0) {
				# 不足
				$lv -= (random(-$addpop) + 1);
				if($lv <= 0) {
					# 平地に戻す
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} elsif($addpop > 0) {
				# 成長
				if($lv < 100) {
					$lv += random($addpop) + 1;
					$lv = 100 if($lv > 100);
				}
			}

			$lv = 200 if($lv > 200);
			$landValue->[$x][$y] = $lv;
		} elsif($landKind == $HlandPlains and $addpop > 0) {
			# 平地
			if($HtownGlow >=random(100)) {
				# 周りに農場、町があれば、ここも町になる
				if(countGrow($land, $landValue, $x, $y)){
					$land->[$x][$y] = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
		} elsif($landKind == $HlandForest) {
			# 森
			$lv += $HtreeUp;			# 木を増やす
			$lv = 200 if($lv > 200);	# 最大数超えた場合
			$landValue->[$x][$y] = $lv; # 代入
		}
	}

	if($HislandFightMode == 1) {
		if((int($HfightTurn / 2) == ($HislandChangeTurn - $HislandTurn)) and ($island->{'missile'} < $do_fight)) {
			if($island->{'fight_id'} > 0) {
				my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
				my $tIsland = $Hislands[$HcurrentNumber];
				if($tIsland->{'dead'} == 0) {
					logGiveup_no_do_fight($id, $name);
					$island->{'dead'} = 1;
				}
			}
		}
	}

}

# 周囲の町、農場があるか判定
sub countGrow {
	my($land, $landValue, $x, $y) = @_;
	my($i, $sx, $sy);
	for($i = 1; $i < 7; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # 行による位置調整
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
		 } else {
			 # 範囲内の場合
			 if(($land->[$sx][$sy] == $HlandTown) ||
				($land->[$sx][$sy] == $HlandFarm)) {
				 if($landValue->[$sx][$sy] != 1) {
					 return 1;
				 }
			 }
		 }
	}
	return 0;
}

# 島全体
sub doIslandProcess {
	my($number, $island) = @_;

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# 食料不足
	if($island->{'food'} < 0) {
		# 不足メッセージ
		logStarve($id, $name);
		$island->{'food'} = 0;

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind == $HlandFarm) ||
			   ($landKind == $HlandFactory) ||
			   ($landKind == $HlandBase) ||
			   ($landKind == $HlandDefence)) {
				# 1/4で壊滅
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
			}
		}
	}


	# 地盤沈下判定
	if(($island->{'area'} > $HdisFallBorder) &&
	   (random(1000) < $HdisFalldown)) {
		# 地盤沈下発生
		logFalldown($id, $name);

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind != $HlandSea) &&
			   ($landKind != $HlandMountain)) {

				# 周囲に海があれば、値を-1に
				if(countAround($land, $x, $y, $HlandSea, 7)) {
					logFalldownLand($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = -1;
					$landValue->[$x][$y] = 0;
				}
			}
		}

		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];

			if($landKind == -1) {
				# -1になっている所を浅瀬に
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 1;
			} elsif ($landKind == $HlandSea) {
				# 浅瀬は海に
				$landValue->[$x][$y] = 0;
			}

		}
	}

	# 食料があふれてたら換金
	if($island->{'food'} > 9999) {
		$island->{'money'} += int(($island->{'food'} - 9999) / 10);
		$island->{'food'} = 9999;
	} 

	# 各種の値を計算
	estimate($number);

	# 繁栄、災難賞
	$pop = $island->{'pop'};
	my($damage) = $island->{'oldPop'} - $pop;
	my($flags) = $island->{'prize'};

	# 繁栄賞
	if((!($flags & 1)) &&  $pop >= 3000){
		$flags |= 1;
		logPrize($id, $name, $Hprize[1]);
	} elsif((!($flags & 2)) &&  $pop >= 5000){
		$flags |= 2;
		logPrize($id, $name, $Hprize[2]);
	} elsif((!($flags & 4)) &&  $pop >= 10000){
		$flags |= 4;
		logPrize($id, $name, $Hprize[3]);
	}

	# 災難賞
	if((!($flags & 64)) &&  $damage >= 500){
		$flags |= 64;
		logPrize($id, $name, $Hprize[7]);
	} elsif((!($flags & 128)) &&  $damage >= 1000){
		$flags |= 128;
		logPrize($id, $name, $Hprize[8]);
	} elsif((!($flags & 256)) &&  $damage >= 2000){
		$flags |= 256;
		logPrize($id, $name, $Hprize[9]);
	}

	$island->{'prize'} = $flags;
}

# 島力計算
sub doIslandPower {
	my($island) = @_;

	my $power = 25 * ($island->{'farm'} + $island->{'factory'} + $island->{'mountain'} + $island->{'pop'} / 10)
	 + 700 * $island->{'area'} + 1000 * $island->{'army'} + 
	 aboutMoney2($island->{'money'}) + $island->{'forest'} - $island->{'waste'};

	$island->{'power'} = random($power) if $power > 0;
}

# 島力順にソート
sub islandPowerSort {
	my($flag, $i, $tmp);

	# 人口が同じときは直前のターンの順番のまま
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'power'} <=> $Hislands[$a]->{'power'} || $a <=> $b } @idx;
	@HislandPower = @Hislands[@idx];
}

# 人口順にソート
sub islandSort {
	my($flag, $i, $tmp);

	# 人口が同じときは直前のターンの順番のまま
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];
}

# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手
# 通常ログ
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 遅延ログ
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 機密ログ
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ミサイル発射ログ
sub logOutM {
	push(@HlogPool,"2,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 記録ログ
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 記録ログ調整
sub logHistoryTrim {
	open(HIN, "${HdirName}/hakojima.his");
	my(@line, $l, $count);
	$count = 0;
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
		$count++;
	}
	close(HIN);

	if($count > $HhistoryMax) {
		open(HOUT, ">${HdirName}/hakojima.his");
		my($i);
		for($i = ($count - $HhistoryMax); $i < $count; $i++) {
			print HOUT "$line[$i]\n";
		}
		close(HOUT);
	}
}

# ログ書き出し
sub logFlush {
	open(LOUT, ">${HdirName}/hakojima.log0");

	# 全部逆順にして書き出す
	my($i);
	for($i = $#HsecretLogPool; $i >= 0; $i--) {
		print LOUT $HsecretLogPool[$i];
		print LOUT "\n";
	}
	for($i = $#HlateLogPool; $i >= 0; $i--) {
		print LOUT $HlateLogPool[$i];
		print LOUT "\n";
	}
	for($i = $#HlogPool; $i >= 0; $i--) {
		print LOUT $HlogPool[$i];
		print LOUT "\n";
	}
	close(LOUT);
}

# ログ削除
sub log_delete {
	my ($line,$bk);
	for($i = 0;$i < $HlogMax;$i++) {
		my @lines;
		my @olines;
		open(LIN, "${HdirName}/hakojima.log${i}");
		@lines = <LIN>;
		close(LIN);

		foreach $line (@lines) {
			my $ng = 0;
			$bk = $line;
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
			($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);
			for($f = 0;$f <= $#delete_log;$f++) {
				$ng = 1 if($delete_log[$f] == $id1 or $delete_log[$f] == $id2);
			}
			push(@olines,$bk) if($ng == 0);
		}

		open(LOUT, ">${HdirName}/hakojima.log${i}");
		print LOUT @olines;
		close(LOUT);
	}
}

#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------
sub log_debug {
	my($one, $two, $three) = @_;
	logOut("$one - $two - $three");
}

# 勝利ログ
sub logWin {
	my($id, $name, $money) = @_;
	my $fTurn = $HislandFightCount + 1;
	if($HislandNumber == 4) {
		$fTurn = '決勝戦';
	} elsif($HislandNumber == 8) { 
		$fTurn = '準決勝';
	} else {
		$fTurn .= '回戦';
	}
	if($HislandNumber == 2) {
		logOut("${HtagName_}${name}島${H_tagName}勝利し、<B>優勝！！</B>",$id);
		logHistory("${HtagName_}${name}島${H_tagName}、<B>優勝！！</B>");
	} elsif($money == 0) {
		logOut("${HtagName_}${name}島${H_tagName}勝利し、<B>$fTurn進出！</B>",$id);
	} else {
		logOut("${HtagName_}${name}島${H_tagName}勝利し、<B>$fTurn進出！　$money$HunitMoney</B>の報酬金が支払われました。",$id);
	}
}

# 敗退
sub logLose {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}、<B>敗退</B>。",$id);
}

# 予選落ち
sub logLoseOut {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}、<B>予選落ち</B>。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、<B>予選落ち</B>。");
}

# 開発期間のため失敗
sub logLandNG {
	my($id, $name, $comName, $cancel) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>$cancel</B>、実行できませんでした。",$id);
END
}

# 資金足りない
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、資金不足のため中止されました。",$id);
}

# 食料足りない
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、備蓄食料不足のため中止されました。",$id);
}

# 対象地形の種類による失敗
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logSecret("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}が<B>$kind</B>だったため中止されました。",$id);
END
}

# 周りに陸がなくて埋め立て失敗
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に陸地がなかったため中止されました。",$id);
END
}

# 整地系成功
sub logLandSuc {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
END
}

# 植林orミサイル基地
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logOut("こころなしか、${HtagName_}${name}島${H_tagName}の<B>森</B>が増えたようです。",$id);
END
}

# 防衛施設売却
sub logSecretSell {
    my($id, $name, $landName, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}地点の<B>${landName}</b>が、${HtagComName_}売却${H_tagComName}されました。",$id);
END
}

# ハリボテ
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logLandSuc($id, $name, $comName2, $point);
END
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)がターゲットがいない
sub logMsNoTarget {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標の島に人が見当たらないため中止されました。",$id);
END
}

# ミサイル発射実行
sub logComMissle {
	my($id, $name, $tName, $comName, $point, $count) = @_;
	logOutM("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて<b>$count発</b>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
END
}

# ミサイル撃とうとしたが基地がない
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>ミサイル設備を保有していない</B>ために実行できませんでした。",$id);
END
}

# ミサイル撃ったが範囲外
sub logMsOut {
	my($id, $tId, $name, $tName, $comName, $point) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
}

# ミサイル撃ったが防衛施設でキャッチ
sub logMsCaught {
	my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
}

# ミサイル撃ったが効果なし
sub logMsNoDamage {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);
}

# 通常ミサイル、荒地に着弾
sub logMsWaste {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}

# ミサイル難民到着
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}島${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}島${H_tagName}は快く受け入れたようです。",$id);
}

# 資金繰り
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 輸出
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が<B>$value$HunitFood</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}

# 放棄
sub logGiveup {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}は放棄され、<B>無人島</B>になりました。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、放棄され<B>無人島</B>となる。");
}

# 追放
sub logGiveup_no_do_fight {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}は規程数戦闘行為を行わなかったため、<B>無人島</B>になりました。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、規程数戦闘行為を行わなかったため、<B>無人島</B>となる。");
}

# 死滅
sub logDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}から人がいなくなり、<B>無人島</B>になりました。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、人がいなくなり<B>無人島</B>となる。");
}

# 発見
sub logDiscover {
	my($name) = @_;
	my($ip) = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ip = $ENV{'REMOTE_ADDR'} if(!$ip);
	logHistory("${HtagName_}${name}島${H_tagName}が発見される。(${ip})");
}

# 名前の変更
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}島${H_tagName}、名称を${HtagName_}${name2}島${H_tagName}に変更する。");
}

# 飢餓
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",$id);
}

# 食料不足被害
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は壊滅しました。",$id);
}

# 地盤沈下発生
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",$id);
}

# 地盤沈下被害
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",$id);
}

# 受賞
sub logPrize {
	my($id, $name, $pName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が<B>$pName</B>を受賞しました。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、<B>$pName</B>を受賞");
}

# 島がいっぱいな場合
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}申し訳ありません、島が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で名前がない場合
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}島につける名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規で名前が不正な場合
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',"?()<>\$'とか入ってたり、「無人島」とかいった変な名前はやめましょうよ〜${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}その島ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# 二度目の登録の場合
sub tempRegistFailed {
	out(<<END);
${HtagBig_}連続して登録は出来ません。${H_tagBig}$HtempBack
END
}

# パスワードがない場合
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function ShowMsg(n){
	status = n;
}
//-->
</SCRIPT>
<CENTER>
${HtagBig_}島を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}と命名します。${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# 地形の呼び方
sub landName {
	my($land, $lv) = @_;
	if($land == $HlandSea) {
		if($lv == 1) {
			return '浅瀬';
		} else {
			return '海';
		}
	} elsif($land == $HlandWaste) {
		return '荒地';
	} elsif($land == $HlandPlains) {
		return '平地';
	} elsif($land == $HlandTown) {
		if($lv < 30) {
			return '村';
		} elsif($lv < 100) {
			return '町';
		} else {
			return '都市';
		}
	} elsif($land == $HlandForest) {
		return '森';
	} elsif($land == $HlandFarm) {
		return '農場';
	} elsif($land == $HlandFactory) {
		return '工場';
	} elsif($land == $HlandBase) {
		return 'ミサイル基地';
	} elsif($land == $HlandDefence) {
		return '防衛施設';
	} elsif($land == $HlandMountain) {
		return '山';
	} elsif($land == $HlandHaribote) {
		return 'ハリボテ';
	}
}

# 人口その他の値を算出
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $farm, $factory, $mountain, $burnmis, $forest) = (0, 0, 0, 0, 0, 0, 0, 0);
	my($waste, $army_m, $army_d) = (0, 0, 0);

	# 地形を取得
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# 数える
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if($kind != $HlandSea) {
				$area++;
				if($kind == $HlandTown) {
					# 町
					$pop += $value;
				} elsif($kind == $HlandFarm) {
					# 農場
					$farm += $value;
				} elsif($kind == $HlandFactory) {
					# 工場
					$factory += $value;
				} elsif($kind == $HlandMountain) {
					# 山
					$mountain += $value;
				} elsif($kind == $HlandBase) {
					# ミサイル基地
					$burnmis += expToLevel($kind, $value);
					$army_m++;
				} elsif($kind == $HlandDefence) {
					# 防衛施設
					$army_d++;
				} elsif($kind == $HlandWaste and $value == 1) {
					# ミサイル跡
					$waste++;
				} elsif($kind == $HlandForest) {
					# 森
					$forest += $value;
				}
			}
		}
	}

	# 代入
	$island->{'pop'}	  = $pop;
	$island->{'area'}	  = $area;
	$island->{'farm'}	  = $farm;
	$island->{'factory'}  = $factory;
	$island->{'mountain'} = $mountain;
	$island->{'fire'}	  = $burnmis;
	$island->{'army'}	  = $army_m + $army_d;
	$island->{'forest'}	  = $forest * $HtreeValue;
	$island->{'waste'}	  = $waste * $HcomCost[$HcomPrepare2]; # 地ならし代

	if($winlose == 2 and $HrewardMode != 2 and $island->{'reward'} == 0) {
		$island->{'reward'} = $army_m + $army_d * 2;
	}
}

# 戦闘期間開始時の島の状態を保存
sub island_save {
	my($island) = @_;
	my($id) = $island->{'id'};

	open(IOUT, ">${Hdirmdata}/islandtmp.$island->{'id'}");
	print IOUT $island->{'money'}."\n";
	print IOUT $island->{'food'}."\n";

	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			printf IOUT ("%x%02x", $land->[$x][$y], $landValue->[$x][$y]);
		}
		print IOUT "\n";
	}
	close(IOUT);
	unlink("${Hdirmdata}/island.$island->{'id'}");
	rename("${Hdirmdata}/islandtmp.$island->{'id'}", "${Hdirmdata}/island.$island->{'id'}");
}

# 敗者の島の状態保存
sub save_lose_island {
	my($island) = @_;
	my($id) = $island->{'id'};

	open(IOUT, ">${Hdirfdata}/islandtmp.$island->{'id'}");
	print IOUT $island->{'name'}."\n";

	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			printf IOUT ("%x%02x", $land->[$x][$y], $landValue->[$x][$y]);
		}
		print IOUT "\n";
	}
	close(IOUT);
	unlink("${Hdirfdata}/island.$island->{'id'}");
	rename("${Hdirfdata}/islandtmp.$island->{'id'}", "${Hdirfdata}/island.$island->{'id'}");
}

# 戦闘期間中に不戦勝
sub fight_no_fight {
	my $id = $_[0];
	my $HcurrentNumber = $HidToNumber{$id};
	my $island = $Hislands[$HcurrentNumber];

	return 0 if($HcurrentNumber eq "");
	my $rest_turn = ($HnofightTurn + $HislandFightCount * $HnofightUp) - ($HfightTurn - ($HislandChangeTurn - $HislandTurn));
	$island->{'rest'} += $rest_turn if($rest_turn > 0);
	open(IN, "$Hdirmdata/island.$island->{'id'}");
	$island->{'money'}  = int(<IN>);
	$island->{'food'} = int(<IN>);
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		$line = <IN>;
		for($x = 0; $x < $HislandSize; $x++) {
			$line =~ s/^(.)(..)//;
			$island->{'land'}[$x][$y] = hex($1);
			$island->{'landValue'}[$x][$y] = hex($2);
		}
	}
	close(IN);

	$island->{'fight_id'} = -1;
	push(@delete_log,$island->{'id'});

	# 各種の値を計算
	estimate($HcurrentNumber);
}


# 範囲内の地形を数える
sub countAround {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # 行による位置調整
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
			 # 範囲外の場合
			 if($kind == $HlandSea) {
				 # 海なら加算
				 $count++;
			 }
		 } else {
			 # 範囲内の場合
			 if($land->[$sx][$sy] == $kind) {
				 $count++;
			 }
		 }
	}
	return $count;
}

# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# 初期値
	if($n == 0) {
		$n = 1;
	}
	@list = (0..$n-1);

	# シャッフル
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		if($i == $j) { next; };
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

# 名前変更失敗
sub tempChangeNothing {
	out(<<END);
${HtagBig_}名前、パスワードともに空欄です${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}資金不足のため変更できません${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
	out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$HtempBack
END
}

1;
