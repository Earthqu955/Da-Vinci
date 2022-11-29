import asyncio
import math
import os
import time
import aiofiles
import aiohttp
import wget
import aiohttp
from io import BytesIO
from traceback import format_exc
from pyrogram import Client, filters
from pyrogram.types import Message
from Python_ARQ import ARQ
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio,    HighQualityVideo,    LowQualityVideo,    MediumQualityVideo
from youtubesearchpython import VideosSearch
from config import HNDLR, bot, call_py
from MusicDarKet.helpers.queues import QUEUE, add_to_queue, get_queue, clear_queue
from MusicDarKet.helpers.decorators import authorized_users_only
from MusicDarKet.helpers.handlers import skip_current_song, skip_item
from pyrogram.errors import FloodWait, MessageNotModified
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from MusicDarKet.helpers.merrors import capture_err
ARQ_API_KEY = "QFOTZM-GSZUFY-CHGHRX-TDEHOZ-ARQ"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0
async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(        "yt-dlp",        "-g",        "-f",                "bestaudio",        f"{link}",        stdout=asyncio.subprocess.PIPE,        stderr=asyncio.subprocess.PIPE,    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://te.legra.ph/file/28519035fc9c98b9263c6.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0
async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(        "yt-dlp",        "-g",        "-f",              "best[height<=?720][width<=?1280]",        f"{link}",        stdout=asyncio.subprocess.PIPE,        stderr=asyncio.subprocess.PIPE,    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

@Client.on_message(filters.command(["ش"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**❤️‍🔥 𓏺يَتَمِ اެݪتَشِغِيَݪ  **")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://te.legra.ph/file/28519035fc9c98b9263c6.jpg",
                    caption=f"""
**❤️‍🔥 𓏺اެݪعَنِۅٛاެنِ : [{songname}]({link})
❤️‍🔥 𓏺اެيَدَيَ اެݪمِحِادَثَة : {chat_id}
❤️‍🔥 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",                )
            else:
                await call_py.join_group_call(                    chat_id,                    AudioPiped(                        dl,                    ),                    stream_type=StreamType().pulse_stream,                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://te.legra.ph/file/28519035fc9c98b9263c6.jpg",
                    caption=f"""
**❤️‍🔥 𓏺اެݪعَنِۅٛاެنِ : [{songname}]({link})
❤️‍🔥 𓏺اެيَدَيَ اެݪمِحِادَثَة : {chat_id}
❤️‍🔥 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",                )

    else:
        if len(m.command) < 2:
            await m.reply("𓏺اެݪࢪدَ عَݪى مِݪفَ صِۅٛتَيَ اެۅٛ اެعَطَاެء شِيَء ݪݪبَحِثَ ❤️‍🔥")
        else:
            await m.delete()
            huehue = await m.reply(" 𓏺جَـاެࢪيَ اެݪبَحِـثَ ❤️‍🔥 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("𓏺ݪمِ يَتَمِ اެݪعَثَۅٛࢪ عَݪى اެݪفَنِاެنِ اެࢪسِݪ اެسِمِ اެݪفَنِاެنِ بَشِكَݪ صِحِيَحِ ❤️‍🔥. ")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**عذرا هناك خطأ  ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**❤️‍🔥  𓏺اެݪعَنِۅٛاެنِ : [{songname}]({url})
𓏺مِـدَة اެݪفَيَدَيَۅٛ 🤺 : {duration}
❤️‍🔥 𓏺اެيَدَيَ اެݪمِحِادَثَة : {chat_id}
❤️‍🔥 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**❤️‍🔥  𓏺اެݪعَنِۅٛاެنِ : [{songname}]({url})
𓏺مِـدَة اެݪفَيَدَيَۅٛ 🤺 : {duration}
𓏺اެيَدَيَ اެݪمِحِادَثَة : {chat_id}
❤️‍🔥 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["ش فيديو"], prefixes=f"{HNDLR}"))
async def vplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**❤️‍🔥 𓏺يَتَمِ اެݪتَشِغِيَݪ  **")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(                        "مسموح فقط بالدقه الأتيه :  720 ، 480 ، 360 \n ينزل الان الآن بدقة 720 بكسل   "                 )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://te.legra.ph/file/28519035fc9c98b9263c6.jpg",
                    caption=f"""
**❤️‍🔥 𓏺اެݪعَنِۅٛاެنِ : [{songname}]({link})
❤️‍🔥 𓏺اެيَدَيَ اެݪمِحِدَثَة : {chat_id}
🤺 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://te.legra.ph/file/28519035fc9c98b9263c6.jpg",
                    caption=f"""
**❤️‍🔥 𓏺اެݪعَنِۅٛاެنِ : [{songname}]({link})
🤺 𓏺اެيَدَيَ اެݪمِحِدَثَة : {chat_id}
❤️‍🔥 𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",                )

    else:
        if len(m.command) < 2:
            await m.reply(                "**𓏺اެݪࢪدَ عَݪى مِݪفَ صِۅٛتَيَ اެۅٛ اެعَطَاެء شِيَء ݪݪبَحِثَ ❤️‍🔥**"            )
        else:
            await m.delete()
            huehue = await m.reply("**𓏺جَـاެࢪيَ اެݪبَحِـثَ ❤️‍🔥 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(                    "**لم يتم العثور على شيء**"                )
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**عذرا هناك خطأ  ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**🤺  𓏺اެݪعَنِۅٛاެنِ : [{songname}]({url})
 𓏺مِـدَة اެݪفَيَدَيَۅٛ 🤺 : {duration}
 ❤️‍🔥𓏺اެيَدَيَ اެݪمِحِدَثَة : {chat_id}
𓏺طَݪبَ مِنِ اެݪكَيَ ❤️‍🔥 : {m.from_user.mention}**
""",                        )
                    else:
                        try:
                            await call_py.join_group_call(                                chat_id,                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),                                stream_type=StreamType().pulse_stream,                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**  𓏺اެݪعَنِۅٛاެنِ : [{songname}]({url})
 𓏺مِـدَة اެݪفَيَدَيَۅٛ 🤺 : {duration}
𓏺اެيَدَيَ اެݪمِحِدَثَة : {chat_id}
𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["عشوائي"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(            f"**استعمال :** \n\n`{HNDLR}اغنيه عشوائيه  [قم بوضع جانب الامر معرف المحادثه او ايدي المحادثه]` \n"        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"🌵 يأخذ {limit} أغنية عشوائية من {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(                        chat_id,                        AudioPiped(location),                        stream_type=StreamType().pulse_stream,                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    await m.reply_photo(
                        photo="https://te.legra.ph/file/28519035fc9c98b9263c6.jpg",
                        caption=f"""
**𓏺تَمِ تَشِغِيَݪ اެݪاެغِنِيَـة عَبَـࢪ سِيَࢪفَـࢪ @Z5ZZ8 ❤️‍🔥 {chat}
𓏺اެݪعَنِۅٛاެنِ : [{songname}]({link})
𓏺اެيَدَيَ اެݪمِحِدَثَة : {chat_id}
𓏺طَݪبَ مِنِ اެݪكَيَ : {m.from_user.mention}**
""",                    )
            await hmm.delete()
            await m.reply(                f"➕ يضيف {lmt} أغنية في قائمة الانتظار \n• ارسل {HNDLR}التشغيل_التلقائي لاضاف اغنيه في القائمه الانتضار**"            )
        except Exception as e:
            await hmm.edit(f"**هناك خطا ** \n`{e}`")


@Client.on_message(filters.command(["التشغيل التلقائي", "queue"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(                f"**🎧 تشغيل الان :** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",                disable_web_page_preview=True,            )
        else:
            QUE = f"**🎧 تشغيل الان :** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ قائمة الانتظار :**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**𓏺مِعَݪيَشِ مِاެفَيَ شِيَ مِشِتَغِݪ 🌵.**")
@Client.on_message(filters.command(["التالي"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**𓏺مِعَݪيَشِ مِاެفَيَ شِيَ مِشِتَغِݪ ݪتَخِطَيَ ،**")
        elif op == 1:
            await m.reply("قائمة انتظار فارغة ، مغادرة الدردشة الصوتية**")
        else:
            await m.reply(                f"**تخطي التشغيل ** \n**🎧 التشغيل الان** - [{op[0]}]({op[1]}) | `{op[2]}`",                disable_web_page_preview=True,            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ تمت إزالة الأغاني التالية من قائمة الانتظار : -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["ك", "ت"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**𓏺تَمِ تَخِطَيَ اެݪتَشِغِيَݪ بَنِجَاެحِ ❤️‍🔥**")
        except Exception as e:
            await m.reply(f"**هناك خطأ ** \n`{e}`")
    else:
        await m.reply("**𓏺مِعَݪيَشِ مِاެفَيَ شِيَ مِشِتَغِݪ 🌵.**")
@Client.on_message(filters.command(["استئناف"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(                f"**⏸ تم إيقاف التشغيل مؤقتًا.**\n\n• يمكنك ارجاع التشغيل بواسطه ارسال امر  » `{HNDLR}ايقاف_الاستئناف`"            )
        except Exception as e:
            await m.reply(f"**هناك خطأ ** \n`{e}`")
    else:
        await m.reply("** ❌ لايوجد اغنيه مشتغله !**") 
@Client.on_message(filters.command(["ايقاف_الاستئناف"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(                f"**▶ استئناف التشغيل المتوقف مؤقتًا **"            )
        except Exception as e:
            await m.reply(f"**هناك خطأ ** \n`{e}`")
    else:
        await m.reply("**❌ لا شيء متوقف مؤقتا حاليا !**")

