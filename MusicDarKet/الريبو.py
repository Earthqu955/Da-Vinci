import os
import sys
from datetime import datetime
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HNDLR, SUDO_USERS
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (    ("Minggu", 60 * 60 * 24 * 7),    ("Hari", 60 * 60 * 24),    ("Jam", 60 * 60),    ("Menit", 60),    ("Detik", 1),)
async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(    filters.user(SUDO_USERS) & filters.command(["ريستارت"], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("**🧸♥️ تـم اعـادة تشـغيل السـورس **")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
@Client.on_message(filters.command(["الاوامر"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b> 𓏺هِݪاެ حِبَيَبَ 🥇 {m.from_user.mention}!

Orders Music DarKet
——————×—————
𓏺ݪتَشِغِيَݪ صِۅٛتَيَة فَيَ اެݪمِكَاެݪمِة أࢪسِݪ ⇦ [ {HNDLR}تَشِغِيَݪ  + اެسِمِ اެݪاެغِنِيَة 
 ݪتَشِغِيَݪ فَيَدَيَۅٛ فَيَ اެݪمِكَاެݪمِة  ⇦ [ {HNDLR}تَشِغِيَݪ_فَيَدَيَۅٛ  + اެسِمِ اެݪاެغِنِيَة ]
– – – – – – – – – – – – – – – 

 | ݪأيَقِاެفَ اެݪاެغِنِيَة اެۅٛ اެݪفَيَدَيَۅٛ مِؤقِتَآ  ⇦ [ {HNDLR}اެسِتَئنِاެفَ ] 
 | ݪأعَاެدَهِ تَشِغِيَݪ اެݪاެغِنِيَة ⇦  [ {HNDLR}اެيَقِاެفَ_اެݪاެسِتَئنِاެفَ ]
 | ݪأيَقِاެفَ اެݪاެغِنِيَة  ⇦ [ {HNDLR}اެيَقِاެفَ ] 
– – – – – – – – – – – – – – – 

 | ݪتَحِمِيَݪ صِۅٛتَيَة أࢪسِݪ  [ {HNDLR}تَحِمِيَݪ + اެسِمِ اެݪاެغِنِيَة اެۅٛ اެݪࢪاެبَطَ ]
 | ݪتَحِمِيَݪ فَيَدَيَۅٛ    [ {HNDLR}تَحِمِيَݪ_فَيَدَيَۅٛ + اެسِمِ اެݪاެغِنِيَة اެۅٛ اެݪࢪاެبَطَ ]
– – – – – – – – – – – – – – – 

 | ݪأعَاެدَهِ تَشِغِيَݪ اެݪتَنِصِيَبَ أࢪسِݪ  [ {HNDLR}ࢪيَسِتَاެࢪتَ ]
– – – – – – – – – – – – – – –
 سـوࢪس Ξ𝗗𝗔𝗩𝗜𝗡𝗖𝗜™ 〆 @Z5ZZ8
مطـور السـورس  @ruur5"""
    await m.reply(HELP)
@Client.on_message(filters.command(["الريبو"], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
    await m.delete()
    REPO = f"""
<b> 𓏺هِݪاެ حِبَيَبَ 🥇 {m.from_user.mention}!

قنـاة السـورس  | @Z5ZZ8
مطـور السـورس | @ruur5
"""
    await m.reply(REPO, disable_web_page_preview=True)
