from items.models import item_message


def unread_messages(request):
    """
    未読メッセージの数をコンテキストに追加するコンテキストプロセッサ
    """
    unread_count = 0
    
    # ログインユーザーがいる場合のみカウント
    if request.user.is_authenticated:
        unread_count = item_message.objects.filter(receiver=request.user).count()
    
    return {
        'unread_message_count': unread_count
    }