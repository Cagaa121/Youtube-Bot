import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from btn import *
from database import *
from config import *
from utils import *
from state import *


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot=bot)

async def set_my_bot_commands(dp: Dispatcher):
   await dp.bot.set_my_commands([
  types.BotCommand("start", "Start bot"),
  types.BotCommand("me", "Myself"),
])
   await create_tables()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await message.answer("<b>🤖Дарова Cagaa Telegram Bot\nЯ помогу тебе скачать видео из Ютуба\nКидай ссылку</b>", reply_markup=menu)
  await add_user(message.from_user.id, message.from_user.username)


@dp.message_handler(text="Найти видео")
async def search_vid(message: types.Message):
  await message.answer("<b>Я могу Скачать Видео из Ютуба\nТолько до 20Мб\n\nСкоро мы это исправим\n\nСейчас можеш отправить ссылку👇</b>")

  await message.answer("⏳")

@dp.message_handler(commands=['send'])
async def sen_users(message: types.Message):
   user_id = message.from_user.id

   if user_id in ADMINS:
    await message.answer("Xabar: ")
    await RassilkaState.admin_message.set()

@dp.message_handler(content_types=['text', 'photo', 'animation'], state=RassilkaState.admin_message)
async def admin_message_state(message: types.Message, state: FSMContext):
  admin_message = message.text
  users = await get_all_user()
  
  await state.finish()


  sent = 0
  error = 0

  admin_message = message.text
  message_content = message.content_type
  users = await get_all_user()

  await state.finish()

  sent = 0
  error = 0
      
  for user in users:
          try:
            if message_content == 'text':
              await bot.send_message(
              chat_id=user[0],
              text=admin_message
              )
            elif message_content == 'photo':
              await bot.send_photo(
              chat_id=user[0],
              photo=message.photo[-1].file_id,
              caption=message.caption
              )
            elif message_content == 'animation':
               await bot.send_animation(
                chat_id=user[0],
                photo=message.photo[-1].file_id,
                caption=message.caption
               )

            sent +- 1
          except:
             error +- 1
             continue

  
  await message.answer(f"Xabar {len(users)} ta userga yollandi")



@dp.message_handler(content_types=['text'])
async def get_youtube_url(message: types.Message):
  video_url = message.text

  if video_url.startswith("https://www.youtube") or video_url.startswith("https://youtu.be"):

    wait_msg = await message.answer("⏳")
    video = await download_video(video_url, message.from_user.id)

    await wait_msg.delete()
    if video == "50mb":
      await message.answer("Hajmi yuqori")
    
    elif video:
      await message.answer_video(video=types.InputFile(video))

    else:
      await message.answer("Xatolik yuz berdi🤖")


if __name__ == "__main__":
 executor.start_polling(dp, on_startup=set_my_bot_commands)
