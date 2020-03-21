from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher

@run_async
def add_sticker(bot: Bot, update: Update):
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    set_name = 'pack_' + str(chat.id)[1:] + '_by_' + bot.username
    # TODO: If replied to images, optimize and stickerize 
    if message.reply_to_message.sticker:
        file_id = message.reply_to_message.sticker.file_id
    else:
        message.reply_text('bruh')
        return
    sticker_file = bot.get_file(file_id)
    sticker_file.download('sticker_input.png')
    sticker_target = 'sticker_input.png'
    sticker_emoji = '👌'
    
    try:
        set_target = bot.get_sticker_set(set_name)
        sticker_added = bot.add_sticker_to_set(
            user.id,
            set_name,
            png_sticker = open(sticker_target, 'rb'),
            emojis = sticker_emoji
        )
        if sticker_added:
            bot.send_message(
                message.chat.id,
                'Added to [%s](t.me/addstickers/%s).' % (set_target.title, set_name),
                parse_mode = ParseMode.MARKDOWN,
                reply_to_message_id = message.reply_to_message.message_id
            )
    except:
        set_title = str(chat.title) + ' Stickers'
        set_created = bot.create_new_sticker_set(
            user.id,
            set_name,
            set_title,
            png_sticker = open(sticker_target, 'rb'),
            emojis = sticker_emoji
        )
        if set_created:
            bot.send_message(
                message.chat.id,
                'Added to new pack: [%s](t.me/addstickers/%s).' % (set_title, set_name),
                parse_mode = ParseMode.MARKDOWN,
                reply_to_message_id = message.reply_to_message.message_id
            )


__mod_name__ = 'Stickers'

ADD_STICKER_HANDLER = CommandHandler('addsticker', add_sticker)

dispatcher.add_handler(ADD_STICKER_HANDLER)