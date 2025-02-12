# ReClaim

## 利用について

本システムの利用には許諾が必要です。
利用をご希望の際は、以下のいずれかの連絡先までお問い合わせください：

- Misskey: [@hirohiroto112607@misskey.resonite.love](https://misskey.resonite.love/@hirohiroto112607)
- X: [@p9WcKtj3d4g0JsF](https://x.com/@p9WcKtj3d4g0JsF)
- メール: [hirohiroto112607@f5.si](mailto:hirohiroto112607@f5.si)

許諾のない場合、このソフトウェアおよびコードの実行は認められません。

## 概要

ReClaimはAIを活用した落とし物管理システムです。
Google GeminiとDjangoを使用し、以下の機能を提供します：

- AIによる落とし物の自動分類・特徴抽出
- 画像認識による詳細な物品情報の生成
- ユーザーフレンドリーなWeb管理インターフェース
- 効率的な検索・管理機能

## 必要要件

- Python 3.12以上
- Django 5.1以上
- インターネット接続
- Google Gemini APIキー（無料版でも可）

## インストール手順

1. リポジトリのクローン：

```bash
mkdir reclaim
cd reclaim
git clone https://github.com/hirohiroto112607/ReClaim.git

```

2. 環境のセットアップ：

```bash
# Condaで新しい環境を作成・有効化
conda create --name reclaim --file reclaim.yml
conda activate reclaim
cd reclaim
```

3. 環境変数の設定：
   - `.env`ファイルを作成し、以下の変数を設定：

```plaintext
GENAI-API-KEY=your_gemini_api_key_here
```

4. プロジェクトのセットアップ：

```bash
python setup.py
```

このコマンドで以下の処理が自動的に実行されます：
- データベースのマイグレーション
- スーパーユーザーの作成
- 静的ファイルの収集
- 基本カテゴリーの作成

5. 開発サーバーの起動：

```bash
python manage.py runserver
```

