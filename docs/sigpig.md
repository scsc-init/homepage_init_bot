# sigpig

## AQMP Request Format (JSON)

### 시그 카테고리 갱신

#### Main -> Bot

```json
{
  "action_code": 3001,
  "body": {
    "category_name": "category_name"
  }
}
```

### 시그 아카이브 카테고리 갱신

#### Main -> Bot

```json
{
  "action_code": 3002,
  "body": {
    "category_name": "category_name"
  }
}
```


### 카테고리 조회 (name-id)

#### Main -> Bot

```json
{
  "action_code": 3003,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "category_name": "category_name",
  }
}
```

#### Bot -> Main

```json
{
    "correlation_id": "asdf",
    "result": {
        "category_id": 12345,
    },
}
```


### 채널 생성 (카테고리 id, 채널 name)

#### Main -> Bot

```json
{
  "action_code": 3004,
  "body": {
    "category_id": 12345,
    "channel_name": "name",
  }
}
```

### 채널 이동 (채널 id, 이동할 카테고리, 이동 후 채널 이름)

#### Main -> Bot

```json
{
  "action_code": 3005,
  "body": {
    "channel_id": 12345,
    "category_to_id": 12345,
    "new_channel_name": "name",
  }
}
```

