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

async def addEntry(userID,message: Message,channelID):
    async with connect() as (conn, cur):
            await cur.execute(f"INSERT INTO conversation_history (timestamp, user, ctx, message) VALUES (CURRENT_TIMESTAMP(), '{userID}', '{channelID}', '{message}')")

async def getPrev(userID,channelID):
    async with connect() as (conn, cur):
        sql = f"SELECT message FROM conversation_history WHERE user = {userID} AND ctx = {channelID} ORDER BY timestamp ASC"
        await cur.execute(sql)
        conversation = " ".join([row[0] for row in await cur.fetchall()])
        return conversation

# async def main():
#     await addEntry('a','12')
# asyncio.run(main())