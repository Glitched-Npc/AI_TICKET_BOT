import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 BUSINESS PANEL
# ============================================================================
AUTHORIZED_SERVERS = [
    1378864322687537262, 
]

SERVER_KNOWLEDGE = {
    1378864322687537262: "You are the support bot for The Silk Road.",
}

# ============================================================================
# 🔑 SECURITY & BOT SETUP
# ============================================================================
GROQ_API_KEY = os.getenv('GROQ_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True

# We add case_insensitive=True so !ASK and !ask both work
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
client = Groq(api_key=GROQ_API_KEY)

@bot.event
async def on_ready():
    print(f'✅ Bot is ONLINE as {bot.user}')
    # BRAIN CHECK: This prints the commands the bot knows
    print(f'🤖 Loaded Commands: {[cmd.name for cmd in bot.commands]}')

# ============================================================================
# 🏓 COMMAND: !ping
# ============================================================================
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("🏓 **Pong!** I can hear you and my commands are working!")

# ============================================================================
# 🎫 COMMAND: !ask
# ============================================================================
@bot.command(name="ask")
async def ask(ctx, *, question: str = None):
    # Check if they actually asked a question
    if question is None:
        await ctx.send("❓ Please provide a question. Example: `!ask What is this server?`")
        return

    # Check Paywall
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        await ctx.send("🔒 **Premium Required.** Contact EXTEKK.")
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

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
