from aiogram.utils import executor
from config import dp
from handlers import start, echo_ban, fsm_form
from admin import start_admin
from database import sql_commands

start.register_handlers(dp=dp)
start_admin.register_handlers_admin(dp=dp)
fsm_form.register_handler_fsm_form(dp=dp)
echo_ban.register_echo_ban(dp=dp)


async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_user_table_query()
    print("Bot is ready")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )
