# user

## AQMP Request Format (JSON)

### 특정인(id)에게 역할(name) 부여

#### Main -> Bot

```json
{
  "action_code": 2001,
  "body": {
    "user_id": "userid",
    "role_name": "role_name", 
  }
}
```

### 특정인(id)에게 역할(name) 제거

#### Main -> Bot

```json
{
  "action_code": 2002,
  "body": {
    "user_id": "userid",
    "role_name": "role_name", 
  }
}
```

### 특정인(name) 으로 특정인(id) 구하기. 반환값 = 리스트

#### Main -> Bot

```json
{
  "action_code": 2003,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "name": "name",
  }
}
```

#### Bot -> Main

```json
{
  "correlation_id": "asdf",
  "result": {
    "id_list": ["id1", "id2"],
  }
}
```

### 특정인들(id[]) 으로 역할(name) 생성

#### Main -> Bot

```json
{
  "action_code": 2004,
  "body": {
    "id_list": ["id1", "id2"],
    "role_name": "role_name",
  }
}
```


