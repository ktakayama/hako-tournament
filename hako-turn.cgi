#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# ������ʹԥ⥸�塼��
# $Id: hako-turn.cgi,v 1.6 2004/11/10 13:01:25 gaba Exp $

# ����2�إå����κ�ɸ
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandMain {
	# �礬���äѤ��Ǥʤ��������å�
	if($HislandNumber >= $HmaxIsland or $HislandTurn > 0) {
		unlock();
		tempNewIslandFull();
		return;
	}

	# ̾�������뤫�����å�
	if($HcurrentName eq '') {
		unlock();
		tempNewIslandNoName();
		return;
	}

	# ̾���������������å�
	if($HcurrentName =~ /[,\"\?\(\)\<\>\$]|^̵��$/) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempNewIslandBadName();
		return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
		# ���Ǥ�ȯ������
		unlock();
		tempNewIslandAlready();
		return;
	}

	# password��¸��Ƚ��
	if($HinputPassword eq '') {
		# password̵��
		unlock();
		tempNewIslandNoPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# �ʰ׽�ʣ�����å�
	if(registCheck()) {
		unlock();
		tempRegistFailed();
		return;
	}

	# ����������ֹ�����
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland();
	my($island) = $Hislands[$HcurrentNumber];

	# �Ƽ���ͤ�����
	$island->{'name'} = $HcurrentName;
	$island->{'id'} = $HislandNextID;
	$HislandNextID ++;
	$island->{'absent'} = 1;
	$island->{'comment'} = '(̤��Ͽ)';
	$island->{'password'} = encode($HinputPassword);
	
	# �͸�����¾����
	estimate($HcurrentNumber);

	# �ǡ����񤭽Ф�
	writeIslandsFile($island->{'id'});
	logDiscover($HcurrentName); # ��

	# ����
	unlock();

	# ȯ������
	tempNewIslandHead($HcurrentName); # ȯ�����ޤ���!!
	islandInfo(); # ��ξ���
	islandMap(1); # ����Ͽޡ�owner�⡼��
}

# ����������������
sub makeNewIsland {
	# �Ϸ�����
	my($land, $landValue) = makeNewLand();

	# ������ޥ�ɤ�����
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

	# ����Ǽ��Ĥ����
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		 $lbbs[$i] = "0>>";
	}

	# ��ˤ����֤�
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

# �ʰ׽�ʣ�����å�
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

# ����������Ϸ����������
sub makeNewLand {
	# ���ܷ������
	my(@land, @landValue, $x, $y, $i);

	# ���˽����
	for($y = 0; $y < $HislandSize; $y++) {
		 for($x = 0; $x < $HislandSize; $x++) {
			 $land[$x][$y] = $HlandSea;
			 $landValue[$x][$y] = 0;
		 }
	}

	# �����4*4�˹��Ϥ�����
	my($center) = int($HislandSize / 2 - 1);
	for($y = $center - 1; $y < $center + 3; $y++) {
		 for($x = $center - 1; $x < $center + 3; $x++) {
			 $land[$x][$y] = $HlandWaste;
		 }
	}

	# �������������Ѹ���롼��
	my($size,$seacon) = (16,0);

	# 8*8�ϰ����Φ�Ϥ�����
	while($size < $HlandSizeValue){
		# �������ɸ
		$x = random(8) + $center - 3;
		$y = random(8) + $center - 3;
		if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
			# �����Φ�Ϥ������硢�����ˤ���
			# �����Ϲ��Ϥˤ���
			# ���Ϥ�ʿ�Ϥˤ���
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

	# ������
	my($count) = 0;
	while($count < 4) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ���������Ǥ˿��Ǥʤ���С�������
		 if($land[$x][$y] != $HlandForest) {
			 $land[$x][$y] = $HlandForest;
			 $landValue[$x][$y] = 5; # �ǽ��500��
			 $count++;
		 }
	}

	# Į����
	$count = 0;
	while($count < 2) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ����������Į�Ǥʤ���С�Į����
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandTown;
			 $landValue[$x][$y] = 5; # �ǽ��500��
			 $count++;
		 }
	}

	# ������
	$count = 0;
	while($count < 1) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ����������Į�Ǥʤ���С�Į����
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandMountain;
			 $landValue[$x][$y] = 0; # �ǽ�Ϻη���ʤ�
			 $count++;
		 }
	}

	return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# �ѥ���ɥ����å�
	if($HoldPassword eq $HspecialPassword) {
		# �ü�ѥ����
		$island->{'money'} = 9999;
		$island->{'food'} = 9999;
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# ̾���ѹ��ξ��		
		# ̾���������������å�
		if($HcurrentName =~ /[,\"\?\(\)\<\>]|^̵��$/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadName();
			return;
		}

		# ̾���ν�ʣ�����å�
		if(nameToNumber($HcurrentName) != -1) {
			# ���Ǥ�ȯ������
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($island->{'money'} < $HcostChangeName) {
			# �⤬­��ʤ�
			unlock();
			tempChangeNoMoney();
			return;
		}

		# ���
		if($HoldPassword ne $HspecialPassword) {
			$island->{'money'} -= $HcostChangeName;
		}

		# ̾�����ѹ�
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;

        if($Htournament == 1) {
           require('hako-chart.cgi');
           makeChartPage();
        }
	}

	# password�ѹ��ξ��
	if($HinputPassword ne '') {
		# �ѥ���ɤ��ѹ�
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if($HownerName ne '') {
		# �����ʡ�̾���ѹ�
		$island->{'ownername'} = $HownerName;
		$flag = 1;
	}

	if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
		# �ɤ�����ѹ�����Ƥ��ʤ�
		unlock();
		tempChangeNothing();
		return;
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);
	unlock();

	# �ѹ�����
	tempChange();
}

#----------------------------------------------------------------------
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {

	# ���ե��������ˤ��餹
	my($i, $j, $s, $d);
	for($i = ($HlogMax - 1); $i >= 0; $i--) {
		$j = $i + 1;
		my($s) = "${HdirName}/hakojima.log$i";
		my($d) = "${HdirName}/hakojima.log$j";
		unlink($d);
		rename($s, $d);
	}

	# �ޤȤṹ�������
	$HislandTurnCount = $HyosenRepCount if($HislandTurn == 0);

	# ��ɸ�������
	makeRandomPointArray();

	# �������ֹ�
	$HislandTurn++;

	# ��Ʈ���֤ؤΰʹ���
	$winlose = 0;
	my $fight_check = 0;

	if($HislandTurn == $HislandChangeTurn && $HislandFightMode == 1) {
		$winlose = 1; # ��Ʈ���ֺǽ�������
		$fight_check = 1;
	} elsif($HislandTurn > $HislandChangeTurn) {
		if($HislandFightMode) {
			# ��Ʈ��λ�塢��ȯ���֤�
			$HislandFightMode = 0;
			$HislandFightCount++;
			$HislandChangeTurn += $HdevelopeTurn;
		} else {
			# ��ȯ��λ�塢��Ʈ���֤�
			$HislandFightMode = 1;
			$HislandChangeTurn += $HfightTurn;
			$winlose = 2;
			# ��ξ��֤���¸
			for($i = 0; $i < $HislandNumber; $i++) {
				island_save($Hislands[$i]);
			}
		}
	}

	# �ǽ��������֤򹹿�
	if($HislandTurnCount > 1) {
		$HislandTurnCount--;
	} elsif(($HislandTurn + $HfightRepCount - 1) == $HislandChangeTurn and $HislandFightMode) {
		# ��Ʈ���ֽ�λ��
		$HislandLastTime += $HinterTime;
		$HislandTurnCount = $HfightRepCount;
	} elsif($HislandFightMode) {
		# ��Ʈ����
		$HislandLastTime += $HfightTime;
		$HislandTurnCount = $HfightRepCount;
	} elsif(($HislandTurn + $HdeveRepCount - 1) == $HislandChangeTurn) {
		# ��ȯ���ֽ�λ��
		$HislandLastTime += $HfightTime;
		$HislandTurnCount = $HdeveRepCount;
	} elsif($HislandTurn <= $HyosenTurn) {
		# ͽ������
		$HislandLastTime += $HunitTime;
		$HislandTurnCount = $HyosenRepCount if($HislandTurn != $HyosenRepCount);
	} else {
		# ��ȯ����
		$HislandLastTime += $HdevelopeTime;
		$HislandTurnCount = $HdeveRepCount;
	}

	# ���ַ��
	my(@order) = randomArray($HislandNumber);

	# ����������ե�����
	for($i = 0; $i < $HislandNumber; $i++) {
		estimate($order[$i]);
		next if($Hislands[$order[$i]]->{'rest'} > 0); # ���ﾡ��ȯ�����
		income($Hislands[$order[$i]]);

		# �����󳫻����ο͸������
		$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	}

	# ���ޥ�ɽ���
	for($i = 0; $i < $HislandNumber; $i++) {
		next if($Hislands[$order[$i]]->{'rest'} > 0); # ���ﾡ��ȯ�����
		# �����1�ˤʤ�ޤǷ����֤�
		while(doCommand($Hislands[$order[$i]]) == 0){};
	}

	# ��Ĺ�����ñ�إå����ҳ�
	for($i = 0; $i < $HislandNumber; $i++) {
		# ���ﾡ��ȯ�����
		if($Hislands[$order[$i]]->{'rest'} > 0) {
			$Hislands[$order[$i]]->{'rest'}--;
			next;
		}
		doEachHex($Hislands[$order[$i]]);
	}


	# �����ν���
	my($remainNumber) = $HislandNumber;
	my($island);
	for($i = 0; $i < $HislandNumber; $i++) {
		$island = $Hislands[$order[$i]];

		doIslandProcess($order[$i], $island); 
		next if($island->{'rest'} > 0);
		# ����Ƚ��
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
				# ¼��Į�ʤɤ������ä����
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
			# ���ǥ�å�����
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
			# ��ȯ��������礬�ʤ��ʤä����ϡ������礬���ﾡ�ˤʤ�
			my $HcurrentNumber	= $HidToNumber{$island->{'fight_id'}};
			my $tIsland = $Hislands[$HcurrentNumber];
			if($HcurrentNumber ne '') {
				$tIsland->{'rest'}	+= $HnofightTurn + $HislandFightCount * $HnofightUp;
				$tIsland->{'fight_id'} = -1;
			}

		}
	}


	# ���Խ���
	if($winlose > 0) {

		$remainNumber = $HislandNumber;
		for($i = 0; $i < $HislandNumber; $i++) {
			$island = $Hislands[$i];

			my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
			my $tIsland = $Hislands[$HcurrentNumber];
			if($winlose == 1) {
				# ��Ʈ��ξ��ԡ��󽷶�
                my $id = $island->{'id'};
				if(($HcurrentNumber ne '' and $island->{'pop'} >= $tIsland->{'pop'}) or ($island->{'fight_id'} == -1)) {
					# ����

					my $reward = $island->{'waste'};
					my $tPop = 0;
					if($island->{'fight_id'} > 0) { # ���ﾡ���󽷶�ʤ�
						# �󽷶�����ˤ��ʬ��
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
                    $HislandChart =~ s/[0-9]+,$id,[^"]+"/$HislandFightCount,$id,$island->{'name'}��"/;
				} elsif($HcurrentNumber ne '' and $island->{'pop'} < $tIsland->{'pop'}) {
                   #$island->{'pop'} = 0;
					logLose($island->{'id'}, $island->{'name'});
					save_lose_island($island);
                    my $turn = $HislandFightCount - 1;
                    $HislandChart =~ s/[0-9]+,$id,[^"]+"/$turn,$id,$island->{'name'}��"/;
				}
				$island->{'reward'}	 = 0;
				$island->{'fly'}	 = 0;
				$island->{'missile'} = 0;
			} else {
				# �󽷶�ե饰����
				if($HcurrentNumber ne '') {
					if($island->{'reward_flag'} == 0 and $HrewardMode == 1) {
						my $my_reward = $island->{'reward'} + $tIsland->{'reward'};
						$island->{'reward'}		  = $my_reward;
						$tIsland->{'reward'}	  = $my_reward;
						$tIsland->{'reward_flag'} = 1;
					}
				} else {
					# ������꤬���ʤ����
					$island->{'reward'} = 0;
				}
			}
		}
	}

	# �͸���˥�����
	islandSort();

	# ͽ�����Ƚ��
	if($HislandTurn == $HyosenTurn) {
		$fight_check = 1;
		if($HislandNumber > $HfightMem) {
			$remainNumber = $HislandNumber;

			for($i = $HfightMem; $i < $HislandNumber; $i++) {
				# ͽ�����
				$island = $Hislands[$i];
				push(@yosen_log, "$island->{'pop'},$island->{'name'}");
				$island->{'pop'} = 0;
				$remainNumber--;
				logLoseOut($island->{'id'},$island->{'name'});
			}
		}
	}

	# ������å�
	$HislandNumber = $remainNumber;

	# ����������
	if($fight_check == 1) {
       if($Htournament == 1) {
          undef %HidToNumber;
          # HidToNumber �κ��� (������� islandSort ���Ƥ�Τ�)
          for($i = 0; $i < $HislandNumber; $i++) {
             my $island = $Hislands[$i];
             $HidToNumber{$Hislands[$i]->{'id'}} = $i;
          }
       }

       if($Htournament == 1 and $HislandChart) {
          # �ȡ��ʥ���ɽ����

          # �夫����֤˳�꿶��
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
                # ���ﾡ
                $island->{'fight_id'} = -1;
                $island->{'rest'}    += $HnofightTurn + $HislandFightCount * $HnofightUp;
             }
          }
       } else {
          # ���Ͻ�

          # ���Ϸ׻�
          for($i = 0; $i < $HislandNumber; $i++) {
             doIslandPower($Hislands[$i]);
          }

          # ���Ͻ�˥�����
          islandPowerSort();

          # ����������
          for($i = 0; $i < $HislandNumber; $i++) {
             $island = $HislandPower[$i];
             next if($island->{'fight_id'} > 0);

             if($i + 1 == $HislandNumber) {
                # ���ﾡ ��ȯ���
                $island->{'fight_id'} = -1;
                $island->{'rest'}	  += $HnofightTurn + $HislandFightCount * $HnofightUp;
                $HislandChart .= "0,$island->{'id'},$island->{'name'}��\"0,-\"";
             } else {
                $tIsland = $HislandPower[$i+1];
                $island->{'fight_id'} = $tIsland->{'id'};
                $tIsland->{'fight_id'} = $island->{'id'};
                $HislandChart .= "0,$island->{'id'},$island->{'name'}��\"0,$tIsland->{'id'},$tIsland->{'name'}��\"";
             }
          }
       }

       if($Htournament == 1) {
          require('hako-chart.cgi');
          makeChartPage();
       }
	}

	# ����ε�Ͽ�Хå����å���
	if(($winlose == 1) or (($HislandTurn % $HbackupTurn) == 0)){
		open(FOUT, "${HdirName}/fight.log");
		while($f = <FOUT>){
			chomp($f);
			push(@offset,"$f\n");
		}
		close(FOUT);
	}

	# �Хå����åץ�����Ǥ���С�������rename
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

		# ���ե���������᤹
		for($i = 0; $i <= $HlogMax; $i++) {
			rename("${HdirName}.bak0/hakojima.log$i",
				   "${HdirName}/hakojima.log$i");
		}
		rename("${HdirName}.bak0/hakojima.his",
			   "${HdirName}/hakojima.his");

		# ����ε�Ͽ��¸
		open(BDOUT, ">${HdirName}/fight.log.bak");
		print BDOUT @offset;
		close(BDOUT);
		rename("${HdirName}/fight.log.bak","${HdirName}/fight.log");
	}

	Hlog_yosen() if($HislandTurn == $HyosenTurn);

	Hfihgt_log() if($winlose == 1);

	# �ե�����˽񤭽Ф�
	writeIslandsFile(-1);

	# �ե������ɤ߹���
	readIslandsFile();

	# ���񤭽Ф�
	logFlush();

	# �����
	log_delete() if(@delete_log);

	# ��Ͽ��Ĵ��
	logHistoryTrim();

	# �ȥåפ�
	topPageMain();
}

