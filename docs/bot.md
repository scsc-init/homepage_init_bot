## SCSCBotConnector Class Reference

`SCSCBotConnector` 클래스는 Discord 봇과 상호작용하기 위한 주요 인터페이스를 제공합니다. 이 클래스는 Discord API 호출을 캡슐화하고, 데이터 관리, 채널/멤버/역할/카테고리 검색 및 조작, 그리고 SIG/PIG 관련 기능을 지원합니다.

### 주요 개념 및 타입 정의

`SCSCBotConnector`는 여러 메서드에서 다양한 식별자 타입을 사용합니다. 이해를 돕기 위해 사전에 정의된 타입들을 소개합니다.

* **`ChannelIdentifierType`**: Discord 채널을 식별하는 데 사용될 수 있는 타입입니다.
    * `int`: 채널의 고유 ID.
    * `str`: 채널의 이름.
    * `discord.VoiceChannel`, `discord.StageChannel`, `discord.ForumChannel`, `discord.TextChannel`, `discord.CategoryChannel`: Discord.py 라이브러리의 채널 객체.
* **`CategoryIdentifierType`**: Discord 카테고리 채널을 식별하는 데 사용될 수 있는 타입입니다.
    * `int`: 카테고리의 고유 ID.
    * `str`: 카테고리의 이름.
    * `discord.CategoryChannel`: Discord.py 라이브러리의 카테고리 채널 객체.
* **`MemberIdentifierType`**: Discord 멤버를 식별하는 데 사용될 수 있는 타입입니다.
    * `int`: 멤버의 고유 ID.
    * `str`: 멤버의 이름, 닉네임 또는 글로벌 이름.
    * `discord.User`, `discord.Member`: Discord.py 라이브러리의 사용자/멤버 객체.
* **`RoleIdentifierType`**: Discord 역할을 식별하는 데 사용될 수 있는 타입입니다.
    * `int`: 역할의 고유 ID.
    * `str`: 역할의 이름.
    * `discord.Role`: Discord.py 라이브러리의 역할 객체.
* **`NOCHANGE`**: 특정 매개변수의 값을 변경하지 않음을 나타내는 특별한 객체입니다.

### 로깅 데코레이터 (`@log`)

`SCSCBotConnector` 클래스의 대부분의 메서드에는 `@log` 데코레이터가 적용되어 있습니다. 이 데코레이터는 봇이 `debug=True` 모드로 초기화되었을 경우, 해당 메서드가 호출될 때 메서드 이름과 전달된 인자들을 콘솔에 출력하여 디버깅에 도움을 줍니다.

### 메서드 목록

---

#### `__init__(self, bot: Optional[DiscordBot] = None, data_path: Optional[Path] = None, data: Optional[dict] = None, command_prefix: str = "!", debug: bool = False)`

* **설명**: `SCSCBotConnector`의 생성자입니다. Discord 봇과의 상호작용을 위한 연결을 설정하고, 데이터를 로드하며, 봇 인스턴스를 초기화합니다.
* **매개변수**:
    * `bot` (`Optional[DiscordBot]`): 사용할 `DiscordBot` 인스턴스. 제공되지 않으면 새로 생성됩니다.
    * `data_path` (`Optional[Path]`): 봇 데이터 파일 (data.json)의 경로. 기본값은 "data/data.json"입니다.
    * `data` (`Optional[dict]`): 봇 초기화에 사용될 데이터 딕셔너리.
    * `command_prefix` (`str`): 봇의 명령어 접두사. 기본값은 "!"입니다.
    * `debug` (`bool`): 디버그 모드 활성화 여부. `True`인 경우 로깅이 활성화됩니다.

---

#### `update_attributes(self)`

* **설명**: 봇의 주요 길드, 채널, 역할 등의 속성을 업데이트합니다. `self.bot.data`에 설정된 ID를 기반으로 객체를 가져와 할당합니다. 봇이 준비된 후 호출되어야 합니다.

---

#### `bot_on_ready(self)`

* **설명**: 봇이 Discord에 성공적으로 연결되었을 때 호출되는 콜백 함수입니다. 주요 속성들을 업데이트합니다.

---

#### `submit_sync(self, coro: Coroutine) -> Any`

