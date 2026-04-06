import discord
from discord.ext import commands
import threading
import os
import random
import string
from flask import Flask

# --- CONFIGURAÇÃO ---
# DICA: No Railway, você pode colocar o Token em "Variables" no painel
# Mas se quiser testar rápido, cole o NOVO TOKEN aqui:
TOKEN = "MTQ5MDUzMTQyNDQ5Mzc2NDY5OQ.GEDthf.yF94S4x3-cKY2LGvM5lBjret_TLOGNhrHvg-Uo" 

app = Flask(__name__)
keys_db = {"ICE-FREE": None}

@app.route('/')
def home():
    return "SOUZA METHODS ONLINE ❄️", 200

@app.route('/check')
def check():
    k = request.args.get('key')
    u = request.args.get('hwid')
    if k in keys_db:
        if keys_db[k] is None:
            keys_db[k] = str(u)
            return {"success": True}, 200
        return {"success": str(keys_db[k]) == str(u)}, 200
    return {"success": False}, 404

# --- BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ BOT ESTÁ VIVO: {bot.user}")

@bot.command()
async def gerar(ctx):
    key = "ICE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    keys_db[key] = None
    await ctx.send(f"❄️ **Key:** `{key}`")

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    # O Railway passa a porta pela variável PORT
    port = int(os.environ.get("PORT", 8080))
    
    # Roda a API em segundo plano
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False), daemon=True).start()
    
    # Roda o Bot no processo principal
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
