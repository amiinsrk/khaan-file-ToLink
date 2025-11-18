from aiohttp import web

async def health(request):
    return web.Response(text="OK")

async def web_server():
    app = web.Application()
    app.router.add_get("/", health)  # Health check for Koyeb
    return app
