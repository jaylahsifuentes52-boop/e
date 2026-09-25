import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

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

threading.Thread(target=start_http_server, daemon=True).start()

class VerifyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        await self.tree.sync()

bot = VerifyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="verify", description="Verify an OTP code.")
@app_commands.describe(otp="Enter the OTP code")
async def verify(interaction: discord.Interaction, otp: str):
    correct_otp = "123456"
    if otp == correct_otp:
        await interaction.response.send_message("✅ OTP verified successfully!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Incorrect or expired OTP.", ephemeral=True)

bot.run(TOKEN)
