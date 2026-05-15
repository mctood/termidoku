import asyncio
import asyncssh

from app.render.handler import handle


class SSHServer(asyncssh.SSHServer):
    def begin_auth(self, username):
        # Разрешаем вход без пароля для любых пользователей
        return False


async def start():
    # Создаем сервер. Важно: для интерактивного ввода клиент должен запросить PTY
    # (обычный ssh-клиент делает это автоматически).
    await asyncssh.create_server(
        SSHServer,
        "",
        2222,
        server_host_keys=["ssh_host_key"],  # Убедитесь, что файл ключа существует
        process_factory=handle,
    )
    print("Сервер запущен на порту 2222")
    await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        pass