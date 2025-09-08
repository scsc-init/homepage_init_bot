# friend

## AMQP Request Format (JSON)

### 친구 추가하기

#### Main -> Bot

```json
{
  "action_code": 103001,
  "body": {
    "phone_number": "01011112222",
    "friend_name": "a"
  }
}
```

### 친구 중에 특정인이 있는지 확인하기

#### Main -> Bot

```json
{
  "action_code": 103002,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
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

