# 카카오톡 봇 애플리케이션 기능정의서

> 최초작성일: 2025-09-02  
> 최신개정일: 2025-09-03
> 최신개정자: [윤영우 ECE](mailto:dan.yun0821@gmail.com)
> 작성자: [윤영우 ECE](mailto:dan.yun0821@gmail.com)

# Global Conventions

## Standard Response Schema

```json
{
    "status": "success" | "error",
    "data": { ... } | null,
    "error": {
        "type": "string",
        "message": "string",
        "params": { ... } | null
    } | null
}
```

- JSON 형식으로 반환
- 성공/오류 여부 를 `status`로 반환
- 성공 시, 반환할 데이터가 있는 경우 `data`로 반환
- 오류 시, 오류의 type과 message를 반환, 필요 시 오류와 관련된 데이터를 `params`로 반환

--- 

## Error Object Reference

| Error Type   | Description   | Return Params | Params Example |
|-----------|--------|-------------|----------|
| `InvalidInput`  | 주어진 input param 이 적절하지 않음 | 부적절한 input param을 그대로 JSON 형태로 반환 | `{"chat_name": ""}` |
| `NotFound` | 주어진 input 이 존재하지 않음 | 부적절한 input param을 그대로 JSON 형태로 반환 | `{"friend_name": ""}` |
| `TooLong` | 주어진 input 이 너무 긺 | 부적절한 input param을 slice해서 JSON 형태로 반환 | `{"message": ""}` |


# 기능 함수(functions)

## 일반 채팅방 관련 기능(regularchat)

- 일반 채팅방(regular chat)을 다루는 기능

---

## Create Regular Chat (일반채팅방 만들기)

### `create_regular_chat(chat_name: str, friend_list: list[str]) -> JSON`

**Purpose:**
주어진 친구리스트에 속한 유저들이 포함된 일반채팅방 생성

**Parameters:**

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 형성할 채팅방의 이름 | Yes | 없음 |
| `friend_list`  | `list[str]` | 포함될 친구 유저의 리스트 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_list is empty, contains only one element, or invalid | `{"friend_list": []}` | |
| `InvalidInput`  | Some friends in the friend_list are invalid or not found | `{"invalid_friend_list": []}` | 부적절한 friend 만 반환 |

---

## Invite Friend to Regular Chat (일반채팅방에 친구 초대하기)

### `invite_to_regular_chat(chat_name: str, friend_name: str) -> JSON`

**Purpose:**  
주어진 채팅방에 친구를 초대

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 초대할 채팅방명 | Yes | 없음 |
| `friend_name`  | `str` | 초대할 친구 유저 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |
| `NotFound`  | friend with friend_name is not found | `{"friend_name": ""}` | |

---

## Send Message to Regular Chat (일반채팅방에 특정 메세지를 작성)

### `send_to_regular_chat(chat_name: str, message: str) -> JSON`

**Purpose:**  
주어진 채팅방에 메시지를 전송

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 메시지를 보낼 채팅방명 | Yes | 없음 |
| `message`  | `str` | 보낼 메시지 내용 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter message is empty or invalid | `{"message": ""}` | |
| `TooLong`  | Parameter message exceeds the length limit | `{"message": ""}` | 메시지의 최대 길이 이하로 잘라서 반환 |

---

## Check for Friend in Regular Chat (일반채팅방에 특정인이 있는지 확인하기)

### `check_friend_in_regular_chat(chat_name: str, friend_name: str) -> JSON`

**Purpose:**  
주어진 채팅방에 메시지를 전송

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 확인할 채팅방명 | Yes | 없음 |
| `friend_name`  | `str` | 확인할 친구명 | Yes | 없음 |

**Return Data:**
```json
{
    "is_exist": true | false
}
```

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |
| `NotFound`  | Friend with friend_name is not found | `{"friend_name": ""}` | |

---

## 팀 채팅방 관련 기능(teamchat)

