import discord
from discord.ext import commands
import os
import threading
import random
import string
from flask import Flask, request, jsonify

# --- 1. BANCO DE KEYS ---
keys_db = {"ICE-FREE": None}

# --- 2. API FLASK ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ICE METHODS ONLINE ❄️", 200

@app.route('/check')
def check():
    k = request.args.get('key')
    u = request.args.get('hwid')
    if k in keys_db:
        if keys_db[k] is None:
            keys_db[k] = str(u)
            return jsonify({"success": True, "msg": "Vinculado"})
        return jsonify({"success": str(keys_db[k]) == str(u)})
    return jsonify({"success": False})

# --- 3. CONFIGURAÇÃO DO BOT ---
# O segredo está aqui: ele busca a variável 'DISCORD_TOKEN' do sistema
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ CONECTADO COMO: {bot.user}")

@bot.command()
async def gerar(ctx):
    key = "ICE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    keys_db[key] = None
    await ctx.send(f"❄️ **Key Gerada:** `{key}`")

# --- 4. INICIALIZAÇÃO ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    # Roda a API
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False), daemon=True).start()
    
    # Roda o Bot usando o Token do Secret
    if TOKEN:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Erro ao iniciar: {e}")
    else:
        print("❌ ERRO: O Token não foi encontrado nas variáveis de ambiente!")
