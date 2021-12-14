import discord, datetime, random, requests, urllib.parse, urllib.request, json, os, asyncio
from discord.ui import View
from discord.ui import Button
from random import randint
from discord.ext.commands import has_permissions, MissingPermissions, Command
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from discord import Embed
from googleapiclient.discovery import build

devbot = commands.Bot(command_prefix = 'db ')
devbot.remove_command('help')
devbot_discord_client = discord.Client()
apiKey = 'AIzaSyDULhEddp2G0c-vPoWiq6TUycYIo119pg8'
status = cycle(['db about', 'db help'])
Shop = [{'name': 'Laptop', 'price': 1690,'description': 'Used for posting videos on youtube and coding.', 'emoji': ':computer:'},
        {'name': 'Phone', 'price': 969,'description': 'Used for calling people and sending feedback to the devs of devbot.', 'emoji': ':iphone:'},
        {'name': 'Mega Devcoins', 'price': 10000000,'description': 'A rare devcoin.', 'emoji': ':moneybag:'},
        {'name': 'Apple', 'price': 100,'description': '**apple**', 'emoji': ':apple:'}]

moderationCMDS = [{'name': '`db kick <user> <reason>`', 'description': 'Kicks a user from the server.'},
                  {'name': '`db ban <user> <reason>`', 'description': 'Bans a user from the server.'},
                  {'name': '`db unban <user>`', 'description': 'Unbans a user from the server.'},
                  {'name': '`db clear <amount>`', 'description': 'Clear/Purge messages for a specified amount.'},
                  {'name': '`db addrole <role> <user>`', 'description': 'Adds a specified role to a user.'},
                  {'name': '`db removerole <role> <user>`', 'description': 'Removes a specified role from a user.'},
                  {'name': '`db mute <user> <reason>`', 'description': 'Mutes a user from the server'},
                  {'name': '`db unmute <user> <reason>`', 'description': 'Unmutes a user from the server.'},
                  {'name': '`db warn <user> <reason>`', 'description': 'Warns a user from the server.'},
                  {'name': '`db userinfo <user>`', 'description': "Shows info about the user's account"},
                  {'name': '`db bw <word>`', 'description': 'Blocks a word from the server.'},
                  {'name': '`db rbw <user>`', 'description': 'Remove blocked words from the server.'}]

funCMDS = [{'name': '`db dm <user> <word>`', 'description': 'Dms someone a specific word.'},
           {'name': '`db meme`', 'description': 'See some DANK MEMES using this command.'},
           {'name': '`db hell`', 'description': 'Idk why this exists.'},
           {'name': '`db 8ball <question>`', 'description': 'The old classic 8ball (im talking about the magical one).'},
           {'name': '`db pic <image>`', 'description': 'Search for any image you want using this command (but pls dont use it for inappropriate stuff).'}]

eCMDS = [{'name': '`db balance`', 'description': 'Shows your balance of devcoins and your bank.','inline': False},
         {'name': '`db deposit <amount>`', 'description': 'Deposits devcoins to your bank.'},
         {'name': '`db withdraw <amount>`', 'description': 'Withdraws devcoins from the bank.'},
         {'name': '`db shop`', 'description': "Shows the shop of devbot's economy system"},
         {'name': '`db buy <item>`', 'description': 'Buys an specified item from the shop.'},
         {'name': '`db beg`', 'description': 'Beg for devcoins and get some.'},
         {'name': '`db slots <amount>`', 'description': 'Use your devcoins to see if you get a random money in a row and double your devcoins.'},
         {'name': '`db rob <user>`', 'description': 'Rob a user from the server.'},
         {'name': '`db bag`', 'description': 'Shows your bag of all the items you bought from the shop.'},
         {'name': '`db sell <item> <amount>`', 'description': 'Sell a specified amount of a specified item.'},
         {'name': '`db use <item>`', 'description': 'Use any tech gadgets and earn devcoins.'},
         {'name': '`db send <user> <amount>`', 'description': 'Sends a specified devcoins to a specified user.'}]

cryptoPercentList = [1,2,3,4,5]

with open('badwords.txt') as f:
     content = f.readlines()
     l = [x.strip() for x in content]

badwordsList = list(l)
badwordsListUpper = [word.upper() for word in badwordsList]

@devbot.event
async def on_ready():
     change_status.start()
     print('devbot has awaken')

@devbot.event
async def on_command_error(ctx, error):
     if isinstance(error, commands.CommandOnCooldown):
          titles = ['**Chill out with the spam**', '**Are you in a rush?**', '**Take a break**', '**Yo slow down a bit wont ya?**', '**Give it a rest!**']
          embed = Embed(title=random.choice(titles), description='Pls wait **{:.2f}s** to use this command again.The default cooldown time is `50s` btw.'.format(error.retry_after), color=discord.Color.random())
          await ctx.send(embed=embed)

