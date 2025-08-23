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

### 피그 카테고리 갱신

#### Main -> Bot

```json
{
  "action_code": 3003,
  "body": {
    "category_name": "category_name"
  }
}
```

### 피그 아카이브 카테고리 갱신

#### Main -> Bot

```json
{
  "action_code": 3004,
  "body": {
    "category_name": "category_name"
  }
}
```


### 카테고리 조회 (name-id)

#### Main -> Bot

```json
{
  "action_code": 3005,
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


### 채널 생성 (카테고리 id, 채널 name, 채널 topic)

#### Main -> Bot

* `topic`은 optional입니다.
```json
{
  "action_code": 3006,
  "body": {
    "category_id": 12345,
    "channel_name": "name",
    "topic": "topic"
  }
}
```

### 채널 수정 (채널 id, 이동할 카테고리, 새 채널 name, 새 채널 topic)

#### Main -> Bot

* `category_id_to_move`, `new_channel_name`, `new_topic`은 optional입니다.
```json
{
  "action_code": 3007,
  "body": {
    "channel_id": 12345,
    "category_id_to_move": 12345,
    "new_channel_name": "name",
    "new_topic": "topic"
  }
}
```

### 봇 내부 데이터 업데이트

#### Main -> Bot

```json
{
  "action_code": 3008,
  "body": {
    "data": {"previousSemester": "2025-1"}
  }
}
```
