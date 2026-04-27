import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 BUSINESS PANEL (AUTHORIZED SERVERS)
# ============================================================================
# Your Server ID is synced here
AUTHORIZED_SERVERS = [
    1378864322687537262, 
]

# I updated the ID below to match your server so it knows what to say!
SERVER_KNOWLEDGE = {
    1378864322687537262: "You are the official support bot for The Silk Road. You help users with questions about the community and services.",
}

# ============================================================================
# 🔑 SECURITY & BOT SETUP
# ============================================================================
GROQ_API_KEY = os.getenv('GROQ_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
client = Groq(api_key=GROQ_API_KEY)

@bot.event
async def on_ready():
    print(f'✅ Bot is ONLINE as {bot.user}')
    print(f'✅ Currently connected to {len(bot.guilds)} server(s)')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # LOGGING: This will show up in Railway Logs for EVERY message
    print(f"📩 RECEIVED: '{message.content}' | FROM: {message.author} | SERVER: {message.guild.id}")

    # MENTION TEST: If you @mention the bot, it will reply even if commands are broken
    if bot.user.mentioned_in(message):
        await message.channel.send(f"👋 Hello {message.author.mention}! I can hear you. My prefix is **!**\nType `!ping` to test my response.")

    # This line is REQUIRED for commands to work when on_message is used
    await bot.process_commands(message)

# ============================================================================
# 🏓 DEBUG COMMAND: !ping
# ============================================================================
@bot.command()
async def ping(ctx):
    print("DEBUG: Ping command triggered")
    await ctx.send("🏓 **Pong!** I am alive and processing commands!")

# ============================================================================
# 🎫 AI COMMAND: !ask
# ============================================================================
@bot.command()
async def ask(ctx, *, question: str):
    # Check Paywall
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        print(f"🚫 BLOCKED: Server {ctx.guild.id} is not authorized.")
        await ctx.send("🔒 **Premium Required.** This server ID is not authorized. Contact EXTEKK.")
        return

    async with ctx.typing():
        try:
            # Get instructions
            instructions = SERVER_KNOWLEDGE.get(ctx.guild.id, "You are a helpful assistant.")
            
            # Call AI
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": question}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.5,
            )
            answer = chat_completion.choices[0].message.content.strip()
            
            # Create Embed
            embed = discord.Embed(
                title="🤖 AI SUPPORT RESPONSE", 
                description=answer, 
                color=0x81c784
            )
            embed.set_footer(text=f"AI Support for {ctx.guild.name}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"❌ ERROR in !ask: {str(e)}")
            await ctx.send(f"❌ **Error:** {str(e)}")

bot.run(DISCORD_BOT_TOKEN)
