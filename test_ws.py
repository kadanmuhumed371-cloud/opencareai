import asyncio
import websockets
import json

async def test():
    uri = "wss://opencareai-backend.onrender.com/ws?lang=Af-Soomaali"
    print("Connecting to Render...")
    async with websockets.connect(uri) as ws:
        print("✅ Connected successfully!")
        payload = json.dumps({"type": "text", "content": "Hi"})
        await ws.send(payload)
        print("Sent: Hi")
        response = await ws.recv()
        print("Received response:", response)

asyncio.run(test())
