import discord
from discord.ext import commands
import threading
import os
import random
import string
from flask import Flask

# --- API MÍNIMA ---
app = Flask(__name__)
keys_db = {"ICE-FREE": None}

@app.route('/')
def home(): 
    return "ONLINE"

@app.route('/health') # Alguns sites usam isso para saber se o app vive
def health(): 
    return "OK", 200

# --- BOT DISCORD ---
TOKEN = "MTQ5MDUzMTQyNDQ5Mzc2NDY5OQ.GEDthf.yF94S4x3-cKY2LGvM5lBjret_TLOGNhrHvg-Uo" # COLOQUE O TOKEN NOVO AQUI!

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def gerar(ctx):
    key = "ICE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    keys_db[key] = None
    await ctx.send(f"❄️ Key: `{key}`")

# --- INICIALIZAÇÃO CRÍTICA ---
def run_flask():
    # O Render/Koyeb passa a porta pela variável 'PORT'
    port = int(os.environ.get("PORT", 10000))
    print(f"Iniciando Flask na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    # 1. Sobe a Web primeiro (importante para o Render não dar erro)
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. Sobe o Bot
    print("Iniciando Bot do Discord...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Erro no Bot: {e}")
