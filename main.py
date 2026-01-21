import discord
import os
import asyncio
import sys

# --- CONFIGURATION ---
TOKEN = os.getenv('DISCORD_TOKEN')
P1_CHANNEL_ID = os.getenv('P1_CHANNEL_ID')
P2_CHANNEL_ID = os.getenv('P2_CHANNEL_ID')

# Validation check for Senior IT peace of mind
if not TOKEN or not P1_CHANNEL_ID or not P2_CHANNEL_ID:
    print("CRITICAL ERROR: Missing environment variables. Check your Portainer Stack.")
    sys.exit(1)

# --- INTENTS SETUP ---
intents = discord.Intents.default()
intents.voice_states = True 
intents.guilds = True       
intents.members = True      

client = discord.Client(intents=intents)

# --- HELPER: CHANNEL UPDATE LOGIC ---
async def check_occupancy(channel, p_num):
    if not channel:
        return
    
    # Check if anyone is in the VC
    is_active = len(channel.members) > 0
    
    # Aesthetic Strings: Using Wide Separator (᲼) and Small Caps
    # ACTIVE: 🟢᲼╎᲼ᴘʟᴀʏᴇʀ᲼𝟷᲼ᴀᴄᴛɪᴠᴇ
    # PENDING: 🟡᲼╎᲼ᴘʟᴀʏᴇʀ᲼𝟷᲼ᴘᴇɴᴅɪɴɢ
    if is_active:
        new_name = f"🟢᲼╎᲼ᴘʟᴀʏᴇʀ᲼{p_num}᲼ᴀᴄᴛɪᴠᴇ"
    else:
        new_name = f"🟡᲼╎᲼ᴘʟᴀʏᴇʀ᲼{p_num}᲼ᴘᴇɴᴅɪɴɢ"
    
    # Only update if the name actually changed to stay under rate limits
    if channel.name != new_name:
        try:
            await channel.edit(name=new_name)
            print(f"STATUS CHANGE: Player {p_num} is now {'ACTIVE' if is_active else 'PENDING'}")
        except discord.errors.Forbidden:
            print(f"PERMISSION ERROR: Bot cannot rename channel {channel.id}. Check Role Hierarchy.")
        except Exception as e:
            print(f"API ERROR: {e}")

# --- EVENTS ---
@client.event
async def on_ready():
    print(f'--- ARCADE CABINET ONLINE ---')
    print(f'Logged in as: {client.user}')
    
    # Sync both channels immediately upon startup
    await check_occupancy(client.get_channel(int(P1_CHANNEL_ID)), "𝟷")
    await check_occupancy(client.get_channel(int(P2_CHANNEL_ID)), "𝟸")

@client.event
async def on_voice_state_update(member, before, after):
    target_ids = [int(P1_CHANNEL_ID), int(P2_CHANNEL_ID)]
    channels_to_check = []
    
    # Detect leaving a channel
    if before.channel and before.channel.id in target_ids:
        num = "𝟷" if before.channel.id == int(P1_CHANNEL_ID) else "𝟸"
        channels_to_check.append((before.channel, num))
        
    # Detect joining a channel
    if after.channel and after.channel.id in target_ids:
        num = "𝟷" if after.channel.id == int(P1_CHANNEL_ID) else "𝟸"
        channels_to_check.append((after.channel, num))

    if channels_to_check:
        # 1-second buffer for Discord's API to catch up with member counts
        await asyncio.sleep(1) 
        for channel, num in channels_to_check:
            await check_occupancy(channel, num)

# --- EXECUTION ---
try:
    client.run(TOKEN)
except Exception as e:
    print(f"FATAL: Bot failed to start: {e}")
