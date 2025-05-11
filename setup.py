import os
import sys

import django
from django.core.management import execute_from_command_line
from django.core.management.utils import get_random_secret_key
from reclaim.items.models import item_category


def setup_project():
    print("ReClaim プロジェクトのセットアップを開始します...")

    # 環境変数の設定
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reclaim.settings')
    django.setup()

    try:
        # SECRET_KEYの生成
        print("SECRET_KEYを生成中...")
        secret_key = get_random_secret_key()
        with open('.env', 'w') as f:
            f.write(f"DJANGO_SECRET_KEY={secret_key}")
        # マイグレーションの実行
        print("データベースのマイグレーションを実行中...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])

        # スーパーユーザーの作成
        print("\nスーパーユーザーを作成します。")
        print("メールアドレス、パスワードを入力してください。")
        execute_from_command_line(['manage.py', 'createsuperuser'])

        # 静的ファイルの収集
        print("\n静的ファイルを収集中...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

        # カテゴリの作成
        print("\nカテゴリを作成中...")
        item_category_objects = []
        item_category_objects.append(item_category(category_name="定期券・カード類"))
        item_category_objects.append(item_category(category_name="傘"))
        item_category_objects.append(item_category(category_name="鍵"))
        item_category_objects.append(item_category(category_name="文具・書類"))
        item_category_objects.append(item_category(category_name="衣類・アクセサリー"))
        item_category_objects.append(item_category(category_name="かばん・バッグ"))
        item_category_objects.append(item_category(category_name="財布・貴重品"))
        item_category_objects.append(item_category(category_name="電子機器"))
        item_category_objects.append(item_category(category_name="その他"))
        item_category.objects.bulk_create(item_category_objects)

        # セットアップ完了
        print("\nセットアップが完了しました!")
        print("開発サーバーを起動するには以下のコマンドを実行してください:")
        print("python start.py")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    setup_project()
