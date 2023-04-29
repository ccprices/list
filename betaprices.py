import discord
import asyncio
import datetime
import random
import json
from discord import Intents
from discord.ext import pages, commands
from discord.ext.commands import cooldown, BucketType
import math
import re
import requests
import pytz
import os
import sys
from github import Github
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import time
import secrets

#intents = discord.Intents.default()
#intents.typing = True
#intents.presences = True
#intents.members = True

client = discord.Bot(intents=Intents.all())

x = datetime.datetime.now()
blocked_error = False

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the prices"))
    print("We have logged in as {0.user}".format(client))

@client.event
async def ban(message):
    global blocked_error

    with open ("id_server.txt","r") as file:
        ban = file.read().split("\n")

    list_server = []

    for bans in ban:
        list_server.append(int(bans))

    if not message.guild.id in list_server:
        return ban

    else:
        blocked_error = True
        await message.respond("Bot has been blocked from accessing this server. :lock:", ephemeral=True)

@client.event
async def is_owner(message):
    full = []
    file = open("id_perm.txt","r")
    perm = file.read().split("\n")
    for perms in perm:
        full.append(int(perms))
        if message.author.id in full:
            return perm
    else:
        await message.respond("You don't have permission to use this command :lock:", ephemeral=True)

@client.event
async def on_message(message):
    with open ("prices.json") as file:
        data = json.load(file)

    for item in data:
        wearables = item['type']['name']

        if "/PRICE" in message.content.upper() and wearables in message.content.upper():
            word = random.choice(["It's","It is","The price is",f"The price of the {item['item']['name']} is"])
            between_c = random.choice(["-","to"])
            bot_reply = f"{word} {int(item['item']['price']['min']):,}c {between_c} {int(item['item']['price']['max']):,}c"
            await message.reply(bot_reply, mention_author=False)
            return
    
    if message.guild.id == 977543116162752573:
        if 'chng.it/' in message.content or 'DOCS.GOOGLE.COM/PRESENTATION/D/1ETWCNJJQIJ7ZEPCLH3C8SAPD3MUX4CDDZW2ZOGPVY9E' in message.content.upper():
            await message.delete()
            f = open("logs.txt", "a+", encoding="utf8")
            f.write("["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y ")+x.strftime("%X")+"]["+f"{message.author.mention} {message.author.name}: {message.content}\n")

#SHOW ERROR
#@client.event
async def on_application_command_error(message, error):
    global blocked_error
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        await message.respond(f'*You have a cooldown of **'+str(remaining_time)+'** minutes.*', ephemeral=True)

    if not blocked_error:
        command = open("logs.txt","a+").write(f'[{x.strftime("%d/")}{x.strftime("%m/")}{x.strftime("%Y ")}{x.strftime("%X")}][{message.author.mention}] used /{message.command.qualified_name} {message.selected_options}\n'+f'[ERROR] Command /{message.command.qualified_name}\n{error}\n')
        error_text = "**Error!**\n*It will be fixed soon, they have a notification when you found a bug.*"
        await message.respond(error_text, ephemeral=True)
        await client.get_channel(999376824456986706).send("<@283224945843109888> Error reported, check logs!")

@client.slash_command()
async def shutdown(message):
    await message.respond("Closing...")
    await client.close()

@commands.check(ban)
@client.slash_command(description="tester..", guild_ids=[977543116162752573])
async def price(message, name: discord.Option(str, require = True), level: discord.Option(int, choices = [0,49], required = False), amount: discord.Option(int, min_value=1, max_value=100000, required = False)):
    data = []
    with open ("prices.json") as file:
        data_wear = json.load(file)
        data.append(data_wear)
    with open ("pets.json") as file:
        data_pet = json.load(file)
        data.append(data_pet)
    with open ("resources.json") as file:
        data_rss = json.load(file)

    global blocked_error

    #recipes
    recipes = requests.get("https://ccrecipes.com/recipes.json").json()

    found = False
    blocked_error = False
    full = []

    emojis_cubit = "<:cubit:999230219250573322>"
    
    #for item in data_pet:
    #    color = {"Stable":0xbdbdbd,"Increasing":0x1fc44b,"Decreasing":0xc41a1a}
    #    state = {"Stable":"⚪","Increasing":"🟢","Decreasing":"🔴"}
    #    if name.upper() == item['type']['name'] and level == int(item['type']['level']):
    #        found = True
    #        embed=discord.Embed(title="**"+item["item"]["section"]+"**", color=color[item['item']['state']])
    #        embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
    #        embed.add_field(name=":notepad_spiral:"+item["item"]["name"]+" Price:", value=f"{int(item['item']['price']['min']):,}{emojis_cubit} - {int(item['item']['price']['max']):,}<:cubit:999230219250573322>", inline=True)
    #        embed.add_field(name=":bar_chart: State:", value=f"{state[item['item']['state']]} {item['item']['state']}", inline=False)
    #        embed.set_footer(text=f"(Last Updated: {item['item']['last_updated']})")
    #        await message.respond(embed=embed)
#
    #    if item['type']['name'] == name.upper() and not level in [0,49]:
    #        await message.respond("You need to use another option for the level. Here, for example...", file=discord.File('option.png'))
    #        found = True
    #        return

    for item in data_wear:
        color = {"Stable":0xe0ffff,"Increasing":0x1fc44b,"Decreasing":0xc41a1a}
        state = {"Stable":"🔵","Increasing":"🟢","Decreasing":"🔴"}
        name2 = item['type']['name']

        if name.upper() == name2 or name.upper() == name2.replace("'S","").replace(".","").replace("& ","") or name.upper() == name2.replace("'",""):
            found = True
            show_img = f'{item["item"]["url"]}.png'.split("/")[1]
            #list_image = ["broken_display","broken2_display","broken3_display","broken4_display","broken5_display","broken6_display","broken7_display",]

            url = 'https://ccprices.github.io/images/'+item["item"]["url"]+'.png'
            #random_image = (random.choices(population=[BytesIO(requests.get(url).content),"dirt.png"],weights=[0.90, 0.10],k=1)[0])
            #img = Image.open(random.choice(list_image)+".png")
            img = Image.open("display4.png")
            img2 = Image.open(BytesIO(requests.get(url).content))
            x_img, y_img = img2.size
            #img2 = img2.rotate(random.randint(0, 360), expand = 1)

            x, y = img.size
            hat_x, hat_y = img2.size
            new_image = Image.new('RGBA', (x,y))
            new_image.paste(img,(0,0))
            new_image.paste(img2,(int(x/2)-int(hat_x/2),int(y/2)-int(hat_y/2)), img2)
            new_image.save(show_img)

            embed=discord.Embed(title=item["item"]["section"], color=color[item['item']['state']])
            file = discord.File(show_img, filename=show_img)
            embed.set_image(url="attachment://"+show_img)
            #embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
            embed.add_field(name=item["item"]["name"]+" Price:", value=f"{int(item['item']['price']['min']):,}{emojis_cubit} - {int(item['item']['price']['max']):,}{emojis_cubit}", inline=True)
            embed.add_field(name="State:", value=f"{state[item['item']['state']]} {item['item']['state']}", inline=True)
            embed.set_footer(text=f"(Last Updated: {item['item']['last_updated']})")
            await message.respond(embed=embed, file=file)

            os.remove(show_img)

            if name and amount:
                await message.respond("The amount option only works for raw materials.")
                return

    for item in data_rss:
        color = {"Stable":0xe0ffff,"Increasing":0x1fc44b,"Decreasing":0xc41a1a}
        state = {"Stable":"🔵","Increasing":"🟢","Decreasing":"🔴"}
        if name.upper() == item["type"]["name"]:

            if item['type']['name'] == name.upper() and level in [0,49]:
                await message.respond("You used option level but maybe you meant amount.")
                found = True
                return

            if item["item"]["operator"] == "*" and not amount:
                n1, n2 = item["item"]["price"]["min"], item["item"]["price"]["max"]
                prices = f"1**/**{n1}{emojis_cubit} - 1**/**{n2}{emojis_cubit}"
                text_footer = "There is one more option for the amount if you need"
            if item["item"]["operator"] == "/" and not amount:
                n1, n2 = item["item"]["price"]["min"], item["item"]["price"]["max"]
                prices = f"{n1}**/**c - {n2}**/**c"
                text_footer = "There is one more option for the amount if you need"

            show_img = f'{item["item"]["url"]}.png'.split("/")[1]
            url = 'https://ccprices.github.io/images/'+item["item"]["url"]+'.png'

            img = Image.open("display4.png")
            img2 = Image.open(BytesIO(requests.get(url).content))

            x_img, y_img = img.size
            bold_arial = ImageFont.truetype("arialbd.ttf", 18)

            x, y = img.size
            hat_x, hat_y = img2.size
            new_image = Image.new('RGBA', (x,y))
            amount_text = f"x{amount}"
            if not amount:
                amount_text = ""
            draw = ImageDraw.Draw(new_image)
            new_image.paste(img,(0,0))
            new_image.paste(img2,(int(x/2)-int(hat_x/2),int(y/2)-int(hat_y/2)), img2)
            draw.text(((x_img)/2, (y_img)/2+35), amount_text, font=bold_arial, stroke_width=2, anchor="mm", stroke_fill='black')
            new_image.save(show_img)

            if item["item"]["operator"] == "*" and amount:
                n1, n2 = item["item"]["price"]["min"], item["item"]["price"]["max"]
                price_min, price_max = amount*n1, amount*n2
                prices = f"{int(price_min):,}{emojis_cubit} - {int(price_max):,}{emojis_cubit}"
                text_footer = ""

            if item["item"]["operator"] == "/" and amount:
                n1, n2 = item["item"]["price"]["min"], item["item"]["price"]["max"]
                price_min, price_max = amount/n1, amount/n2
                prices = f"{int(math.ceil(price_max)):,}{emojis_cubit} - {int(math.ceil(price_min)):,}{emojis_cubit}"
                text_footer = ""

            embed=discord.Embed(title=item["item"]["section"], color=color[item['item']['state']])
            file = discord.File(show_img, filename=show_img)
            embed.set_image(url="attachment://"+show_img)
            embed.add_field(name=item["item"]["name"]+" Price:", value=prices, inline=True)
            embed.add_field(name="State:", value=f"{state[item['item']['state']]} {item['item']['state']}", inline=True)
            embed.set_footer(text=text_footer)
            await message.respond(embed=embed, file=file)

            os.remove(show_img)
            return

    for craft in recipes:
        if name.upper() == craft["item"]["item"].upper():
            found = True
            await message.respond("*Resources or crafting items have no prices*", delete_after=30)

    word = False
    another_found = False

    if not found:
        alldata = []
        for list_error in data:
            for item in list_error:
                if name.upper() in item['type']['name'] or name.upper() in item['type']['name'].replace("'S", "").replace(".", "").replace("& ",""):
                    another_found = True
                    result = item['item']['name']

                    if item["type"]["section"] == "PETS" and item["type"]["level"] == 0:
                        result = item['type']['name'].title()
                    if item["type"]["section"] == "PETS" and item["type"]["level"] == 49:
                        result = ""

                    alldata.append(result+"\n")
                    alldata.sort()

                    while ("\n" in alldata):
                        alldata.remove("\n")

        if not another_found:
            for list_error in data:
                for item in list_error:
                    search = name.upper()
                    out_list = ''.join(search).split()
                    if out_list[0] in item['type']['name']:
                        word = True
                        result = item['item']['name']

                        if item["type"]["section"] == "PETS" and item["type"]["level"] == 0 and not item["type"]["level"] == 49:
                            result = item['type']['name'].title()
                        if item["type"]["section"] == "PETS" and item["type"]["level"] == 49: 
                            result = ""

                        alldata.append(result+"\n")
                        alldata.sort()

                        while ("\n" in alldata):
                            alldata.remove("\n")

            if not word:
                await message.respond("*Item not found*", delete_after=30)
                return

        if len(alldata) == 1:
            remove_list = ''.join(alldata).replace("\n","")
            await message.respond(f"Exact or full name could not be found,\nmaybe you mean ``{remove_list}``")
            return

        book = []
        page_num = int(math.ceil(len(alldata)/5))
        for page in range(page_num):
            prices = ''
            page_section = alldata[5*page:5+(5*page)]
            for i in range(len(page_section)):
                prices+=page_section[i]
            embed = discord.Embed(title="Failed", description="Couldn't find exact or full name, here are some possible suggestions"+"```\n"+prices+"```", color=0xde1219)
            book.append(embed)
        final_book = pages.Paginator(pages=book, show_disabled=True)
        await final_book.respond(message.interaction)

@client.slash_command()
async def edit(message, name: discord.Option(str, require = True), min: discord.Option(int, require = True), max: discord.Option(int, require = True), level: discord.Option(int, choices = [0,49], required = False)):
    with open("prices.json") as file:
        data = json.load(file)
    with open("pets.json") as file:
        data_pets = json.load(file)

    found = False

    for item in data:
        if name.upper() == item['type']['name']:
            found = True
            min_price = item['item']['price']['min']
            max_price = item['item']['price']['max']
            embed = discord.Embed(title=f"{item['item']['name']} has changed price:",description=f"{int(min_price):,}c - {int(max_price):,}c <:update:1050026511614353548> {int(min):,}c - {int(max):,}c", color=0x4c4fcf)
            embed.set_footer(text=f"({item['item']['state']})")
            item['item']['price']['min'] = min
            item['item']['price']['max'] = max
            item['item']['last_updated'] = (x.strftime("%d/")+x.strftime("%b/")+x.strftime("%Y"))
            embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
            f = open("logs_prices.txt", "a+", encoding="utf8")
            #contents = repo.get_contents("logs.txt")
            f.write("["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"]["+f"{message.author.mention} {message.author.name}] "+ item['item']['name'] + ": "+str(min_price)+"-"+str(max_price)+" -> "+str(item['item']['price']['min'])+"-"+str(item['item']['price']['max'])+"\n")
            #repo.update_file(contents.path, "["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"]", "["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"]["+f"{message.author.mention} {message.author.name}] "+ item['item']['name'] + ": "+str(min_price)+"-"+str(max_price)+" -> "+str(item['item']['price']['min'])+"-"+str(item['item']['price']['max'])+"\n",contents.sha)
            await message.respond(embed=embed)

    with open("prices.json","w") as file:
        json.dump(data,file,indent=4)

    for item in data_pets:
        if name.upper() == item['type']['name'] and level == int(item['type']['level']):
            found = True
            min_price = item['item']['price']['min']
            max_price = item['item']['price']['max']
            embed = discord.Embed(title=f"**{item['item']['name']} has changed price:**",description=f"{int(min_price):,}c - {int(max_price):,}c :arrow_right: {int(min):,}c - {int(max):,}c", color=0x4c4fcf)
            item['item']['price']['min'] = min
            item['item']['price']['max'] = max
            item['item']['last_updated'] = (x.strftime("%d/")+x.strftime("%b/")+x.strftime("%Y"))
            embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
            f = open("logs_prices.txt", "a+", encoding="utf8")
            f.write("["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"]["+f"{message.author.mention} {message.author.name}] "+item['item']['name']+": "+str(min_price)+"-"+str(max_price)+" -> "+str(item['item']['price']['min'])+"-"+str(item['item']['price']['max'])+"\n")
            await message.respond(embed=embed)

    with open("pets.json","w") as file:
        json.dump(data_pets,file,indent=4)

    if not found:
        await message.respond("*Item not found*", delete_after=30)

@commands.check(is_owner)
@client.slash_command()
async def edit_state(message, name: discord.Option(str, require = True), state: discord.Option(str, choices = ["Stable","Increasing","Decreasing"],require = True), level: discord.Option(int, choices = [0,49], required = False)):
    with open("prices.json") as file:
        data = json.load(file)
    with open("pets.json") as file:
        data_pets = json.load(file)

    found = False

    for item in data:
        if name.upper() == item['type']['name']:
            found = True
            old_state = item['item']['state']
            embed = discord.Embed(title=f"**{item['item']['name']} has changed state:**",description=f"{old_state} :arrow_right: {state}", color=0x4c4fcf)
            embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
            item['item']['state'] = state
            f = open("logs_prices.txt", "a+", encoding="utf8")
            f.write("["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"] "+f"{message.author.mention} {message.author.name}]"+" changed the state of "+item['item']['name']+": "+str(old_state)+" -> "+str(item["item"]["state"])+"\n")
            await message.respond(embed=embed)

    for item in data_pets:
        if name.upper() == item['type']['name'] and level == int(item['type']['level']):
            found = True
            old_state = item['item']['state']
            embed = discord.Embed(title=f"**{item['item']['name']} has changed state:**",description=f"{old_state} :arrow_right: {state}", color=0x4c4fcf)
            embed.set_thumbnail(url='https://ccprices.github.io/images/'+item["item"]["url"]+'.png')
            item['item']['state'] = state
            f = open("logs_prices.txt", "a+", encoding="utf8")
            f.write("["+x.strftime("%d/")+x.strftime("%m/")+x.strftime("%Y")+"] "+f"{message.author.mention} {message.author.name}] "+name+": "+str(old_state)+" -> "+str(item["item"]["state"])+"\n")
            await message.respond(embed=embed)
            
    if not found:
        await message.respond("*Item not found*", delete_after=30)
        
    with open("prices.json","w") as file:
        json.dump(data,file,indent=4)
    with open("pets.json","w") as file:
        json.dump(data_pets,file,indent=4)

@client.slash_command(description="You can search for minimalny 3 letters")
async def search2(message, name: discord.Option(str, require = True)):
    data = []
    with open("prices.json") as file:
        data.append(json.load(file))
    with open("pets.json") as file:
        data.append(json.load(file))
    with open("resources.json") as file:
        data.append(json.load(file))
    
    found = False
    alldata = []
    alldata2 = []

    for searchlist in data:
        searchlist = sorted(searchlist, key= lambda k: k['type']['name'])
        for item in searchlist:
            search2 = item['type']['name']
            search = name.upper()
            out_list = ''.join(search)
            search_word = out_list.split()
            if name.upper() in item['type']['name'] or item['type']['name'] in name.upper() or name.upper() in item['type']['section'] or item['type']['section'] in name.upper():
                found = True
                section = (item['type']['name'].title()+"\n")
                alldata.append(section)

            #search2 = item['type']['name']
            #search = name.upper()
            #out_list = ''.join(search)
            #elif search_word[0] in item['type']['name']:
            #    found = True
            #    section = (item['type']['name'].title()+"\n")
            #    alldata.append(section)

    another_found = False
    if not found:
        for searchlist in data:
            searchlist = sorted(searchlist, key= lambda k: k['type']['name'])
            for item in searchlist:
                search = name.upper()
                out_list = ''.join(search)
                search_word = out_list.split()
                if search_word[0] in item['type']['name']:
                    another_found = True
                    section = (item['type']['name'].title()+"\n")
                    alldata.append(section)

    if not another_found:
        await message.respond("*Nothing was found for your search*", delete_after=30)
        return

    book = []
    page_num = int(math.ceil(len(alldata)/10))
    for page in range(page_num):
        prices = ''
        page_section = alldata[10*page:10+(10*page)]
        for i in range(len(page_section)):
            prices+=page_section[i]
        embed = discord.Embed(title=":mag_right: Searching: ``"+name+"``", description="Use the ``/price <name>`` command for an item in the search results to check it is price"+"```"+prices+"```", color=0xff7d23)
        book.append(embed)
    final_book = pages.Paginator(pages=book)
    await final_book.respond(message.interaction)

@client.slash_command()
async def section2(message, name: discord.Option(str, require = True)):
    data = []
    with open("prices.json") as file:
        data.append(json.load(file))
    with open("pets.json") as file:
        data.append(json.load(file))
    with open("resources.json") as file:
        data.append(json.load(file))

    found = False

    alldata = []
    alldata2 = []

    color = 0x4c4fcf

    if message.guild.id == 977543116162752573:
        color = 0x9b59b6

    for pricelist in data:
        pricelist = sorted(pricelist, key= lambda k: k['item']['name'])
        for item in pricelist:
            state = {"Stable":"⚪","Increasing":"🟢","Decreasing":"🔴"}
            if item['type']['section'] in name.upper() and not item['type']['section'] == "MATERIALS":
                #if len(name) >= 3:
                found = True
                min_price = item['item']['price']['min']
                max_price = item['item']['price']['max']
                info_footer = "⚪Stable  🟢Increasing  🔴Decreasing"
                text = ""
                section = '{:33} {:1s} - {:5}\n'.format(state[item['item']['state']]+" "+item['item']['name'], f"{int(min_price):,}c", f"{int(max_price):,}c")
                named_section = item['type']['section'].title().replace("'S","'s")
                alldata.append(section)

            if name.upper() == "STATES":
                if item['item']['state'] == "Decreasing" or item['item']['state'] == "Increasing":
                    found = True
                    named_section = "Increasing / Decreasing"
                    section = state[item['item']['state']]+" "+item['item']['name']+"\n"
                    text = "Other wearables are stable."
                    info_footer = "🟢Increasing  🔴Decreasing"
                    alldata.append(section)

            if name.upper() == "NEW":
                if item['type']['section'] == "NEW_WEARABLES":
                    found = True
                    named_section = "New"
                    section = item['item']['name']+"\n"
                    text = ""
                    info_footer = ""
                    alldata.append(section)

            if name.upper() == "MATERIALS":
                if item['type']['section'] == "MATERIALS":
                    found = True
                    named_section = "Raw Materials"
                    section = item['item']['name']+"\n"
                    text = ""
                    info_footer = "Only the /price command displays the price"
                    alldata.append(section)

    if not found:
        section2 = ["Hat Pack","Wing Pack","Critter Suit Pack","Accessories Pack","Clothes Pack","Clothes Item",
                     "Quest","Virus","Dungeon Pack","Track Pack","Kitchen Pack","Ocean Pack","Scifi Pack","Steampunk Pack",
                     "Adventure Pack","Fishing Pack","Chess Pack","April Pack","Easter Pack","Valentine Pack","Summer Pack",
                     "Fan Pack","Halloween Pack","Thanksgiving Pack","Yuletide Pack","Slymecorp Pack","Farm Pack","Wands","Cars","Pets","New Year"]
        section2.sort()
        for items in section2:
            alldata2.append(items+"\n")

        book2 = []
        page_num2 = int(math.ceil(len(alldata2)/5))
        for page2 in range(page_num2):
            prices2 = ''
            page_section2 = alldata2[5*page2:5+(5*page2)]
            for i in range(len(page_section2)):
                prices2+=page_section2[i]
            embed2 = discord.Embed(title="Failed", description="Couldn't find ``"+name+"``. Here are some possible suggestions."+"```\n"+prices2+"```", color=0xde1219)
            book2.append(embed2)
        final_book2 = pages.Paginator(pages=book2)
        await final_book2.respond(message.interaction)
        return

    book = []
    page_num = int(math.ceil(len(alldata)/20))
    for page in range(page_num):
        prices = ''
        page_section = alldata[20*page:20+(20*page)]
        for i in range(len(page_section)):
            prices+=page_section[i]
        embed = discord.Embed(title=named_section, description=text+"```"+prices+"```", color=color)#, url="https://www.ccrecipes.com/prices/cctest/")
        embed.set_footer(text=info_footer)
        book.append(embed)
    final_book = pages.Paginator(pages=book)
    await final_book.respond(message.interaction)

@client.slash_command(description="")
async def craft(message, item: discord.Option(str, require = True)):
    url = requests.get("https://ccrecipes.com/recipes.json").json()
    image = requests.get("https://ccrecipes.com/images.json").json()
    found = False
    
    for items in url:
        if item.upper() == items["item"]["item"].upper():
            found = True
            images = image[items["item"]["item"]].replace("i_","")
            if "_cropped" in images:
                img = "ItemIcons_Blocks__Tile/"+images
            elif "IMG_" in images:
                img = "ItemIcons_Wear__Tile/"+images
            else:
                img = "ItemIcons_Misc__Tile/"+images
            embed = discord.Embed(title="Cubic Castles - Crafting Recipes", url=f"https://ccrecipes.com/recipe?recipe={items['item']['item'].replace(' ','%20')}" ,description="Easy to use Crafting Recipe webpage for Cubic Castles blocks and items!", color=0x4c4fcf)
            embed.set_thumbnail(url="https://ccprices.github.io/images/"+img+".png")
            await message.respond(f"https://ccrecipes.com/recipe?recipe={items['item']['item'].replace(' ','%20')}", embed=embed, delete_after=60)

    word = False

    if not found:
        alldata = []
        for items in url:
            name2 = items['item']['item']
            if item.upper() in name2.upper():
                word = True
                section = (items['item']['item']+"\n")
                fail = "Couldn't find the exact name. Here are some possible suggestions."
                alldata.append(section)

        if not word:
            await message.respond("*Item not found*", delete_after=10)
            return

        book = []
        page_num = int(math.ceil(len(alldata)/5))
        for page in range(page_num):
            prices = ''
            page_section = alldata[5*page:5+(5*page)]
            for i in range(len(page_section)):
                prices+=page_section[i]
            embed = discord.Embed(title="Failed", description=fail+"```\n"+prices+"```", color=0xde1219)
            embed.set_thumbnail(url='https://play-lh.googleusercontent.com/MPzTIluID2R_90rGPWQk8UuyjHnKtozRV0x2nSQBXelbf5y2zGo49QW3GqGugy32OZmu')
            book.append(embed)
        final_book = pages.Paginator(pages=book)
        result = await final_book.respond(message.interaction)
        await result.delete(delay=300)

@client.slash_command(description="Servers")
async def status(message):
    url = 'https://cubiccastles.com/status.php'
    file = requests.get(url).text
    print(file)

    updown = re.findall('(?<= )(.*?)(?= )', file)
    #status = re.findall('(?<=110)(.*?)(?=:)', file)
    status = re.findall('(?<=110)(.*?)(?= )', file)

    allserver = ""
    allserver2 = ""

    for i in range(12):
        color = {"UP!":"🟢","DOWN!":"🔴"}
        server = (f'{color[updown[i]]}Server {status[i]}\n')
        allserver+=server

    for i in range(12,24):
        color = {"UP!":"🟢","DOWN!":"🔴"}
        down = {""}
        server = (f'{color[updown[i]]}Server {status[i]}\n')
        allserver2+=server
    
    embed = discord.Embed(title="Cubic Castles Status", description="", color=0x4c4fcf)
    country_time_zone = pytz.timezone('America/New_York')
    country_time = datetime.datetime.now(country_time_zone)
    cctime = country_time.strftime("%A %d/%b/%Y - %X")
    embed.add_field(name="Time", value="```"+cctime+"```", inline=False)
    embed.add_field(name="Servers", value="```"+allserver+"```", inline=True)
    embed.add_field(name="**te**", value="```"+allserver2+"```", inline=True)
    embed.set_footer(text="🟢Up Server  🔴Down Server")
    await message.respond(embed=embed)

@client.slash_command(guild_ids=[977543116162752573])
async def restart(message):
    file = open("logs.txt", "a").write(f'[{x.strftime("%d/")}{x.strftime("%m/")}{x.strftime("%Y ")}{x.strftime("%X")}] Restarted\n')

    await message.respond("Restarting bot2...")
    os.execv(sys.executable, ['python'] + sys.argv)

@client.slash_command(guild_ids=[977543116162752573])
async def server(message, name: discord.Option(str, required = False)):
    alldata = []
    number = 0

    for guild in client.guilds:
        user_count = len([x for x in guild.members if not x.bot])
        number+=1
        servers = f"{number}. {guild.name} ({guild.member_count})\n" #[{guild.id}]
        alldata.append(servers)

        if name == guild.name:
            await message.respond(f"**Owner:** {guild.owner} *(ID: {guild.owner.id})*\n**ID Server:** {guild.id}\n**Members:** {user_count}")

    book = []
    page_num = int(math.ceil(len(alldata)/10))
    for page in range(page_num):
        prices = ''
        page_section = alldata[10*page:10+(10*page)]
        for i in range(len(page_section)):
            prices+=page_section[i]
        embed = discord.Embed(title="Servers", description="```\n"+prices+"```", color=0x4c4fcf)
        book.append(embed)
    final_book = pages.Paginator(pages=book)
    await final_book.respond(message.interaction)

@client.slash_command()
async def send_dm(message, member: discord.Member):
    channel = await member.create_dm()
    spolu = ""
    test = ["||<:nothing:1063406921710829618>||"]*36
    test[random.randint(0,35)] = "||<:cubit:999230219250573322>||"
    test[5] += "\n"
    test[11] += "\n"
    test[17] += "\n"
    test[23] += "\n"
    test[29] += "\n"
    test[35] += "\n"

    for testt in test:
        spolu += testt

    await channel.send("Find cubit!\n"+spolu)
    await message.respond("You sent", ephemeral=True)

@client.slash_command()
async def send_game(message):
    spolu = ""
    test = ["||<:nothing:1063406921710829618>||"]*36
    test[random.randint(0,35)] = "||<:cubit:999230219250573322>||"
    test[5] += "\n"
    test[11] += "\n"
    test[17] += "\n"
    test[23] += "\n"
    test[29] += "\n"
    test[35] += "\n"

    for testt in test:
        spolu += testt

    channel = client.get_channel(977543116619911230)
    await channel.send("Find cubit!\n"+spolu)
    await message.respond("You sent", ephemeral=True)

#@client.slash_command(description="Some prices may change, correcting the prices of in-game items")
@commands.cooldown(1, 300, commands.BucketType.user)
async def suggest(message, text: discord.Option(str, require = True, max_length=500), image: discord.Option(discord.Attachment, required = False)):
    f = open("suggestion.txt","a+").write(f'[{x.strftime("%d/")}{x.strftime("%m/")}{x.strftime("%Y ")}{x.strftime("%X")}][{message.author.mention}] {message.author.name}: {text}\n[LINK] {image}\n')
    await message.respond("Thank you for sending us!", ephemeral=True)

#@client.slash_command()
async def play(message):
    spolu = ""
    test = ["||<:nothing:1063406921710829618>||"]*36
    test[random.randint(0,35)] = "||<:cubit:999230219250573322>||"
    test[5] += "\n"
    test[11] += "\n"
    test[17] += "\n"
    test[23] += "\n"
    test[29] += "\n"
    test[35] += "\n"

    for testt in test:
        spolu += testt
        embed = discord.Embed(title="Find Cubit!", description=spolu, color=0x4c4fcf)

    await message.respond(embed=embed)
    await message.respond(spolu)

#@client.slash_command()
async def time(message):
    country_time_zone = pytz.timezone('America/New_York')
    country_time = datetime.datetime.now(country_time_zone)
    cctime = country_time.strftime("%X")
    guild = client.get_guild(977543116162752573)
    channel = await guild.create_voice_channel(cctime)
    sets = discord.utils.get(client.get_all_channels(), name=cctime)
    update_time = client.get_channel(sets.id)
    await channel.edit(name=channel)
    print(sets.id)

@client.slash_command(guild_ids=[977543116162752573])
async def pack(message):
    with open("prices.json") as file:
        data = json.load(file)

    user = []
    with open("database.json") as person:
        user = json.load(person)

    wearables = []
    list_users = []

    old_user = False

    file = open("id_user.txt","r")
    id_members = file.read().split("\n")[:-1]
    for users in id_members:
        list_users.append(int(users))

    test = (random.choices(population=[(50, 249),(250, 999),(1000, 4999),(5000, 19999),(20000, 99999),(100000, 249999),(250000, 499999),(500000, 999999),(1000000, 5000000)],weights=[50,20,15,5,0.90,0.50,0.035,0.01,0.0005],k=1)[0])
    for item in data:
        price_min = item["item"]["price"]["min"]
        price_max = item["item"]["price"]["max"]

        if price_min > test[0] and price_max < test[1] and message.author.id in list_users:
            old_user = True
            name = item["item"]["name"]
            #create_list = {'user': {'id': message.author.id, 'pack': 2, 'timeout': '18:00:00'}}
            wearables.append(name)
            wearabless = random.choice(wearables)

        if not message.author.id in list_users:
            wearables = ""
            await message.respond(f"You cant.......")
            return

    await message.respond(f"{wearabless} {test}")

    file = open("id_user.txt", "w")
    for member in user:
        file.write(str(member["user"]["id"])+"\n")

    #user.append(create_list)
    #with open("database.json","w") as file:
    #    json.dump(user, file, indent=4)

client.run("MTAxMjY3NTY2NjU1MjAzMzMxMA.GhS75f.55u_ZPDWs15tCbzRRLQA9XsMX7YfOA5CW0fae4")