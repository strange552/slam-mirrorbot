from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import deleteMessage, sendMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import dispatcher


def targdNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"Processing: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result, button = gd.targd(link)
        deleteMessage(context.bot, msg)
        if button == "":
            sendMessage(result, context.bot, update)
        else:
            if update.message.from_user.username:
                uname = f'@{update.message.from_user.username}'
            else:
                uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
            if uname is not None:
                cc = f'\n\ncc: {uname}'
            sendMarkup(result + cc, context.bot, update, button)
    else:
        sendMessage('Provide G-Drive Shareable Link to Tar.', context.bot, update)

targd_handler = CommandHandler(BotCommands.TargdCommand, targdNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(targd_handler)