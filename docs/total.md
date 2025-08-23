# total

## AQMP Request Format (JSON)

### 시그 생성(id[], name, description=None) (채널 생성, 특정인들 역할 생성)

#### Main -> Bot

* `sig_description`은 optional입니다.
```json
{
  "action_code": 4001,
  "body": {
    "sig_name": "sig_name",
    "user_id_list": [12345, 12346],
    "sig_description": "sig_description"
  }
}
```


### 시그 아카이브(name) (채널 이동)

#### Main -> Bot

```json
{
  "action_code": 4002,
  "body": {
    "sig_name": "sig_name",
    "previous_semester": "2025-1"
  }
}
```

### 피그 생성(id[], name, description=None) (채널 생성, 특정인들 역할 생성)

#### Main -> Bot

```json
{
  "action_code": 4003,
  "body": {
    "pig_name": "pig_name",
    "user_id_list": [12345, 12346],
    "pig_description": "pig_description"
  }
}
```


### 피그 아카이브(name) (채널 이동)

#### Main -> Bot

```json
{
  "action_code": 4004,
  "body": {
    "pig_name": "pig_name",
    "previous_semester": "2025-1"
  }
}
```

### 시그 수정(name) (이름, 채널명, topic)

#### Main -> Bot

```json
{
  "action_code": 4005,
  "body": {
    "sig_name": "sig_name",
    "new_sig_name": "new_sig_name",
    "new_topic": "new_topic"
  }
}
```

### 피그 수정(name) (이름, 채널명, topic)

#### Main -> Bot

```json
{
  "action_code": 4006,
  "body": {
    "pig_name": "pig_name",
    "new_pig_name": "new_pig_name",
    "new_topic": "new_topic"
  }
}
```
