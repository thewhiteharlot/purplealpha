"""Find Songs Fast"""
# Made by- @DeletedUser420 idea- @AnInnocentboy
# Ported by @buddhhu

from typing import Tuple, Optional
from telethon.tl.types import InputMessagesFilterMusic
from telethon.errors import BadRequest
from userbot.events import register

def get_file_id_and_ref(message) -> Tuple[Optional[str], Optional[str]]:
    """ get file_id and file_ref """
    file_ = (message.audio or message.photo 
        or message.sticker or message.voice or message.video_note 
        or message.video or message.document)
    if file_:
        return file_.id, file_.file_reference
    return None, None

@register(pattern="^.smd(?: )(.*)")
async def search_song(event):
    """get movie from channel"""
    query = event.pattern_match.group(1)
    if not query:
        await event.reply("Provide a song to search")
        return
    search = await event.reply("🔍 __Searching For__ **{}**".format(query))
    chat_id = event.chat_id
    f_id = ""
    f_ref = ""
    try:
	      async for msg in event.client.iter_messages(-1001271479322, search=query,  limit=1, filter=InputMessagesFilterMusic):
	          f_id, f_ref = get_file_id_and_ref(msg)
  	except BadRequest:
		    await search.edit(
            "Join [THIS](https://t.me/joinchat/DdR2SUvJPBouSW4QlbJU4g) channel first"
        )
        return
	  if not (f_id or f_ref):
		    await search.edit("Song Not Found !")
	    	return
    await event.client.send_file(chat_id, msg)
    await search.delete()
    await search.delete()