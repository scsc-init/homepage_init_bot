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
        "invite_url": "asdfasdf",
    },
}
```

### 문자열을 특정 채널(id | name)에 전송

#### Main -> Bot

```json
{
  "action_code": 1002,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "id": "asdfasdf" | "name": "sig",
    "content": "message",
    "embed": {
      "title": "Hello!",
      "description": "This is a message.",
      "color": 65280,
      "fields": [
        {
          "name": "Field 1",
          "value": "Value 1",
          "inline": false
        }
      ]
    }
  }
}
```

