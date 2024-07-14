import discord
from discord.ext import commands

TOKEN = 'test'

intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Gok Bot Z: Extreme Butōden"))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content} in channel {message.channel.name} (ID: {message.channel.id})")
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    
    # Check if the message contains 'gok' in any form (case insensitive)
    if 'gok' in message.content.lower():
        if message.author.id == 763920617937829909 or message.author.id == 536190960003055627:
            print(f"Received 'gok' from {message.author}")
            await message.reply("fuck you")
        else:
            await message.reply("hey its me gok")
        return  # Stop further processing if handled
    
    await bot.process_commands(message)

@bot.command(name='list_roles')
async def list_roles(ctx):
    """List all roles and their corresponding emojis."""
    emoji_to_role = {
        '🟣': 1261738877928865792,
        '🔵': 1261739463214629027,
        '🟢': 1261739507057688617,
        '🔴': 1261743272498565162,
        '🐷': 1261743086036582571,
    }
    roles_list = [f"{emoji}: {ctx.guild.get_role(role_id).name}" for emoji, role_id in emoji_to_role.items()]
    await ctx.send("\n".join(roles_list))

@bot.command(name='add')
async def add_points(ctx, member: discord.Member, points: int):
    leaderboard = {}  # Assuming you want to reset leaderboard each time bot restarts
    if member.id not in leaderboard:
        leaderboard[member.id] = 0
    leaderboard[member.id] += points
    await ctx.send(f'Added {points} points to {member.display_name}. Total points: {leaderboard[member.id]}')

@bot.command(name='leaderboard')
async def show_leaderboard(ctx):
    leaderboard = {}  # Assuming you want to reset leaderboard each time bot restarts
    if not leaderboard:
        await ctx.send("The leaderboard is empty.")
        return

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    message = "Leaderboard:\n"
    for i, (user_id, points) in enumerate(sorted_leaderboard, start=1):
        user = await bot.fetch_user(user_id)
        message += f"{i}. {user.display_name} - {points} points\n"
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You do not have the necessary permissions to use this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

bot.run(TOKEN)
