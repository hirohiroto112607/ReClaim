import base64
import os
import json

import google.generativeai as genai
import httpx
from background_task import background
from django.shortcuts import get_object_or_404
from items.models import item, item_category
from django.utils import timezone

from reclaim.settings import BASE_DIR


def init():
    genai.configure(api_key=os.getenv("GENAI-API-KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash",
                                  generation_config={
                                      "response_mime_type": "application/json"},
                                  system_instruction="""
                                  600文字以内にしてください。
                                  多く回答すること。
                                  キーワードのみを上げてください。
                                  """)
    print("Initialized model")
    return model


def generate_item_info(image_path):
    """画像からタイトル、カテゴリー、キーワードを生成する"""

    image_path = os.path.join(BASE_DIR, "media", str(
        image_path))  # ここでimagepathを絶対パスに変更
    with open(image_path, 'rb') as f:
        data = f.read()
    base = base64.b64encode(data).decode('utf-8')
    file_etx = image_path.split(".")[-1]
    if file_etx == "jpg":
        file_etx = "jpeg"

    # カテゴリーの選択肢を改善
    # TODO カテゴリーの選択肢を変更する
    prompt = """
    この画像について以下の情報をJSON形式で出力してください：
    1. タイトル（item_name）: 50文字以内で簡潔に
    2. カテゴリー（category）: 以下のカテゴリー名から【完全一致・1つだけ】選んでください：
    定期券・カード類
	傘
	鍵
	文具・書類
	衣類・アクセサリー
	かばん・バッグ
	財布・貴重品
	電子機器
	その他
    3. キーワード（keywords）: できるだけ詳細に、日本語と英語で（900文字以内）
    
    必ず以下の形式のJSONのみを出力してください。説明文は不要です：
    {"item_name": "タイトル", "category": "カテゴリー", "keywords": "キーワード"}

    カテゴリーは必ず上記リストの中から【完全一致】で選んでください。
    """

    try:
        response = model.generate_content([{
            'mime_type': f'image/{file_etx}',
            'data': base
        }, prompt])

        text = response.text.strip()
        # コードブロックを除去
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].strip()

        # JSONオブジェクトの抽出
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            text = text[start:end]

        print("Cleaned response:", text)  # デバッグ出力

        result = json.loads(text)

        # カテゴリー名の検証
        valid_categories = [
            "定期券・カード類",
            "傘",
            "鍵",
            "文具・書類",
            "衣類・アクセサリー",
            "かばん・バッグ",
            "財布・貴重品",
            "電子機器",
            "その他"
        ]
        """
以下がカテゴリーの選択肢です：
	定期券・カード類
	傘
	鍵
	文具・書類
	衣類・アクセサリー
	かばん・バッグ
	財布・貴重品
	電子機器
	その他
        """
        # TODO カテゴリーの選択肢を変更する

        if 'category' in result:
            category = result['category'].strip()
            if category not in valid_categories:
                print(f"Invalid category: {category}")
                result['category'] = "その他"  # デフォルトカテゴリー
        print("Result:", result)
        return result

    except Exception as error:
        print(f"Error in generate_item_info: {str(error)}")
        print(
            f"Response text: {response.text if 'response' in locals() else 'No response'}")
        return {
            "item_name": "不明なアイテム",
            "category": "その他",
            "keywords": "解析中にエラーが発生しました。"
        }


@background(schedule=0)
def process_ai_generate(item_id, item_image):
    print("AI生成を開始します")
    item_instance = get_object_or_404(item, pk=item_id)
    image_path = os.path.join(BASE_DIR, "media", str(item_image))
    print("image_path: " + image_path)
    ai_info = generate_item_info(image_path)
    print("ai_info: " + str(ai_info))
    
    if isinstance(ai_info, dict):
        ai_data = ai_info
    else:
        try:
            ai_data = json.loads(ai_info)
        except Exception as e:
            print("ai_infoのパースに失敗しました: " + str(e))
            ai_data = {}
    
    try:
        # キーワードをJSON形式で保存
        keywords_json = json.dumps({'keywords': ai_data.get('keywords', '')})
        item_instance.ai_generated_json = keywords_json
        
        item_instance.item_name = ai_data.get('item_name', '')
        print("item_instance.item_name: " + str(item_instance.item_name))
        
        category_name = ai_data.get('category', 'その他')
        item_instance.item_category_id = get_object_or_404(item_category, category_name=category_name)
        print("item_instance.item_category_id: " + str(item_instance.item_category_id))
        
        # 現在時刻を設定
        item_instance.item_date = timezone.now()
        
        item_instance.save()
        print("AI生成が完了しました")
    except Exception as e:
        print(f"保存時にエラーが発生しました: {str(e)}")


global model
model = init()
