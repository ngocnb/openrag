"""Development entry point with hot reload support."""

from src.main import create_app


class LazyApp:
    """Lazily initializes the ASGI app on first request to avoid
    calling asyncio.run() at module import time (which fails when
    uvicorn's reloader imports the module inside a running event loop)."""

    def __init__(self):
        self._app = None

    async def __call__(self, scope, receive, send):
        if self._app is None:
            self._app = await create_app()
        await self._app(scope, receive, send)


app = LazyApp()
