import interactions
import os
import random
import subprocess
import glob
from dotenv import load_dotenv

#Globals
load_dotenv()
bot_token = str(os.getenv("TOKEN"))
bot       = interactions.Client(bot_token)
SCOPE     = int(str(os.getenv("SCOPE")))

#Functions
@bot.event()
async def on_ready():
    print("The Kernel is ready!", flush=True)

@bot.command(
    name="greeting",
    description="Receive a greeting from The Kernel",
    scope=SCOPE
)
async def greeting(context:interactions.CommandContext):
    greetings = [{"msg":"Hello","end":"!"},
                 {"msg":"What's good,","end":"?"}, 
                 {"msg":"Hey","end":"!"}, 
                 {"msg":"Yooo","end":"!"},
                 {"msg":"What's popping,","end":"?"},
                 {"msg":"What's up,","end":"?"},
                 {"msg":"How you living,","end":"?"}]
    greeting  = random.choice(greetings)
    await context.send(f"{greeting['msg']} {context.user.mention}{greeting['end']}")


@bot.command(
    name="delete-all-messages",
    description="Delete ALL messages 😈",
    scope=SCOPE,
)
async def delete_all_messages(context:interactions.CommandContext):
    await context.send("Deleting messages 😉")
    channel_id = int(context.channel_id)
    messages = await context.client.get_channel_messages(channel_id=channel_id,limit=100)
    try:
        message_ids = [message["id"] for message in messages]
        await context.client.delete_messages(channel_id=channel_id, message_ids=message_ids)
    except Exception as e:
        print(e)
        await context.send(f"There was an error deleting messages 😬\nSorry about that, {context.user.mention}!")

@bot.command(
    name="update-proxies",
    description="Update Proxy list on main server computer",
    scope=SCOPE
)
async def update_proxies(context:interactions.CommandContext):
    await context.send("Updating proxies...")
    try:
        discord_home_dir = os.path.abspath(".") #used to get back here in the future
        scripts = glob.glob("../*/*.py")
        cmd = ""
        for script in scripts:
            if "get_IPs.py" in script:
                cmd = f"python3 {script}"
                cmd_dir = script.split("/")
                cmd_dir.pop(-1)
                cmd_dir = "/".join(cmd_dir)
                break
        if not cmd or not cmd_dir:
            raise Exception
        os.chdir(cmd_dir)
        subprocess.call(cmd,shell=True)
    except Exception as e:
        await context.send(f"Error updating proxies: {str(e)}")
    finally:
        os.chdir(discord_home_dir)
        await context.send("Done handling 'update-proxies' command")

@bot.command(
    name="shutdown",
    description="Put me to sleep 😢",
    scope=SCOPE,
)
async def shutdown(context:interactions.CommandContext):
    await context.send("Farewell 😭\nI'm going offline...")
    print("I should be asleep")
    exit(0)

    
if __name__ == "__main__":
    bot.start()
