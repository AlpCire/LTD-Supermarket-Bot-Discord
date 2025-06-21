import discord
from discord.ext import commands
from discord import app_commands
import os
from db import init_db, alta_local, dar_membresia, agregar_compra, obtener_compras

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

ROLES_PERMITIDOS_IDS = {
    1386101305197592746,  # Gerente General
    # Puedes agregar más IDs aquí si lo deseas
}

def tiene_roles_permitidos(member: discord.Member, permitidos_ids: set):
    return any(role.id in permitidos_ids for role in member.roles)

async def get_member(interaction: discord.Interaction):
    if isinstance(interaction.user, discord.Member):
        return interaction.user
    if interaction.guild:
        member = interaction.guild.get_member(interaction.user.id)
        if member:
            return member
        try:
            return await interaction.guild.fetch_member(interaction.user.id)
        except discord.NotFound:
            return None
    return None

@bot.event
async def on_ready():
    init_db()
    await tree.sync()
    print(f"Bot conectado como {bot.user}")

@tree.command(name="alta", description="Dar de alta un local")
@app_commands.describe(nombre="Nombre del local")
async def alta(interaction: discord.Interaction, nombre: str):
    member = await get_member(interaction)
    if member is None or not tiene_roles_permitidos(member, ROLES_PERMITIDOS_IDS):
        await interaction.response.send_message("⛔ No tienes permiso para usar este comando.", ephemeral=True)
        return
    alta_local(nombre)
    await interaction.response.send_message(f"✅ Local '{nombre}' dado de alta.")

@tree.command(name="membresia", description="Dar membresía a un local")
@app_commands.describe(nombre="Nombre del local")
async def membresia(interaction: discord.Interaction, nombre: str):
    member = await get_member(interaction)
    if member is None or not tiene_roles_permitidos(member, ROLES_PERMITIDOS_IDS):
        await interaction.response.send_message("⛔ No tienes permiso para usar este comando.", ephemeral=True)
        return
    dar_membresia(nombre)
    await interaction.response.send_message(f"🏅 Membresía otorgada al local '{nombre}'.")

@tree.command(name="compra", description="Agregar compra si monto > $10,000")
@app_commands.describe(nombre="Nombre del local", monto="Monto total de la compra en USD")
async def compra(interaction: discord.Interaction, nombre: str, monto: float):
    member = await get_member(interaction)
    if member is None or not tiene_roles_permitidos(member, ROLES_PERMITIDOS_IDS):
        await interaction.response.send_message("⛔ No tienes permiso para usar este comando.", ephemeral=True)
        return
    if monto < 10000:
        await interaction.response.send_message(
            f"❌ La compra debe ser superior a $10,000 USD. Monto ingresado: ${monto}", ephemeral=True)
        return
    compras, membresia = agregar_compra(nombre)
    mensaje = f"🛒 Compra registrada para '{nombre}'. Total compras: {compras}"
    if membresia and compras % 10 == 0:
        mensaje += f" 🎉 ¡El local '{nombre}' ha alcanzado {compras} compras y gana un premio!"
    await interaction.response.send_message(mensaje)

@tree.command(name="premio", description="Ver cuántas compras tiene un local")
@app_commands.describe(nombre="Nombre del local")
async def premio(interaction: discord.Interaction, nombre: str):
    member = await get_member(interaction)
    if member is None or len(member.roles) <= 1:
        await interaction.response.send_message("⛔ No tienes permiso para usar este comando.", ephemeral=True)
        return
    total = obtener_compras(nombre)
    await interaction.response.send_message(f"📊 El local '{nombre}' tiene {total} compras registradas.")

bot.run(TOKEN)
