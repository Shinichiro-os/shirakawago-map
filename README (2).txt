# 白川郷観光マップアプリ

このアプリは白川郷の観光スポット・混雑状況・ルート案内を地図上で分かりやすく表示するWebアプリです。

## 主な機能
- 観光地の混雑状況を色分けで表示
- 各スポットの写真・説明・Googleマップ連携
- おすすめルート自動作成・分散化提案
- 現在地からの距離・ルート表示

## 起動方法（ローカル）
1. 必要なパッケージをインストール
   ```
   pip install -r requirements.txt
   ```
2. アプリを起動
   ```
   streamlit run shirakawago_app.py
   ```

## Web公開（Streamlit Community Cloud推奨）
1. このプロジェクト一式をGitHubにアップロード
2. https://streamlit.io/cloud にアクセスし、GitHubリポジトリを指定してデプロイ
3. 公開URLが発行されます

## QRコードでアクセス
公開URLが決まったら、QRコード生成サイトやPythonのqrcodeライブラリでQRコード画像を作成し、案内板等に設置してください。