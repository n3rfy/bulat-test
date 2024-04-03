import asyncio
import signal
from collections.abc import Sequence
from concurrent.futures import Executor
from typing import Any

import grpc


class GRPCServer(grpc.aio._server.Server):
    def __init__(
            self,
            host: str,
            port: str,
            migration_thread_pool: Executor | None = None,
            handlers: Sequence[grpc.GenericRpcHandler] | None = None,
            interceptors: Sequence[Any] | None = None,
            options: grpc.aio.ChannelArgumentType | None = None,
            maximum_concurrent_rpcs: int | None = None,
            compression: grpc.Compression | None = None,
    ):
        loop = asyncio.get_event_loop()
        for signal_name in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(
                getattr(signal, signal_name),
                lambda: asyncio.ensure_future(self._graceful_shutdown()),
            )

        super().__init__(
            migration_thread_pool,
            () if handlers is None else handlers,
            () if interceptors is None else interceptors,
            () if options is None else options,
            maximum_concurrent_rpcs,
            compression,
        )

        self._host = host
        self._port = port
        self._context = {}

    def on_startup(self, context: dict) -> None:
        pass

    async def start(self):
        self.on_startup(self._context)
        super().add_insecure_port(f'{self._host}:{self._port}')
        await super().start()

    def on_shutdown(self, context: dict) -> None:
        pass

    async def _graceful_shutdown(self, *_):
        self.on_shutdown(self._context)
        await self.stop(10)
