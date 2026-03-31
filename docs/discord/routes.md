# FastAPI Routes

## Login Status

- **Method**: `GET`
- **URL**: `/status`
- **Description**: 로그인된 여부 반환 

- **Response**:
```json
{
  "logged_in": true
}
```
- **Status Codes**:
  - `200 OK`: 반환

---


## Request Login

- **Method**: `POST`
- **URL**: `/login`
- **Description**: Main BE에 로그인하도록 요청


- **Status Codes**:
  - `204 No Content`: 요청 성공
  - `400 Bad Request`: 오류 반환
  
---
