# general

## AQMP Request Format (JSON)

### 초대 코드 생성

#### Main -> Bot

```json
{
  "action_code": 1001,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
}
```

#### Bot -> Main

```json
{
    "correlation_id": "asdf",
    "result": {
        "invite_code": "asdfasdf",
    },
}
```

### 문자열을 특정 채널(id)에 전송

#### Main -> Bot

```json
{
  "action_code": 1002,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "string": "message",
  }
}
```

### 채널 name으로 id 검색

#### Main -> Bot

```json
{
  "action_code": 1001,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
}
```

#### Bot -> Main

```json
{
    "correlation_id": "asdf",
    "result": {
        "invite_code": "asdfasdf",
    },
}
```

