####################################
# PornHub Telegram Bot by Garz Project
# name : tegar prayuda
# telegram channel : t.me/garzproject
# telegram profile : t.me/tegarprayudaa
# github profile : github.com/GarzProject
# Copyright 2022 | Garz Project
####################################

import asyncio
import os
import youtube_dl
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from pyrogram import Client, filters
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from pyrogram import Client, filters
from pyrogram.errors.exceptions import UserNotParticipant
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQuery,
                            InlineQueryResultArticle, InputTextMessageContent,
                            Message)
from youtube_dl.utils import DownloadError

from config import *
from helpers import download_progress_hook
from pyrogram import filters



SUDO = int(SUDO)
APP_ID = APP_ID
APP_HASH = APP_HASH
BOT_TOKEN = BOT_TOKEN
MUST_JOIN = MUST_JOIN
app = Client("pornhub_bot",
            api_id=APP_ID,
            api_hash=APP_HASH,
            bot_token=BOT_TOKEN)

if os.path.exists("downloads"):
    print("Unduhan Sudah Ada")
else:
    print("Unduhan Telah Dibuat")

btn1 = InlineKeyboardButton("Cari Disini",switch_inline_query_current_chat="",)
btn2 = InlineKeyboardButton("Masukan Grup", switch_inline_query="")

active_list = []
queue = []


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


def link_fil(filter, client, update):
    if "www.pornhub" in update.text:
        return True
    else:
        return False

link_filter = filters.create(link_fil, name="link_filter")


@app.on_message(~filters.edited & filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Bukan member channel
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"Kamu Harus Gabung Channel Terlebih Dahulu.\n\n[klik disini]({link}) Untuk Gabung Dan Mulai Menggunakan Bot Ini. \n\nSetelah Bergabung Silahkan Ketik /start Kembali !",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✨ Gabung Channel ✨", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")

@app.on_inline_query()
async def search(client, InlineQuery : InlineQuery):
    query = InlineQuery.query
    backend = AioHttpBackend()
    api = PornhubApi(backend=backend)
    results = []
    try:
        src = await api.search.search(query)#, ordering="mostviewed")
    except ValueError as e:
        results.append(InlineQueryResultArticle(
                title="Video Tidak Ditemukan!",
                description="Maaf! Video Tidak Ditemukan. Coba Lagi!!",
                input_message_content=InputTextMessageContent(
                    message_text="Video Tidak Ditemukan!"
                )
            ))
        await InlineQuery.answer(results,
                            switch_pm_text="Hasil Pencarian",
                            switch_pm_parameter="start")
            
        return


    videos = src.videos
    await backend.close()
    

    for vid in videos:

        try:
            pornstars = ", ".join(v for v in vid.pornstars)
            categories = ", ".join(v for v in vid.categories)
            tags = ", #".join(v for v in vid.tags)
        except:
            pornstars = "N/A"
            categories = "N/A"
            tags = "N/A"
        msgg = (f"**JUDUL** : `{vid.title}`\n"
                f"**DURASI** : `{vid.duration}`\n"
                f"JUMLAH PENONTON : `{vid.views}`\n\n"
                f"**{pornstars}**\n"
                f"Kategori : {categories}\n\n"
                f"{tags}"
                f"Link : {vid.url}")

        msg = f"{vid.url}"
         
        results.append(InlineQueryResultArticle(
            title=vid.title,
            input_message_content=InputTextMessageContent(
                message_text=msg,
            ),
            description=f"Durasi : {vid.duration}\nJumlah Penonton : {vid.views}\nRating Video : {vid.rating}",
            thumb_url=vid.thumb,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Tonton Diwebsite", url=vid.url),
                btn1
            ]]),
        ))

    await InlineQuery.answer(results,
                            switch_pm_text="Hasil Pencarian",
                            switch_pm_parameter="start")

# Memulai Bot
@app.on_message(filters.command("start"))
async def start(client, message : Message):
    value = str(message.chat.id)
    with open("member.txt", "a+") as file:
        file.seek(0) # set position to start of file
        lines = file.read().splitlines() # now we won't have those newlines
        if value in lines:
          print(f"user {value} lagi make bot")
        else:
          file.write(value + "\n")
    await message.reply(f"Hai @{message.from_user.username},\n"
                        "━━━━━━━━━━━━━━━\n"
                        "Saya Adalah Bot PornHub Indonesia\n"
                        "━━━━━━━━━━━━━━━\n"
                        "⚠️ Konten 18+\n"
                        "- Jangan Spam Pada Bot\n"
                        "- Tidak Diperuntukan Untuk Anak Dibawah Umur\n" 
                        "- Tidak Bermaksud Menyebatkan Pornografi.\n"
                        "- Ini Hanya Bot Dari Permintaan Orang Banyak.\n" 
                        "━━━━━━━━━━━━━━━\n\n"
			"Mari Bergabung Ke Channel @GarzProject\n\n"
			"Note: Pilih Video Durasi Sebentar Agar Proses Unduhan Dapat Lebih Cepat!!!\n\n\n"
                        "Klik Tombol Dibawah Ini Untuk Mencari:", reply_markup=InlineKeyboardMarkup([[btn1, btn2]]))
    

@app.on_message(link_filter)
async def options(client, message : Message):
    print(message.text)
    await message.reply("Apa Yang Anda Ingin Lakukan?", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Unduh", f"d_{message.text}"), InlineKeyboardButton("Tonton Di Web",url=message.text)]
            ])
            )


@app.on_callback_query(filters.regex("^d"))
async def download_video(client, callback : CallbackQuery):
    url = callback.data.split("_",1)[1]
    msg = await callback.message.edit("Mengunduh...")
    user_id = callback.message.from_user.id

    if "isjwhs" in active_list:
        await callback.message.edit("Maaf, Anda Hanya Dapat Mengunduh Video Dalam Satu Waktu!")
        return
    else:
        active_list.append(user_id)

    ydl_opts = {
            "progress_hooks": [lambda d: download_progress_hook(d, callback.message, client)]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            await run_async(ydl.download, [url])
        except DownloadError:
            await callback.message.edit("Maaf, Terjadi Kesalahan...")
            return


    for file in os.listdir('.'):
        if file.endswith(".mp4"):
            await callback.message.reply_video(f"{file}", caption="**Ini Adalah Video Yang Anda Minta Tuan**\n\nBot by:- @garzproject\n\nKami Butuh Biaya Sewa Server, Jika Anda Berkenan Untuk Terus Mendukung Silahkan Donasi Melalui saweria.co/tegarprayuda.",
                                reply_markup=InlineKeyboardMarkup([[btn1, btn2]]))
            os.remove(f"{file}")
            break
        else:
            continue

    await msg.delete()
    active_list.remove(user_id)


@app.on_message(filters.command("cc"))
async def download_video(client, message : Message):
    files = os.listdir("downloads")
    await message.reply(files)

@app.on_message(filters.command("stats") & filters.user(SUDO))
async def botsatats(_, message):
    users = open("member.txt").readlines()
    user = open("member.txt").read()
    total = len(users)
    await message.reply_text(f"Total : {total} Pengguna")
    await message.reply_text(f"{user}")

# Fitur broadcastttt
@app.on_message(filters.command('bcast') & filters.user(SUDO))
async def broadcast(_, message):
    if message.reply_to_message :
        await message.reply_text("Memulai Broadcast")
        query = open("member.txt").readlines()
        for row in query:
           try: 
            reply = message.reply_to_message
            await reply.copy(row)
           except:
            pass
            


app.run()
