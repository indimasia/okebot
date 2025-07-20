import discord
from discord.ext import commands
import asyncio
import datetime
from config import DISCORD_TOKEN, BOT_PREFIX, BOT_NAME, BOT_VERSION

# Setup bot dengan intents yang diperlukan
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Event called when bot is ready"""
    print(f'🤖 {bot.user} has logged in to Discord!')
    print(f'📊 Bot connected to {len(bot.guilds)} servers')
    print(f'👥 Serving {len(bot.users)} users')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME} v{BOT_VERSION}"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Command not found! Use `{BOT_PREFIX}help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")

@bot.command(name='ping')
async def ping(ctx):
    """Test bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: **{latency}ms**",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title=f"ℹ️ {BOT_NAME} Information",
        description="A simple Discord bot built with Python",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    
    embed.add_field(name="📊 Statistics", value=f"Servers: {len(bot.guilds)}\nUsers: {len(bot.users)}", inline=True)
    embed.add_field(name="⚡ Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🔧 Version", value=BOT_VERSION, inline=True)
    
    embed.add_field(name="👨‍💻 Developer", value="Built with ❤️ using discord.py", inline=False)
    embed.add_field(name="📝 Prefix", value=f"`{BOT_PREFIX}`", inline=False)
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='server')
async def server_info(ctx):
    """Display server information"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"🏠 Server Information: {guild.name}",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    
    # Server stats
    total_members = guild.member_count
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    
    embed.add_field(name="👥 Members", value=f"Total: {total_members}\nOnline: {online_members}", inline=True)
    embed.add_field(name="📅 Created", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
    
    embed.add_field(name="📝 Channels", value=f"Text: {len(guild.text_channels)}\nVoice: {len(guild.voice_channels)}", inline=True)
    embed.add_field(name="🎭 Roles", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="😀 Emojis", value=str(len(guild.emojis)), inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.set_footer(text=f"Server ID: {guild.id}")
    await ctx.send(embed=embed)

@bot.command(name='user')
async def user_info(ctx, member: discord.Member = None):
    """Display user information"""
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(
        title=f"👤 User Information: {member.name}",
        color=member.color,
        timestamp=datetime.datetime.utcnow()
    )
    
    # User info
    roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
    roles_str = " ".join(roles) if roles else "No roles"
    
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 Joined", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📅 Created", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    
    embed.add_field(name="🎭 Roles", value=roles_str, inline=False)
    embed.add_field(name="📊 Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="🎮 Activity", value=member.activity.name if member.activity else "None", inline=True)
    
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Delete messages (default: 5 messages)"""
    if amount > 100:
        await ctx.send("❌ Maximum 100 messages can be deleted at once!")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to delete command
    
    embed = discord.Embed(
        title="🗑️ Messages Deleted",
        description=f"Successfully deleted **{len(deleted) - 1}** messages!",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name='help')
async def help_command(ctx):
    """Display list of commands"""
    embed = discord.Embed(
        title=f"📚 {BOT_NAME} Commands",
        description="Here are the available commands:",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    
    commands_info = [
        ("🏓 ping", "Test bot latency"),
        ("ℹ️ info", "Bot information"),
        ("🏠 server", "Server information"),
        ("👤 user [@user]", "User information"),
        ("🗑️ clear [amount]", "Delete messages (requires permission)"),
        ("📚 help", "Show this command list")
    ]
    
    for cmd, desc in commands_info:
        embed.add_field(name=f"{BOT_PREFIX}{cmd}", value=desc, inline=False)
    
    embed.add_field(name="💡 Tips", value=f"Use `{BOT_PREFIX}help [command]` for detailed command info", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    
    await ctx.send(embed=embed)

@bot.command(name='say')
async def say(ctx, *, message):
    """Bot will send the message you write"""
    await ctx.message.delete()  # Delete command
    await ctx.send(message)

@bot.command(name='embed')
async def create_embed(ctx, title, *, description):
    """Create embed with title and description"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.random(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=f"Created by {ctx.author.name}")
    await ctx.send(embed=embed)

# Event for welcome message
@bot.event
async def on_member_join(member):
    """Event when new member joins"""
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="🎉 Welcome!",
            description=f"Welcome **{member.mention}** to **{member.guild.name}**!",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")
        await channel.send(embed=embed)

# Event for member leave
@bot.event
async def on_member_remove(member):
    """Event when member leaves"""
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Member Left",
            description=f"**{member.name}** has left the server.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text=f"Members remaining: {member.guild.member_count}")
        await channel.send(embed=embed)

def main():
    """Main function to run the bot"""
    print(f"🚀 Starting {BOT_NAME}...")
    print(f"📝 Prefix: {BOT_PREFIX}")
    print(f"🔧 Version: {BOT_VERSION}")
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Discord token is invalid!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 