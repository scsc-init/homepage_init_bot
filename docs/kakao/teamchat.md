# teamchat

## AMQP Request Format (JSON)

### 팀채팅방 만들기

#### Main -> Bot

```json
{
  "action_code": 102001,
  "body": {
    "chat_name": "chat_name",
    "friend_list": ["a", "b", "c"]
  }
}
```

### 팀채팅방에 친구 초대하기

#### Main -> Bot

```json
{
  "action_code": 102002,
  "body": {
    "chat_name": "chat_name",
    "friend_name": "a"
  }
}
```

### 팀채팅방에 특정 메세지를 작성

#### Main -> Bot

```json
{
  "action_code": 102003,
  "body": {
    "chat_name": "chat_name",
    "message": "message content"
  }
}
```

### 팀채팅방에 특정인이 있는지 확인하기

#### Main -> Bot

```json
{
  "action_code": 102004,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "chat_name": "chat_name",
    "friend_name": "a"
  }
}
```

#### Bot -> Main

```json
{
    "correlation_id": "asdf",
    "result": {
        "is_exist": true
    },
}
```

