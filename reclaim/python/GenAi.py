import base64
import os

import google.generativeai as genai
import httpx
from dotenv import load_dotenv

from reclaim.settings import BASE_DIR

load_dotenv()


def init():
    genai.configure(api_key=os.getenv("GENAI-API-KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config={
                                  "response_mime_type": "application/json"}, 
                                  system_instruction="""
                                  この画像についてできる限り多く細かく詳しくJson"配列"でキーワードを上げてください。
                                  """)
    return model


def generate_by_text(prompt):
    model = init()
    response = model.generate_content(prompt)
    return response


def generate_by_image_url(prompt, image_url):
    model = init()
    image = httpx.get(image_url)
    file_etx = image_url.split(".")[-1]

    response = model.generate_content(
        [{'mime_type': f'image/{file_etx}', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])

    return response


def generate_by_image_path(prompt, image_path):
    model = init()
    image_path = os.path.join(BASE_DIR, "media", image_path)
    with open(image_path, 'rb') as f:
        data = f.read()
    # Base64で画像をエンコード
    base = base64.b64encode(data).decode('utf-8')
    file_etx = image_path.split(".")[-1]
    response = model.generate_content(
        [{'mime_type': f'image/{file_etx}', 'data': base}, prompt])
    print(response.text)
    return response


"""
reclaim/media/images/タウンロート_1.jpeg
"""
if __name__ == "__main__":

    prompt = "この画像はなんですか？"
    # image_url = "https://s3.resonite.love/resonite/d2cf6937-aeda-4ef3-9c6e-982a94cb0a7c.webp"
    # print(generate_by_image_url(prompt, image_url).text)
    image_path = "reclaim/media/images/タウンロート_1.jpeg"
    print(generate_by_image_path(prompt, image_path).text)
