from aiogram import types
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
import asyncio
from typing import Union, List

from bot.bot import bot


async def broadcast_message(
        user_ids: List[int],
        text: str = "",
        media: Union[types.InputFile, str] = None,
        media_type: str = None,
        parse_mode: str = "HTML",
        disable_notification: bool = False,
        button_data: dict = None,
        disable_web_page_preview: bool = True  # Добавляем новый параметр
) -> dict:
    """
    Делает массовую рассылку сообщений пользователям

    :param user_ids: Список user_id для рассылки
    :param text: Текст сообщения
    :param media: Медиафайл (путь или объект InputFile)
    :param media_type: Тип медиа ('photo', 'video', 'audio', 'voice', 'document')
    :param parse_mode: Режим парсинга текста
    :param disable_notification: Отправлять без уведомления
    :param button_data: Данные кнопки в формате {'name': str, 'url': str}

    :return: Статистика {success: int, failed: int, errors: dict}
    """
    results = {
        'success': 0,
        'failed': 0,
        'errors': {}
    }

    # Создаем клавиатуру с кнопкой, если она передана
    reply_markup = None
    if button_data:
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton(
            text=button_data['name'],
            url=button_data['url']
        ))

    for user_id in user_ids:
        try:
            if media and media_type:
                # Отправка медиа
                send_method = {
                    'photo': bot.send_photo,
                    'video': bot.send_video,
                    'audio': bot.send_audio,
                    'voice': bot.send_voice,
                    'document': bot.send_document,
                    'animation': bot.send_animation
                }.get(media_type)

                if not send_method:
                    raise ValueError(f"Неизвестный тип медиа: {media_type}")

                # Формируем аргументы для отправки
                kwargs = {
                    'chat_id': user_id,
                    media_type: media,  # ✅ Только нужный параметр (photo/video/audio...)
                    'caption': text,
                    'parse_mode': parse_mode,
                    'disable_notification': disable_notification,
                }

                # Добавляем клавиатуру, если есть
                if reply_markup:
                    kwargs['reply_markup'] = reply_markup

                await send_method(**kwargs)
            else:
                # Отправка текста
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_web_page_preview,
                )

            results['success'] += 1

            # Небольшая задержка чтобы не нагружать сервер
            await asyncio.sleep(0.01)

        except BotBlocked:
            results['failed'] += 1
            results['errors'][user_id] = "Пользователь заблокировал бота"

        except ChatNotFound:
            results['failed'] += 1
            results['errors'][user_id] = "Чат не найден"
        except Exception as e:
            results['failed'] += 1
            results['errors'][user_id] = str(e)

    return results