# sigpig

## AQMP Request Format (JSON)

### 카테고리 생성

#### Main -> Bot

```json
{
  "action_code": 3001,
  "body": {
    "name": "category_name"
  }
}
```

### 카테고리 수정(id)

#### Main -> Bot

```json
{
  "action_code": 3002,
  "body": {
    "id": "id",
    "name": "new_category_name"
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
    "name": "category_name",
  }
}
```

#### Bot -> Main

```json
{
    "correlation_id": "asdf",
    "result": {
        "id": "id_category1",
    },
}
```


### 채널 생성 (카테고리 id, 채널 name)

#### Main -> Bot

```json
{
  "action_code": 3004,
  "body": {
    "category_id": "id",
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
    "channel_id": "id1",
    "category_to_id": "id2",
    "new_channel_name": "name",
  }
}
```

