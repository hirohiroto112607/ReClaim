from django.db import migrations

def add_item_categories(apps, schema_editor):
    ItemCategory = apps.get_model('items', 'item_category')
    categories = [
        '電子機器',
        '財布・貴重品',
        'かばん・バッグ',
        '衣類・アクセサリー',
        '文具・書類',
        '鍵',
        '傘',
        '定期券・カード類',
        'その他'
    ]
    for category in categories:
        ItemCategory.objects.create(category_name=category)

class Migration(migrations.Migration):
    dependencies = [
        ('items', '0009_alter_item_item_keyword'),
    ]

    operations = [
        migrations.RunPython(add_item_categories),
    ]