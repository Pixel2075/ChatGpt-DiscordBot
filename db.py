import aiomysql
import asyncio
import contextlib
from discord import Message

@contextlib.asynccontextmanager
async def connect():
    conn = await aiomysql.connect(
        host="localhost",
        user="Pixel",
        password="Dolla$ign",
        db="test",
        autocommit=True
    )
    async with conn.cursor() as cur:
        yield conn, cur
    conn.close()

async def addEntry(userID: str,channelID: str,message: Message,response: str):
    async with connect() as (conn, cur):
            escapedMessage = aiomysql.escape_string(message)
            truncatedMessage = escapedMessage[:255] 
            await cur.execute(f"INSERT INTO conversation_history (timestamp, user, ctx, message,response) VALUES (CURRENT_TIMESTAMP(), '{userID}', '{channelID}', '{message}','{truncatedMessage}')")

async def getPrev(userID: str,channelID: str,userName: str):
    async with connect() as (conn, cur):
        sql = f"SELECT message,response FROM conversation_history WHERE user = {userID} AND ctx = {channelID} ORDER BY timestamp ASC"
        await cur.execute(sql)
        conversation = await cur.fetchall()
        convoDictList = [{'message':convo[0],'response':convo[1]} for convo in conversation]
        convoStr = ""
        for both in convoDictList:
            convoStr += f'{userName}:{both["message"]}\nAI:{both["response"]}\n'
        return convoStr

# async def main():
#     await getPrev('696248940810731541','1061819571146870804','Human')
# asyncio.run(main())