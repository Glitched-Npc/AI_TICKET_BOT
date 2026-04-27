import discord
from discord.ext import commands
from groq import Groq
import os

# ============================================================================
# 🟢 CUSTOMER LIST & KNOWLEDGE BASE (TEACH THE BOT HERE)
# ============================================================================

# 1. Add Paid Server IDs here
AUTHORIZED_SERVERS = [
    123456789012345678,  # Your Server
    # 222222222222222222, # Customer Server 1
]

# 2. Teach the bot for each server here.
# Copy the Server ID, then paste their custom instructions.
SERVER_KNOWLEDGE = {
    123456789012345678: "You are the support bot for EXTEKK. We sell AI Discord bots. Our support hours are 9am-5pm. Our website is extekk.com.",
    
    # Example for a customer:
    # 222222222222222222: "You are the bot for 'Pizza Planet'. We offer Pepperoni and Cheese. Delivery takes 30 mins. Do not answer questions about burgers."
}

# ============================================================================
# 🔑 SECURITY & CONFIG
# ============================================================================
GROQ_API_KEY = os.getenv('GROQ_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# You can use "llama-3.3-70b-versatile" for a "smarter" support bot if you want
GROQ_MODEL = "llama-3.1-8b-instant" 

# ============================================================================
# 🤖 BOT SETUP
# ============================================================================
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)
client = Groq(api_key=GROQ_API_KEY)

@bot.event
async def on_ready():
    print(f'✅ AI Ticket Bot is online as {bot.user}')

# ============================================================================
# 🎫 SUPPORT COMMAND: !support <your question>
# ============================================================================
@bot.command()
async def support(ctx, *, question: str):
    
    # 1. Check Paywall
    if ctx.guild.id not in AUTHORIZED_SERVERS:
        embed = discord.Embed(title="🔒 Premium AI Required", description="Contact The Silk Road to enable AI Support for this server.", color=0xff5350)
        await ctx.send(embed=embed)
        return

    # 2. Get this server's specific instructions
    # If no instructions are found, it uses a default one
    instructions = SERVER_KNOWLEDGE.get(ctx.guild.id, "You are a helpful assistant.")

    async with ctx.typing():
        try:
            # 3. Call Groq with the "System Prompt" (The teaching part)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": question}
                ],
                model=GROQ_MODEL,
                temperature=0.5, # Slightly higher for more "natural" conversation
            )
            
            answer = chat_completion.choices[0].message.content.strip()
            
            # 4. Professional Support Embed
            embed = discord.Embed(
                title="🤖 AI SUPPORT RESPONSE",
                description=answer,
                color=0x81c784 # Green for support
            )
            embed.set_footer(text=f"AI Support for {ctx.guild.name} • Powered by EXTEKK")
            
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ **Support Error:** {str(e)}")

bot.run(DISCORD_BOT_TOKEN)
