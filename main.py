import discord
from discord.ext import commands
from discord.commands import Option
from src.storeDatas.storeDatas import *
from src.duelView.duelView import InitDuel
from src.chessView.chessView import InitChessGame
from src.quoteHandler.quoteHandler import QuoteHandler

# Created by Djason Gadiou (Magicred1#3948) on Discord
# Github : https://github.com/Magicred-1/self-improvement-bot
# This bot is made to help you workout by counting your push ups, pull ups and squats
# You we be able to add or remove points to other users (admin only)
# You will be able to reset your score (admin only)
# You will be able to see the leaderboard of the entire server.
# You will be able to see your score
# Do some push-ups, pull-ups and squats and get fit !
# For any questions, contact me on Discord (Magicred1#3948)

if __name__ == "__main__":

    testing_servers = [GUILD]

    bot = commands.Bot(
        command_prefix = "/", intents=discord.Intents.all(), help_command=None
    )  # The bot's prefix is "/" to call a command

    bot.remove_command("help")

    @bot.event
    async def on_ready():
        # Prints the bot's name
        print(
            f"{bot.user} (id : {bot.user.id}) has connected to the Discord and he's here to make you workout and rich !"
        )
        # We're also able to use property methods to gather additional data.
        print(f"The bot's latency is {round(bot.latency*100)} ms.")


    # Application command error handler
    @bot.event
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):

        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if isinstance(error, commands.CommandOnCooldown):
            message =  f"Not so quick {ctx.author.mention} ! Wait {round(error.retry_after, 2)} seconds before using this command again ! :moyai:"
            await ctx.respond(
                message,
                ephemeral=True,
            )
            writeLogs(ctx, message)
        elif isinstance(error, commands.MissingPermissions):
            message = f"{ctx.author.mention} you don't have the permission to use this command !"
            await ctx.respond(
                message,
                ephemeral=True,
            )
            writeLogs(ctx, message)
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"{ctx.author.mention} you're missing an argument !"
            await ctx.respond(
                message,
                ephemeral=True,
            )
            writeLogs(ctx, message)
        else:
            message_content = getattr(ctx.message, "content", "<unknown command>")
            message = f"An error has occured while {ctx.author} was using the command {message_content} in {ctx.channel} at {timestamp}.\n The error is : {error}"
            await ctx.respond(
                f"Sorry {ctx.author.name}, an error has occured ! Please contact the bot's owner !",
                ephemeral=True,
            )
            writeLogs(ctx, message)
            raise error
        

    # Bot commands logs and error handling
    @bot.event
    async def on_application_command(ctx):
        if ctx.channel.id == CHANNEL:
            message = f'{ctx.author} has used the command {ctx.message.content} in {ctx.channel} at {ctx.message.created_at}.'
            print(f'{ctx.author} has used the command {ctx.message.content} in {ctx.channel} at {ctx.message.created_at}.')

            writeLogs(ctx, message)

    @bot.event
    async def on_command(ctx):
        if ctx.channel.id == CHANNEL:
            message = f'{ctx.author} has used the command {ctx.message.content} in {ctx.channel} at {ctx.message.created_at}.'
            print(f'{ctx.author} has used the command {ctx.message.content} in {ctx.channel} at {ctx.message.created_at}.')

            writeLogs(ctx, message)


    # Error handler
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f":x: Hey {ctx.author.mention} this command doesn't exist but nice try .. :x:"
            )
            writeLogs(ctx, f"{ctx.author} tried to use the command {ctx.message.content} but it doesn't exist !")
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Sorry {ctx.author.mention}, you're missing some arguments ! Please use /help to see the list of commands !"
            await ctx.send(
                message
            )
            writeLogs(ctx, f"Sorry {ctx.author.mention}, you're missing some arguments ! Please use /help to see the list of commands !")
        elif isinstance(error, commands.MissingPermissions):
            message = f"Sorry {ctx.author.mention}, you don't have the permissions to use this command !"
            await ctx.send(
                message
            )
            writeLogs(ctx, message)
        else:
            message = f"Sorry {ctx.author.mention}, an error has occured ! Please contact the bot's owner !"
            await ctx.send(
                message
            )
            writeLogs(ctx, message)


    @bot.slash_command(
        name="pushups",
        description="Add the number of push-ups you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def pushups(
            ctx,
            number_of_pushups:Option(int, "The number of push-ups you've done", required=True)
        ):
        if ctx.channel.id == int(CHANNEL):
            # Adds the number of push-ups done by the user to the leaderboard
            if number_of_pushups != 0 and number_of_pushups > 0 and number_of_pushups <= 1000:
                await ctx.respond(
                    f"You've done {number_of_pushups} push-ups ! :partying_face:", ephemeral=True
                )
                # We store the number of push-ups multiplied by 2 in the leaderboard.json file
                updateLeaderboard(ctx.author.name, "pushups", number_of_pushups, ctx.author.id)
            else:
                error = discord.Embed(
                    title="You can't do 0 or negative push-ups or higher than 1000 ! Brookie !",
                    color=discord.Colour.random(),
                )
                error.set_image(
                    url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
                )
                error.set_author(name=f"{ctx.author.name}")
                return await ctx.respond(embed=error, ephemeral=True)


    @bot.slash_command(
        name="pullups",
        description="Add the number of squats you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def pullups(
            ctx, 
            number_of_pullups:Option(int, "The number of squats you've done", required=True)
        ):
        if ctx.channel.id == int(CHANNEL):
            # Adds the number of pull-ups done by the user to the leaderboard
            if number_of_pullups > 0 and number_of_pullups <= 1000:
                await ctx.respond(
                    f"You've done {number_of_pullups} pull-ups ! :partying_face:", ephemeral=True
                )
                # We store the number of pull-ups multiplied by 2 in the leaderboard.json file
                updateLeaderboard(ctx.author.name, "pullups", number_of_pullups, ctx.author.id)
            else:
                error = discord.Embed(
                    title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                    color=discord.Colour.random(),
                )
                error.set_image(
                    url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
                )
                error.set_author(name=f"{ctx.author.name}")
                return await ctx.respond(embed=error, ephemeral=True)


    @bot.slash_command(
        name="squats",
        description="Add the number of squats you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def squats(
            ctx,
            number_of_squats:Option(int, "The number of squats you've done", required=True)
        ):
        if ctx.channel.id == int(CHANNEL):
            # We divide the number of squats by 5 because it's easier to do 5 squats than 1 push-up
            if number_of_squats > 0 and number_of_squats <= 1000:
                await ctx.respond(
                    f"You've done {number_of_squats} squats, keep going ! :partying_face:", ephemeral=True
                )
                # We store the number of squats divided by 5 in the leaderboard.json file
                updateLeaderboard(ctx.author.name, "squats", number_of_squats, ctx.author.id)
            else:
                error = discord.Embed(
                    title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                    color=discord.Colour.random(),
                )
                error.set_image(
                    url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
                )
                error.set_author(name=f"{ctx.author.name}")
                return await ctx.respond(embed=error)


    @bot.slash_command(
        name="jumpingjacks",
        description="Add the number of jumping jacks you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def jumpingjacks(
            ctx, 
            number_of_jumpingjacks: Option(int, "The number of jumping jacks you've done", required=True)
        ):
        if ctx.channel.id == int(CHANNEL):
            if number_of_jumpingjacks > 0 and number_of_jumpingjacks <= 1000:
                await ctx.respond(
                    f"You've done {number_of_jumpingjacks} jumping jacks, keep going ! :partying_face:", ephemeral=True
                )
                # We store the number of jumping jacks divided by 3 in the leaderboard.json file
                updateLeaderboard(ctx.author.name, "jumping_jacks", number_of_jumpingjacks, ctx.author.id)
            else:
                error = discord.Embed(
                    title="You can't do 0 or negative jumping jacks or higher than 1000 ! Brookie !",
                    color=discord.Colour.random(),
                )
                error.set_image(
                    url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
                )
                error.set_author(name=f"{ctx.author.name}")
                return await ctx.respond(embed=error, ephemeral=True)


    @bot.slash_command(
        name="burpees",
        description="Add the number of burpees you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def burpees(
            ctx, 
            number_of_burpees: Option(int, "The number of burpees you've done", required=True)
        ):
        if ctx.channel.id == int(CHANNEL):
            if number_of_burpees > 0 and number_of_burpees <= 1000:
                await ctx.respond(
                    f"You've done {number_of_burpees} burpees, keep going ! :partying_face:"
                )
                # We store the number of burpees multiplied by 2 in the leaderboard.json file
                updateLeaderboard(ctx.author.name, "burpees", number_of_burpees, ctx.author.id)
            else:
                error = discord.Embed(
                    title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                    color=discord.Colour.random(),
                )
                error.set_image(
                    url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
                )
                error.set_author(name=f"{ctx.author.name}")
                return await ctx.respond(embed=error, ephemeral=True)

    @bot.slash_command(
        name="situps",
        description="Add the number of sit-ups you've done to the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def situps(
            ctx, 
            number_of_situps: Option(int, "The number of sit-ups you've done", required=True)
        ):
        if number_of_situps > 0 and number_of_situps <= 1000:
            await ctx.respond(
                f"You've done {number_of_situps} sit-ups, keep going ! :partying_face:"
            )
            # We store the number of sit-ups divided by 2 in the leaderboard.json file
            updateLeaderboard(ctx.author.name, "situps", number_of_situps, ctx.author.id)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.random(),
            )
            error.set_image(
                url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
            )
            error.set_author(name=f"{ctx.author.name}")
            await ctx.respond(embed=error, ephemeral=True)


    @bot.slash_command(
        name="score",
        description="Get your score or of other users in the leaderboard",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def score(
            ctx, 
            username: Option(str, "Username of the user you want to get the score of", required=False)
        ):
        if ctx.channel.id == int(CHANNEL):
            if username is None:
                username = ctx.author.name
                user_id = str(ctx.author.id)
            else:
                # remove < @ >
                user_id = username[2:-1]
                username = ctx.guild.get_member(int(user_id)).name
            
            leaderboard = getLeaderboard()

            # Sends the user's score to the channel
            score_window = discord.Embed(
                title=":stars: **__Your score__** :stars:",
                description=f"**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point** / 3 jumping jack = **1 point** / 1 burpee = **2 points** / 2 sit-ups = **1 point**",
                color=discord.Colour.random(),
            )
            score_window.set_author(name=f"{username}")
            score_window.set_thumbnail(
                url="https://media.tenor.com/BrHJBHqAxWAAAAAM/andrew-tate-top-g.gif"
            )
            
            # If the user is in the leaderboard and has done at least one exercise

            if user_id in leaderboard:
                score_window.add_field(
                    name="Push-ups", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['pushups']}** push-ups", 
                    inline=True
                )
                score_window.add_field(
                    name="Pull-ups", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['pullups']}** pull-ups", 
                    inline=True
                )
                score_window.add_field(
                    name="Squats", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['squats']}** squats", 
                    inline=True
                )
                score_window.add_field(
                    name="Jumping Jack", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['jumping_jacks']}** jumping jacks", 
                    inline=True
                )
                score_window.add_field(
                    name="Burpees", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['burpees']}** burpees", 
                    inline=True
                )
                score_window.add_field(
                    name="Sit-ups", 
                    value=f"**{leaderboard[str(user_id)]['exercises']['situps']}** sit-ups", 
                    inline=True
                )
                score_window.add_field(
                    name="Total", 
                    value=f"**{getUserScore(user_id)}** points", 
                    inline=True
                )
                return await ctx.respond(embed=score_window, ephemeral=True)
            else:
                score_window.add_field(
                    name="You did no exercises ..", 
                    value="Your score is **0**, Brookie !\nHealth is Wealth use the command **__/help__** to start your journey !", 
                    inline=True
                )
                return await ctx.respond(embed=score_window, ephemeral=True)



    @bot.slash_command(
        name="help",
        description="Get started with the bot",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def help(ctx):
        if ctx.channel.id == int(CHANNEL):
            # Sends the help message to the channel
            help = discord.Embed(
                title=":robot: **__Commands available :__** :robot:",
                color=discord.Colour.blue(),
            )
            help.add_field(
                name="<:absolutely_halal:1004850376513695844> **/score <username>* ** <:absolutely_halal:1004850376513695844>", 
                value="Shows your personnal score", 
                inline=False
            )
            help.add_field(
                name=":hand_splayed: **/pushups <number>** :hand_splayed: ",
                value="Adds the number of push-ups you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":muscle: **/pullups <number>** :muscle:",
                value="Adds the number of pull-ups you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":leg: **/squats <number>** :leg:",
                value="Adds the number of squats you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":up: **/jumpingjacks <number>** :up:",
                value="Adds the number of jumping jacks you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":leftwards_hand: **/burpees <number>** :rightwards_hand: ",
                value="Adds the number of burpees you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":chair: **/situps <number>** :chair:",
                value="Adds the number of sit-ups you have done to your score",
                inline=False,
            )
            help.add_field(
                name=":people_wrestling: **/leaderboard** :people_wrestling:",
                value="Shows the leaderboard of the server",
                inline=False,
            )
            help.add_field(
                name=":speech_balloon: **/quote** :speech_balloon:", 
                value="Send a quote.", 
                inline=False
            )
            help.add_field(
                name="<:1257gigachadpink:1002689383763292240> **/topG** <:1257gigachadpink:1002689383763292240>", 
                value="Shows the TOP G OF THE MONTH", 
                inline=False
            )
            help.add_field(name="<:9588openhandleft:1002689810483388456> **/avatar** <:4525openhandright:1002689478760091658>", 
                value="Shows your avatar", 
                inline=False
            )
            help.add_field(
                name=":heart: **/credits** :heart:", 
                value="Shows the credits", 
                inline=False
            )
            help.add_field(
                name="<:7607walterwhite:1002689704971473007> **/help_admin** <:7607walterwhite:1002689704971473007>",
                value="Admins only : Show the admins commands",
                inline=False,
            )
            help.add_field(
                name="WIP :crossed_swords: **/duel** :crossed_swords:",
                value="Challenge someone to a fitness duel",
                inline=False,
            )
            help.set_image(
                url="https://media.tenor.com/x_30tXZ_DRQAAAAM/tate-andrew-tate.gif"
            )
            help.set_footer(
                text="* Optional argument",
            )

            return await ctx.respond(embed=help, ephemeral=True)


    @bot.slash_command(
        name="quote",
        description="Send a quote",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def quote(ctx):
        handler = QuoteHandler('quotes.txt')
        quotes = handler.getRandomQuote()

        if ctx.channel.id == int(CHANNEL):
            # Sends one random quote from Andrew Tate to the channel
            andrewGIF = discord.Embed(
                title="Andrew Tate - The Top G",
                description="Quotes from Andrew Tate and more ...",
                color=discord.Colour.random(),
            )
            andrewGIF.add_field(
                name="**Quote of the day :**",
                value=f"{quotes}",
                inline=False,
            )
            andrewGIF.set_image(
                url="https://media.tenor.com/xSfy4B1dbrsAAAAM/cobra-tate-cobra.gif"
            )
            return await ctx.respond(embed=andrewGIF, ephemeral=True)


    @bot.slash_command(
        name="leaderboard",
        description="Shows the leaderboard of the server",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def leaderboard(ctx):  # Shows the leaderboard
        if ctx.channel.id == int(CHANNEL):
            # Sends the leaderboard to the channel
            numberUser = 0

            leaderboard = getLeaderboard()

            if getTotalScore() == 0:
                return await ctx.respond(
                    ":x: No one has done any workout yet ! Do some push-ups, pull-ups and squats to get started ! :x:", ephemeral=True
                )
            else:
                ranking_embed = discord.Embed(
                    title=":moyai: **__Leaderboard - TOP 10 only__** :moyai:",
                    description="**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point**",
                    color=discord.Colour.random(),
                )
                ranking_embed.add_field(
                    name="**:dart: __Discord Server Cumulated Score :__**",
                    value=f"{getTotalScore()} points :dart:",
                    inline=False,
                )
                ranking_embed.add_field(
                    name="**__Ladder : __**", 
                    value="", inline=False
                )
                ranking_embed.set_image(
                    url="https://media.discordapp.net/attachments/553215505712807938/826206690399617044/finna-pnut.gif"
                )
                # we use getUserScore() to sort the leaderboard by score (highest score first)
                # we use reverse=True to get a descending order
                # We exlude Andrew Tate ID from the leaderboard
                foreachUser = sorted(
                    leaderboard, key=lambda x: getUserScore(x), reverse=True
                )
                # remove Andrew Tate ID from the foreachUser list

                foreachUser.remove("1074307468160667648") # Andrew Tate ID

                foreachUser = foreachUser[:10] # We only want the TOP 10

                for user_id in foreachUser:
                    if getUserScore(user_id) > 0:
                        if user_id == foreachUser[0]:
                            ranking_embed.add_field(
                                name=f":crown: {getUsernameByUserID(user_id)} :",
                                value=f"{getUserScore(user_id)} points",
                                inline=False,
                            )
                        elif user_id == foreachUser[1]:
                            ranking_embed.add_field(
                                name=f":second_place: {getUsernameByUserID(user_id)} :",
                                value=f"{getUserScore(user_id)} points",
                                inline=False,
                            )
                        elif user_id == foreachUser[2]:
                            ranking_embed.add_field(
                                name=f":third_place: {getUsernameByUserID(user_id)} :",
                                value=f"{getUserScore(user_id)} points",
                                inline=False,
                            )
                        else:
                            ranking_embed.add_field(
                                name=f"{numberUser+1} - {getUsernameByUserID(user_id)} :",
                                value=f"{getUserScore(user_id)} points",
                                inline=False,
                            )
                        numberUser += 1
                    else:
                        break
                return await ctx.respond(embed=ranking_embed)


    @bot.slash_command(
        name="avatar",
        description="Shows your avatar",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def avatar(ctx):
        # Sends the avatar of the user who sent the message https://cdn.discordapp.com/avatars/..../{user_avatar}.png
        if ctx.channel.id == int(CHANNEL):
            avatar = discord.Embed(
                color=discord.Colour.random(), title=f"**__{ctx.author.name}'s Avatar :__**"
            )
            avatar.set_image(url=f"{ctx.author.avatar}.png")
            return await ctx.respond(embed=avatar, ephemeral=True)

    @bot.slash_command(
        name="duel",
        description="Challenge someone to a duel",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def duel(ctx, user: Option(discord.Member, "User to challenge", required=True)):
        if ctx.channel.id == int(CHANNEL):
            if user.id == ctx.author.id:
                return await ctx.respond(
                    "You can't challenge yourself :smirk:", ephemeral=True
                )
            elif user.bot:
                return await ctx.respond("You can't challenge a bot :smirk:", ephemeral=True)
            else:
                await ctx.respond(
                    f"You choosen to challenge {user.mention} to a fitness duel.:japanese_goblin:\nPlease select an exercise and a time limit.", 
                    ephemeral=True,
                    view=InitDuel(ctx.author, user, ctx.author),
                )

    @bot.slash_command(
        name="chess",
        description="Challenge someone to a chess game",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def chess(ctx, opponent: Option(discord.Member, "User to challenge to a chess game", required=True)):
        if ctx.channel.id == int(CHANNEL):
            if opponent.id == ctx.author.id:
                return await ctx.respond(
                    "You can't challenge yourself :smirk:", ephemeral=True
                )
            elif opponent.bot:
                return await ctx.respond("You can't challenge a bot :smirk:", ephemeral=True)
            else:
                await ctx.respond(
                    f"Chess game started between {ctx.author.mention} and {opponent.mention} :chess_pawn:\n\nPlease select the type of chess game you want to play :",
                    ephemeral=True,
                    view=InitChessGame(ctx, ctx.author.name, opponent.name),
                )

    @bot.slash_command(
        name="topg",
        description="Shows the top g of the month",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def topg(ctx):
        top_g = getTheTopG()
        top_g_embed = discord.Embed(
            title="**TOP G OF THE MONTH :**", color=discord.Colour.random()
        )
        top_g_embed.add_field(
            name=f"{top_g}",
            value="",
            inline=False,
        )
        top_g_embed.set_image(url="https://cdn3.emoji.gg/emojis/9749-andrew-tate.png")
        top_g_embed.set_footer(text="Made by Andrew Tate")
        await ctx.respond(embed=top_g_embed)

    @bot.slash_command(
        name="credits",
        description="Shows the credits of the bot",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def credits(ctx):
        if ctx.channel.id == int(CHANNEL):
            credits = discord.Embed(
                title=":robot: **__Credits :__** :robot:",
                color=discord.Colour.random(),
            )
            credits.add_field(
                name="**__:tools: Self Improvement Bot :tools:__**",
                value="Made by **__Magicred1#3948__ with DiscordPy [GitHub Repo](https://github.com/Magicred-1/self-improvement-bot)**",
                inline=False,
            )
            credits.add_field(
                name="**__:bulb: Original Idea from :bulb:__**",
                value="**__@Ali_95482375#7378__**",
                inline=False,
            )
            credits.add_field(
                name="**__:thought_balloon: Inspired by :thought_balloon:__**",
                value="**__The Tate Bros (Andrew & Tristan)__**",
                inline=False,
            )
            credits.add_field(
                name="**__:heart: Special thanks to :heart:__**",
                value="**__@Ali_95482375#7378__**\n**__@Dr. Legat#3936__**\n**__@endeavour#9952__**\n**__@Muru#1304__**\n**__@F3nneC#9440__**",
                inline=False,
            )
            credits.set_image(
                url="https://media.tenor.com/_kBC_WQDcHUAAAAC/tristantate-no-were-boozing.gif"
            )

            return await ctx.respond(embed=credits)


    # /!\ Admin only commands /!\


    @bot.slash_command(
        name="help_admin",
        description="Shows the admin commands",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def help_admin(ctx):
        if ctx.channel.id == int(CHANNEL):
            # Sends the help message to the channel
            help = discord.Embed(
                title="Admin commands available :", color=discord.Colour.random()
            )
            help.add_field(
                name="**/reset_points <user>**",
                value="Resets the score of a user",
                inline=False,
            )
            help.add_field(
                name="**/add_points <user> <pushups> <pullups> <squats> <jumping_jacks> <burpees> <situps>**",
                value="Adds points to a user",
                inline=False,
            )
            help.add_field(
                name="**/remove_points <user> <pushups> <pullups> <squats> <jumping_jacks> <burpees> <situps>**",
                value="Removes points to a user",
                inline=False,
            )
            help.add_field(
                name="**/reset_leaderboard**",
                value="Resets the leaderboard",
                inline=False,
            )
            help.add_field(
                name="**/settopg <user>**",
                value="Sets the TOP_G_OF_THE_MONTH",
                inline=False,
            )
            help.add_field(
                name="**/help_admin**",
                value="Shows all the admin commands available.",
                inline=False,
            )

            return await ctx.respond(embed=help, ephemeral=True)


    # Reset the points of a user
    @bot.slash_command(
        name="reset_points",
        description="Resets the score of a user",
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def reset_points(
            ctx, 
            reset_user_points: Option(str, "The user to reset the score of", required=True)
        ):
        if reset_user_points == "":
            return await ctx.respond(
                f"Please specify a user to reset the score of !", ephemeral=True
            )

        def getUserID(username):
            for member in ctx.guild.members:
                if member.name == username:
                    return member.id

        user_id = getUserID(reset_user_points)

        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.respond(
                f"Are you sure you want to reset the score of {reset_user_points} ? (y/n)", ephemeral=True
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for("message", check=check)
            if msg.content == "y":
                deleteUserLeaderboard(user_id)
                await ctx.respond(
                    f"{reset_user_points} score has been reset !", ephemeral=True
                )
                
                await msg.delete()
            else:
                return await ctx.respond(
                    f"The score of {reset_user_points} has not been reset !", ephemeral=True
                )


    # Add points to a user
    @bot.slash_command(
        name="add_points",
        description="Adds points to a user",
        guild_ids = testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def add_points(
        ctx,
        add_user_points: Option(str, "The user to add points to", required=True),
        add_pushups: Option(int, "The number of push-ups to add", required=False, default=0),
        add_pullups: Option(int, "The number of pull-ups to add", required=False, default=0),
        add_squats: Option(int, "The number of squats to add", required=False, default=0),
        add_jumping_jacks: Option(int, "The number of jumping jacks to add", required=False, default=0),
        add_burpees: Option(int, "The number of burpees to add", required=False, default=0),
        add_situps: Option(int, "The number of situps to add", required=False, default=0),
    ):

        if add_user_points == "":
            return await ctx.respond(f"Please specify a user to add points to !")

        if ctx.channel.id == int(CHANNEL):
            # get user id from username
            def getUserID(username):
                for member in ctx.guild.members:
                    if member.name == username:
                        return member.id

            user_id = getUserID(add_user_points)

            # Prompt the user to confirm the reset
            await ctx.respond(
                f"Are you sure you want to add {add_pushups} push-ups, {add_pullups} pull-ups, {add_squats} squats, {add_jumping_jacks}, {add_burpees} and sit-ups {add_situps} to {add_user_points}'s score ? (y/n)", ephemeral=True
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for("message", check=check)

            if msg.content == "y":
                leaderboard = getLeaderboard()
                if add_user_points in leaderboard:
                    # Add the points to the user in the leaderboard
                    updateLeaderboard(add_user_points, "pushups", add_pushups, user_id)
                    updateLeaderboard(add_user_points, "pullups", add_pullups, user_id)
                    updateLeaderboard(add_user_points, "squats", add_squats, user_id)
                    updateLeaderboard(add_user_points, "jumping_jacks", add_jumping_jacks, user_id)
                    updateLeaderboard(add_user_points, "burpees", add_burpees, user_id)
                    updateLeaderboard(add_user_points, "situps", add_situps, user_id)

                    await msg.delete()

                    await ctx.respond(
                        f"{add_user_points} has been added {add_pushups} push-ups, {add_pullups} pull-ups, {add_squats} squats, {add_jumping_jacks} jumping jacks, {add_burpees} burpees and {add_situps} sit-ups to {add_user_points}'s score !", ephemeral=True
                    )
                else:
                    updateLeaderboard(add_user_points, "pushups", add_pushups, user_id)
                    updateLeaderboard(add_user_points, "pullups", add_pullups, user_id)
                    updateLeaderboard(add_user_points, "squats", add_squats, user_id)
                    updateLeaderboard(add_user_points, "jumping_jacks", add_jumping_jacks, user_id)
                    updateLeaderboard(add_user_points, "burpees", add_burpees, user_id)
                    updateLeaderboard(add_user_points, "situps", add_situps, user_id)
                    await ctx.respond(
                        f"{add_user_points} has been created and added to the leaderboard with {add_pushups} push-ups, {add_pullups} pull-ups, {add_squats} squats, {add_jumping_jacks} jumping jacks, {add_burpees} burpees and {add_situps} sit-ups to {add_user_points}'s score !", ephemeral=True
                    )


    # Reset the leaderboard
    @bot.slash_command(
        name="reset_leaderboard",
        description="Resets the leaderboard",
        guild_ids = testing_servers,
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    async def reset_leaderboard(ctx):
        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.respond(f"Are you sure you want to reset the leaderboard ? (y/n)", ephemeral=True)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for("message", check=check)

            if msg.content == "y":
                leaderboard = getLeaderboard()
                for user in leaderboard:
                    if user == "1074307468160667648":
                        continue
                    deleteUserLeaderboard(user)

                await msg.delete()

                await ctx.respond(f"The leaderboard has been reset !", ephemeral=True)
            else:
                return await ctx.respond(f"The leaderboard has not been reset !", ephemeral=True)

    @bot.slash_command(
        name="settopg",
        description="Set the TOP_G_OF_THE_MONTH",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def settopg(ctx, top_g_user: Option(str, "The user to set as the TOP G OF THE MONTH", required=True)):

        # remove the @ from the username
        top_g_user = top_g_user[2:-1]

        # get user id from username
        username = bot.get_user(int(top_g_user)).name

        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.respond(
                f"Are you sure you want to set {username} as the TOP_G_OF_THE_MONTH ? (y/n)", ephemeral=True
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for("message", check=check, timeout=60)

            if msg.content == "y":
                setTheTopG(ctx, top_g_user)

                await msg.delete()

                await ctx.respond(f"{username} is now the TOP_G_OF_THE_MONTH !", ephemeral=True)
            else:

                await msg.delete()

                return await ctx.respond(f"{username} is not the TOP_G_OF_THE_MONTH !", ephemeral=True)

            # clear the last message sent by the user
            await ctx.channel.purge(limit=1, check=lambda m: m.author == ctx.author)


    # Remove points from a user
    @bot.slash_command(
        name="remove_points",
        description="Remove points from a user",
        guild_ids=testing_servers,
    )
    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def remove_points(
        ctx,
        remove_user_points: Option(str, "The user to remove points from", required=True),
        remove_pushups: Option(int, "The number of push-ups to remove", required=False, default=0),
        remove_pullups: Option(int, "The number of pull-ups to remove", required=False, default=0),
        remove_squats: Option(int, "The number of squats to remove", required=False, default=0),
        remove_jumping_jacks: Option(int, "The number of jumping jacks to remove", required=False, default=0),
        remove_burpees: Option(int, "The number of burpees to remove", required=False, default=0),
        remove_situps: Option(int, "The number of sit-ups to remove", required=False, default=0),
    ):
        if ctx.channel.id == int(CHANNEL):
            if remove_user_points == "":
                await ctx.respond(f"You must specify a user !", ephemeral=True)
                return

            # get user id from username
            def getUserID(username):
                for member in ctx.guild.members:
                    if member.name == username:
                        return member.id

            user_id = getUserID(remove_user_points)
                

            if remove_pushups <= 0:
                remove_pushups = 0

            elif remove_pullups <= 0:
                remove_pullups = 0

            elif remove_squats <= 0:
                remove_squats = 0

            elif remove_jumping_jacks <= 0:
                remove_jumping_jacks = 0

            elif remove_burpees <= 0:
                remove_burpees = 0

            elif remove_situps <= 0:
                remove_situps = 0


            # Prompt the user to confirm the reset
            await ctx.respond(
                f"Are you sure you want to remove {remove_pushups} push-ups, {remove_pullups} pull-ups, {remove_squats} squats, {remove_jumping_jacks} jumping jacks, {remove_burpees} burpees and {remove_situps} situps from {remove_user_points} ? (y/n)", ephemeral=True
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for("message", check=check)
            if msg.content == "y":
                leaderboard = getLeaderboard()
                # Check if the user has points
                if remove_user_points in leaderboard:
                    # Check if the user has enough points to remove
                    if (
                        leaderboard[remove_user_points]["pushups"] >= remove_pushups
                        and leaderboard[remove_user_points]["pullups"] >= remove_pullups
                        and leaderboard[remove_user_points]["squats"] >= remove_squats
                        and leaderboard[remove_user_points]["jumping_jacks"] >= remove_jumping_jacks
                        and leaderboard[remove_user_points]["burpees"] >= remove_burpees
                        and leaderboard[remove_user_points]["situps"] >= remove_situps
                    ):
                        updateLeaderboard(
                            remove_user_points, "pushups", -remove_pushups, user_id
                        )
                        updateLeaderboard(
                            remove_user_points, "pullups", -remove_pullups, user_id
                        )
                        updateLeaderboard(
                            remove_user_points, "squats", -remove_squats, user_id
                        )
                        updateLeaderboard(
                            remove_user_points, "jumping_jacks", -remove_jumping_jacks, user_id
                        )
                        updateLeaderboard(
                            remove_user_points, "burpees", -remove_burpees, user_id
                        )
                        updateLeaderboard(
                            remove_user_points, "situps", -remove_situps, user_id
                        )

                        await msg.delete()
                    else:
                        await msg.delete()
                        return await ctx.respond(
                            f"{remove_user_points} does not have enough points to remove {remove_pushups} push-ups, {remove_pullups} pull-ups, {remove_squats} squats, {remove_jumping_jacks} jumping jacks, {remove_burpees} burpees and {remove_situps} situps !", ephemeral=True
                        )
            else:
                return await ctx.respond(
                    f"No points have been removed from {remove_user_points}'s score !"
                )
                
    bot.run(TOKEN)