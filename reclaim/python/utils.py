# -*- coding: utf-8 -*-
"""
utils.py

このモジュールでは、item_instanceの各フィールドのUnicode正規化や
AI生成JSONデータのデコードを行うヘルパー関数を提供します。
"""

import json
import unicodedata


def normalize_item_fields(item_instance):
    """
    item_instanceのフィールドをUnicode正規化して辞書形式で返します。
    :param item_instance: 対象のオブジェクト
    :return: 正規化されたフィールドを含む辞書
    """
    return {
        'name': unicodedata.normalize('NFKC', item_instance.item_name),
        'description': unicodedata.normalize('NFKC', item_instance.item_description),
        'location': unicodedata.normalize('NFKC', item_instance.item_lost_location),
    }


def decode_ai_json(ai_generated_json):
    """
    ai_generated_jsonが存在する場合にデコードして、必要に応じて
    'keywords'フィールドを抽出し返します。
    JSONのデコードに失敗した場合はNoneを返します。
    :param ai_generated_json: JSON形式の文字列
    :return: デコード結果、またはNone
    """
    if not ai_generated_json:
        return None
    try:
        data = json.loads(ai_generated_json)
        if isinstance(data, dict) and "keywords" in data:
            return data["keywords"]
        return data
    except json.JSONDecodeError:
        return None