- 팀 채팅방(team chat)을 다루는 기능
- 위의 일반 채팅방 기능과 동일함

---

## Create Team Chat (팀채팅방 만들기)

### `create_team_chat(chat_name: str, friend_list: list[str]) -> JSON`

**Purpose:**
주어진 친구리스트에 속한 유저들이 포함된 팀채팅방 생성

**Parameters:**

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 형성할 채팅방의 이름 | Yes | 없음 |
| `friend_list`  | `list[str]` | 포함될 친구 유저의 리스트 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_list is empty, contains only one element, or invalid | `{"friend_list": []}` | |
| `InvalidInput`  | Some friends in the friend_list are invalid or not found | `{"invalid_friend_list": []}` | 부적절한 friend 만 반환 |

---

## Invite Friend to Team Chat (팀채팅방에 친구 초대하기)

### `invite_to_team_chat(chat_name: str, friend_name: str) -> JSON`

**Purpose:**  
주어진 채팅방에 친구를 초대

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 초대할 채팅방명 | Yes | 없음 |
| `friend_name`  | `str` | 초대할 친구 유저 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |
| `NotFound`  | friend with friend_name is not found | `{"friend_name": ""}` | |

---

## Send Message to Team Chat (팀채팅방에 특정 메세지를 작성)

### `send_to_team_chat(chat_name: str, message: str) -> JSON`

**Purpose:**  
주어진 채팅방에 메시지를 전송

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 메시지를 보낼 채팅방명 | Yes | 없음 |
| `message`  | `str` | 보낼 메시지 내용 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter message is empty or invalid | `{"message": ""}` | |
| `TooLong`  | Parameter message exceeds the length limit | `{"message": ""}` | 메시지의 최대 길이 이하로 잘라서 반환 |

---

## Check for Friend in Team Chat (팀채팅방에 특정인이 있는지 확인하기)

### `check_friend_in_team_chat(chat_name: str, friend_name: str) -> JSON`

**Purpose:**  
주어진 채팅방에 메시지를 전송

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `chat_name`  | `str` | 확인할 채팅방명 | Yes | 없음 |
| `friend_name`  | `str` | 확인할 친구명 | Yes | 없음 |

**Return Data:**
```json
{
    "is_exist": true | false
}
```

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter chat_name is empty or invalid | `{"chat_name": ""}` | |
| `NotFound`  | Chat with chat_name is not found | `{"chat_name": ""}` | |
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |
| `NotFound`  | Friend with friend_name is not found | `{"friend_name": ""}` | |

---


## 친구 관련 기능(friend)

- 카카오톡 친구의 추가, 조회 등을 다루는 기능

---

## Add Friend (친구 추가하기)

### `add_friend(phone_number: str, friend_name: str) -> JSON`

**Purpose:**  
주어진 전화번호로 조회한 유저를 주어진 친구명으로 지정해서 친구 추가

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `phone_number`  | `str` | 추가할 유저의 전화번호, `01011111111`의 형식 | Yes | 없음 |
| `friend_name`  | `str` | 지정할 친구명 | Yes | 없음 |

**Return Data:**
null

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter phone_number has invalid format | `{"phone_number": "010111122"}` | |
| `NotFound`  | User with given phone_number is not found | `{"phone_numebr": "01011111111"}` | |
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |

---

## Check for User in Friend (현재 친구 중에 특정인이 있는지 확인하기)

### `check_friend(friend_name: str) -> JSON`

**Purpose:**  
주어진 친구명으로 등록된 친구가 있는지 확인

**Parameters:**  

| Name      | Type   | Description | Required | Default |
|-----------|--------|-------------|----------|---------|
| `friend_name`  | `str` | 확인할 친구명 | Yes | 없음 |

**Return Data:**
```json
{
    "is_exist": true | false
}
```

**Possible Errors:**

| Type      | Message | Example Params | Description |
|-----------|--------|-------------|------------|
| `InvalidInput`  | Parameter friend_name is invalid | `{"friend_name": ""}` | |

---
