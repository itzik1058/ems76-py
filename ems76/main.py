import signal
from asyncio import get_event_loop
from ems76.login.server import LoginServer


async def run(loop):
    await LoginServer(('0.0.0.0', 8484)).run(loop)


def main():
    loop = get_event_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
        loop.add_signal_handler(signal.SIGTERM, loop.stop)
    except NotImplementedError:
        pass

    future = loop.create_task(run(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # TODO log
        pass
    finally:
        future.remove_done_callback(lambda _: loop.stop)
        loop.run_until_complete(loop.shutdown_asyncgens())
        # TODO log


if __name__ == '__main__':
    main()
