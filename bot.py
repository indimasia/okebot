import discord
from discord.ext import commands
import asyncio
import datetime
from supabase import create_client, Client
from config import DISCORD_TOKEN, BOT_PREFIX, BOT_NAME, BOT_VERSION, SUPABASE_URL, SUPABASE_KEY

# Setup Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@bot.event
async def on_member_join(member):
    """Welcome new members"""
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Welcome {member.mention} to {member.guild.name}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    """Goodbye message when members leave"""
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Goodbye!",
            description=f"**{member.name}** has left the server.",
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

async def ensure_server_registered(guild: discord.Guild):
    """Ensure server is registered in database"""
    try:
        # Check if server exists
        response = supabase.table('servers').select('*').eq('server_id', str(guild.id)).execute()
        
        if not response.data:
            # Insert new server
            server_data = {
                'server_id': str(guild.id),
                'name': guild.name,
                'icon_url': str(guild.icon.url) if guild.icon else None,
                'member_count': guild.member_count,
                'created_at': guild.created_at.isoformat(),
                'owner_id': str(guild.owner_id)
            }
            response = supabase.table('servers').insert(server_data).execute()
        
        return response.data[0]['id'] if response.data else None
    except Exception as e:
        print(f"Error ensuring server registration: {e}")
        return None

@bot.command(name='register')
@commands.has_permissions(administrator=True)
async def register(ctx, member: discord.Member = None, *, username: str = None):
    """Register user in the database"""
    if member is None:
        member = ctx.author
    
    if username is None:
        username = member.name

    try:
        # Ensure server is registered first
        server_id = await ensure_server_registered(ctx.guild)
        if not server_id:
            raise Exception("Failed to register server")

        # Check if user already exists
        response = supabase.table('users').select('*')\
            .eq('discord_id', str(member.id))\
            .execute()
        
        if response.data:
            user_id = response.data[0]['id']
            # Check if user is already registered in this server
            user_server_response = supabase.table('user_servers')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('server_id', server_id)\
                .execute()
            
            if user_server_response.data:
                embed = discord.Embed(
                    title="❌ Registration Failed",
                    description=f"{member.mention} is already registered in this server!",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
            else:
                # Add user to this server
                user_server_data = {
                    'user_id': user_id,
                    'server_id': server_id,
                    'joined_at': member.joined_at.isoformat() if member.joined_at else datetime.datetime.utcnow().isoformat(),
                    'registered_by': str(ctx.author.id)
                }
                supabase.table('user_servers').insert(user_server_data).execute()
                
                embed = discord.Embed(
                    title="✅ Server Registration Successful",
                    description=f"{member.mention} has been registered in **{ctx.guild.name}**.",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
        else:
            # Insert new user
            user_data = {
                'discord_id': str(member.id),
                'username': username,
                'registered_at': datetime.datetime.utcnow().isoformat(),
                'avatar_url': str(member.avatar.url) if member.avatar else str(member.default_avatar.url)
            }
            
            user_response = supabase.table('users').insert(user_data).execute()
            user_id = user_response.data[0]['id']
            
            # Register user in this server
            user_server_data = {
                'user_id': user_id,
                'server_id': server_id,
                'joined_at': member.joined_at.isoformat() if member.joined_at else datetime.datetime.utcnow().isoformat(),
                'registered_by': str(ctx.author.id)
            }
            supabase.table('user_servers').insert(user_server_data).execute()
            
            embed = discord.Embed(
                title="✅ Registration Successful",
                description=f"{member.mention} has been registered as **{username}** in **{ctx.guild.name}**.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
        
        # Add registration details
        embed.add_field(name="Registered By", value=ctx.author.mention, inline=True)
        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Registration Time", value=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Registration Error",
            description=f"An error occurred during registration: {str(e)}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='unregister')
@commands.has_permissions(administrator=True)
async def unregister(ctx, member: discord.Member = None):
    """Unregister a user from the current server"""
    # Default to command author if no member specified
    if member is None:
        member = ctx.author
    
    try:
        # Ensure server is registered first
        server_id = await ensure_server_registered(ctx.guild)
        if not server_id:
            raise Exception("Failed to register server")

        # Check if user exists
        user_response = supabase.table('users').select('*')\
            .eq('discord_id', str(member.id))\
            .execute()
        
        if not user_response.data:
            embed = discord.Embed(
                title="❌ Unregistration Failed",
                description=f"{member.mention} is not registered in the system!",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
        else:
            user_id = user_response.data[0]['id']
            
            # Check if user is registered in this server
            user_server_response = supabase.table('user_servers')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('server_id', server_id)\
                .execute()
            
            if not user_server_response.data:
                embed = discord.Embed(
                    title="❌ Unregistration Failed",
                    description=f"{member.mention} is not registered in this server!",
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
            else:
                # Remove user from this server
                supabase.table('user_servers')\
                    .delete()\
                    .eq('user_id', user_id)\
                    .eq('server_id', server_id)\
                    .execute()
                
                embed = discord.Embed(
                    title="✅ Unregistration Successful",
                    description=f"{member.mention} has been unregistered from **{ctx.guild.name}**.",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
                
                # Add unregistration details
                embed.add_field(name="User", value=member.mention, inline=True)
                embed.add_field(name="Server", value=ctx.guild.name, inline=True)
                embed.add_field(name="Unregistered by", value=ctx.author.mention, inline=True)
                embed.add_field(name="Unregistration Time", value=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Unregistration Error",
            description=f"An error occurred during unregistration: {str(e)}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='changeusername')
@commands.has_permissions(administrator=True)
async def change_username(ctx, member: discord.Member = None, *, new_username: str = None):
    """Change username for a registered user"""
    # Default to command author if no member specified
    if member is None:
        member = ctx.author
    
    if new_username is None:
        embed = discord.Embed(
            title="❌ Invalid Usage",
            description=f"Please provide a new username!\n\n**Usage:** `{BOT_PREFIX}changeusername [@user] <new_username>`",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
        return
    
    try:
        # Check if user exists
        user_response = supabase.table('users').select('*')\
            .eq('discord_id', str(member.id))\
            .execute()
        
        if not user_response.data:
            embed = discord.Embed(
                title="❌ Username Change Failed",
                description=f"{member.mention} is not registered in the system!",
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
        else:
            old_username = user_response.data[0]['username']
            
            # Update username
            supabase.table('users')\
                .update({'username': new_username})\
                .eq('discord_id', str(member.id))\
                .execute()
            
            embed = discord.Embed(
                title="✅ Username Changed Successfully",
                description=f"Username for {member.mention} has been updated!",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            
            # Add change details
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="Old Username", value=old_username, inline=True)
            embed.add_field(name="New Username", value=new_username, inline=True)
            embed.add_field(name="Changed by", value=ctx.author.mention, inline=True)
            embed.add_field(name="Change Time", value=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Username Change Error",
            description=f"An error occurred while changing username: {str(e)}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='userlist')
@commands.has_permissions(administrator=True)
async def user_list(ctx):
    """List all registered users on this server"""
    try:
        # Ensure server is registered first
        server_id = await ensure_server_registered(ctx.guild)
        if not server_id:
            raise Exception("Failed to register server")

        # Get all registered users for this server with their details
        response = supabase.table('user_servers')\
            .select('*, users(discord_id, username, registered_at, avatar_url)')\
            .eq('server_id', server_id)\
            .order('joined_at', desc=False)\
            .execute()
        
        if not response.data:
            embed = discord.Embed(
                title="📋 Registered Users",
                description=f"No users are registered in **{ctx.guild.name}** yet.",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                title="📋 Registered Users",
                description=f"List of registered users in **{ctx.guild.name}**",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            
            # Add server stats
            total_registered = len(response.data)
            total_members = ctx.guild.member_count
            registration_rate = round((total_registered / total_members) * 100, 1) if total_members > 0 else 0
            
            embed.add_field(
                name="📊 Statistics",
                value=f"**Registered:** {total_registered}\n**Total Members:** {total_members}\n**Registration Rate:** {registration_rate}%",
                inline=False
            )
            
            # Create user list with pagination if needed
            user_list = []
            for i, record in enumerate(response.data, 1):
                user_data = record['users']
                discord_id = user_data['discord_id']
                username = user_data['username']
                joined_at = record['joined_at']
                registered_by = record['registered_by']
                
                # Try to get Discord member object for mention
                try:
                    member = ctx.guild.get_member(int(discord_id))
                    user_mention = member.mention if member else f"<@{discord_id}>"
                except:
                    user_mention = f"<@{discord_id}>"
                
                # Format join date
                try:
                    join_date = datetime.datetime.fromisoformat(joined_at.replace('Z', '+00:00'))
                    formatted_date = join_date.strftime("%Y-%m-%d")
                except:
                    formatted_date = "Unknown"
                
                user_list.append(f"`{i:2d}.` {user_mention} **{username}** *(joined: {formatted_date})*")
            
            # Split into chunks if too many users (Discord embed limit)
            chunk_size = 20
            user_chunks = [user_list[i:i + chunk_size] for i in range(0, len(user_list), chunk_size)]
            
            for i, chunk in enumerate(user_chunks):
                field_name = "👥 Users" if i == 0 else f"👥 Users (continued {i+1})"
                embed.add_field(
                    name=field_name,
                    value="\n".join(chunk),
                    inline=False
                )
                
                # Discord has a limit of 25 fields per embed
                if i >= 24:
                    embed.add_field(
                        name="⚠️ Note",
                        value=f"Only showing first {(i+1) * chunk_size} users. Use database queries for complete list.",
                        inline=False
                    )
                    break
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while fetching user list: {str(e)}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
    
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Test bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: **{latency}ms**')

@bot.command(name='info')
async def info(ctx):
    """Bot information and statistics"""
    embed = discord.Embed(
        title=f"ℹ️ {BOT_NAME} Information",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Version", value=BOT_VERSION, inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Prefix", value=BOT_PREFIX, inline=True)
    embed.add_field(name="Library", value="discord.py", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='server')
async def server(ctx):
    """Server information"""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"🏠 {guild.name} Information",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    await ctx.send(embed=embed)

@bot.command(name='user')
async def user(ctx, member: discord.Member = None):
    """User information"""
    member = member or ctx.author
    embed = discord.Embed(
        title=f"👤 User Information",
        color=member.color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"User ID: {member.id}")
    await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Delete messages"""
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f'🗑️ Deleted {amount} messages.')
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name='say')
async def say(ctx, *, message: str):
    """Make the bot say something"""
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(name='embed')
async def embed(ctx, title: str, *, description: str):
    """Create a custom embed"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text=f"Created by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help(ctx):
    """Show help message"""
    embed = discord.Embed(
        title=f"📚 {BOT_NAME} Commands",
        description=f"Prefix: `{BOT_PREFIX}`",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    
    # Basic Commands
    basic_commands = [
        f"`{BOT_PREFIX}ping` - Test bot latency",
        f"`{BOT_PREFIX}info` - Bot information",
        f"`{BOT_PREFIX}server` - Server information",
        f"`{BOT_PREFIX}user [@user]` - User information",
        f"`{BOT_PREFIX}say [message]` - Make bot say something",
        f"`{BOT_PREFIX}embed [title] [description]` - Create embed"
    ]
    embed.add_field(name="📋 Basic Commands", value="\n".join(basic_commands), inline=False)
    
    # Admin Commands
    admin_commands = [
        f"`{BOT_PREFIX}register [@user] [username]` - Register user",
        f"`{BOT_PREFIX}unregister [@user]` - Unregister user",
        f"`{BOT_PREFIX}changeusername [@user] [new_username]` - Change username for a registered user",
        f"`{BOT_PREFIX}userlist` - List all registered users on this server",
        f"`{BOT_PREFIX}clear [amount]` - Delete messages",
        f"`{BOT_PREFIX}userlist` - List all registered users on this server"
    ]
    embed.add_field(name="⚡ Admin Commands", value="\n".join(admin_commands), inline=False)
    
    embed.set_footer(text=f"Type {BOT_PREFIX}help to see this message")
    await ctx.send(embed=embed)

async def main():
    """Main function to run the bot"""
    try:
        print("🚀 Starting bot...")
        print(f"📝 Bot Name: {BOT_NAME}")
        print(f"📌 Version: {BOT_VERSION}")
        print(f"⚡ Prefix: {BOT_PREFIX}")
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