* **설명**: 비동기 코루틴을 동기적으로 실행하고 결과를 반환합니다. 봇의 이벤트 루프에서 코루틴을 안전하게 실행하며 발생할 수 있는 예외를 처리합니다.
* **매개변수**:
    * `coro` (`Coroutine`): 실행할 비동기 코루틴.
* **반환값**:
    * `Any`: 코루틴 실행 결과.
* **예외 발생**:
    * `TypeError`: `coro`가 코루틴이 아닐 경우 발생합니다.
    * `Exception`: 코루틴 실행 중 예외가 발생할 경우 해당 예외를 다시 발생시킵니다.

---

#### `start(self, token)`

* **설명**: Discord 봇을 별도의 이벤트 루프 스레드에서 실행합니다. 이를 통해 GUI와 봇의 비동기 작업이 동시에 원활하게 작동할 수 있습니다.
* **매개변수**:
    * `token` (`str`): Discord 봇 토큰.

---

#### `set_data(self, data: dict)`

* **설명**: 봇의 내부 데이터를 업데이트하고, 변경된 데이터를 JSON 파일에 저장합니다. 데이터를 저장한 후, 관련 봇 속성들을 업데이트합니다.
* **매개변수**:
    * `data` (`dict`): 새로 업데이트할 데이터를 포함하는 딕셔너리.

---

#### `slugify(self, text: str) -> str`

* **설명**: 텍스트를 Discord 채널 이름 format에 맞게 변환합니다.
 
* **매개변수**:
    * `text` (`str`): 변환할 텍스트. 
* **반환값**:
    * `str`: 채널 이름 format에 맞게 변환된 텍스트.

---

#### `get_channel(self, identifier: ChannelIdentifierType, category_identifier: Optional[CategoryIdentifierType] = NOCHANGE) -> None|discord.VoiceChannel|discord.StageChannel|discord.ForumChannel|discord.TextChannel|discord.CategoryChannel`

* **설명**: 제공된 식별자를 사용하여 Discord 채널 객체를 가져옵니다. 식별자는 채널 ID (정수), 채널 이름 (문자열), 또는 기존 채널 객체일 수 있습니다. 카테고리 식별자가 제공되면 해당 카테고리 내에서 채널을 검색합니다.
* **매개변수**:
    * `identifier` (`ChannelIdentifierType`): 채널의 ID, 이름 또는 채널 객체.
    * `category_identifier` (`Optional[CategoryIdentifierType]`): 채널이 속한 카테고리의 ID, 이름 또는 카테고리 객체. 기본값은 `NOCHANGE`로, 카테고리 필터링을 하지 않습니다.
* **반환값**:
    * `None | discord.VoiceChannel | discord.StageChannel | discord.ForumChannel | discord.TextChannel | discord.CategoryChannel`: 찾은 채널 객체 또는 찾지 못한 경우 `None`을 반환합니다.

---

#### `get_category(self, identifier: CategoryIdentifierType) -> None|discord.CategoryChannel`

* **설명**: 제공된 식별자를 사용하여 Discord 카테고리 채널 객체를 가져옵니다. 식별자는 카테고리 ID (정수), 카테고리 이름 (문자열), 또는 기존 카테고리 객체일 수 있습니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): 카테고리의 ID, 이름 또는 카테고리 객체.
* **반환값**:
    * `None | discord.CategoryChannel`: 찾은 카테고리 객체 또는 찾지 못한 경우 `None`을 반환합니다.

---

#### `get_member(self, identifier: MemberIdentifierType) -> None | discord.Member`

* **설명**: 제공된 식별자를 사용하여 Discord 멤버 객체를 가져옵니다. 식별자는 멤버 ID (정수), 멤버 이름/닉네임/글로벌 이름 (문자열), 또는 기존 User/Member 객체일 수 있습니다.
* **매개변수**:
    * `identifier` (`MemberIdentifierType`): 멤버의 ID, 이름, 닉네임 또는 User/Member 객체.
* **반환값**:
    * `None | discord.Member`: 찾은 멤버 객체 또는 찾지 못한 경우 `None`을 반환합니다.

---