# �ǥ��쥯�ȥ�ä�
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

# ����������ե�����
sub income {
	my($island) = @_;
	my($pop, $farm, $factory, $mountain) = 
		(	  
		 $island->{'pop'},
		 $island->{'farm'} * 10,
		 $island->{'factory'},
		 $island->{'mountain'}
		 );

	# ����
	if($pop > $farm) {
		# ���Ȥ�������꤬;����
		$island->{'food'} += $farm; # ����ե��Ư
		$island->{'money'} +=
			min(int(($pop - $farm) / 10), $factory + $mountain);
	} else {
		# ���Ȥ����Ǽ���դξ��
		$island->{'food'} += $pop; # �������ɻŻ�
	}

	# ��������
	$island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
	$island->{'down'} = 1 if($pop - ($farm + $factory * 10 + $mountain * 10) >= $Hno_work);
}


# ���ޥ�ɥե�����
sub doCommand {
	my($island) = @_;

	# ���ޥ�ɼ��Ф�
	my($comArray, $command);
	$comArray = $island->{'command'};
	$command = $comArray->[0];		# �ǽ�Τ���Ф�
	slideFront($comArray, 0);		# �ʹߤ�ͤ��

	# �����Ǥμ��Ф�
	my($kind, $target, $x, $y, $arg) = 
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );

	# Ƴ����
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
		# ��ⷫ��
		logDoNothing($id, $name, $comName);
		$island->{'money'} += 10;
		$island->{'absent'} ++;
		
		# ��ư����
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

	# �����ȥ����å�
	if($cost > 0) {
		# ��ξ��
		if($island->{'money'} < $cost) {
			logNoMoney($id, $name, $comName);
			return 0;
		}
	} elsif($cost < 0) {
		# �����ξ��
		if($island->{'food'} < (-$cost)) {
			logNoFood($id, $name, $comName);
			return 0;
		}
	}

	if(($kind == $HcomAutoPrepare3 or $kind == $HcomFastFarm) and ($HislandFightMode == 1)){
		logLandNG($id, $name, $comName, '������Ʈ������Τ���');
		return 0;
	}

	# ���ޥ�ɤ�ʬ��
	if(($kind == $HcomPrepare) ||
	   ($kind == $HcomPrepare2)) {
		# ���ϡ��Ϥʤ餷
		if(($landKind == $HlandSea) || 
		   ($landKind == $HlandMountain)) {
			# �����������ä����ϤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, '����', $point);

		# ��򺹤�����
		$island->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# �Ϥʤ餷
			# ��������񤻤�
			return 0;
		} else {
			# ����
			return 1;
		}
	} elsif($kind == $HcomAutoPrepare3) {
		# ��缫ư�Ϥʤ餷
		my($prepareM, $preFlag) = ($HcomCost[$HcomPrepare2], 0);
		for($i = 0; $i < $HpointNumber; $i++) {
			$bx = $Hrpx[$i];
			$by = $Hrpy[$i];
			if(($land->[$bx][$by] == $HlandWaste) && ($island->{'money'} >= $prepareM)){
				# ��Ū�ξ���ʿ�Ϥˤ���
				$land->[$bx][$by] = $HlandPlains;
				$landValue->[$bx][$by] = 0;
				logLandSuc($id, $name, '����', "($bx, $by)");
				# ��򺹤�����
				$island->{'money'} -= $prepareM;
				$island->{'prepare2'}++;
				$preFlag++;
				if($preFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
		# ��������񤻤�
		return 0;
	} elsif($kind == $HcomReclaim) {
		# ���Ω��
		if($landKind != $HlandSea) {
			# �����������Ω�ƤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# �����Φ�����뤫�����å�
		my($seaCount) =	(countAround($land, $x, $y, $HlandSea, 7));

		if($seaCount == 7) {
			# ���������������Ω����ǽ
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if(($landKind == $HlandSea and $lv == 1) or $HeasyReclaim) {
			# �����ξ��
			# ��Ū�ξ�����Ϥˤ���
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, $comName, $point);
			$island->{'area'}++;

			if($seaCount <= 4) {
				# ����γ���3�إå�������ʤΤǡ������ˤ���
				my($i, $sx, $sy);

				for($i = 1; $i < 7; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];

					# �Ԥˤ�����Ĵ��
					if((($sy % 2) == 0) && (($y % 2) == 1)) {
						$sx--;
					}

					if(($sx < 0) || ($sx >= $HislandSize) ||
					   ($sy < 0) || ($sy >= $HislandSize)) {
					} else {
						# �ϰ���ξ��
						if($land->[$sx][$sy] == $HlandSea) {
							$landValue->[$sx][$sy] = 1;
						}
					}
				}
			}
		} else {
			# ���ʤ顢��Ū�ξ��������ˤ���
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			logLandSuc($id, $name, $comName, $point);
		}
		
		# ��򺹤�����
		$island->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomDestroy) {
		# ����
		if($landKind == $HlandSea and $lv == 0) {
			# ���Ϸ���Ǥ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
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

		# ��򺹤�����
		$island->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomSellTree) {
		# Ȳ��
		if(!(($landKind == $HlandForest) || ($landKind == $HlandDefence))) {
			# �����ɱһ��߰ʳ���Ȳ�ΤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);

		# ��Ѷ������
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

		# �Ͼ���߷�
		if(!
		   (($landKind == $HlandPlains) ||
			($landKind == $HlandTown) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFastFarm)) ||
			(($landKind == $HlandFactory) && ($kind == $HcomFactory)))) {
			# ��Ŭ�����Ϸ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# �����ʬ��
		if($kind == $HcomPlant) {
			# ��Ū�ξ��򿹤ˤ��롣
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # �ڤϺ���ñ��
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			# ��Ū�ξ���ߥ�������Ϥˤ��롣
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # �и���0
			logPBSuc($id, $name, $comName, $point) if($Hhide_missile);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_missile);
			$island->{'missile'}++ if($HislandFightMode == 1);
		} elsif($kind == $HcomHaribote) {
			# ��Ū�ξ���ϥ�ܥƤˤ���
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
			logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
		} elsif($kind == $HcomFarm or $kind == $HcomFastFarm) {
			# ����
			if($landKind == $HlandFarm) {
				# ���Ǥ�����ξ��
				$landValue->[$x][$y] += 2; # ���� + 2000��
				if($landValue->[$x][$y] > 50) {
					$landValue->[$x][$y] = 50; # ���� 50000��
				}
			} else {
				# ��Ū�ξ��������
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10; # ���� = 10000��
			}
			logPBSuc($id, $name, $comName, $point) if($Hhide_farm);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_farm);
			if($kind == $HcomFastFarm){
				$island->{'money'} -= $cost;
				return 0;
			}
		} elsif($kind == $HcomFactory) {
			# ����
			if($landKind == $HlandFactory) {
				# ���Ǥ˹���ξ��
				$landValue->[$x][$y] += 10; # ���� + 10000��
				if($landValue->[$x][$y] > 100) {
					$landValue->[$x][$y] = 100; # ���� 100000��
				}
			} else {
				# ��Ū�ξ��򹩾��
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30; # ���� = 10000��
			}
			logPBSuc($id, $name, $comName, $point) if($Hhide_factory);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_factory);
		} elsif($kind == $HcomDbase) {
			# �ɱһ���
			# ��Ū�ξ����ɱһ��ߤ�
			$land->[$x][$y] = $HlandDefence;
			$landValue->[$x][$y] = 0;
			logPBSuc($id, $name, $comName, $point) if($Hhide_deffence);
			logLandSuc($id, $name, $comName, $point) if(!$Hhide_deffence);
			$island->{'missile'}++ if($HislandFightMode == 1);
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
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
		# �η���
		if($landKind != $HlandMountain) {
			# ���ʳ��ˤϺ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		$landValue->[$x][$y] += 5; # ���� + 5000��
		if($landValue->[$x][$y] > 200) {
			$landValue->[$x][$y] = 200; # ���� 200000��
		}
		logLandSuc($id, $name, $comName, $point);

		# ��򺹤�����
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
		# �ߥ������
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		my($flag) = 0;
		if($arg == 0) {
			# 0�ξ��Ϸ�Ƥ����
			$arg = 10000;
		}

		# ��������
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tx, $ty, $err);

		# ȯ�Ͳ��ݳ�ǧ
		if($HislandFightMode == 0) {
			# ��ȯ���֤ʤΤ����
			logLandNG($id, $name, $comName, '���߳�ȯ������Τ���');
			return 0;
		} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
			# ������ꤸ��ʤ��������
			logLandNG($id, $name, $comName, '��ɸ���������Ǥʤ�����');
			return 0;
		}

		# ��̱�ο�
		my($boat) = 0;

		# ��
		if($kind == $HcomMissilePP) {
			$err = 7;
		} else {
			$err = 19;
		}

		# ��Ʈ�԰ٲ���������
		$island->{'missile'}++ if($HislandFightMode == 1);

		# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼��
		my($bx, $by, $count, $ms_count) = (0,0,0,0);
		while(($arg > 0) &&
			  ($island->{'money'} >= $cost)) {
			# ���Ϥ򸫤Ĥ���ޤǥ롼��
			while($count < $HpointNumber) {
				$bx = $Hrpx[$count];
				$by = $Hrpy[$count];
				if($land->[$bx][$by] == $HlandBase) {
					last;
				}
				$count++;
			}
			if($count >= $HpointNumber) {
				# ���Ĥ���ʤ��ä��餽���ޤ�
				last;
			}
			# �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
#			$flag++;

			# ���ϤΥ�٥�򻻽�
			my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
			# ������ǥ롼��
			while(($level > 0) &&
				  ($arg > 0) &&
				  ($island->{'money'} > $cost)) {
				# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
				$level--;
				$arg--;
				$island->{'money'} -= $cost;

				# �ߥ�����ȯ�Ϳ��������
				$island->{'fly'}++;
				$tIsland->{'fly'}++;
				$flag++;

				# ����������
				my($r) = random($err);
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				if((($ty % 2) == 0) && (($y % 2) == 1)) {
					$tx--;
				}

				# �������ϰ��⳰�����å�
				if(($tx < 0) || ($tx >= $HislandSize) ||
				   ($ty < 0) || ($ty >= $HislandSize)) {
					# �ϰϳ�
					logMsOut($id, $target, $name, $tName,  $comName, $point);
					next;
				}

				# ���������Ϸ�������
				my($tL) = $tLand->[$tx][$ty];
				my($tLv) = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# �ɱһ���Ƚ��
				my($defence) = 0;
				if($HdefenceHex[$id][$tx][$ty] == 1) {
					$defence = 1;
				} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
					$defence = 0;
				} else {
					if($tL == $HlandDefence) {
						# �ɱһ��ߤ�̿��
						# �ե饰�򥯥ꥢ
						my($i, $count, $sx, $sy);
						for($i = 0; $i < 19; $i++) {
							$sx = $tx + $ax[$i];
							$sy = $ty + $ay[$i];

							# �Ԥˤ�����Ĵ��
							if((($sy % 2) == 0) && (($ty % 2) == 1)) {
								$sx--;
							}

							if(($sx < 0) || ($sx >= $HislandSize) ||
							   ($sy < 0) || ($sy >= $HislandSize)) {
								# �ϰϳ��ξ�粿�⤷�ʤ�
							} else {
								# �ϰ���ξ��
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
					# ��������
					logMsCaught($id, $target, $name, $tName, $comName, $point, $tPoint);
					next;
				}

				# �ָ��̤ʤ���hex��ǽ��Ƚ��  ���ޤ��ϻ�
				if($tL == $HlandSea || $tL == $HlandMountain) {
					$tLname = landName($tL, $tLv);

					# ̵����
					logMsNoDamage($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
					next;
				}

				# �ߥ�����
				if($tL == $HlandWaste) {
					# ����(�ﳲ�ʤ�)
					logMsWaste($id, $target, $name, $tName,	$comName, $tLname, $point, $tPoint);
				} else {
					# �̾��Ϸ�
					logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
				}

				# �и���
				if($tL == $HlandTown) {
					if($land->[$bx][$by] == $HlandBase) {
						$landValue->[$bx][$by] += int($tLv / 20);
						$boat += $tLv; # �̾�ߥ�����ʤΤ���̱�˥ץ饹
						if($landValue->[$bx][$by] > $HmaxExpPoint) {
							$landValue->[$bx][$by] = $HmaxExpPoint;
						}
					}
				} elsif($tL == $HlandDefence){
					# ����ε�Ͽ���ݻ�
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

				
				# ���Ϥˤʤ�
				$tLand->[$tx][$ty] = $HlandWaste;
				$tLandValue->[$tx][$ty] = 1; # ������

			}

			# ����������䤷�Ȥ�
			$count++;
		}


		if($flag > 0) {
			# �ߥ�����ȯ�Ϳ�
			logComMissle($id, $name, $tName, $comName, $point, $flag) if($Hmissile_log);
		} else {
			# ���Ϥ���Ĥ�̵���ä����
			logMsNoBase($id, $name, $comName);
			return 0;
		}

		# ��̱Ƚ��
		$boat = int($boat / 2);
		if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
			# ��̱ɺ��
			my($achive); # ��ã��̱
			my($i);
			for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if($land->[$bx][$by] == $HlandTown) {
					# Į�ξ��
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
					# ʿ�Ϥξ��
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
				# �����Ǥ����夷����硢�����Ǥ�
				logMsBoatPeople($id, $name, $achive);

				# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
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
		# ͢���̷���
		if($arg == 0) { $arg = 1; }
		my($value) = min($arg * (-$cost), $island->{'food'});

		# ͢�Х�
		logSell($id, $name, $comName, $value);
		$island->{'food'} -=  $value;
		$island->{'money'} += ($value / 10);
		return 0;
	} elsif($kind == $HcomGiveup) {
		# ����
		logGiveup($id, $name);
		$island->{'dead'} = 1;
		return 1;
	}

	return 1;
}


# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
	my($island) = @_;

	# Ƴ����
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# ������͸��Υ�����
	my($addpop)  = $HtownUp;  # ¼��Į
	$addpop = 0 if(($HislandTurn <= $HyosenTurn) and 	# Ϣ³��ⷫ�꤫����������­��ʤ���祹�ȥå�
				($island->{'absent'} >= $HstopAddPop or $island->{'down'}));
	$addpop = -30 if($island->{'food'} < 0);	# ������­

	# �롼��
	my($x, $y, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];

		if($landKind == $HlandTown) {
			# Į��
			if($addpop < 0) {
				# ��­
				$lv -= (random(-$addpop) + 1);
				if($lv <= 0) {
					# ʿ�Ϥ��᤹
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} elsif($addpop > 0) {
				# ��Ĺ
				if($lv < 100) {
					$lv += random($addpop) + 1;
					$lv = 100 if($lv > 100);
				}
			}

			$lv = 200 if($lv > 200);
			$landValue->[$x][$y] = $lv;
		} elsif($landKind == $HlandPlains and $addpop > 0) {
			# ʿ��
			if($HtownGlow >=random(100)) {
				# ��������졢Į������С�������Į�ˤʤ�
				if(countGrow($land, $landValue, $x, $y)){
					$land->[$x][$y] = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
		} elsif($landKind == $HlandForest) {
			# ��
			$lv += $HtreeUp;			# �ڤ����䤹
			$lv = 200 if($lv > 200);	# �����Ķ�������
			$landValue->[$x][$y] = $lv; # ����
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

# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
	my($land, $landValue, $x, $y) = @_;
	my($i, $sx, $sy);
	for($i = 1; $i < 7; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # �Ԥˤ�����Ĵ��
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
		 } else {
			 # �ϰ���ξ��
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

# ������
sub doIslandProcess {
	my($number, $island) = @_;

	# Ƴ����
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# ������­
	if($island->{'food'} < 0) {
		# ��­��å�����
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
				# 1/4�ǲ���
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
			}
		}
	}


	# ��������Ƚ��
	if(($island->{'area'} > $HdisFallBorder) &&
	   (random(1000) < $HdisFalldown)) {
		# ��������ȯ��
		logFalldown($id, $name);

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind != $HlandSea) &&
			   ($landKind != $HlandMountain)) {

				# ���Ϥ˳�������С��ͤ�-1��
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
				# -1�ˤʤäƤ�����������
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 1;
			} elsif ($landKind == $HlandSea) {
				# �����ϳ���
				$landValue->[$x][$y] = 0;
			}

		}
	}

	# ���������դ�Ƥ��鴹��
	if($island->{'food'} > 9999) {
		$island->{'money'} += int(($island->{'food'} - 9999) / 10);
		$island->{'food'} = 9999;
	} 

	# �Ƽ���ͤ�׻�
	estimate($number);

	# �˱ɡ������
	$pop = $island->{'pop'};
	my($damage) = $island->{'oldPop'} - $pop;
	my($flags) = $island->{'prize'};

	# �˱ɾ�
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

	# �����
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

# ���Ϸ׻�
sub doIslandPower {
	my($island) = @_;

	my $power = 25 * ($island->{'farm'} + $island->{'factory'} + $island->{'mountain'} + $island->{'pop'} / 10)
	 + 700 * $island->{'area'} + 1000 * $island->{'army'} + 
	 aboutMoney2($island->{'money'}) + $island->{'forest'} - $island->{'waste'};

	$island->{'power'} = random($power) if $power > 0;
}

# ���Ͻ�˥�����
sub islandPowerSort {
	my($flag, $i, $tmp);

	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'power'} <=> $Hislands[$a]->{'power'} || $a <=> $b } @idx;
	@HislandPower = @Hislands[@idx];
}

# �͸���˥�����
sub islandSort {
	my($flag, $i, $tmp);

	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���
# �̾��
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �ٱ��
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��̩��
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �ߥ�����ȯ�ͥ�
sub logOutM {
	push(@HlogPool,"2,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��Ͽ��
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ��Ͽ��Ĵ��
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

# ���񤭽Ф�
sub logFlush {
	open(LOUT, ">${HdirName}/hakojima.log0");

	# �����ս�ˤ��ƽ񤭽Ф�
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

# �����
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
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
sub log_debug {
	my($one, $two, $three) = @_;
	logOut("$one - $two - $three");
}

# ������
sub logWin {
	my($id, $name, $money) = @_;
	my $fTurn = $HislandFightCount + 1;
	if($HislandNumber == 4) {
		$fTurn = '�辡��';
	} elsif($HislandNumber == 8) { 
		$fTurn = '��辡';
	} else {
		$fTurn .= '����';
	}
	if($HislandNumber == 2) {
		logOut("${HtagName_}${name}��${H_tagName}��������<B>ͥ������</B>",$id);
		logHistory("${HtagName_}${name}��${H_tagName}��<B>ͥ������</B>");
	} elsif($money == 0) {
		logOut("${HtagName_}${name}��${H_tagName}��������<B>$fTurn�ʽС�</B>",$id);
	} else {
		logOut("${HtagName_}${name}��${H_tagName}��������<B>$fTurn�ʽС���$money$HunitMoney</B>���󽷶⤬��ʧ���ޤ�����",$id);
	}
}

# ����
sub logLose {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>����</B>��",$id);
}

# ͽ�����
sub logLoseOut {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>ͽ�����</B>��",$id);
	logHistory("${HtagName_}${name}��${H_tagName}��<B>ͽ�����</B>��");
}

# ��ȯ���֤Τ��Ἲ��
sub logLandNG {
	my($id, $name, $comName, $cancel) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>$cancel</B>���¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# ���­��ʤ�
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������­�Τ�����ߤ���ޤ�����",$id);
}

# ����­��ʤ�
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ����߿�����­�Τ�����ߤ���ޤ�����",$id);
}

# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logSecret("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$kind</B>���ä�������ߤ���ޤ�����",$id);
END
}

# �����Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ�Φ�Ϥ��ʤ��ä�������ߤ���ޤ�����",$id);
END
}

# ���Ϸ�����
sub logLandSuc {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
END
}

# ����or�ߥ��������
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logOut("������ʤ�����${HtagName_}${name}��${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
END
}

# �ɱһ������
sub logSecretSell {
    my($id, $name, $landName, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}������<B>${landName}</b>����${HtagComName_}���${H_tagComName}����ޤ�����",$id);
END
}

# �ϥ�ܥ�
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logLandSuc($id, $name, $comName2, $point);
END
}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)���������åȤ����ʤ�
sub logMsNoTarget {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ����˿ͤ���������ʤ�������ߤ���ޤ�����",$id);
END
}

# �ߥ�����ȯ�ͼ¹�
sub logComMissle {
	my($id, $name, $tName, $comName, $point, $count) = @_;
	logOutM("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����<b>$countȯ</b>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
END
}

# �ߥ������Ȥ��Ȥ��������Ϥ��ʤ�
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>�ߥ�������������ͭ���Ƥ��ʤ�</B>����˼¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# �ߥ������ä����ϰϳ�
sub logMsOut {
	my($id, $tId, $name, $tName, $comName, $point) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
}

# �ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaught {
	my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
}

# �ߥ������ä������̤ʤ�
sub logMsNoDamage {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);
}

# �̾�ߥ����롢���Ϥ�����
sub logMsWaste {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}

# �ߥ�������̱����
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}��${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}��${H_tagName}�ϲ����������줿�褦�Ǥ���",$id);
}

