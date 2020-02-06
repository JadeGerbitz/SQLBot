import discord
from discord.ext import commands
import os
import sqlite3
from sqlite3 import Error

class SQLCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SQL cog loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            print("Failed: Command not found")
            print("------------------------------------------------------")
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("An argument is missing")
            print("Failed: An argument is missing")
            print("------------------------------------------------------")

    @commands.command()
    async def ListDBs(self, ctx):
        """Returns a list of all DBs"""
        print("Command: List DBs in system")
        DBlist = "DBs in the system: "
        num = 0
        for filename in os.listdir("./Cogs/DBs"):
            if filename.endswith(".db"):
                DBlist += filename + "   "
                num += 1
        if(num == 0):
            await ctx.send("There are no DBs in the system")
            print("Succeded: No DBs present")
        else:
            await ctx.send(DBlist)
            print("Succeded: Returned list of DBs")

    @commands.command()
    async def CreateDB(self, ctx, *, DBName:str):
        """Creates a DB with the given name"""
        print("Command: CreateDB")
        if(DBName == ""):
            await ctx.send("A name is required")
            print("Failed: Cannot create a nameless DB")
            return
        found = False
        for filename in os.listdir("./Cogs/DBs"):
            if(filename == DBName + ".db"):
                await ctx.send("This DB already exists")
                print("Failed: DB already exists")
                found = True
        if(found == False):
            try:
                connection = sqlite3.connect("./Cogs/DBs/" + DBName + ".db")
                await ctx.send("DB: " + DBName + " has been created")
                print("Succeded: DB has been created")
            except Error as e:
                print(e)

    @commands.command()
    async def DeleteDB(self, ctx, *, DBName:str):
        """Deletes a DB with the given name"""
        print("Command: DeleteDB")
        found = False
        for filename in os.listdir("./Cogs/DBs"):
            if(filename == DBName + ".db"):
                os.remove("./Cogs/DBs/" + DBName + ".db")
                found = True
        if(found == True):
            await ctx.send("DB found and deleted")
            print("Succeded: DB found and deleted")
        else:
            await ctx.send("DB not found")
            print("Failed: DB could not be found")

    @commands.command()
    async def ProcessCommand(self, ctx, DBName:str, * , Command:str):
        """Processes a given command on the provided DB {DBName, Command}"""
        print("Command: ProcessCommand")
        print(Command)
        found = False
        for filename in os.listdir("./Cogs/DBs"):
            if(filename == DBName + ".db"):
                found = True
        if(found == False):
            await ctx.send("DB not found")
            print("Failed: DB could not be found")
        else:
            try:
                connection = sqlite3.connect("./Cogs/DBs/" + DBName + ".db")
                cursor = connection.cursor()
                cursor.execute(Command)
                connection.commit()
                await ctx.send("Command has completed successfully")
                print("Succeded: Command parsed successfully")
            except Error as e:
                await ctx.send(str(e))
                print("Failed: " + str(e))

    @commands.command()
    async def QueryDatabase(self, ctx, DBName:str, *, Query:str):
        """Performs a given query on the provided DB {DBName, Query}"""
        print("Command: QueryDatabase")
        print(Query)
        found = False
        for filename in os.listdir("./Cogs/DBs"):
            if(filename == DBName + ".db"):
                found = True
        if(found == False):
            await ctx.send("DB not found")
            print("Failed: DB could not be found")
        else:
            try:
                connection = sqlite3.connect("./Cogs/DBs/" + DBName + ".db")
                cursor = connection.cursor()
                cursor.execute(Query)
                list = cursor.fetchall()
                print(list)
                listF = "Query results: "
                for i in list:
                    listF += str(i) + "   "
                await ctx.send(listF)
                print("Succeded: Query parsed successfully")
            except Error as e:
                await ctx.send(str(e))
                print("Failed: " + str(e))

def setup(bot):
    bot.add_cog(SQLCog(bot))
