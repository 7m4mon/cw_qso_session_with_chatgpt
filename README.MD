# 生成AIを相手にしてCWの交信練習をしてみよう！

OpenAI社が提供する生成AI（GPT-4）にモールス信号の交信相手になってもらうプログラムです。プログラムの流れは以下のとおりです。

1. OpenAI社が提供するAPI にPythonプログラムからアクセスします。
1. Clientに初期プロンプトで交信の条件などを設定したら、入力待ち状態になります。
1. ターミナルでCQをこちらから出すと、生成AIが適当なコールサインで応答してきます。
1. 応答された文字列からモールス信号の wav ファイルを作成して再生しますので、音響受信を行います。文字列はターミナル上に表示されますので、ミスコピーしても大丈夫です。
1. AIが応答したコールサインに対して通常のQSOを進めていきます。つまり、RSTレポート、名前、QTHの交換などです。
1. 交信を進めて送るものがなくなったらファイナルを送ります。
1. 最後は「CL」という文字列でセッションを終了します。

---

[生成AIを相手にしてCWの交信練習をしてみよう!](https://www.fbnews.jp/202408/special2/ "")

