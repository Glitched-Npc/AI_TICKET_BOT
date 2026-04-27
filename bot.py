import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 BUSINESS PANEL
# ============================================================================
AUTHORIZED_SERVERS = [
    1378864322687537262, # <--- DOUBLE CHECK THIS ID IS CORRECT
]

SERVER_KNOWLEDGE = {
    123456789012345678: "You are a support bot for The Silk Road.",
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
    print(f'✅ I am in {len(bot.guilds)} servers')

# This will print EVERY message the bot sees to the Railway logs
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"📩 I saw a message: '{message.content}' in server {message.guild.id}")
    await bot.process_commands(message)

# ============================================================================
# 🏓 DEBUG COMMAND: !ping
# ============================================================================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! I am alive and can see your messages!")

# ============================================================================
# 🎫 AI COMMAND: !ask
# ============================================================================
@bot.command()
async def ask(ctx, *, question: str):
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        await ctx.send("🔒 Premium Required. This server ID is not authorized.")
        return

    async with ctx.typing():
        try:
            instructions = SERVER_KNOWLEDGE.get(ctx.guild.id, "You are a helpful assistant.")
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": question}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.5,
            )
            answer = chat_completion.choices[0].message.content.strip()
            
            embed = discord.Embed(title="🤖 AI RESPONSE", description=answer, color=0x81c784)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

bot.run(DISCORD_BOT_TOKEN)
