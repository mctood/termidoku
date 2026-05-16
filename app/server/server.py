import asyncio
import os

import asyncssh

from app.render.handler import handle


class SSHServer(asyncssh.SSHServer):
    def begin_auth(self, username):
        return False


async def start():
    host = os.getenv("SSH_HOST", "0.0.0.0")
    port = int(os.getenv("SSH_PORT", "2222"))
    host_key_path = os.getenv("SSH_HOST_KEY_PATH", "ssh_host_key")

    await asyncssh.create_server(
        SSHServer,
        host,
        port,
        server_host_keys=[host_key_path],
        process_factory=handle,
    )
    print(f"Server running on {host}:{port}")
    await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass
