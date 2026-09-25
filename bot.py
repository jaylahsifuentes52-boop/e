import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1538740748709658694

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")


# -------------------------
# Render HTTP server
# -------------------------

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Discord bot is online.")

    def log_message(self, format, *args):
        return


def start_http_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()


threading.Thread(
    target=start_http_server,
    daemon=True
).start()


# -------------------------
# Discord bot
# -------------------------

intents = discord.Intents.default()


class VerifyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        print(f"Slash commands synced to server: {GUILD_ID}")


bot = VerifyBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")


# -------------------------
# /verify otp
# -------------------------

@bot.tree.command(
    name="verify",
    description="Verify an OTP code."
)
@app_commands.describe(
    otp="Enter the OTP code"
)
async def verify(
    interaction: discord.Interaction,
    otp: str
):

    correct_otp = "5EEA22B601764B7DFC6B8B0D9F0E7A64A0417D03C29E0"

    if otp == correct_otp:
        await interaction.response.send_message(
            "✅ OTP verified successfully!",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ Incorrect or expired OTP.",
            ephemeral=True
        )


# -------------------------
# Start bot
# -------------------------

bot.run(TOKEN)