#### `get_members(self, identifier: str, exact: bool = False) -> list[Member]`

* **설명**: 주어진 식별자와 일치하는 Discord 멤버 리스트를 가져옵니다. 이름 또는 닉네임을 기준으로 멤버를 검색합니다.
* **매개변수**:
    * `identifier` (`str`): 검색할 멤버의 이름 또는 닉네임.
    * `exact` (`bool`): `True`인 경우 정확히 일치하는 멤버만 반환하고, `False`인 경우 부분적으로 일치하는 멤버도 반환합니다.
* **반환값**:
    * `list[Member]`: 검색 조건에 해당하는 멤버 객체들의 리스트.

---

#### `get_role(self, identifier: RoleIdentifierType) -> None | discord.Role`

* **설명**: 제공된 식별자를 사용하여 Discord 역할 객체를 가져옵니다. 식별자는 역할 ID (정수), 역할 이름 (문자열), 또는 기존 역할 객체일 수 있습니다.
* **매개변수**:
    * `identifier` (`RoleIdentifierType`): 역할의 ID, 이름 또는 역할 객체.
* **반환값**:
    * `None | discord.Role`: 찾은 역할 객체 또는 찾지 못한 경우 `None`을 반환합니다.

---

#### `create_invite(self, identifier: Optional[ChannelIdentifierType] = None, max_age: int = 0, max_uses: int = 0, reason: str = None, unique: bool = True, **kwargs) -> discord.Invite`

* **설명**: 특정 채널에 대한 초대 코드를 생성합니다.
* **매개변수**:
    * `identifier` (`Optional[ChannelIdentifierType]`): 초대 코드를 생성할 채널의 식별자. 기본값은 `self.mainChannel`입니다.
    * `max_age` (`int`): 초대 링크의 유효 기간 (초). `0`은 무한대입니다.
    * `max_uses` (`int`): 초대 링크의 최대 사용 횟수. `0`은 무한대입니다.
    * `reason` (`str`): 감사 로그에 표시될 이유.
    * `unique` (`bool`): `True`인 경우 고유한 초대 링크를 생성합니다.
    * `**kwargs`: `discord.TextChannel.create_invite` 메서드에 전달될 추가 키워드 인자.
* **반환값**:
    * `discord.Invite`: 생성된 초대 객체.

---

#### `send_message(self, identifier: ChannelIdentifierType, content, embed: Optional[discord.Embed] = None, **kwargs)`

* **설명**: 특정 채널에 문자열 메시지를 전송합니다.
* **매개변수**:
    * `identifier` (`ChannelIdentifierType`): 메시지를 전송할 채널의 식별자.
    * `content` (`str`): 전송할 메시지 내용.
    * `embed` (`Optional[discord.Embed]`): 메시지와 함께 전송할 임베드 객체.
    * `**kwargs`: `discord.TextChannel.send` 메서드에 전달될 추가 키워드 인자.

---

#### `create_text_channel(self, name: str, category_identifier: Optional[CategoryIdentifierType] = None, topic: Optional[str] = None, reason: Optional[str] = None) -> discord.TextChannel`

* **설명**: 새로운 텍스트 채널을 생성합니다.
* **매개변수**:
    * `name` (`str`): 생성할 텍스트 채널의 이름.
    * `category_identifier` (`Optional[CategoryIdentifierType]`): 채널이 속할 카테고리의 식별자.
    * `topic` (`Optional[str]`): 채널의 주제.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
* **반환값**:
    * `discord.TextChannel`: 생성된 텍스트 채널 객체.

---

#### `create_category(self, name: str, position: Optional[int] = None, reason: Optional[str] = None) -> discord.CategoryChannel`

* **설명**: 새로운 카테고리 채널을 생성합니다.
* **매개변수**:
    * `name` (`str`): 생성할 카테고리 채널의 이름.
    * `position` (`Optional[int]`): 카테고리의 위치.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
* **반환값**:
    * `discord.CategoryChannel`: 생성된 카테고리 채널 객체.

---

