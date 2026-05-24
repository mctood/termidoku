<h1 align="center"><a href="https://termidoku.xyz">TERMIDOKU</a></h1>

<p align="center">
  <b>Play Sudoku directly in your terminal</b>
</p>

<p align="center">
  <img width=45% src="https://github.com/mctood/termidoku/blob/master/preview/preview.jpg?raw=true" />
  <img width=45% src="https://github.com/mctood/termidoku/blob/master/preview/preview_game.jpg?raw=true" />
</p>


<h1>How to Play</h1>

- open Terminal or Command Prompt;
- enter the command:

```sh
ssh termidoku.xyz
```
- enter `yes` to confirm connection;
- enjoy!

<h1>How to Self-Host</h1>

<h2>Using docker-compose</h2>

- clone the repository:
```sh
git clone https://github.com/mctood/termidoku
cd termidoku
```
- create `.env` file:
```sh
cp .env.example .env
nano .env
```
- fill the parameters except SSH_HOST_KEY_PATH;
- generate the SSH key:
```sh
ssh-keygen -f ssh_host_key -N ""
```
- build & run the application:
```sh
docker compose up --build
```
- connect via SSH and play!

<h2>Using pure Python</h2>

- clone the repository:
```sh
git clone https://github.com/mctood/termidoku
cd termidoku
```
- create & activate virtual environment:
```sh
python -m venv .venv

source .venv/bin/activate
# OR, for fish:
source .venv/bin/activate.fish
```

- install requirements:
```sh
python -m pip install -r requirements.txt
```

- generate the SSH key:
```sh
ssh-keygen -f ssh_host_key -N ""
```
- create `.env` file:
```sh
cp .env.example .env
nano .env
```
- fill the parameters, in SSH_HOST_KEY_PATH specify the absolute path to ssh_host_key file;
- run the application:
```sh
python -m app.server.server
```
- connect via SSH and play!


<h1> Star History (why not?)</h2>

<p align="center">
<picture align="center">
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=mctood/termidoku&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=mctood/termidoku&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=mctood/termidoku&type=Date" />
</picture>
</p>
