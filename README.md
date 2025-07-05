# homepage_init_bot

> 최신 개정일: 2025.7.5

## AQMP Request Format (JSON)

check `/docs`

## .env 파일 형식

.env 파일은 반드시 root에 위치해야 하며 아래 형식으로 작성합니다. 

```env
RABBITMQ_HOST="rabbitmq"
DISCORD_RECEIVE_QUEUE="discord_bot_queue"
TOKEN="..."
COMMAND_PREFIX="!"
```

| Key Name             | Description                                                      |
|----------------------|------------------------------------------------------------------|
| `RABBITMQ_HOST`          | RabbitMQ가 돌아가는 호스트명. docker의 경우 container 이름과 동일. 메인 BE의 환경 변수명과 동일해야 함. |
| `DISCORD_RECEIVE_QUEUE`  | 메인 서버에서 요청을 받는 큐의 명칭. 메인 BE의 환경 변수명과 동일해야 함. |
| `TOKEN`                  | 디스코드 봇의 토큰. 디스코드 개발자 사이트 참고. |
| `COMMAND_PREFIX`         | 봇의 커맨드 호출자. 현재는 slashcommand로 구현되어 있으므로 불필요. |

## Developer Dependencies

`environment.yml`에서 conda로 환경 설치.

## How to Run

### 초기 봇 데이터 설정(data.json)과 Discord 내부 시스템

봇 구동을 위한 주요 데이터는 `src/bot/discord/data/data.json`에 저장됩니다.

`data_example.json`에 각 내용을 채운 후 파일명을 `data.json`으로 바꿔주세요.

Discord의 object ID는 18여 자리의 정수입니다.  
설정 - 앱 설정 - 고급에서 개발자 모드를 on으로 설정하고 각 object(유저, 역할, ...)을 오른쪽 클릭하면 ID를 복사할 수 있습니다.  
카테고리에도 각각의 ID가 존재합니다. 

Discord 봇 생성에 관해서는, [discord.py 공식 문서](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro)를 참고하세요.

### 실행
In root directory,

```bash
docker-compose up --build
```

For the whole MSA, check main repo.

### 실행 후 로그

```
start() called with token='...'
Logged in as Tester2(...)
```