# ��ⷫ��
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ͢��
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>$value$HunitFood</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}

# ����
sub logGiveup {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}���������졢<B>̵����</B>�ˤʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}��${H_tagName}����������<B>̵����</B>�Ȥʤ롣");
}

# ����
sub logGiveup_no_do_fight {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}�ϵ�������Ʈ�԰٤�Ԥ�ʤ��ä����ᡢ<B>̵����</B>�ˤʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}��${H_tagName}����������Ʈ�԰٤�Ԥ�ʤ��ä����ᡢ<B>̵����</B>�Ȥʤ롣");
}

# ����
sub logDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}����ͤ����ʤ��ʤꡢ<B>̵����</B>�ˤʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}��${H_tagName}���ͤ����ʤ��ʤ�<B>̵����</B>�Ȥʤ롣");
}

# ȯ��
sub logDiscover {
	my($name) = @_;
	my($ip) = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ip = $ENV{'REMOTE_ADDR'} if(!$ip);
	logHistory("${HtagName_}${name}��${H_tagName}��ȯ������롣(${ip})");
}

# ̾�����ѹ�
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}��${H_tagName}��̾�Τ�${HtagName_}${name2}��${H_tagName}���ѹ����롣");
}

# ����
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}

# ������­�ﳲ
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",$id);
}

