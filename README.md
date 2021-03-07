# Discord.py bot template
TODO: Write a README

```
python -m venv venv
source venv/bin/activate
python main.py
```
Or with Docker:
```
docker-compose up -d
```
After changing the code:
```
docker-compose up -d --build
```
Or mount the code as a volume so you can use the `reload` command (only allows to reload cogs). docker-compose:
```
services:
  bot:
    build: .
    volumes:
      - ./:/app
    env_file:
      - ./.env
```
