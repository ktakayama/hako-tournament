┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

　箱庭トーナメント２ readme -2005/12/22更新-
　　By　Kyosuke Takayama (ドン・ガバチョ) support@mc.neweb.ne.jp
　　　配布サイト　(http://espion.just-size.jp/archives/dist_hako/)

┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○スクリプト配布元

・箱庭諸島２配布元（現在は配布終了）
  オリジナル箱庭諸島２
  http://t.pos.to/hako/

・ＪＡＶＡスクリプト版箱庭諸島配布元
  あっぽー箱庭諸島
  http://appoh.execweb.cx/hakoniwa/


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○ご質問はこちらへ・・・

・通常の箱庭２に関する質問は、オリジナル配布元の
	「意見・質問・雑談・その他」掲示板に
　http://t.pos.to/hako/

・スクリプト設置等に関するご質問は、Tsubasa's HomePageの
	「ＣＧＩ駆け込み寺」に
　http://homepage3.nifty.com/himajin2001/

・その他、バグ報告や提案等は「バグ情報」までお願いします
　http://espion.just-size.jp/bts/html/guest.cgi?project=hakoniwa&action=top

┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○免責

  使用者の責任において使用してください。
　作者は、いかなる損害・トラブルにも一切責任は負わないものとします。

  
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○設置方法

　通常の箱庭諸島２が設置出来れば特に問題はありません。
　最初に hako-ini.cgi で設定を行ってから設置して下さい。


　＊追加されているファイルの説明です
　hako-ini.cgi
　　各種設定のファイルです
　hako-help.cgi
　　設定一覧や、マニュアルを表示するためのファイルです
　hako-js.cgi
　　JavaScript版の開発画面で開発するためのファイルです
　hako-mobile.cgi
　　携帯端末での処理をするためのファイルです
　hako-chart.cgi
　　トーナメント表を生成するためのファイルです
　access.cgi
　　アクセスログ閲覧用のCGIです

　hako-*.cgi のファイルに新しいパーミッション等を設定する必要はありません。
　hako-turn.cgi等と同じように設置して下さい。 
　access.cgi には実行権限が必要です。
　Perl のパスを確認し、hako-main.cgi 等と同じパーミッションを設定して下さい。
　また、内部でパスワードの設定も行っていますので、こちらも設定します。

　設置禁止のサーバー等もありますので、オリジナルの配布元、及び当配布ページも
　よくお読みの上設置して下さい。

　imgexpフォルダには、画像のローカル設定用の説明ファイルが入ってます。
　ただし、画像は同梱されてませんので、圧縮したファイルをアップしておく
　必要があります。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○設定について

　以下は hako-ini.cgi で設定する項目の説明です。

　◇セキュリティに関する項目
　hako-ini.cgiで設定を行えますが、以下の項目は必ず変更して下さい。
　変更しないと、セキュリティ上問題が生じ、参加者に迷惑が掛かります。

　$masterPassword　管理人用のマスターパスワードです
　$HspecialPassword　同じくスペシャルパスワードです
　$HdirName　データファイルが保存されているディレクトリです
　$Hdirmdata　同じく対戦前の島の状態が保存されているディレクトリです


　◇追加・変更されている設定個所の注意点

　・ロックの方式
　ロックの方式が二種類になりました。
　一つは、従来からある、信頼性の高いflockの方式です。

　もう一つは、こちら(http://www.din.or.jp/~ohzaki/perl.htm#File_Lock)を
　参考にして作ったものです。
　160島3時間更新の改造箱庭で、データが飛んだ事はありません。
　こちらを使用する場合は、lockfile というファイルを、
　cgi と同じディレクトリに置いて下さい。
　どんなプラットフォームでも動作しますので、
　flock方式がうまく動かない場合は、こちらを使用して下さい。

　・デバッグモード
　デバッグモードで動作させる場合は、$HdeveRepCount、$HdeveRepCount、
　$HfightRepCount の値が自動的に1になります。
　これは、ターンをまとめて更新する処理が少し特殊なため、
　デバッグ中は、1ターンずつ更新させるようにした方がいいと判断したためです。

　・ミサイルログの簡略化
　ミサイル発射のログを自島の分は表示しないようにするものです。
　この設定を行えば、サーバーの負担軽減に繋がります。

　・その他
　hako-mente.cgi のメンテ用パスワードは、hako-ini.cgi で設定した、
　$masterPasswordです。


　◇特殊設定

　・埋め立ての簡易化
　これを設定すると、海を埋め立てした場合、浅瀬を飛ばして荒地になります。
　つまり、陸地に面している部分なら二度埋めしなくても、陸地に出来るのです。
　通常版同様浅瀬は発生しますが、特に関係ありません。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○トーナメント表

　トーナメント表は見た目の華やかさや、楽しさがありますが、以下のような
　デメリットや、既知のバグが存在するので運用には注意して下さい。

　◇対戦状況による対戦相手決定のバランスが悪くなります。

　デフォルト状態では、対戦終了時の島力を見てから対戦相手を決定すると言う
　方法で、多少ランダムではありますが、なるべく同等の力を持った島同士が
　対戦するように仕向けています。
　トーナメント表では完全に最後まで対戦の道筋が決まってしまうので、
　そう言った意味でのバランスは悪くなると考えられます。


　◇不戦勝が多数発生する環境では、表の通りに対戦相手が決定しません

　トーナメント表のシステムでは、対戦終了時に、表の上から順番に2島ずつ対戦相手を
　割り振って行くという形で表の体裁を保っています。
　この時途中で不戦勝が発生するような場合では、強制的に次のブロックの島が
　選ばれる事になり、最終的には一番下の島が不戦勝と言う事になってしまいます。

　◇シードは使えません

　つまり、予選通過後の島数が2のべき乗で無い場合はトーナメント表が
　正しく表示されません。
　どちらにせよ、島数が2のべき乗で無い場合は、常に不戦勝が発生するので
　設定するべきではありません。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○アクセスログ

　acce_log ディレクトリに日毎にログを保存してあります。
　保存されるタイミングは、「開発画面に入る」「計画を送信する」
　「コメントを変更する」「開発画面から観光者通信に書き込みする」場合です。
　ファイルは無制限に増えますので、ある程度時期が過ぎたら手動で削除して下さい。

　参照する場合は、access.cgi で確認して下さい。
　怪しい島は、青色ラインで表示されます。
　「IPカット」にチェックをすると、IPアドレスの最後の区切りの部分を無視して表示します。
　ダイヤルアップ等でIPアドレスが変わっても追いかけやすくなってますが、
　一般ユーザー同士も青色として表示される事もありますので、気を付けてください。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○hako-mente.cgi のメンテナンスモードについて

　データファイルが破損して、バックアップからデータを復旧させる場合、
　復旧直後にアクセスされるとターンが進んでしまいます。

　これを防ぐために、メンテナンスモードに入ってから作業すれば、
　ブラウザからアクセスする事が出来ませんので、安心です。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○改造について

　オリジナルの箱庭の使用条件にそって、改造するのは自由ですが、
　難しい部分がありますので、注意しておきます。

　◇コマンドの追加
　追加自体はそれほど難しくありません。
　JavaScript版の開発画面にて、メニューを表示する所があると思いますが、
　このメニューは、画面の枠内からはみ出さないように微調整されています。

　コマンドを追加した場合は、このメニューが長くなるので、
　その部分を調整し直さないといけません。
　hako-js.cgiの332行目付近のshowMenuという関数内です。


　その他の部分に関しては、恐らく問題なく改造出来るかと思います。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○ひとこと

　オリジナル設定のトーナメントばかりが蔓延してしまい、
　参加者が場所選びに新鮮味を味わえないため、今回のバージョンより、
　設定個所が少し増えました。

　農場や工場の偽装、ミサイル基地を丸見えにするなど、
　Perlに詳しくなくても簡単に設定出来るようになっております。
　食料の消費率を0にしたりするのもいいでしょう。

　これらの特徴を生かして、是非オリジナルトーナメントの開催を行って下さい。


　設置終えたら、是非当サイトのトーナメントリンク集に登録して下さい。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○今後の予定

　◇報酬金設定の追加
　◇特殊設定の追加
　◇管理人のみ島が登録可能
　◇管理人権限で強制島削除機能
　◇スクリプト記述の簡略化


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○主な変更点

　◇2005/12/22　Ver.0.97  　XSS 脆弱性の対策
　◇2005/10/10　Ver.0.96  　コマンドのD&D移動、画面遷移無しでの計画送信機能を導入
　◇2005/01/23　Ver.0.95  　携帯端末対応
　　          　          　マニュアルの言い回しを修正
　　          　          　ミサイルの都市命中時のログ修正
　◇2004/11/10　Ver.0.94.3　トーナメント表導入
　　          　          　マーキング処理実装
　　          　          　予選、開発期間のまとめ更新数を別々に設定出来るように修正
　　          　          　NN 系ブラウザのいくつかのバグ修正
　　          　          　余分な関数を削除
　　          　          　$Hhide_town $Hhide_farm $Hhide_factory 設定時の不具合を修正
　　          　          　その他細かい修正をいくつか
　◇2004/06/03　Ver.0.92  　配布元URLの変更
　◇2004/04/27　Ver.0.91  　NN系ブラウザでステータスバーに地形情報が表示されない問題を修正
　　          　          　余計な変数名を削除 (Thx. NONさん)
　　          　          　準決勝との表示がなされない問題の修正 (Thx. NONさん)
　◇2004/02/18　Ver.0.90  　マップサイズが奇数の際のバグ修正 (Thx. チヨリスタさん)
　　          　          　たまに浅瀬が少ない島が出来てしまうバグ修正 (Thx. チヨリスタさん)
　　          　          　window.open時のバグ修正
　　          　          　IE6でレイアウトが崩れてしまうバグ修正(多分)
　　          　          　XSS脆弱性対策(2)
　◇2003/10/28　Ver.0.88  　XSS脆弱性対策(1)
　◇2003/07/02　Ver.0.87  　ログ表示のバグ修正
　◇2003/05/07　Ver.0.86  　ターン進行行程の不具合を解消
　　          　          　アクセスログ記録方式変更
　　          　          　アクセスログ読み取りスクリプト作成
　　          　          　簡易重複チェック機能を搭載
　◇2002/05/02　Ver.0.84  　開発期間のまとめ更新の際の不具合解消
　◇2001/12/31　Ver.0.83  　対戦の記録表示不具合解消
　◇2001/12/10　Ver.0.82  　対戦の記録表示不具合解消
　◇2001/12/05　Ver.0.81  　配布開始


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○最後に・・

　配布に至るまでに、沢山の方の協力を頂きました。
　テスト版に参加して下さった方、意見を言って頂いた方、
　この場をお借りしまして、感謝致します。
　みなさんの協力が無ければ、到底完成しなかったでしょう。
　本当に有難う御座います。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○番外編: バージョン管理のススメ

　プログラムの開発を進めていると、以前行なった修正点を確認したかったり、
　昔のバージョンのファイルが必要になったりする事があると思います。
　ある程度はバックアップを取ったりして対処していると思いますが、
　それぞれのバージョンとファイル名の対応や管理は大変じゃないでしょうか。

　バージョン管理システムを使う事によってこういった煩わしい事から解放されます。

　バージョン管理システムを使えば、

　* 任意のバージョンの取り出し
　* 任意のバージョンと任意のバージョンの変更点の差分の取り出し
　* バージョンを登録する際に変更の記録を付けられる

　などがおこなえます。

　特に、差分の確認は使用頻度も高く、誤って修正してしまった場合でも
　すぐに戻せるので非常に便利です。

　バージョン管理のシステム自体は沢山ありますが、その中でも CVS と言うのが有名で、
　数多くあるオープンソースのプロジェクトでも利用頻度は高いです。

　Google などで CVS として検索してみれば、多くの解説ページがひっかかるので、
　興味があったら色々と調べてみて下さい。

　ちなみに、私は Subversion と言うシステムを利用しています。
　CVS に比べると新しいのですが、新しいだけあって色々と改良されているのでお薦めです。

　プログラムの開発をするなら、バージョン管理は必須です。
　これを機会に導入してみては如何でしょうか？


　◇Subversion のススメ

　導入は如何でしょうかとか書いておきながら、基本はサーバ・クライアント型なので、
　人によっては導入が結構面倒だったりします。

　実は私が使っているサーバで Subversion が使えるように解放されているので、
　もし使ってみたい方がいらっしゃったら、専用のスペースを用意するのでメールなどを下さい。


┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
