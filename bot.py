import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 BUSINESS PANEL: MANAGE CUSTOMERS HERE
# ============================================================================

# 1. Add Paid Server IDs here
AUTHORIZED_SERVERS = [
    1378864322687537262,  # <--- REPLACE WITH YOUR SERVER ID
]

# 2. Teach the bot for each server here
SERVER_KNOWLEDGE = {
    123456789012345678: "You are the support bot for The Silk Road. We sell AI bots. Support hours: 24/7 Support. Website: thesilkroad.mysellauth.com",
    
    # Add customers like this:
    # 987654321098765432: "You are the bot for [Store Name]. We sell [Products].",
}

# ============================================================================
# 🔑 SECURITY & BOT SETUP
# ============================================================================
GROQ_API_KEY = os.getenv('GROQ_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True # Required to read the !ask command
bot = commands.Bot(command_prefix="!", intents=intents)
client = Groq(api_key=GROQ_API_KEY)

@bot.event
async def on_ready():
    print(f'✅ AI Support Bot Online as {bot.user}')
    print('Prefix set to !')

# ============================================================================
# 🎫 CLASSIC COMMAND: !ask <question>
# ============================================================================
@bot.command()
async def ask(ctx, *, question: str):
    
    # Check if server is authorized
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        embed_error = discord.Embed(
            title="🔒 Premium Required",
            description="Contact **The Silk Road** to enable AI Support for this server.",
            color=0xff5350 
        )
        await ctx.send(embed=embed_error)
        return

    async with ctx.typing():
        try:
            # Get this server's specific training
            instructions = SERVER_KNOWLEDGE.get(ctx.guild.id, "You are a helpful assistant.")

            # Call Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": question}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.5,
            )
            answer = chat_completion.choices[0].message.content.strip()

            # Professional Support Embed
            embed = discord.Embed(
                title="🤖 AI SUPPORT RESPONSE",
                description=answer,
                color=0x81c784
            )
            embed.set_footer(text=f"AI Support for {ctx.guild.name} • Powered by EXTEKK")
            
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ **Error:** {str(e)}")

bot.run(DISCORD_BOT_TOKEN)
