# Pyhonを用いたオリジナルテトリスの作成

### 作成日
2023年12月

### 作成理由
1年間プログラミング1の授業を通してPythonを学んできたので、その集大成として作成した。

### ゲームについて
既存のゲームであるテトリスをPythonで実施にプレイできるようになっている

### ルール
- マスの横一列にブロックをそろえると消えてScoreに100ポイントが加算される。
- 制限時間は2分
- 1000点を取るとCLEAR画面、1000点未満だとGAME OVER画面が出力される。

### 操作方法
- 上下⇅矢印キー:ブロックを90°回転
- 左右⇆矢印キー:ブロックの位置移動
- Enterキー:ブロック投下

### 注意点
- ブロックはエンターを押すと一気に下まで落下する。
- ブロックを回転するときに、ほかのブロックが周りにあると回転できないことがある。
- Windows環境以外で実行すると、文字がうまく表示されない。