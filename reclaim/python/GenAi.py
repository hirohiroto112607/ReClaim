import base64
import os
import json

import google.generativeai as genai
import httpx
from background_task import background
from django.shortcuts import get_object_or_404
from items.models import item, item_category

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


def generate_by_text(prompt):
    response = model.generate_content(prompt)
    return response


def generate_by_image_url(prompt, image_url):
    image = httpx.get(image_url)
    file_etx = image_url.split(".")[-1]

    response = model.generate_content(
        [{'mime_type': f'image/{file_etx}', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])

    return response


def generate_by_image_path(image_path,
                           prompt="""
                この画像についてできる限り多く細かく詳しく
                この画像について
                できる限り多く細かく詳しく
                日本語と英語でキーワードを考えてください。
                背景・バックグラウンドは無視してください
                """):

    image_path = os.path.join(BASE_DIR, "media", str(image_path))
    print("image_path"+image_path)
    with open(image_path, 'rb') as f:
        data = f.read()
    # Base64で画像をエンコード
    base = base64.b64encode(data).decode('utf-8')
    file_etx = image_path.split(".")[-1]
    response = model.generate_content(
        [{'mime_type': f'image/{file_etx}', 'data': base}, prompt])

    # print(response.text)
    # response = "test"
    return response.text


def generate_item_info(image_path):
    """画像からタイトル、カテゴリー、キーワードを生成する"""

    image_path = os.path.join(BASE_DIR, "media", str(image_path))#ここでimagepathを絶対パスに変更
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


@background(schedule=1)
def process_ai_generate(item_id, item_image):
    print("AI生成を開始します")
    item_instance = get_object_or_404(item, pk=item_id)
    image_path = os.path.join(BASE_DIR, "media", str(item_image))
    print("image_path"+image_path)
    ai_info = generate_item_info(image_path)#この時点ではimagepathは相対パス
    print("ai_info"+str(ai_info))
    item_instance.ai_generated_json = ai_info.get('keywords', '')
    item_instance.item_name = ai_info.get('item_name', '')
    print("item_instance.item_name"+str(item_instance.item_name))
    item_instance.item_category_id = get_object_or_404(item_category,category_name = ai_info.get('category', 'その他'))
    print("item_instance.item_category_id"+str(item_instance.item_category_id))
    
    item_instance.save()
    print("AI生成が完了しました")


global model
model = init()

if __name__ == "__main__":

    prompt = "この画像はなんですか？"
    # image_url = "https://s3.resonite.love/resonite/d2cf6937-aeda-4ef3-9c6e-982a94cb0a7c.webp"
    # print(generate_by_image_url(prompt, image_url).text)
    image_path = "reclaim/media/images/タウンロート_1.jpeg"
    print(generate_by_image_path(prompt, image_path).text)
