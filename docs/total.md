# total

## AQMP Request Format (JSON)

### 시그 생성(id[], name) (채널 생성, 특정인들 역할 생성)

#### Main -> Bot

```json
{
  "action_code": 4001,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "sig_name": "sig_name",
    "id_list": ["id1", ]
  }
}
```


### 시그 아카이브(name) (채널 이동)

#### Main -> Bot

```json
{
  "action_code": 4002,
  "correlation_id": "asdf",
  "reply_to": "main_response_queue",
  "body": {
    "sig_name": "sig_name",
  }
}
```