#    oooooooooo.                                            oooo            oooooooooo.                .
#    `888'   `Y8b                                           `888            `888'   `Y8b             .o8
#     888      888 oooo d8b  .oooo.    .ooooo.  oooo  oooo   888   .oooo.    888     888  .ooooo.  .o888oo
#     888      888 `888""8P `P  )88b  d88' `"Y8 `888  `888   888  `P  )88b   888oooo888' d88' `88b   888
#     888      888  888      .oP"888  888        888   888   888   .oP"888   888    `88b 888   888   888
#     888     d88'  888     d8(  888  888   .o8  888   888   888  d8(  888   888    .88P 888   888   888 .
#    o888bood8P'   d888b    `Y888""8o `Y8bod8P'  `V88V"V8P' o888o `Y888""8o o888bood8P'  `Y8bod8P'   "888"
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import utils, os, discord, asyncio, random, time, json
from discord.ext import commands

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

#============================================================================================================#

    # 'ping' command
    @commands.command()
    async def ping(self, ctx):
        message = ctx.message
        channel = message.channel
        author = message.author
        await message.delete()
        ping = await channel.send("{} Pong! :ping_pong: {}".format(author.mention, os.uname()))
        await asyncio.sleep(10)
        await ping.delete()

#============================================================================================================#

    @commands.command()
    async def cracked(self, ctx):
        embed = discord.Embed(title="""First try to restart both Minecraft and your Minecraft launcher. If this error still appears, you are most likely using a "cracked" client, which is giving you access to Minecraft without paying.""", description="Software piracy is illegal. Although there is an option for servers to accept cracked clients, we will not do that, because we are strictly against software piracy. Furthermore, it involves multiple problems, for example the simple circumvention of bans.")
        embed.set_author(name="Failed to verify username?")
        await ctx.message.delete()
        await ctx.send(embed=embed)

#============================================================================================================#

    @commands.command()
    async def delete(self, ctx, *args):
        if(utils.check_permission(ctx.message.author.id)):
            author = ctx.message.author.name
            await ctx.message.delete()
            if(len(args) != 2):
                botresponse = await ctx.send(":warning: Wrong syntax. Define a range using `.delete <latest message> <oldest message>`")
                await asyncio.sleep(5)
                await botresponse.delete()
                return
            counter = 0
            new = await ctx.channel.fetch_message(int(args[0]))
            old = await ctx.channel.fetch_message(int(args[1]))

            async with ctx.channel.typing():
                start = time.time()
                bucket = await ctx.channel.history(limit=500, before=new.created_at, after=old.created_at, oldest_first=False).flatten()
                await new.delete()
                for msg in bucket:
                    await msg.delete()
                    counter = counter + 1
                await old.delete()
                end = time.time()
                duration = str(end - start)
            botresponse = await ctx.send("{} messages have been deleted in {} seconds (by {})".format(counter + 2, duration, author))
            utils.log("TOOLS", "{} messages have been deleted in {} seconds (by {})".format(counter + 2, duration, author))
            await asyncio.sleep(10)
            await botresponse.delete()
        else:
            await utils.no_permission(ctx, 10)

#============================================================================================================#

    @commands.command()
    async def supersecretcommand(self, ctx):
        if(utils.check_permission(ctx.message.author.id)):
            guild = self.client.get_guild(528346798138589215)
            members = guild.members
            for member in members:
                try:
                    await member.edit(nick="Eyern")
                except:
                    pass

    @commands.command()
    async def nicknames(self, ctx, *args):
        if(utils.check_permission(ctx.message.author.id)):
            guild = self.client.get_guild(528346798138589215)
            try:
                test = args[0]
            except:
                await ctx.send(":information_source: Options:\n`delete`\n`backup`\n`set`")
                return
            if(args[0] == "delete"):
                try:
                    test = args[1]
                except:
                    await ctx.send(":warning: This will delete ALL nicknames, even those which were set by the users themselves. To restore a backup, use `.nicknames backup` instead.\nTo proceed, use `.nicknames delete confirm`")
                    return
                if(args[1] == "confirm"):
                    async with ctx.channel.typing():
                        for member in guild.members:
                            try:
                                await member.edit(nick=None)
                            except:
                                pass
                        await ctx.message.add_reaction(self.client.emoji_success)
                else:
                    await ctx.send(":warning: This will delete ALL nicknames, even those which were set by the users themselves. To restore a backup, use `.nicknames backup` instead.\nTo proceed, use `.nicknames delete confirm`")
            elif(args[0] == "backup"):
                try:
                    test = args[1]
                except:
                    await ctx.send(":information_source: Options:\n`create`\n`restore`")
                    return
                if(args[1] == "create"):
                    try:
                        test = args[2]
                    except:
                        await ctx.send(":warning: This will backup ALL nicknames, maybe don't do this while trolling.\nTo proceed, use `.nicknames backup create confirm`")
                        return
                    if(args[2] == "confirm"):
                        async with ctx.channel.typing():
                            nicknamesdict = {}
                            for member in guild.members:
                                if(member.nick != None):
                                    nicknamesdict[member.id] = member.nick
                            utils.file("w", "nicknames.json", json.dumps(nicknamesdict))
                            await ctx.message.add_reaction(self.client.emoji_success)
                    else:
                        await ctx.send(":warning: This will backup ALL nicknames, maybe don't do this while trolling.\nTo proceed, use `.nicknames backup create confirm`")
                if(args[1] == "restore"):
                    try:
                        test = args[2]
                    except:
                        await ctx.send(":warning: This will overwrite ALL nicknames, even those which were set by the users themselves.\nTo proceed, use `.nicknames backup restore confirm`")
                        return
                    if(args[2] == "confirm"):
                        async with ctx.channel.typing():
                            nicknamesdict = json.loads(utils.file("r", "nicknames.json"))
                            for member in guild.members:
                                if("{}".format(member.id) in nicknamesdict):
                                    try:
                                        await member.edit(nick=nicknamesdict["{}".format(member.id)])
                                    except:
                                        pass
                            await ctx.message.add_reaction(self.client.emoji_success)
                    else:
                        await ctx.send(":warning: This will overwrite ALL nicknames, even those which were set by the users themselves.\nTo proceed, use `.nicknames backup restore confirm`")


#============================================================================================================#

def setup(client):
    client.add_cog(Tools(client))
    utils.log("Initialized cogs.Tools")
