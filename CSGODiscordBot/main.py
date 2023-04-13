from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context
import TrackerGG
from TrackerGG import CSGOClient

from constants import EMOJIS, TOKEN, TRACKERAPI_KEY


intents: discord.Intents = discord.Intents.all()
bot: commands.Bot = commands.Bot(
    command_prefix="$", intents=intents, case_insensitive=True
)

client = CSGOClient(TRACKERAPI_KEY)


def get_error_embed(desc: str) -> discord.Embed:
    return discord.Embed(title=":no_entry: Error", description=desc, color=0xFF0000)


@bot.event
async def on_ready() -> None:
    game = discord.Game(f"{len(bot.guilds)} 서버 / {len(bot.users)} 유저")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def profile(ctx: Context) -> None:
    if ctx.author.bot:
        return

    loading_message: discord.Message = await ctx.send(f"{EMOJIS.LOADING} Loading...")

    try:
        profile = await client.get_profile(ctx.message.content.split()[1])

        embed = discord.Embed(
            title=f"CSGO Stat of {profile.platform_info.platform_user_handle}",
            description=f"Playtime - {profile.segments[0].stats.time_played.display_value}",
        )
        embed.add_field(
            name="K/D", value=profile.segments[0].stats.kd.display_value, inline=False
        )
        embed.add_field(
            name="W/L",
            value=profile.segments[0].stats.wl_percentage.display_value,
            inline=False,
        )
        embed.add_field(
            name="Kill",
            value=profile.segments[0].stats.kills.display_value,
            inline=False,
        )
        embed.add_field(
            name="Headshot",
            value=profile.segments[0].stats.headshot_pct.display_value,
            inline=False,
        )
        embed.add_field(
            name="Accuracy",
            value=profile.segments[0].stats.shots_accuracy.display_value,
            inline=False,
        )
        embed.set_thumbnail(url=profile.platform_info.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        embed = get_error_embed(str(e))
        await ctx.send(embed=embed)

    finally:
        await loading_message.delete()


bot.run(TOKEN)
