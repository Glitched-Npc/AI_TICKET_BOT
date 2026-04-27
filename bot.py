import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 BUSINESS PANEL (SYNCED WITH YOUR ID)
# ============================================================================
AUTHORIZED_SERVERS = [
    1378864322687537262, # Your Server ID
]

SERVER_KNOWLEDGE = {
    1378864322687537262: "You are the support bot for The Silk Road. You help users with questions about the community and services. You can answer any question a member asks. Be kind and friendly and keep your answers short.",
}

# ============================================================================
# 🔑 SECURITY & BOT SETUP
# ============================================================================
GROQ_API_KEY = os.getenv('GROQ_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 

# case_insensitive=True means !ASK and !ask both work
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
client = Groq(api_key=GROQ_API_KEY)

@bot.event
async def on_ready():
    print(f'✅ Bot is ONLINE as {bot.user}')
    # This checks if the commands are actually loaded
    print(f'🤖 Commands loaded: {[cmd.name for cmd in bot.commands]}')

# ============================================================================
# 🏓 COMMAND: !ping
# ============================================================================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 **Pong!** I am alive and my commands are working!")

# ============================================================================
# 🎫 COMMAND: !ask
# ============================================================================
@bot.command()
async def ask(ctx, *, question: str):
    # Check Paywall
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        await ctx.send("🔒 **Premium Required.** Contact The Silk Road.")
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
            
            embed = discord.Embed(
                title="🤖 AI SUPPORT RESPONSE", 
                description=answer, 
                color=0x81c784
            )
            embed.set_footer(text=f"AI Support for {ctx.guild.name} • Powered by The Silk Road")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ **Error:** {str(e)}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
