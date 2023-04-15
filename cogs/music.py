from discord.ext import commands

import settings

import wavelink

class Music(commands.Cog):
    vc : wavelink.Player = None
    node = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        """Simple play command."""


        if self.node is None:
            node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password=settings.LAVA_PASS)
            await wavelink.NodePool.connect(client=self.bot, nodes=[node])

        if not ctx.voice_client:  
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        print(track)
        await vc.play(track)


    @commands.command()
    async def disconnect(self, ctx: commands.Context) -> None:
        """Simple disconnect command.

        This command assumes there is a currently connected Player.
        """
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

async def setup(bot):
    music_bot = Music(bot)
    await bot.add_cog(Music(bot))