# ��������ȯ��
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",$id);
}

# ���������ﳲ
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",$id);
}

# ����
sub logPrize {
	my($id, $name, $pName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",$id);
	logHistory("${HtagName_}${name}��${H_tagName}��<B>$pName</B>�����");
}

# �礬���äѤ��ʾ��
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}����������ޤ����礬���դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ������̾�����ʤ����
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}��ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ������̾���������ʾ��
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',"?()<>\$'�Ȥ����äƤ��ꡢ��̵����פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}������ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �����ܤ���Ͽ�ξ��
sub tempRegistFailed {
	out(<<END);
${HtagBig_}Ϣ³������Ͽ�Ͻ���ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
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
${HtagBig_}���ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �Ϸ��θƤ���
sub landName {
	my($land, $lv) = @_;
	if($land == $HlandSea) {
		if($lv == 1) {
			return '����';
		} else {
			return '��';
		}
	} elsif($land == $HlandWaste) {
		return '����';
	} elsif($land == $HlandPlains) {
		return 'ʿ��';
	} elsif($land == $HlandTown) {
		if($lv < 30) {
			return '¼';
		} elsif($lv < 100) {
			return 'Į';
		} else {
			return '�Ի�';
		}
	} elsif($land == $HlandForest) {
		return '��';
	} elsif($land == $HlandFarm) {
		return '����';
	} elsif($land == $HlandFactory) {
		return '����';
	} elsif($land == $HlandBase) {
		return '�ߥ��������';
	} elsif($land == $HlandDefence) {
		return '�ɱһ���';
	} elsif($land == $HlandMountain) {
		return '��';
	} elsif($land == $HlandHaribote) {
		return '�ϥ�ܥ�';
	}
}

# �͸�����¾���ͤ򻻽�
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $farm, $factory, $mountain, $burnmis, $forest) = (0, 0, 0, 0, 0, 0, 0, 0);
	my($waste, $army_m, $army_d) = (0, 0, 0);

	# �Ϸ������
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# ������
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if($kind != $HlandSea) {
				$area++;
				if($kind == $HlandTown) {
					# Į
					$pop += $value;
				} elsif($kind == $HlandFarm) {
					# ����
					$farm += $value;
				} elsif($kind == $HlandFactory) {
					# ����
					$factory += $value;
				} elsif($kind == $HlandMountain) {
					# ��
					$mountain += $value;
				} elsif($kind == $HlandBase) {
					# �ߥ��������
					$burnmis += expToLevel($kind, $value);
					$army_m++;
				} elsif($kind == $HlandDefence) {
					# �ɱһ���
					$army_d++;
				} elsif($kind == $HlandWaste and $value == 1) {
					# �ߥ�������
					$waste++;
				} elsif($kind == $HlandForest) {
					# ��
					$forest += $value;
				}
			}
		}
	}

	# ����
	$island->{'pop'}	  = $pop;
	$island->{'area'}	  = $area;
	$island->{'farm'}	  = $farm;
	$island->{'factory'}  = $factory;
	$island->{'mountain'} = $mountain;
	$island->{'fire'}	  = $burnmis;
	$island->{'army'}	  = $army_m + $army_d;
	$island->{'forest'}	  = $forest * $HtreeValue;
	$island->{'waste'}	  = $waste * $HcomCost[$HcomPrepare2]; # �Ϥʤ餷��

	if($winlose == 2 and $HrewardMode != 2 and $island->{'reward'} == 0) {
		$island->{'reward'} = $army_m + $army_d * 2;
	}
}

# ��Ʈ���ֳ��ϻ�����ξ��֤���¸
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

# �ԼԤ���ξ�����¸
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

# ��Ʈ����������ﾡ
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

	# �Ƽ���ͤ�׻�
	estimate($HcurrentNumber);
}


# �ϰ�����Ϸ��������
sub countAround {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # �Ԥˤ�����Ĵ��
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
			 # �ϰϳ��ξ��
			 if($kind == $HlandSea) {
				 # ���ʤ�û�
				 $count++;
			 }
		 } else {
			 # �ϰ���ξ��
			 if($land->[$sx][$sy] == $kind) {
				 $count++;
			 }
		 }
	}
	return $count;
}

# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# �����
	if($n == 0) {
		$n = 1;
	}
	@list = (0..$n-1);

	# ����åե�
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		if($i == $j) { next; };
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

# ̾���ѹ�����
sub tempChangeNothing {
	out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ�${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
	out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$HtempBack
END
}

1;