#### `edit_text_channel(self, channel_identifier: int|str|discord.TextChannel, name: Optional[str] = NOCHANGE, category_identifier: Optional[CategoryIdentifierType] = NOCHANGE, topic: Optional[str] = NOCHANGE, position: Optional[int] = NOCHANGE, reason: Optional[str] = None)`
* **설명**: 기존 텍스트 채널의 속성을 편집합니다.
* **매개변수**:
    * `channel_identifier` (`int | str | discord.TextChannel`): 편집할 텍스트 채널의 식별자.
    * `name` (`Optional[str]`): 채널의 새 이름. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `category_identifier` (`Optional[CategoryIdentifierType]`): 채널을 이동시킬 새 카테고리의 식별자. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `topic` (`Optional[str]`): 채널의 새 주제. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `position` (`Optional[int]`): 채널의 새 위치. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `edit_category(self, identifier: CategoryIdentifierType, name: Optional[str] = NOCHANGE, position: Optional[int] = NOCHANGE, reason: Optional[str] = None)`

* **설명**: 기존 카테고리 채널의 속성을 편집합니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): 편집할 카테고리 채널의 식별자.
    * `name` (`Optional[str]`): 카테고리의 새 이름. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `position` (`Optional[int]`): 카테고리의 새 위치. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `create_role(self, name: str, members: Optional[Iterable[MemberIdentifierType]] = None, reason: Optional[str] = None) -> discord.Role`

* **설명**: 새로운 역할을 생성하고, 선택적으로 멤버들에게 해당 역할을 부여합니다.
* **매개변수**:
    * `name` (`str`): 생성할 역할의 이름.
    * `members` (`Optional[Iterable[MemberIdentifierType]]`): 새로 생성된 역할을 부여할 멤버들의 식별자 리스트.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
* **반환값**:
    * `discord.Role`: 생성된 역할 객체.

---

#### `edit_role(self, role_identifier: RoleIdentifierType, name: Optional[str] = None, reason: Optional[str] = None)`

* **설명**: 기존 역할의 속성을 편집합니다.
* **매개변수**:
    * `role_identifier` (`RoleIdentifierType`): 편집할 역할의 식별자.
    * `name` (`Optional[str]`): 역할의 새 이름.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `add_role(self, member_identifier: MemberIdentifierType, role_identifier: RoleIdentifierType, reason: Optional[str] = None)`

* **설명**: 특정 유저에게 역할을 부여합니다.
* **매개변수**:
    * `member_identifier` (`MemberIdentifierType`): 역할을 부여할 멤버의 식별자.
    * `role_identifier` (`RoleIdentifierType`): 멤버에게 부여할 역할의 식별자.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `remove_role(self, member_identifier: MemberIdentifierType, role_identifier: RoleIdentifierType, reason: Optional[str] = None)`

* **설명**: 특정 유저로부터 역할을 제거합니다.
* **매개변수**:
    * `member_identifier` (`MemberIdentifierType`): 역할을 제거할 멤버의 식별자.
    * `role_identifier` (`RoleIdentifierType`): 멤버로부터 제거할 역할의 식별자.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `grant_admin(self, member_identifier: MemberIdentifierType, reason: Optional[str] = None)`

* **설명**: 특정 유저에게 관리자 역할을 부여합니다.
* **매개변수**:
    * `member_identifier` (`MemberIdentifierType`): 관리자 역할을 부여할 멤버의 식별자.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `grant_executive(self, member_identifier: MemberIdentifierType, reason: Optional[str] = None)`

* **설명**: 특정 유저에게 회장단 역할을 부여합니다.
* **매개변수**:
    * `member_identifier` (`MemberIdentifierType`): 회장단 역할을 부여할 멤버의 식별자.
    * `reason` (`Optional[str]`): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

---

#### `create_sig(self, name: str, members: Iterable[MemberIdentifierType], topic: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]`
* **설명**: 주어진 이름과 구성원 리스트를 기반으로 새로운 SIG를 생성합니다. 이는 새로운 텍스트 채널과 역할을 생성하고, 멤버들에게 해당 역할을 부여합니다.
* **매개변수**:
    * `name` (`str`): SIG의 이름. 채널 이름과 역할 이름으로 사용됩니다.
    * `members` (`Iterable[MemberIdentifierType]`): SIG에 참여할 멤버들의 식별자 리스트.
    * `topic` (`Optional[str]`): SIG의 주제(설명). 채널 주제로 사용됩니다.