@devbot.event
async def on_message(msg):
     if str(msg.channel) == '┃📢┃main-annoc':
          if '@everyone' in msg.content:
               pass
          if '@here' in msg.content:
               pass
     else:
          if '@everyone' in msg.content:
               await msg.delete()
               await msg.author.send(f'Hello, why are you trying to ping everyone in {msg.guild.name}?')
          if '@here' in msg.content:
               await msg.delete()
               await msg.author.send(f'Hello, why are you trying to ping everyone in {msg.guild.name}?')

     if str(msg.channel) == '┃🎫┃advertise':
          if 'https:/' in msg.content:
               pass
          if 'http:/' in msg.content:
               pass
     else:
          if 'https:/' in msg.content:
               await msg.delete()
               await msg.channel.send(f'Hey {msg.author.mention}, if you want to advertise please advertise in the advertise channel. If you cant find the advertise channel then you dont have the youtuber role')
          if 'http:/' in msg.content:
               await msg.delete()
               await msg.channel.send(f'Hey {msg.author.mention}, if you want to advertise please advertise in the advertise channel. If you cant find the advertise channel then you dont have the youtuber role')
          if 'http:/tenor.com' in msg.content:
               pass
          if 'https://tenor.com' in msg.content:
               pass
          if 'https://google.com' in msg.content:
               pass
          if 'http:/google.com' in msg.content:
               pass

     for word in badwordsList:
          if word in msg.content:
               await msg.delete()
               await msg.author.send(f"Hey!, don't use any foul language in {msg.guild.name}")

     for Word in badwordsListUpper:
          if Word in msg.content:
               await msg.delete()
               await msg.author.send(f"Hey!, don't use any foul language in {msg.guild.name}")

     await devbot.process_commands(msg)

