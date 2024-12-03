from aiogram import Bot, Dispatcher, types, F
import asyncio
from anaylise import has_cyrillic
from baza import to_cyrillic, to_latin
from read_word import word_reader

token = '7701673870:AAEVxnO7k7bMlPhY_PQd3qLFwyohGx48sl4'
bot = Bot(token=token)
dp = Dispatcher()

@dp.message(F.text)
async def get_message(message:types.Message):
    text = message.text
    if has_cyrillic(text=text):
       await message.answer(to_latin(text))
    else:
       await message.answer(to_cyrillic(text))

@dp.message(F.document)
async def get_doc(message:types.Message):
    document = message.document
    file_id = message.document.file_id
    file_name = message.document.file_name
    type = str(message.document.mime_type)
    size = message.document.file_size
    document_type = file_name[file_name.rindex('.')+1:]
    if document_type == 'docx':
        import time
        custom_name = f"{file_id}_{time.time}"
        file = await bot.get_file(file_id=file_id)
        await bot.download(file=file, destination=custom_name)
        black = '🖤' 
        whait = '🤍'
        data = await message.answer("Fayl qabul qilindi")
        for i in range(1,11):
            await data.edit_text(f"Fayl serverga yuklanmoqda\n"
            f"{i*black}{(10-i)*whait}")
            await data.delete()
            word_reader(file=custom_name)
            new_document = types.input_file.FSInputFile(path=custom_name, filename=file_name)
            await message.answer_document(document=new_document)
    else:
        await message.answer("Iltimos faylni word(docx) tipida yuboring")
async def main():

    await dp.start_polling(bot)
if __name__=='__main__':
    asyncio.run(main())