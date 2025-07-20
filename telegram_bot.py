import asyncio
import os
import time

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from google.adk.events import Event, EventActions
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from requests import HTTPError

from utils.http_client import login
from agents import root_erp_agent
from utils.call_agent import call_agent_async


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable must be set.")

# All of your Bot events should be handled in the Dispatcher.
dp = Dispatcher()
bot = Bot(TOKEN)

session_service = InMemorySessionService()
APP_NAME = "erp_agent"

# Initialize Runner globally
runner_agent_team = Runner(
    agent=root_erp_agent,
    app_name=APP_NAME,
    session_service=session_service
)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    user_id = str(message.from_user.id)
    session_id = f"telegram_{user_id}"

    # Check if a session already exists
    existing_session = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)

    if existing_session and "user_language" in existing_session.state and existing_session.state["user_language"]:
        # If session and language exist, just re-introduce in the existing language
        lang_code = existing_session.state["user_language"]
        if lang_code == "uz":
            response_text = "Assalomu alaykum! Men Asilman, ERP yordamchingiz. Siz bilan qanday mahsulotlarni boshqarishim mumkin?"
        elif lang_code == "ru":
            response_text = "Здравствуйте! Я Асил, ваш ERP помощник. Чем могу помочь вам в управлении продуктами?"
        elif lang_code == "en":
            response_text = "Hello! I am Asil, your ERP assistant. How can I help you manage products today?"
        else:
            response_text = "Hello! I am Asil, your ERP assistant. How can I help you manage products today?"
        await message.answer(response_text)
    else:
        # If no session or language, prompt for language selection
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data="lang_uz"))
        builder.add(types.InlineKeyboardButton(text="🇷🇺 Russian", callback_data="lang_ru"))
        builder.add(types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"))

        await message.answer(
            "Please choose your preferred language: ",
            reply_markup=builder.as_markup()
        )


@dp.callback_query(lambda c: c.data and c.data.startswith('lang_'))
async def process_language_selection(callback_query: types.CallbackQuery):
    lang_code = callback_query.data.split('_')[1]  # Extracts 'uz', 'ru', or 'en'
    user_id = str(callback_query.from_user.id)
    session_id = f"telegram_{user_id}"

    # Attempt to get the session
    session_data = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)

    # Since there's no update, we delete the old session (if any) and create a new one with the selected language
    if session_data:
        await session_service.delete_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    initial_state = {
        "user_language": lang_code,
        "awaiting_credentials": True
    }
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state=initial_state
    )

    # Acknowledge the callback query to remove the loading state on the button
    await callback_query.answer()

    # Ask for credentials
    if lang_code == "uz":
        response_text = "Iltimos, login va parolingizni bir qatorda, bo'sh joy bilan ajratib yuboring."
    elif lang_code == "ru":
        response_text = "Пожалуйста, отправьте ваш логин и пароль в одной строке, разделенные пробелом."
    elif lang_code == "en":
        response_text = "Please send your login and password in one line, separated by a space."
    else:
        response_text = "Please send your login and password in one line, separated by a space."

    await bot.send_message(callback_query.message.chat.id, response_text, parse_mode=ParseMode.HTML)


async def credentials_handler(message: types.Message):
    user_id = str(message.from_user.id)
    session_id = f"telegram_{user_id}"
    credentials = message.text.split()

    session = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    lang_code = session.state.get("user_language", "en")

    if len(credentials) != 2:
        if lang_code == "uz":
            await message.answer("Iltimos, login va parolni bo'sh joy bilan ajratib, bitta xabarda yuboring.")
        elif lang_code == "ru":
            await message.answer("Пожалуйста, отправьте логин и пароль в одном сообщении, разделив их пробелом.")
        else:
            await message.answer("Please send the login and password in a single message, separated by a space.")
        return

    input_login, password = credentials
    try:
        login_response = login(input_login, password)

        """
        Session State update
        """
        state_update = {
            "user_language": lang_code,
            "awaiting_credentials": False,
            "user_id": login_response["user_id"],
            "merchant_id": login_response["merchant_id"],
            "branch_id": login_response["branch_id"],
            "bearer_token": login_response["bearer_token"],
            "refresh_token": login_response["refresh_token"]
        }
        actions_with_update = EventActions(state_delta=state_update)
        system_event = Event(
            invocation_id="inv_login_update",
            author="system",
            actions=actions_with_update,
            timestamp=time.time()
        )
        await session_service.append_event(session, system_event)

        if lang_code == "uz":
            response_text = "Rahmat! Siz tizimga muvaffaqiyatli kirdingiz. Endi savollaringizni berishingiz mumkin."
        elif lang_code == "ru":
            response_text = "Спасибо! Вы успешно вошли в систему. Теперь вы можете задавать свои вопросы."
        else:
            response_text = "Thank you! You have successfully logged in. You can now ask your questions."
        await message.answer(response_text)

    except HTTPError:
        if lang_code == "uz":
            await message.answer("Login yoki parol noto'g'ri. Iltimos, qayta urinib ko'ring.")
        elif lang_code == "ru":
            await message.answer("Неверный логин или пароль. Пожалуйста, попробуйте еще раз.")
        else:
            await message.answer("Invalid login or password. Please try again.")
    except Exception as e:
        if lang_code == "uz":
            await message.answer(f"Tizimga kirishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring. {str(e)}")
        elif lang_code == "ru":
            await message.answer(f"Произошла ошибка при входе в систему. Пожалуйста, повторите попытку позже. {str(e)}")
        else:
            await message.answer(f"An error occurred while logging in. Please try again later. {str(e)}")


@dp.message()
async def all_messages_handler(message: types.Message) -> None:
    user_id = str(message.from_user.id)
    session_id = f"telegram_{user_id}"
    user_query = message.text

    # Fetch the session to get the user's language preference
    session_data = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)

    if not session_data or "user_language" not in session_data.state or not session_data.state["user_language"]:
        await message.answer("Please select your language first by typing /start.")
        return

    if session_data.state.get("awaiting_credentials"):
        await credentials_handler(message)
        return

    if "bearer_token" not in session_data.state:
        await message.answer("Please login first.")
        return

    # Send a loading message
    loading_message = await message.answer("⏳...")

    # Use the user_language from the session state when calling the agent
    # The root_shop_agent will use this from tool_context.state

    final_response_text = await call_agent_async(user_query, runner=runner_agent_team, user_id=user_id, session_id=session_id)

    # Edit the loading message with the final response
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=loading_message.message_id,
        text=final_response_text,
        parse_mode=ParseMode.HTML
    )


async def main() -> None:
    # And the run events dispatching using aiogram.
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
