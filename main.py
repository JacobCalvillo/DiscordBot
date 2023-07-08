import os
import openai
import discord
from discord.ext import commands
import asyncio
import dotenv
from alive import alive

dotenv.load_dotenv()

openai.api_key = os.environ.get('API_KEY')

conv_status = []

def ask_me(pregunta):
    global conv_status
    conv_status.append(pregunta)
    pregunta_completa = ''.join(conv_status)
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = pregunta,
        max_tokens= 2048,
        temperature= 0.6,
        )

    respuesta = response.choices[0].text
    return respuesta


def create_img(request):
    response = openai.Image.create(
        prompt= request,
        n=1,
        size="256x256"   
        )

    return response['data'][0]['url']

#def create_translation(translate):
    #trad = openai.


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.command()
async def help_me(ctx):
    await ctx.send("-hello\nDevuelve hello {tu_nombre}\n-ask\nPreguntas a ChatGPT, escribe exit para dejar de preguntar.\n-create_image\nCrea una imagen en base a lo que pides")

@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}')
        
@client.command()
async def ask(ctx):
    await ctx.send('Cual es tu pregunta? ')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    while True:
        try:
            pregunta = await client.wait_for('message', check=check, timeout=60)
            if pregunta.content.lower() == 'exit':
                await ctx.send('Sesion concluida')
                global conv_status 
                conv_status = []
                break
            else:
                respuesta = ask_me(pregunta.content)
                await ctx.send(respuesta)
        except asyncio.TimeoutError:
            await ctx.send("Tiempo de espera agotado.")
            break

@client.command()
async def create_image(ctx):
    await ctx.send("¿Qué imagen quieres crear?")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        peticion = await client.wait_for('message', check=check, timeout=60)
        image_url = create_img(peticion.content)
        print("esta es la url generada: ",image_url)
        await ctx.send(image_url)
    except asyncio.TimeoutError:
        await ctx.send("Tiempo de espera agotado.")

clave = os.environ.get('TOKEN')

alive()
client.run(clave)

