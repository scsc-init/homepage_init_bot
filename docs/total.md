# total

## AQMP Request Format (JSON)

### 시그 생성(id[], name) (채널 생성, 특정인들 역할 생성)

#### Main -> Bot

```json
{
  "action_code": 4001,
  "body": {
    "sig_name": "sig_name",
    "user_id_list": [12345, 12346]
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
  }
}
```

### 피그 생성(id[], name) (채널 생성, 특정인들 역할 생성)

#### Main -> Bot

```json
{
  "action_code": 4003,
  "body": {
    "pig_name": "pig_name",
    "user_id_list": [12345, 12346]
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
  }
}
```
