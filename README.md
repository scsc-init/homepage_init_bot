# homepage_init_bot

> 최종개정일: 2025-08-15

## 브랜치 설명

- main: 배포된 코드를 저장하며 버전 별로 태그가 붙어 있습니다.
- develop(default): 개발 중인 코드를 저장합니다.

## AQMP Request Format (JSON)

check `/docs`

## .env 파일 형식

.env 파일은 반드시 root에 위치해야 하며 아래 형식으로 작성합니다. 

```env
RABBITMQ_HOST="rabbitmq"
MAIN_BACKEND_HOST="backend"
DISCORD_RECEIVE_QUEUE="discord_bot_queue"
TOKEN="..."
COMMAND_PREFIX="!"
API_SECRET="some-secret-code"
```

| Key Name             | Description                                                      |
|----------------------|------------------------------------------------------------------|
| `RABBITMQ_HOST`          | RabbitMQ가 돌아가는 호스트명. docker의 경우 container 이름과 동일. 메인 BE의 환경 변수명과 동일해야 함. |
| `MAIN_BACKEND_HOST`      | MainBE가 돌아가는 호스트명. docker의 경우 container 이름과 동일. 메인 BE의 환경 변수명과 동일해야 함.  |
| `DISCORD_RECEIVE_QUEUE`  | 메인 서버에서 요청을 받는 큐의 명칭. 메인 BE의 환경 변수명과 동일해야 함. |
| `TOKEN`                  | 디스코드 봇의 토큰. 디스코드 개발자 사이트 참고. |
| `COMMAND_PREFIX`         | 봇의 커맨드 호출자. 현재는 slashcommand로 구현되어 있으므로 불필요. |
| `API_SECRET`             | API 요청 시 검증에 사용되는 비밀 코드. 메인 BE의 환경 변수명과 동일해야 함. |

## `data.json` 파일 형식
`./src/bot/discord/data/data.json`에 디스코드 봇 구동을 위한 SCSC 디스코드 서버에 대한 필수 정보가 담겨 있습니다. 디스코드 봇이 명령에 따라 이 데이터를 업데이트하기도 합니다. 초기 설정 방식은 다음과 같습니다.
```json
{
  "guildID": 0,
  "channelID": 0,
  "adminRoleID": 0,
  "executiveRoleID": 0,
  "sigCategoryID": 0,
  "sigArchiveCategoryID": 0,
  "pigCategoryID": 0,
  "pigArchiveCategoryID": 0,
  "defaultReason": "from SCSCBot",
  "previousSemester": ""
}
```
`data.example.json`의 내용을 수정 후 파일명을 `data.json`으로 바꿔주세요.

| Key Name             | Description                                                      |
|----------------------|------------------------------------------------------------------|
| `guildID`                | 디스코드 서버의 ID |
| `channelID`              | 새로운 사용자가 초대될 디스코드 서버의 메인 채널 ID(SCSC 서버의 경우 `chat`) |
| `adminRoleID`            | 필요 없음. 0으로 고정. |
| `executiveRoleID`        | 필요 없음. 0으로 고정. |
| `sigCategoryID`          | 현재 시점에서 활성화되어 있는 시그 카테고리의 ID. 서버 세팅 후 ID를 복사해서 직접 입력. |
| `sigArchiveCategoryID`   | 바로 직전 학기에 활성화되어 있던 시그 카테고리의 ID. 서버 세팅 후 ID를 복사해서 직접 입력. |
| `pigCategoryID`          | 현재 시점에서 활성화되어 있는 피그 카테고리의 ID. 서버 세팅 후 ID를 복사해서 직접 입력. |
| `pigArchiveCategoryID`   | 바로 직전 학기에 활성화되어 있던 피그 카테고리의 ID. 서버 세팅 후 ID를 복사해서 직접 입력. |
| `defaultReason`          | 필요 없음. ''으로 고정. |
| `previousSemester`       | 직전 학기의 이름(ex. 2025-1, 2025-S). 학기가 바뀐 후 자동 업데이트됨. |

디스코드 UI에서 객체를 우클릭하고 `Copy xxx ID`를 누르면 오브젝트 ID를 얻을 수 있습니다.

## Developer Dependencies

`environment.yml`에서 conda로 환경 설치.

## How to Run

### `logs/`

- 루트에 `logs/` 폴더를 추가합니다

### 디스코드 서버 세팅

Discord 봇 생성에 관해서는, [discord.py 공식 문서](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro)를 참고하세요.

SCSC 디스코드 서버에서 `dormant`, `newcomer`, `member`, `oldboy`, `executive`, `president`와 같은 6가지 role을 각각의 권한에 맞게 추가합니다.
`SIG`, `PIG`라는 이름의 카테고리를 생성(이미 없다면)하고 각각의 ID를 복사하여 `data.json`에 삽입합니다.
SIG Archive, PIG Archive로 사용될 카테고리를 생성(이미 없다면)하고 각각의 ID를 복사하여 `data.json`에 삽입합니다. 카테고리의 이름은 `2025-1 SIG Archive`, `2025-W PIG Archive` 등의 형식으로 하고, case sensitive 입니다.
`previousSemester`에 지난 학기의 명칭을 기입합니다(ex. `"2025-1"`또는 `"2025-S"`).

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
