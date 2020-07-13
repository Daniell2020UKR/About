#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# requires: youtube_dl>=2020.6.16.1

import os
import tempfile
import logging
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtube_dl import YoutubeDL
from .. import loader, utils  # pylint: disable=relative-beyond-top-level

logger = logging.getLogger(__name__)


@loader.tds
class YtDlMod(loader.Module):
    """ YouTube media downloader """
    strings = {
        "name": "YouTube DL"
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def yt2acmd(self, message):
        """ Download audio from YouTube """
        chat = await message.get_chat()
        args = utils.get_args(message)
        if args:
            dargs = {
                'format': 'bestaudio[ext=m4a][filesize<?250M]',
                'outtmpl': f'ytdl/audio-%(id)s.%(ext)s',
                'writethumbnail': True
            }
            await utils.answer(message, '<b>Downloading...</b>')
            try:
                audio_info = YoutubeDL(dargs).extract_info(args[0])
                id = audio_info['id']
                if os.path.exists(f'ytdl/audio-{id}.webp'):
                    thumbext = 'webp'
                else:
                    thumbext = 'jpg'
            except Exception as e:
                if "HTTP Error 429" in str(e):
                    await utils.answer(
                        message,
                        "<b>Your IP are banned by YouTube :(</b>"
                    )
                else:
                    await utils.answer(message, "<b>Error! Check logs for more info.</b>")
                logger.error(e, exc_info=True)
                try:
                    os.system("rm -rf ytdl/*")
                except Exception:
                    pass
                return
            await utils.answer(message, "<b>Uploading...</b>")
            try:
                await self.client.send_file(
                    chat,
                    file=open(f'ytdl/audio-{id}.m4a', 'rb'),
                    thumb=open(f'ytdl/audio-{id}.{thumbext}', 'rb')
                )
                await message.delete()
            except Exception as e:
                await utils.answer(message, "<b>Error! Check logs for more info.</b>")
                logger.error(e, exc_info=True)
                try:
                    os.system("rm -rf ytdl/*")
                except Exception:
                    pass
                return
            try:
                os.system("rm -rf ytdl/*")
            except Exception:
                pass
        else:
            await utils.answer(message, "<b>No arguments!</b>")

    async def yt2vcmd(self, message):
        """ Download video from YouTube """
        chat = await message.get_chat()
        args = utils.get_args(message)
        if args:
            dargs = {
                'format': ('bestvideo[ext=mp4]'
                           '[filesize<?250M]+bestaudio[ext=m4a]'
                           '[filesize<?250M]'),
                'outtmpl': f'ytdl/video-%(id)s.%(ext)s',
                'writethumbnail': True
            }
            await utils.answer(message, '<b>Downloading...</b>')
            try:
                video_info = YoutubeDL(dargs).extract_info(args[0])
                id = video_info['id']
                if os.path.exists(f'ytdl/video-{id}.webp'):
                    thumbext = 'webp'
                else:
                    thumbext = 'jpg'
            except Exception as e:
                if "HTTP Error 429" in str(e):
                    await utils.answer(
                        message,
                        "<b>Your IP are banned by YouTube :(</b>"
                    )
                else:
                    await utils.answer(message, "<b>Error! Check logs for more info.</b>")
                logger.error(e, exc_info=True)
                try:
                    os.system("rm -rf ytdl/*")
                except Exception:
                    pass
                return
            await utils.answer(message, '<b>Uploading...</b>')
            try:
                await self.client.send_file(
                    chat,
                    file=open(f'ytdl/video-{id}.mp4', 'rb'),
                    thumb=open(f'ytdl/video-{id}.{thumbext}', 'rb'),
                    attributes=[DocumentAttributeVideo(
                        duration=video_info['duration'],
                        w=video_info['width'],
                        h=video_info['height'],
                        round_message=False,
                        supports_streaming=True
                    )]
                )
                await message.delete()
            except Exception as e:
                await utils.answer(message, "<b>Error! Check logs for more info.</b>")
                logger.error(e, exc_info=True)
                try:
                    os.system("rm -rf ytdl/*")
                except Exception:
                    pass
                return
            try:
                os.system("rm -rf ytdl/*")
            except Exception:
                pass
        else:
            await utils.answer(message, "<b>No arguments!</b>")
