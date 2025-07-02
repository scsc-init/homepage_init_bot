# homepage_init_bot

| 최신 개정일: 2025.7.3

## features & action code

### general (1000)

|feature(기능)|action code|
|:-----------:|:---------:|
| 초대 코드 생성 | 1001 |
| 문자열을 특정 채널(id)에 전송 | 1002 |
| 문자열을 특정 채널(name)에 전송 | 1003 |
| 채널 name으로 id 검색 | 1004 |

### user (2000)

|feature(기능)|action code|
|:-----------:|:---------:|
| 특정인(id)에게 역할(name) 부여 | 2001 |
| 특정인(id)에게 역할(name) 제거 | 2002 |
| 특정인(name) 으로 특정인(id) 구하기. 반환값 = 리스트 | 2003 |
| 특정인들(id[]) 으로 역할(name) 생성 | 2004 |

### sigpig (3000) - in progress

|feature(기능)|action code|
|:-----------:|:---------:|
| 시그 카테고리 변경(id) | 3001 |
| 아카이브 카테고리 변경(id) | 3002 |
| 카테고리 조회 (name-id) | 3003 |
| 채널 생성 (카테고리 id, 채널 name) | 3005 |
| 채널 이동 (채널 id, 이동할 카테고리, 이동 후 채널 이름) | 3006 |

### total (4000) - in progress

|feature(기능)|action code|
|:-----------:|:---------:|
| 시그 생성(id[], name) (채널 생성, 특정인들 역할 생성) | 4001 |
| 시그 아카이브(name) (채널 이동) | 4002 |


## AQMP Request Format (JSON)

check `/docs`

## How to Run(Backend MSA)

### File Structure

```
/homepage_init_be_msa
ㄴ/homepage_init_backend (cloned from github)
ㄴ/homepage_init_bot (this repo, also cloned from github)
ㄴ.env
ㄴdocker-compose.yml
```

### `docker-compose.yml` contents

the compose files from each of the repos are combined in the root directory of the MSA

```yaml
services:
  backend:
    build: ./homepage_init_backend
    ports:
      - "8080:8080"
    env_file:
      - ./homepage_init_backend/.env
    volumes:
      - ./homepage_init_backend:/app/
    depends_on:
      - rabbitmq
    entrypoint: bash
    command: >
      -c '
      echo "Checking DB at /app/${SQLITE_FILENAME}";

      if [ ! -f "/app/${SQLITE_FILENAME}" ]; then
        echo "Database was not found. Initializing...";
        mkdir -p /app/db
        chmod +x ./script/*.sh &&
        ./script/init_db.sh "/app/${SQLITE_FILENAME}" &&
        ./script/insert_scsc_global_status.sh "/app/${SQLITE_FILENAME}" &&
        ./script/insert_user_roles.sh "/app/${SQLITE_FILENAME}" &&
        ./script/insert_majors.sh "/app/${SQLITE_FILENAME}" ./docs/majors.csv &&
        ./script/insert_boards.sh "/app/${SQLITE_FILENAME}" &&
        ./script/insert_sample_users.sh "/app/${SQLITE_FILENAME}" &&
        ./script/insert_sample_articles.sh "/app/${SQLITE_FILENAME}";
      else
        echo "Database already exists. Skipping initialization.";
      fi;

      exec fastapi run main.py --host 0.0.0.0 --port 8080
      '
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
      - "5672:5672"
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  bot:
    build: ./homepage_init_bot
    env_file:
      - ./homepage_init_bot/.env
    volumes:
      - ./homepage_init_bot:/app/
    depends_on:
      rabbitmq:
        condition: service_healthy
```

### `.env` contents

#### `./.env`

```
SQLITE_FILENAME="db/YOUR_DB_FILENAME.db"
```

#### `./homepage_init_backend/.env`

same as original repo

#### `./homepage_init_bot/.env`

```
RABBITMQ_HOST="rabbitmq"
TOKEN="YOUR_BOT_TOKEN"
COMMAND_PREFIX="!"
```

### Running

In the root directory,

```bash
docker-compose up --build
```