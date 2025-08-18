from bot.bot import bot


async def is_subscribed(user_id: int, channel_id: int) -> bool:
    """Проверяет, подписан ли пользователь на указанный канал."""
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False
