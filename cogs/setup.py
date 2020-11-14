import discord, asyncio
from Admin.database import Database as db
from Admin.admin import Files

commands = discord.ext.commands
emoji = Files.emoji

class Setup(commands.Cog): 
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    try:
      await guild.owner.send(embed=discord.Embed(
        title="Thanks for inviting BytesBump",
        description=Files.read("Admin/Messages/invite.txt").format(guild.owner.mention,guild.name),
        color=discord.Color.blurple()
      )
      .set_author(name="BytesBump", icon_url=self.bot.user.avatar_url, url="https://discord.gg/jT8wGa9s5g"))
    except: pass
    return db.add(guild)
  
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    return db.delete(guild)

  @commands.guild_only()
  @commands.has_permissions(manage_guild=True)
  @commands.command(name="setup")
  async def setup(self, ctx):
    if not db.exists(ctx.guild): db.add(ctx.guild)
    async def cancel(t):
      return await ctx.send(embed=discord.Embed(
        description=f"{emoji('warn')} {t}",
        color=discord.Color.orange()
      ))

    async def ask(q):
      return await ctx.send(embed=discord.Embed(
        description=f"{emoji('loading')} {q}",
        color=discord.Color.blurple()
      ))
    
    def basic_check(message):
      return message.author == ctx.author and message.channel == message.channel and len(message.content) != 0
    
    await ask("Enter your server's description!")
    try:
      description = await self.bot.wait_for("message", check=basic_check, timeout=120)
      description = description.content
      if len(description) < 250 or len(description) >= 2048:
        return await cancel("Your description must be at least **250 characters long** and can't be more than **2048 characters**! Setup canceled.")
    except asyncio.TimeoutError:
      return await cancel("Setup timed out! Please redo the command!")

    await ask("Mention the channel you want to fetch invites from!")
    try:
      channel = await self.bot.wait_for("message", check=basic_check, timeout=60)
      channel = channel.content
    except asyncio.TimeoutError:
      return await cancel("Setup timed out! Please redo the command!")
    try:
      channel = await commands.TextChannelConverter().convert(ctx, channel)
    except commands.ChannelNotFound:
      return await cancel("Invalid channel, please mention a valid **Text Channel**!")

    await ask("Mention the channel you want to send bumps at!")    
    try:
      lp = await self.bot.wait_for("message", check=basic_check, timeout=60)
      lp = lp.content
    except asyncio.TimeoutError:
      return await cancel("Setup timed out! Please redo the command!")
    
    try:
      lp = await commands.TextChannelConverter().convert(ctx, lp)
    except commands.ChannelNotFound:
      return await cancel("Invalid channel, please mention a valid **Text Channel**!")
    
    await ask("Enter the color you want for your server! (Only `HEX` codes are accepted)")
    try:
      color = await self.bot.wait_for("message", check=basic_check, timeout=120)
      color = color.content
    except asyncio.TimeoutError:
      return await cancel("Setup timed out! Please redo the command!")
    try:
      color = int(color.replace("#",""), 16)
    except ValueError:
      return await cancel("This is an invalid color! You can use [this tool](https://htmlcolorcodes.com/) to choose a valid HEX color!")
    
    post = {
      "fetch_invite": channel.id,
      "listing":lp.id,
      "color":color,
      "description":description
    }
    db.update(ctx.guild, post)
    return await ctx.send(embed=discord.Embed(
      description=f"{emoji('ccheck')} Your server is ready to be bumped! Use `=bump` to bump it every 1 hour!",
      color=discord.Color.green()
    ))

def setup(bot):
  bot.add_cog(Setup(bot))