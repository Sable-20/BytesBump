import discord
from Admin.admin import Files

commands = discord.ext.commands
emoji = Files.emoji

class General(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def support(self, ctx):
    appinfo = await self.bot.application_info()
    return await ctx.send(embed=discord.Embed(
      description=f"**BytesBump** was developed by the [BytesToBits](https://discord.gg/r2rAUJZ) development team, and it is owned by `{appinfo.team.owner}`!\n\n[You can join the support server here!](https://discord.gg/8akycDh)",
      color=discord.Color.blue()
    )
    .set_footer(text="Powered by • BytesBump")
    .set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png")))

  @commands.command()
  async def invite(self, ctx):
    return await ctx.send(embed=discord.Embed(
      description=f"You can invite **BytesBump** by [Clicking Here!](https://discord.com/api/oauth2/authorize?client_id=776077253473337366&permissions=347137&scope=bot)",
      color=discord.Color.blue()
    )
    .set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png")))
  
  @commands.command(aliases=["about"])
  async def info(self, ctx):
    appinfo = await self.bot.application_info()
    owners = ', '.join([str(i) for i in appinfo.team.members])
    return await ctx.send(embed=discord.Embed(
      title=f"{self.bot.user.name} | Information",
      color=discord.Color.blurple()
    )
    .add_field(name="Version", value=Files.config("main", "version"))
    .add_field(name="Library", value="Discord.py")
    .add_field(name="Prefix", value=Files.config("main", "prefix"))
    .add_field(name="Guilds", value=len(self.bot.guilds))
    .add_field(name="Users", value=len(self.bot.users))
    .add_field(name="Support Server", value=f"[BytesToBits](https://discord.gg/r2rAUJZ)")
    .set_footer(text=f"Owned by {owners}")
    .set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png")))

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      seconds = round(error.retry_after)
      hours = seconds//3600
      seconds %= 3600
      minutes = seconds//60
      seconds %= 60
      if hours == 0:
        if minutes == 0:
          d = f"{seconds} seconds"
        else:
          d = f"{minutes} minutes and {seconds} seconds"
      else:
        d = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
      return await ctx.send(embed=discord.Embed(
        description=f"{emoji('warn')} You are on cooldown! Try again in **{d}**!",
        color=discord.Color.orange()
      ))

def setup(bot):
  bot.add_cog(General(bot))