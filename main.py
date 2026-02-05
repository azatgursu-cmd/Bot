import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = []
current_speaker = None
time_per_turn = 60  # secondes

# --- /parole ---
@bot.slash_command(name="parole", description="Demander la parole")
async def parole(ctx):
    global queue
    user_id = ctx.author.id
    if user_id in queue:
        await ctx.respond("Tu es déjà dans la file.", ephemeral=True)
        return
    queue.append(user_id)
    await ctx.respond("🎤 Tu es inscrit pour parler !", ephemeral=True)

# --- /quitter ---
@bot.slash_command(name="quitter", description="Quitter la file")
async def quitter(ctx):
    global queue
    user_id = ctx.author.id
    if user_id in queue:
        queue.remove(user_id)
        await ctx.respond("Tu as quitté la file.", ephemeral=True)
    else:
        await ctx.respond("Tu n'étais pas dans la file.", ephemeral=True)

# --- /file (optionnel, juste pour tester) ---
@bot.slash_command(name="file", description="Voir la file d'attente")
async def file(ctx):
    if queue:
        await ctx.respond(f"File actuelle : {', '.join(str(uid) for uid in queue)}", ephemeral=True)
    else:
        await ctx.respond("La file est vide.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot connecté : {bot.user}')

TOKEN = os.environ["TOKEN"]  # Va chercher ton token dans Railway
bot.run(TOKEN)
