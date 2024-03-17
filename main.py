import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import spotipy
from spotipy import SpotifyOAuth
from spotipy import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">sss", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.command()
async def manualsync(ctx):
    await ctx.channel.send("Synced!!!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


class Menu(discord.ui.View, discord.Interaction):
    def __init__(self):
        super().__init__(timeout=None)
        self.bot = bot
        self.view = None
        self.song_title = None
        self.user = None
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.blurple)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        playlist_editor_id = 1218657049475551252

        if playlist_editor_id in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Accepted successfully!!!", ephemeral=True)
            sp = spotipy.Spotify(auth_manager=self.bot.spotipy_auth_manager)
            search_query = self.song_title
            search_results = sp.search(q=search_query)
            if search_results:
                accepted_channel = discord.utils.get(interaction.guild.channels, id=1218875051407839272)
                track_url = search_results['tracks']['items'][0]['external_urls']['spotify']
                sp.playlist_add_items("2HIUDd0GayOT2ktD85H0zz", [track_url])
                embed = discord.Embed(
                    title=f"{self.song_title}",
                    description=f"{self.user.mention} your song has been accepted!",
                    color=discord.Color.green()
                )
                await accepted_channel.send(embed=embed)
        else:
            await interaction.response.send_message("nuh uh:)", ephemeral=True)
        return


    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        declined_channel = discord.utils.get(interaction.guild.channels, id=1218875358431023104)
        playlist_editor_id = 1218657049475551252

        if playlist_editor_id in [role.id for role in interaction.user.roles]:
            embed = discord.Embed(
                title=f"{self.song_title}",
                description=f"{self.user.mention} Your song has been declined:(",
                color=discord.Color.red()
            )
            await declined_channel.send(embed=embed)
        else:
            await interaction.response.send_message("Nuh uh:)", ephemeral=True)



@bot.tree.command(name="suggest", description="Suggest a song to the playlist!")
@app_commands.describe(song_title="Song title!!!")
async def suggest(interaction: discord.Interaction, song_title: str):
    channel_id = 1218648302908608632
    channel = discord.utils.get(interaction.guild.channels, id=channel_id)
    embed = discord.Embed(
        title=f"{song_title}",
        description=f"User: {interaction.user} suggested {song_title}",
        color=discord.Color.blue()
    )
    await interaction.response.send_message("Has been sent in {}!".format(channel.mention), ephemeral=True)
    menu = Menu()
    menu.song_title = song_title
    menu.user = interaction.user
    await channel.send(embed=embed, view=menu)

bot.spotipy_auth_manager = SpotifyOAuth(client_id="",
                                        client_secret="",
                                        redirect_uri="",
                                        scope='playlist-modify-private playlist-modify-public')

token = "TOKEN HERE"
bot.run(token)