@devbot.command(description='shows what the im is about')
async def about(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**About Me**', description="Hi!, my name is devbot and im a bot that replays to certian commands, just like any other bot! but i have little special commands that i want you to test!.type `db help` to view all of the commands that you can test.", color=custom_color, timestamp=ctx.message.created_at)
     embed.add_field(name='Creator/Developer of devbot:', value='The DevKid#4148')
     embed.add_field(name='Devbot was added at:', value='Tue, 29 June datetime.date.year, 06:33 AM UTC')
     embed.set_footer(text='hope you like how i perform!')
     embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/859320193045233674/6f40fa4ee3af004aecc54b44be42cd9d.webp?size=128')

     await ctx.send(embed=embed)

@devbot.group(invoke_without_command=True)
async def help(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title="**Help Command**", description='Hi!, you must have came from the about command!, or not.Here are some commands that can make your devbot experience better!', color=custom_color, timestamp=ctx.message.created_at)
     embed.add_field(name='Moderation', value='`db help moderation`')
     embed.add_field(name='Fun', value='`db help fun`')
     embed.add_field(name='Economy', value='`db help economy`')
     embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/859320193045233674/6f40fa4ee3af004aecc54b44be42cd9d.webp?size=128')
     await ctx.send(embed=embed)

@help.command()
async def moderation(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Moderation Commands**', color=custom_color, timestamp=ctx.message.created_at)
     for info in moderationCMDS:
          name = info['name']
          desc = info['description']
          embed.add_field(name=name,value=desc)

     await ctx.send(embed=embed)

@help.command()
async def economy(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Economy System Commands**', color=custom_color, timestamp=ctx.message.created_at)
     embed.add_field(name='**Currency**', value='`devcoins`',inline=True)
     for info in eCMDS:
          name = info['name']
          desc = info['description']
          embed.add_field(name=name,value=desc)
     
     await ctx.send(embed=embed)
  
@help.command()
async def fun(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Fun Commands**', color=custom_color)
     for info in funCMDS:
          name = info['name']
          desc = info['description']
          embed.add_field(name=name, value=desc)
     
     await ctx.send(embed=embed)

@devbot.command(aliases=['bal'])
async def balance(ctx,member: discord.Member = None):
     member = ctx.author if not member else member
     await openAccount(member)

     user = member
     
     users = await getBankData()
     
     devcoins_amt = users[str(user.id)]['devcoins']
     bank_amt = users[str(user.id)]['bank']

     embed = Embed(title=f"**{member.name}'s balance**", color=discord.Color.green(), timestamp=ctx.message.created_at)
     embed.add_field(name='devcoins', value=devcoins_amt)
     embed.add_field(name='bank', value=bank_amt)

     await ctx.send(embed=embed)

@devbot.command()
@commands.cooldown(1,50,commands.BucketType.user)
async def beg(ctx):
     await openAccount(ctx.author)

     names = ['Beluga', 'Dank Memer', 'Dream', 'Sounddrout', 'Obama', 'Micheal Jordan', 'DevKid']
     user = ctx.author

     users = await getBankData()

     earnings = random.randrange(69)

     users[str(user.id)]['devcoins'] += earnings
     s = [f'Hey little buddy here is {earnings} devcoins!!', f'Ah look a little poor guy, guess ill give you {earnings} devcoins', f'Bruhh another begger, fine take {earnings} devcoins.', f'ok take {earnings} devcoins']

     embed = Embed(title=random.choice(names), description=random.choice(s), color=discord.Color.green(), timestamp=ctx.message.created_at)

     with open('bank.txt','w') as f:
          json.dump(users, f)

     await ctx.send(embed=embed)

@devbot.command(aliases=['wd', 'with'])
async def withdraw(ctx,amount=None):
     await openAccount(ctx.author)

     if amount == None:
          await ctx.send('Please enter the amount to withdraw')
          return

     bal = await updateBank(ctx.author)

     if amount == 'max' or amount == 'all':
          amount = bal[1]

     amount = int(amount)

     if amount > bal[1]:
          await ctx.send('Hey!, You dont have that much money, also im not that easy to exploit.')
          return

     if amount < 0:
          await ctx.send('hey bud you cant withdraw negative numbers of devcoins, thats not how math works..')
          return

     await updateBank(ctx.author,amount)
     await updateBank(ctx.author,-1*amount,'bank')

     await ctx.send(f'You have withdrew {amount} devcoins!')

@devbot.command(aliases=['dep'])
async def deposit(ctx,amount=None):
     await openAccount(ctx.author)

     if amount == None:
          await ctx.send('Please enter the amount to deposit')
          return

     
     bal = await updateBank(ctx.author)

     if amount == 'max' or amount == 'all':
          amount = bal[0]

     amount = int(amount)

     if amount > bal[0]:
          await ctx.send('Hey!, You dont have that much money, also im not that easy to exploit.')
          return

     if amount < 0:
          await ctx.send('hey bud you cant deposit negative numbers of devcoins, thats not how math works..')
          return

     await updateBank(ctx.author,-1*amount)
     await updateBank(ctx.author,amount,'bank')

     await ctx.send(f'You have deposited {amount} devcoins!')

@devbot.command(aliases=['s','give'])
async def send(ctx, member: discord.Member,amount=None):
     await openAccount(ctx.author)
     await openAccount(member)

     if amount == None:
          await ctx.send('Please enter the amount to send')
          return

     
     bal = await updateBank(ctx.author)

     if amount == 'max' or amount == 'all':
          amount = bal[0]

     amount = int(amount)
     

     if amount > bal[0]:
          await ctx.send('Hey!, you dont have that much money, also im not that easy to exploit.')
          return

     if amount < 0:
          await ctx.send('hey bud you cant deposit negative numbers of devcoins, thats not how math works..')
          return

     await updateBank(ctx.author,-1*amount)
     await updateBank(member,amount,'bank')

     await ctx.send(f'You gave {amount} devcoins to {member.mention}!')

@devbot.command(aliases=['sl'])
@commands.cooldown(1,50,commands.BucketType.user)
async def slots(ctx,amount=None):
     await openAccount(ctx.author)

     if amount == None:
          await ctx.send('Please enter a amount')
          return

     bal = await updateBank(ctx.author)

     if amount == 'max' or amount == 'all':
          amount = bal[0]

     amount = int(amount)

     if amount > bal[0]:
          await ctx.send('Hey!, You dont have that much money, also im not that easy to exploit.')
          return

     if amount < 0:
          await ctx.send('hey bud you cant deposit negative numbers of devcoins, thats not how math works..')
          return

     finalList = []
     for i in range(3):
          a = random.choice([':dollar:',':yen:',':euro:'])

          finalList.append(a)
     

     if finalList[0] == finalList[1] or finalList[0] == finalList[2] or finalList[2] == finalList[1]:
          await updateBank(ctx.author,2*amount)
          embed = Embed(title='Slot Game', description=f'{str(finalList[0])},{str(finalList[1])},{str(finalList[2])}', color=discord.Color.green(), timestamp=ctx.message.created_at)
          embed.add_field(name='Results:',value='You won :)!')
          await ctx.send(embed=embed)
     else:
          await updateBank(ctx.author,-1*amount)
          embed = Embed(title='Slot Game', description=f'{str(finalList[0])},{str(finalList[1])},{str(finalList[2])}', color=discord.Color.red(), timestamp=ctx.message.created_at)
          embed.add_field(name='Results:',value='You lost :(')
          await ctx.send(embed=embed)

@devbot.command(aliases=['r'])
@commands.cooldown(1,50,commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    global earnings, earnings2

    gcList = ['You got caught!', 'You did not get caught!']
    gc = random.choice(gcList)

    bal = await updateBank(member)

    myBal = await updateBank(ctx.author)

    
    earnings = random.randrange(0, bal[0])
    earnings2 = random.randrange(1, myBal[0])


    await openAccount(ctx.author)
    await openAccount(member)

    if gc == gcList[0]:
          await ctx.send(f'You tried to rob {member.mention} but you got caught, so you had to give him {earnings2} devcoins.')
          await updateBank(ctx.author,earnings)
          await updateBank(member,-1*earnings)

    if bal[0]<100:
        await ctx.send('Hey, they dont have the devcoins you would need so next time try to rob from someone else.')
        return

    if earnings == 0:
        await ctx.send(f'You robbed {member.mention} and got NOTHING LMFAOOOOOO xD')

        await updateBank(ctx.author,0)
        await updateBank(member,0)

    if earnings == bal[0]:
        await ctx.send(f'You robbed {member.mention} and basically took ALL OF HIS DEVCOINS xD')
        await updateBank(ctx.author,earnings)
        await updateBank(member,-1*earnings)

    if earnings == 69:
        await ctx.send(f'You robbed {member.mention} and got 69(nice) devcoins!')
    
   

    await ctx.send(f'You robbed {member.mention} and got {earnings} devcoins!')
      
    await updateBank(ctx.author,earnings)
    await updateBank(member,-1*earnings)

@devbot.command()
async def shop(ctx):
     embed = Embed(title='Shop',color=discord.Color.dark_green(), timestamp=ctx.message.created_at)

     for item in Shop:
          name = item['name']
          price = item['price']
          desc = item['description']
          emoji = item['emoji']
          embed.add_field(name=f'{emoji}{name}',value=f'{price} dc | {desc}')

     await ctx.send(embed=embed)

@devbot.command()
@commands.cooldown(1,50,commands.BucketType.user)
async def buy(ctx,*,item,amount=1):
     await openAccount(ctx.author)
     
     res = await buyThis(ctx.author,item,amount)
     users = await getBankData()
     user = ctx.author


     if not res[0]:
          if res[1] == 1:
               await ctx.send('That doesnt exist in the shop, ask for something that is in the shop')
               return
          if res[1] == 2:
               await ctx.send(f'Hey you cant just buy something without enough money..')
               return

     if amount > 1:
          await ctx.send(f'You bought {amount} {item}s')

     await ctx.send(f'You bought {amount} {item}')

@devbot.command()
async def bag(ctx,member: discord.Member = None):
     member = ctx.author if not member else member
     await openAccount(member)
     user = member
     users = await getBankData()

     try:
          bag = users[str(user.id)]['bag']
     except:
          bag = []
     
     embed = Embed(title=f"{member.name}'s Bag",color=member.color, timestamp=ctx.message.created_at)
     for item in bag:
          name = item['item']
          amount = item['amount']

          embed.add_field(name=name,value=amount)

     await ctx.send(embed=embed)

@devbot.command()
async def sell(ctx,*,item,amount):
    await openAccount(ctx.author)

    res = await sell_this(ctx.author,item, amount)

    if amount == None:
        await ctx.send(f'Please enter a amount to sell a {item}')

    if not res[0]:
        if res[1] == 1:
              await ctx.send('That doesnt even exist..')
              return
        if res[1] == 2:
              await ctx.send(f'You dont have {amount} {item} in your bag.')
              return
        if res[1] == 3:
              await ctx.send(f'You dont have {item} in your bag. Sell something that you actually have...')
              return
        
    await ctx.send(f'You sold {amount} {item}')

async def sell_this(user,item_name,amount,price=None):
     item_name = item_name.lower()
     name_ = None
     for item in Shop:
          name = item['name'].lower()
          if name == item_name:
               name_ = name
               if price == None:
                    price = item['price']
               break
     
     if name_ == None:
          return[False, 1]
     
     cost = price*amount
     users = await getBankData()
     bal = await updateBank(user)

     try:
          index = 0
          t = None
          for thing in users[str(user.id)]['bag']:
               n = thing['item']
               if n == item_name:
                    old_amt = thing['amount']
                    new_amt = old_amt - amount
                    if new_amt < 0:
                         return [False,2]
                    users[str(user.id)]['bag'][index]['amount'] = new_amt
                    users[str(user.id)]['bag'].remove(item_name)
                    users[str(user.id)]['bag'].remove(amount)
                    t = 1
                    break
               index += 1
          if t == None:
               return [False, 3]
     
     except:
          return[False, 3]
     
     with open('bank.txt', 'w') as f:
          json.dump(users,f)
     
     await updateBank(user,cost,'bank')

     return [True, 'Worked']

@devbot.group(invoke_without_command=True)
async def use(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Use Command**', description='This command is used to use items you bought from the shop.', color=custom_color, timestamp=ctx.message.created_at)
     embed.add_field(name='how to use this command:', value='`db use <item you want to use>`')

     await ctx.send(embed=embed)

@use.command()
@commands.cooldown(1,50,commands.BucketType.user)
async def phone(ctx):
     embed = Embed(title='**Using Phone**', description='What do you want to use ur phone for?', color=discord.Color.darker_grey())
     embed.set_image(url='https://thumbs.dreamstime.com/t/white-phone-black-screen-mobile-smartphone-cell-dark-touchscreen-flat-vector-cartoon-illustration-objects-isolated-96487179.jpg')
     button1 = Button(label='Post a video', style=discord.ButtonStyle.green, emoji='<:uploadavideo:918524296538751047>')
     button2 = Button(label='Take A Picture', style=discord.ButtonStyle.green, emoji='<:images:920211347944407101>')
     buttonList  = [button1,button2]
     view = View()
     user = ctx.author
     users = await getBankData()

     for b in buttonList:
          view.add_item(b)
     
     async def b1_callback(interaction):
          await ctx.channel.purge(limit=1)
          await pv(ctx, 'https://thumbs.dreamstime.com/t/white-phone-black-screen-mobile-smartphone-cell-dark-touchscreen-flat-vector-cartoon-illustration-objects-isolated-96487179.jpg')

     async def b2_callback(interaction):
          await ctx.channel.purge(limit=1)
          await code(ctx)
     
     for thing in users[str(user.id)]['bag']:
          amt = thing['amount']
          item = {"item": "phone", "amount": amt}
          
     if item in users[str(user.id)]['bag']:
               button1.callback = b1_callback
               button2.callback = b2_callback
               await ctx.send(embed=embed, view=view)
               if amt > 1:
                    button1.callback = b1_callback
                    button2.callback = b2_callback
                    await ctx.send(embed=embed, view=view)
     else:
          await ctx.send('You dont have a laptop!')

@use.command()
@commands.cooldown(1,50,commands.BucketType.user)
async def laptop(ctx):
    embed = Embed(title='**Using Laptop**', description='What do you want to use ur laptop for?', color=discord.Color.greyple(), timestamp=ctx.message.created_at)
    embed.set_thumbnail(url='http://clipart-library.com/images_k/laptop-transparent-image/laptop-transparent-image-19.png')
    button1 = Button(label='Code', style=discord.ButtonStyle.green, emoji='<:code:918523770887610408>')
    button2 = Button(label='Post a video', style=discord.ButtonStyle.green, emoji='<:uploadavideo:918524296538751047>')
    button3 = Button(label='Crypto Mine', style=discord.ButtonStyle.green, emoji='⛏')
    buttonList = [button1,button2,button3]
    view = View()

    user = ctx.author
    users = await getBankData()

    for b in buttonList:
        view.add_item(b)
    
    async def b1_callback(interaction):
        await ctx.channel.purge(limit=1)
        await code(ctx)
    
    async def b2_callback(interaction):
        await ctx.channel.purge(limit=1)
        await pv(ctx, 'http://clipart-library.com/images_k/laptop-transparent-image/laptop-transparent-image-19.png')
    
    async def b3_callback(interaction):
        await ctx.channel.purge(limit=1)
        await crypto(ctx)

    for thing in users[str(user.id)]['bag']:
      amt = thing['amount']
      item = {"item": "laptop", "amount": amt}
      
    if item in users[str(user.id)]['bag']:
          button1.callback = b1_callback
          button2.callback = b2_callback
          button3.callback = b3_callback
          await ctx.send(embed=embed, view=view)
          if amt > 1:
               button1.callback = b1_callback
               button2.callback = b2_callback
               button3.callback = b3_callback
               await ctx.send(embed=embed, view=view)
    else:
     await ctx.send('You dont have a laptop!')

@commands.cooldown(1,50,commands.BucketType.user)
async def crypto(ctx):
     await openAccount(ctx.author)
     
     user = ctx.author
     users = await getBankData()
     item_name = "laptop"

     for num in range(100):
          message = await ctx.send(f'Starting mining, {num}% done')
          await message.edit(f'Starting mining, {num+1}% done')
          await message.delete()

          if num == 99:
               something = random.randint(1,2)
               if something == 1:
                    earnings = random.randint(1,1412)
                    message = await ctx.send(f'Successfully mined {earnings} devcoins!')
                    await updateBank(ctx.author,earnings,'bank')
                    break
               else:
                    earnings = random.randint(1,1412)
                    message = await ctx.send(f'I was about to give you {earnings} devcoins, but as your laptop crashed for mining too much, you cant get the crypto :(')
                    break

@commands.cooldown(1,50,commands.BucketType.user)
async def pv(ctx, thumb):
     await openAccount(ctx.author)

     user = ctx.author
     users = await getBankData()
     item_name = "laptop"

     embed = Embed(title='**Post A Video**', description='What type of video do you want to post in youtube?',color=discord.Color.brand_red())
     embed.set_thumbnail(url=thumb)

     b1 = Button(label='Reaction', style=discord.ButtonStyle.green)
     b2 = Button(label='Gaming', style=discord.ButtonStyle.green)
     b3 = Button(label='Art', style=discord.ButtonStyle.green)
     b4 = Button(label='Skits', style=discord.ButtonStyle.green)
     b5 = Button(label='Challenge', style=discord.ButtonStyle.green)
     b6 = Button(label='Tutorials', style=discord.ButtonStyle.green)
     view = View()
     bList = [b1,b2,b3,b4,b5,b6]

     for b in bList:
          view.add_item(b)
     
     async def b1_callback(interaction):
          earnings = random.randint(10,350)
          subs = random.randint(1,20)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a reaction video and got {earnings} devcoins and {subs} subscribers', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     async def b2_callback(interaction):
          earnings = random.randint(42,615)
          subs = random.randint(1,40)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a gaming video and got {earnings} devcoins and {subs} subscribers for your sweaty gameplay!!', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     async def b3_callback(interaction):
          earnings = random.randint(16,145)
          subs = random.randint(3,58)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a art video and got {earnings} devcoins and {subs} subscribers for your amazing drawing!!', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     async def b4_callback(interaction):
          earnings = random.randint(16,305)
          subs = random.randint(4,30)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a skit and got {earnings} devcoins and {subs} subscribers for your funny jokes xD !', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     async def b5_callback(interaction):
          earnings = random.randint(16,1000)
          subs = random.randint(10,200)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a challenge video and got {earnings} devcoins and {subs} subscribers', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     async def b6_callback(interaction):
          earnings = random.randint(19,559)
          subs = random.randint(10,30)
          embed2 = Embed(title='**Posted A Video**', description=f'You posted a tutorial video and got {earnings} devcoins and {subs} subscribers for your effort!!', color=discord.Color.brand_red())
          embed.set_thumbnail(url='https://image.pngaaa.com/955/2381955-middle.png')

          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
     
     b1.callback = b1_callback
     b2.callback = b2_callback
     b3.callback = b3_callback
     b4.callback = b4_callback
     b5.callback = b5_callback
     b6.callback = b6_callback

     await ctx.send(embed=embed,view=view)

@commands.cooldown(1,50,commands.BucketType.user)
async def code(ctx):
    await openAccount(ctx.author)

    user = ctx.author
    users = await getBankData()
    item_name = "laptop"

    embed = Embed(title='Code', description='***code anything. -devkid 2021***', color=discord.Color.blurple())
    embed.set_image(url='https://cdn.discordapp.com/attachments/859333846868426763/914552117249835088/empty_code.png')

    button1 = Button(label='Print hello world', style=discord.ButtonStyle.green)
    button2 = Button(label='Game', style=discord.ButtonStyle.green)
    button3 = Button(label='Website', style=discord.ButtonStyle.green)
    
    view = View()
    buttonList  = [button1,button2,button3]

    for button in buttonList:
        view.add_item(button)
  
    async def button1_callback(interaction):
      earnings = random.randint(16,35)
      embed2 = Embed(title='Code', description=f'You printed hello world and got {earnings} devcoins!', color=discord.Color.blurple())
      embed2.set_image(url='https://cdn.discordapp.com/attachments/890904447423770627/914830215631470622/unknown.png')
      view2 = View()

      await interaction.response.edit_message(embed=embed2, view=None)
      await updateBank(ctx.author,earnings,'bank')

    async def button2_callback(interaction):
      earnings = random.randint(169,6654)
      embed2 = Embed(title='Code', description=f'You coded a game and got {earnings} devcoins!', color=discord.Color.blurple())
      embed2.set_image(url='https://cdn.discordapp.com/attachments/912912262711369789/914916449108242462/unknown.png')
      view2 = View()

      await interaction.response.edit_message(embed=embed2, view=None)
      await updateBank(ctx.author,earnings,'bank')

    async def button3_callback(interaction):
          earnings = random.randint(200, 69420)
          embed2 = Embed(title='Code', description=f'You coded a game and got {earnings} devcoins!', color=discord.Color.blurple())
          embed2.set_image(url='https://cdn.discordapp.com/attachments/899864751725744138/920171839978893362/website.PNG')
          view2 = View()
          
          await interaction.response.edit_message(embed=embed2, view=None)
          await updateBank(ctx.author,earnings,'bank')
    
    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button3_callback
    await ctx.send(embed=embed,view=view)

async def buyThis(user,item_name,amount):
     item_name = item_name.lower()
     name_ = None
     for item in Shop:
          name = item['name'].lower()
          if name == item_name:
               name_ = name
               price = item['price']
               break

     if name_ == None:
          return [False, 1]
     
     cost = price*amount
     
     users = await getBankData()

     bal= await updateBank(user)

     if bal[0]<cost:
          return [False,2]
     
     try:
          index = 0
          t = None
          for thing in users[str(user.id)]['bag']:
               n = thing['item']
               if n == item_name:
                    old_amt = thing['amount']
                    new_amt = old_amt + amount
                    users[str(user.id)]['bag'][index]['amount'] = new_amt
                    t = 1
                    break
               index += 1
          if t == None:
               obj = {'item':item_name, 'amount':amount}
               users[str(user.id)]['bag'].append(obj)

     except:
          obj = {'item':item_name, 'amount':amount}
          users[str(user.id)]['bag'] = [obj]
     
     with open('bank.txt', 'w') as f:
          json.dump(users, f)

     for thing in users[str(user.id)]['bag']:
          n = thing['item']
          if n == 'Mega DevCoins' or 'mega devcoins':
               await updateBank(user,100000000*amount,'bank')

     await updateBank(user,cost*-1,'devcoins')

     return [True, 'Worked']

async def openAccount(user):
     users = await getBankData()

     if str(user.id) in users:
          return False
     else:
          users[str(user.id)] = {}
          users[str(user.id)]['devcoins'] = 0
          users[str(user.id)]['bank'] = 0
     
     with open('bank.txt', 'w') as f:
          json.dump(users,f)

     return True

async def getBankData():
     with open('bank.txt', 'r') as f:
          users = json.load(f)

     return users

async def updateBank(user,change=0,mode='devcoins'):
     users = await getBankData()

     users[str(user.id)][mode] += change

     with open('bank.txt', 'w') as f:
          json.dump(users, f)
     
     bal = [users[str(user.id)]['devcoins'],users[str(user.id)]['bank']]

     return bal

@devbot.command(description='dms you')
async def dm(ctx, member: discord.Member = None, *, send_dm):
     member = ctx.author if not member else member
     await member.send(f'{send_dm}')

@has_permissions(manage_messages=True)
@devbot.command(aliases=['BW', 'blockword'])
async def bw(ctx, *, word):
     if word in badwordsList:
          await ctx.send(f'This word is already blocked!')
     elif word not in badwordsList:
          badwordsList.append(f'{str(word)}')
          await ctx.send(f'Now blocking word {word}')

@bw.error
async def bw_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to block words, you must need the `manage messages` permission")

@has_permissions(manage_messages=True)
@devbot.command(aliases=['RBW', 'removeblockword', 'removeblockedword'])
async def rbw(ctx, *, word):
     if word not in badwordsList:
          await ctx.send(f'This word is already removed!, or it wasnt ever blocked..')
     if word in badwordsList:
          badwordsList.remove(str(word))
          await ctx.send(f'Removed {word} from blocked words')


@rbw.error
async def rbw_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to remove blocked words, you must need the `manage messages` permission")


@devbot.command()
async def pic(ctx, *, search):
     ran = random.randint(0, 10)
     resource = build('customsearch', 'v1', developerKey=apiKey).cse()
     result = resource.list(
          q=f"{search}", cx="1cc1c003789d32ce9", searchType="image"
     ).execute()
     url = result['items'][ran]['link']
     
     if search in badwordsList:
          pass
     else: 
          embed1 = discord.Embed(title=f"**Results for {search.title()}**",color=discord.Color.random())
          embed1.set_image(url=url)
          await ctx.send(embed=embed1)

@devbot.command()
async def userinfo(ctx, member: discord.Member):
     roles = [role for role in member.roles]
     
     embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
     embed.set_author(name=f"User Info - {member}")
     embed.set_thumbnail(url=member.avatar_url)
     embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar_url)
     embed.add_field(name='ID:', value=member.id)
     embed.add_field(name='Server nickname:', value=member.display_name)
     embed.add_field(name='Account Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
     embed.add_field(name='Joined the server at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
     embed.add_field(name=f'Roles in this server ({len(roles)})', value=' '.join([role.mention for role in roles]))
     embed.add_field(name='top role:', value=member.top_role.mention)
     embed.add_field(name='is a bot?', value=member.bot)
     
     await ctx.send(embed=embed)
     
     
@devbot.command()
async def devkidserver(ctx):
     await ctx.send("here is the link to the official devkid's server: https://discord.gg/VK3Ku329d8")
    

@devbot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
     responses = ['yes', 'no????', 'no', 'idk', 'well duh', 'what a idiot', 'maybe', 'honestly, i dont care', 'definitely', '*laughs*', '**wut**', 'huh, wdym']
     embed = Embed(title=f'Question: {question}', description=f'{random.choice(responses)}', color=discord.Color.random(), timestamp=ctx.message.created_atq)
     await ctx.send(embed=embed)


@devbot.command()
async def hell(ctx):
     custom_color = discord.Color.from_rgb(255, 0, 0)
     embed = Embed(title='hell', color=custom_color, timestamp=ctx.message.created_at)
     embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/022/134/elmo.jpg')
     await ctx.send(embed=embed)


@devbot.command(description='this command can warn people')
@has_permissions(manage_messages=True, administrator=True)
async def warn(ctx, member: discord.Member, *, reason=None):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Warned a Member**', description=f'{member.mention} has been warned for {reason}',color=custom_color, timestamp=ctx.message.created_at)
     embed2 = Embed(title='**You have been warned**', description=f'You have been warned in {ctx.guild.name}, reason: {reason}',color=custom_color, timestamp=ctx.message.created_at)
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to warn yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to warn me :/')
     
     await ctx.send(embed=embed)
     await member.send(embed=embed2)

@devbot.command()
@has_permissions(manage_messages=True, administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Muted a Member**', description=f'{member.mention} has been muted for {reason}', color=custom_color, timestamp=ctx.message.created_at)
     embed2 = Embed(title='**You have been muted**', description=f'You have been muted in {ctx.guild.name}, reason: {reason}', color=custom_color, timestamp=ctx.message.created_at)
     muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
     if member.id in [ctx.author.id]:
          await ctx.send("Don't be a fool and mute yourself :/")
     if member.id in [devbot.user.id]:
          await ctx.send("Why you want to mute me :/")

     if not muted_role:
          muted_role = await ctx.guild.create_role(name='Muted')

          for channel in ctx.guild.channels:
               await ctx.send("There is no muted role, so i'll be creating one...")
               await channel.set_permission(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)     

     await member.add_roles(muted_role, reason=reason)
     await ctx.send(embed=embed)
     await member.send(embed=embed2)

     
@devbot.command()
@has_permissions(manage_messages=True, administrator=True)
async def unmute(ctx, member: discord.Member):
     custom_color= discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**Unmuted a Member**', description=f'{member.mention} has been unmuted', color=custom_color, timestamp=ctx.message.created_at)
     embed2 = Embed(title='**You have been unmuted**', description=f'You have been unmuted from {ctx.guild.name}.', color=custom_color, timestamp=ctx.message.created_at)
     muted_role = discord.utiles.get(ctx.guild.roles, name='Muted')
     if not muted_role:
          await ctx.send('there is no muted role or the member is not muted.')
          return
     
     await member.remove_roles(muted_role)
     await ctx.send(embed=embed)
     await member.send(embed=embed2)
     

@mute.error
async def mute_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to mute people!.")


@unmute.error
async def unmute_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to unmute people!.")

@devbot.command()
@has_permissions(manage_roles=True)
async def createrole(ctx,*,role):
     Role = await ctx.guild.create_role(name=role)
     await ctx.send(f'created the role {role}')

@createrole.error
async def createrole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to manage/create roles!")
     

@devbot.command(description='this command can add any role to people')
@has_permissions(manage_roles=True)
async def addrole(ctx, role: discord.Role, member: discord.Member):
     await member.add_roles(role)
     await ctx.send(f'gave {role.name} role to {member.mention}.')

@devbot.command(description='this command can remove any role from people')
@has_permissions(manage_roles=True)
async def removerole(ctx, role: discord.Role, member: discord.Member):
     await member.remove_roles(role)
     await ctx.send(f'removed {role.name} role from {member.mention}')


@addrole.error
async def addrole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to add/manage roles!")
          await ctx.author.send("You don't have permission to add/manage members!")
     

@removerole.error
async def removerole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to remove/manage roles!")
          await ctx.author.send("You don't have permission to remove/manage roles!")
     

@warn.error
async def warn_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to warn people!")
          await ctx.author.send("You don't have permission to warn members!")
     

@devbot.command(description='shows dank memes')
async def meme(ctx):
     r = requests.get('https://memes.blademaker.tv/api?lang=en')
     res = r.json()
     title = res['title']
     ups = res['ups']
     downs = res['downs']
     nsfw = res['nsfw']
     if nsfw == True:
          await ctx.channel.purge(limit=1)
     else:
          embed = discord.Embed(title = f'{title}', color=discord.Color.brand_green(), timestamp=ctx.message.created_at)
          embed.set_image(url = res['image'])
          embed.set_footer(text=f'👍 {ups} 👎 {downs}')
          await ctx.send(embed=embed)

@devbot.command(aliases=['devkidyt', 'devytchannel', 'devyt'], description="shows the devkid's channel(the devkid is the creator of devbot btw)")
async def devkidytchannel(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title="**DevKid's Youtube Channel**", description='go sub to devkid!:',color=custom_color, timestamp=ctx.message.created_at)
     button = Button(label='Sub to DevKid',url='https://www.youtube.com/channel/UC51gai-7PFhvps79o0L-K9A')
     view = View()
     view.add_item(button)
     await ctx.send(embed=embed, view=view)


@devbot.command(description='shows what the date is today')
async def today(ctx):
     tday = datetime.date.today()
     await ctx.send(f'today is {str(tday)}')

          
@tasks.loop(minutes=100)
async def change_status():
     await devbot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(next(status)))

@devbot.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
     await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to manage/clear messages!")
          await ctx.author.send("You don't have permission to manage/clear messages!")

@devbot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to kick yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to kick me :/')
     embed = Embed(title='**Kicked a Member**', description=f'{member.mention} has been kicked for {reason}')
     embed2 = Embed(title='**You have been kicked**', description=f'you have been kicked from {ctx.guild.name}, reason: {reason}')
     await member.kick(reason=reason)
     await member.send(embed=embed2)
     await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to kick members!")
          await ctx.author.send("You don't have permission to kick members!")

@devbot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to ban yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to ban me :/')
     embed = Embed(title='**Banned a Member**', description=f'{member.mention} has been banned for {reason}')
     embed2 = Embed(title='**You have been banned**', description=f'you have been banned from {ctx.guild.name}, reason: {reason}')
     await member.ban(reason=reason)
     await member.send(embed=embed2)
     await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to ban members!")
          await ctx.author.send("You don't have permission to ban members!")
     

@devbot.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
     banned_members = await ctx.guild.bans()
     member_name, member_discriminator = member.split('#')

     for ban_entry in banned_members:
          user = ban_entry.user

          if (user.name, user.discriminator) == (member_name, member_discriminator):
               await ctx.guild.unban(user)
               await ctx.send(f"{user.mention} has been unbanned from the server")
               await user.send(f"you have been unbanned from {ctx.guild.name}")
               return

@unban.error
async def unban_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to unban members!")
          await ctx.author.send("You don't have permission to unban members!")


devbot.run('ODU5MzIwMTkzMDQ1MjMzNjc0.YNq-Sw.M9y7wT97ZJkzxHtxtw-L2HUOPic')