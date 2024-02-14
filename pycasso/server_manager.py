import asyncio
from aiohttp import web
from websockets import serve
import webbrowser
import threading
import os
from websockets.server import WebSocketServerProtocol


class ServerManager:
    def __init__(
        self,
        http_port=3000,
        ws_port=3001,
        open_browser=True,
        initial_instructions: str = None,
    ):
        self.http_port = http_port
        self.ws_port = ws_port
        self.open_browser = open_browser
        self.websockets: set[WebSocketServerProtocol] = set()
        # Event loop to the servers and websocket messsaging
        self.loop = None
        self.initial_instructions = initial_instructions

    def broadcast(self, message):
        """Broadcast a message to all connected WebSocket clients."""

        for ws in self.websockets:
            if not ws.closed:
                asyncio.run_coroutine_threadsafe(ws.send(message), self.loop)

    async def websocket_handler(self, websocket: WebSocketServerProtocol, path: str):
        self.websockets.add(websocket)
        # Send initial instructions to set up the canvas
        asyncio.run_coroutine_threadsafe(
            websocket.send(self.initial_instructions), self.loop
        )

        try:
            async for message in websocket:
                await websocket.send(message)
        finally:
            self.websockets.remove(websocket)

    async def start_websocket_server(self):
        server = await serve(self.websocket_handler, "localhost", self.ws_port)
        return server

    async def serve_html(self, request: web.Request):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(script_dir, "index.html")
        return web.FileResponse(html_path)

    async def start_http_server(self):
        app = web.Application()
        app.router.add_get("/", self.serve_html)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.http_port)
        await site.start()
        return site

    def run(self):
        """Run the servers in a new thread and open the browser."""

        def start_loop():
            loop = asyncio.new_event_loop()
            self.loop = loop  # Store the loop in the instance variable
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.start_servers())
            if self.open_browser:
                webbrowser.open(f"http://localhost:{self.http_port}")
            loop.run_forever()

        threading.Thread(target=start_loop, daemon=True).start()

    async def start_servers(self):
        # Start both servers
        await asyncio.gather(
            self.start_http_server(),
            self.start_websocket_server(),
        )