* **반환값**:
    * `tuple[discord.TextChannel, discord.Role]`: 생성된 텍스트 채널과 역할 객체.


---

#### `archive_sig(self, name: str, previous_semester: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]`

* **설명**: 특정 SIG를 아카이브 처리하고 관련 채널을 이동시킵니다. SIG 역할의 이름을 변경하고, 채널을 아카이브 카테고리로 이동시킵니다.
* **매개변수**:
    * `name` (`str`): 아카이브할 SIG의 이름.
    * `previous_semester` (`Optional[str]`): 이전 학기 정보. 역할 이름에 추가됩니다. 제공되지 않으면 `self.previousSemester` 값이 사용됩니다.
* **반환값**:
    * `tuple[discord.TextChannel, discord.Role]`: 이동된 텍스트 채널과 이름이 변경된 역할 객체.

---

#### `update_sig_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel`

* **설명**: SIG 카테고리를 업데이트합니다. 필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): SIG 카테고리의 ID, 이름 또는 카테고리 객체.
      * `create` (`bool`): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다. `False`인 경우, 기존 카테고리를 가져옵니다.
* **반환값**:
    * `discord.CategoryChannel`: 업데이트되거나 생성된 카테고리 채널 객체.

---

#### `update_sig_archive_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel`

* **설명**: SIG 아카이브 카테고리를 업데이트합니다. 필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): SIG 아카이브 카테고리의 ID, 이름 또는 카테고리 객체.
    * `create` (`bool`): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다. `False`인 경우, 기존 카테고리를 가져옵니다.
* **반환값**:
    * `discord.CategoryChannel`: 업데이트되거나 생성된 카테고리 채널 객체.

---

#### `create_pig(self, name: str, members: Iterable[MemberIdentifierType], topic: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]`
* **설명**: 주어진 이름과 구성원 리스트를 기반으로 새로운 PIG를 생성합니다. 이는 새로운 텍스트 채널과 역할을 생성하고, 멤버들에게 해당 역할을 부여합니다.
* **매개변수**:
    * `name` (`str`): PIG의 이름. 채널 이름과 역할 이름으로 사용됩니다.
    * `members` (`Iterable[MemberIdentifierType]`): PIG에 참여할 멤버들의 식별자 리스트.
    * `topic` (`Optional[str]`): PIG의 주제(설명). 채널 주제로 사용됩니다.
* **반환값**:
    * `tuple[discord.TextChannel, discord.Role]`: 생성된 텍스트 채널과 역할 객체.

---

#### `archive_pig(self, name: str, previous_semester: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]`
* **설명**: 특정 PIG를 아카이브 처리하고 관련 채널을 이동시킵니다. PIG 역할의 이름을 변경하고, 채널을 아카이브 카테고리로 이동시킵니다.
* **매개변수**:
    * `name` (`str`): 아카이브할 PIG의 이름.
    * `previous_semester` (`Optional[str]`): 이전 학기 정보. 역할 이름에 추가됩니다. 제공되지 않으면 `self.previousSemester` 값이 사용됩니다.
* **반환값**:
    * `tuple[discord.TextChannel, discord.Role]`: 이동된 텍스트 채널과 이름이 변경된 역할 객체.

---

#### `update_pig_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel`
* **설명**: PIG 카테고리를 업데이트합니다. 필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): PIG 카테고리의 ID, 이름 또는 카테고리 객체.
    * `create` (`bool`): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다. `False`인 경우, 기존 카테고리를 가져옵니다.
* **반환값**:
    * `discord.CategoryChannel`: 업데이트되거나 생성된 카테고리 채널 객체.

---

#### `update_pig_archive_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel`
* **설명**: PIG 아카이브 카테고리를 업데이트합니다. 필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.
* **매개변수**:
    * `identifier` (`CategoryIdentifierType`): PIG 아카이브 카테고리의 ID, 이름 또는 카테고리 객체.
    * `create` (`bool`): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다. `False`인 경우, 기존 카테고리를 가져옵니다.
* **반환값**:
    * `discord.CategoryChannel`: 업데이트되거나 생성된 카테고리 채널 객체.