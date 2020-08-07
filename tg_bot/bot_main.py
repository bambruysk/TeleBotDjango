from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.utils.request import Request

from TeleBotDjango.settings import TELEGRAM_BOT_TOKEN, PROXY_URL
from tg_bot.test_db import create_test_db





def run():
    token = TELEGRAM_BOT_TOKEN
    # token = os.environ.get("TG_BOT_TOKEN", "")
    # clear_database()
    create_test_db()
    # 1 -- правильное подключение
    request = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(

        token=token,
        base_url=PROXY_URL,
    )
    print(bot.get_me())

    # 2 -- обработчики
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(show_answer, pattern=str(ASK_QUESTIONS)))
    dispatcher.add_handler(CreatePetitionHandler(ep_pattern=r"^" + str(PETITION), ret=show_main_menu))
    #  dispatcher.add_handler(CallbackQueryHandler(edit_profile, pattern=r"^" + str(PROFILE)))
    dispatcher.add_handler(edit_profile_handler)

    updater.start_polling()

    updater.idle()
