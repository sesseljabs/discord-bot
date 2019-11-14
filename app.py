import discord
import requests
import json
import random
import urllib.request as url

headers = {
    'User-Agent': 'Discord bot (by slashdash)',
}
color = 0x9b59b6

#print(sent)
#sent.append(2052826)

# with open("sent.txt","w") as f:
#     f.truncate()
#     f.write(str(sent))
# sent = []
# def write(towrite):
#     with open("sent.txt") as f:
#         sent = json.loads(f)
#     sent.append(towrite)
#     with open("sent.txt","w") as f:
#         f.truncate()
#         f.write(str(sent))

def getlist(tag):
    print(tag)
    if tag == "popular":
        with requests.get(f"https://e621.net/post/popular_by_day.json",headers=headers) as f:
            data = json.loads(f.text)
    else:
        with requests.get(f"https://e621.net/post/index.json?tags={tag}", headers=headers) as f:
            data = json.loads(f.text)
    # with open("sent.txt") as f:
    #     sent = json.loads(f)
    toremove = []
    for i in data:
        if i["file_ext"] in ["swf", "gif", "webm"]:
            toremove.append(i)
    data = [ e for e in data if e not in toremove ]

    if len(data) == 0:
        return False
    return data


# add to server: https://discordapp.com/oauth2/authorize?client_id=644147507378651138&scope=bot&permissions=0

token = "NjQ0MTQ3NTA3Mzc4NjUxMTM4.Xcv1aQ.XSKWOInbItij-fU8_Vix_yiAVdc"
message = 0

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as',self.user)

    async def on_message(self,message):

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "furhelp":
            embed = discord.Embed(title="Help on BOT",description="Some useful commands", colour=color)
            embed.add_field(name="furporn",value="Add a tag after to find some nice e621 porn. You can use multiple tags by seperating them with a comma withour spaces")

            await message.channel.send(content=None,embed=embed)

        if "hello there" in message.content.lower():
            print(message.content)
            await message.channel.send("General Kenobi")

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith("a"):
            await message.channel.send(message.content)
        if message.content == "uwu me":
            embed = discord.Embed(title="Help on BOT",description="Some useful commands")
            embed.add_field(name="furporn", value="Add a tag after to find some nice e621 porn. You can use multiple tags by seperating them with a comma withour spaces")
            await message.channel.send("""
            
- furp | uwu
""")

        if message.content.lower().startswith("furporn"):
            if message.channel.nsfw:
                if len(message.content.split()) < 2:
                    await message.channel.send("U need a tag, dummy")
                    return
                elif len(message.content.split()) > 2:
                    await message.channel.send("Bruh this is so much im overwhelmed")
                    return
                tag = message.content.split()[1].lower()
                listi = getlist(tag)
                if listi == False:
                    await message.channel.send("I can't find anything like this.")
                    await message.channel.send("Make it yourself you sick fuck")
                    return
                porn = random.choice(listi)
                if len(porn["artist"]) == 0:
                    porn["artist"][0] = porn["author"]
                embed = discord.Embed(title=f"By {porn['artist'][0]}", colour=color, description=f"e621 link [here](https://e621.net/post/show/{porn['id']})")
                embed.set_image(url=f"{porn['file_url']}")
                print(f"id: {porn['id']}")
                await message.channel.send(content=None,embed=embed)

                if tag == "popular":
                    pass

            else:
                await message.channel.send("You should be in a nsfw channel rn")


client = MyClient()

client.run(token)