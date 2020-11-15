import discord, asyncio
from Admin.database import Database as db
from Admin.admin import Files

commands = discord.ext.commands
emoji = Files.emoji

class Bump(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.guild_only()
  @commands.cooldown(1, 3600, commands.BucketType.guild)
  @commands.command()
  async def bump(self, ctx):
    guild = ctx.guild
    if not db.exists(guild):
      ctx.command.reset_cooldown(ctx)
      return await ctx.send(embed=discord.Embed(
        description=f"{emoji('cross')} This server seems to not exist in the Database! Use `=setup`!",
        color=discord.Color.red()
      ))
    invchannel, description, color = db.get(guild)["fetch_invite"], db.get(guild)["description"], db.get(guild)["color"]

    try:
      invite = await ctx.guild.get_channel(invchannel).create_invite(max_uses=0, temporary=False, max_age=0, unique=False)
    except Exception as e:
      ctx.command.reset_cooldown(ctx)
      return await ctx.send(embed=discord.Embed(
        description=f"{emoji('cross')} Cannot fetch invite! Please review the following error, and if you can't solve it, please contact the developers in the [Support Server](https://discord.gg/r2rAUJZ)!",
        color=discord.Color.red()
      )
      .add_field(name="Exception", value=f"```{e}```"))
    
    embed = discord.Embed(
      title=guild.name,
      description=description,
      color=discord.Color(value=color),
      url=invite.url
    )
    embed.add_field(name="👑 **Owner**", value=guild.owner.name)
    embed.add_field(name=f"{emoji('boost')} **Boosts**", value=guild.premium_subscription_count)
    embed.add_field(name=f"{emoji('online')} **Members**", value=len(guild.members))
    embed.add_field(name=f"{emoji('emojis')} **Emojis**", value=f"{len(guild.emojis)}/{guild.emoji_limit}")
    embed.add_field(name=f"{emoji('region')} **Region**", value=str(guild.region).capitalize())
    embed.add_field(name=f"{emoji('ccheck')} **Join**", value=f"**[Join {guild.name}!]({invite.url})**")
    embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
    embed.set_footer(text="Powered by • BytesBump")
    msg = await ctx.send(embed=discord.Embed(
      description=f"{emoji('loading')} **Bumping your server...!**\nThis might take some time, so don't worry!",
      color=discord.Color.orange()
    ))
    success, fail = 0, 0
    channels = [i["listing"] for i in db.get_all() if not i["listing"] == None]
    for channel in channels:
      try:
        await asyncio.sleep(1)
        await self.bot.get_channel(channel).send(embed=embed)
        success+=1
      except:
        try:
          temp = self.bot.get_guild(db.find({"listing":channel})["_id"])
          db.delete(temp)
        except:
          return db.delete(db.find({"listing":channel})["_id"])
        await temp.owner.send(embed=discord.Embed(
          title=f"{emoji('warn')} ATTENTION REQUIRED {emoji('warn')}",
          description=f"The bot cannot find or send messages in your listing channel, therefore we have removed your server ({temp.name}) from the Database! Run `=setup` again to set it up!",
          color=discord.Color.red()
        ))
        fail+=1
    await msg.edit(embed=discord.Embed(
      title=f"{emoji('ccheck')} Guild Bumped!",
      description=f"Your server was successfully bumped to `{success}` guilds! There were {fail} errors encountered on guilds, and they were removed from the database!",
      color=discord.Color.green()
    ))
    await asyncio.sleep(60)
    return await msg.edit(embed=discord.Embed(
      title="Server was bumped, but this is the MOTD!",
      description=Files.read("Admin/Messages/promotional.txt"),
      color=discord.Color.green()
      ))
    
    
def setup(bot):
  bot.add_cog(Bump(bot))
