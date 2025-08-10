from discord import VoiceChannel, StageChannel, ForumChannel, TextChannel, CategoryChannel, Member
from discord.abc import GuildChannel

from .bot import DiscordBot

import json
import discord
import asyncio
import threading
from typing import Coroutine, Optional, Any, Iterable, Union
from types import SimpleNamespace
from pathlib import Path
import inspect

ChannelIdentifierType = Union[int, str, discord.VoiceChannel, discord.StageChannel, discord.ForumChannel, discord.TextChannel, discord.CategoryChannel]
CategoryIdentifierType = Union[int, str, discord.CategoryChannel]
MemberIdentifierType = Union[int, str, discord.User, discord.Member]
RoleIdentifierType = Union[int, str, discord.Role]

NOCHANGE = object()

SLUGDIFF = {
    " ": "-"
}

def log(func):
    """
    SCSCBotConnector 클래스의 메서드 호출을 로깅하는 데코레이터.
    메서드 이름과 전달된 인자(self 제외)를 출력합니다.
    """

    def wrapper(self, *args, **kwargs):
        if self.debug:  # debug 모드가 True일 때만 로깅
            # 메서드 이름 추출
            method_name = func.__name__

            # 함수의 시그니처를 가져옵니다.
            sig = inspect.signature(func)

            # 바인드된 인자들을 가져옵니다.
            # self를 포함한 모든 인자들을 바인드합니다.
            # inspect.Signature.bind는 함수/메서드에 전달될 인자들을 시그니처에 맞게 매핑합니다.
            try:
                # self를 포함한 모든 인자를 바인딩
                bound_args = sig.bind(self, *args, **kwargs)
                # bound_args.apply_defaults()  # 기본값이 있는 경우 적용
            except TypeError as e:
                # 시그니처 바인딩 실패 (예: 인자 개수 불일치)
                print(f"Error binding arguments for {method_name}: {e}")
                # Fallback to simple args/kwargs if binding fails
                arg_strings = [f"{k}={v!r}" for k, v in kwargs.items()]
                if args:
                    arg_strings.insert(0, f"args={args!r}")
                log_message = f"{method_name}({', '.join(arg_strings)}) called: Binding failed"
                print(log_message)
                return func(self, *args, **kwargs)

            # 'self' 파라미터는 로깅에서 제외하고 싶으므로, 이를 제외한 인자들만 처리합니다.
            # ordered_arguments는 OrderedDict 형태로 (파라미터명: 값)을 가집니다.
            ordered_arguments = bound_args.arguments

            # 'self' 인자가 있다면 제거 (메서드인 경우)
            # Python 3.8+ 에서는 inspect.Signature.parameters.keys()로 파라미터 순서를 얻을 수 있습니다.
            # 첫 번째 파라미터가 'self'인지 확인합니다.
            param_names = list(sig.parameters.keys())
            if param_names and param_names[0] == 'self':
                # 'self' 파라미터가 있다면 제거
                if 'self' in ordered_arguments:
                    del ordered_arguments['self']

            # 파라미터 이름과 값을 'name=value' 형식으로 포맷팅합니다.
            arg_strings = []
            for name, value in ordered_arguments.items():
                arg_strings.append(f"{name}={value!r}")  # !r은 repr()을 사용하여 값을 정확히 표현

            # -----------

            # # 인자를 보기 좋게 포맷팅
            # arg_strings = []
            # if args:
            #     arg_strings.append(f"args={args!r}")  # repr()로 정확한 표현
            # if kwargs:
            #     arg_strings.append(f"kwargs={kwargs!r}")

            log_message = f"{method_name}() called"
            if arg_strings:
                log_message += f" with {', '.join(arg_strings)}"

            print(log_message)

        return func(self, *args, **kwargs)

    return wrapper

class SCSCBotConnector:
    def __init__(self, bot: Optional[DiscordBot] = None, data_path: Optional[Path] = None, data: Optional[dict] = None, command_prefix: str = "!", debug: bool = False):
        """
        SCSCBotConnector의 생성자.

        Discord 봇과의 상호작용을 위한 연결을 설정하고,
        데이터를 로드하며, 봇 인스턴스를 초기화합니다.

        Args:
            bot (Optional[DiscordBot]): 사용할 DiscordBot 인스턴스. 제공되지 않으면 새로 생성됩니다.
            data_path (Optional[Path]): 봇 데이터 파일 (data.json)의 경로. 기본값은 "data/data.json"입니다.
            data (Optional[dict]): 봇 초기화에 사용될 데이터 딕셔너리.
            command_prefix (str): 봇의 명령어 접두사. 기본값은 "!"입니다.
            debug (bool): 디버그 모드 활성화 여부. True인 경우 로깅이 활성화됩니다.
        """
        if data is None:
            data = {}
        with open(data_path or Path(__file__).parent / "data/data.json", "r", encoding="UTF-8") as f:
            data.update(json.load(f))
        if bot is None:
            self.bot = DiscordBot(command_prefix=command_prefix, intents=discord.Intents.all(), data=data)
        else:
            self.bot = bot
            self.bot.data = data
        self.dataPath = data_path or Path(__file__).parent / "data/data.json"
        self.debug = debug
        self.defaultReason = self.bot.data["defaultReason"]
        self.previousSemester = self.bot.data["previousSemester"]
        self.enroll_event_listeners = []
        self.bot.connectors.append(self)

    def update_attributes(self):
        """
        봇의 주요 길드, 채널, 역할 등의 속성을 업데이트합니다.
        `self.bot.data`에 설정된 ID를 기반으로 객체를 가져와 할당합니다.
        봇이 준비된 후 호출되어야 합니다.
        """
        self.mainGuild: discord.Guild = self.bot.get_guild(self.bot.data["guildID"])
        self.mainChannel: discord.TextChannel = self.mainGuild.get_channel(self.bot.data["channelID"])
        self.adminRole: discord.Role = self.mainGuild.get_role(self.bot.data["adminRoleID"])
        self.executiveRole: discord.Role = self.mainGuild.get_role(self.bot.data["executiveRoleID"])
        self.sigCategory: discord.CategoryChannel = self.mainGuild.get_channel(self.bot.data["sigCategoryID"])
        self.sigArchiveCategory: discord.CategoryChannel = self.mainGuild.get_channel(self.bot.data["sigArchiveCategoryID"])
        self.pigCategory: discord.CategoryChannel = self.mainGuild.get_channel(self.bot.data["pigCategoryID"])
        self.pigArchiveCategory: discord.CategoryChannel = self.mainGuild.get_channel(self.bot.data["pigArchiveCategoryID"])
        self.previousSemester: str = self.bot.data["previousSemester"]

    def bot_on_ready(self):
        """
        봇이 Discord에 성공적으로 연결되었을 때 호출되는 콜백 함수.
        주요 속성들을 업데이트합니다.
        """
        self.update_attributes()

    def submit_sync(self, coro: Coroutine) -> Any:
        """
        비동기 코루틴을 동기적으로 실행하고 결과를 반환합니다.
        봇의 이벤트 루프에서 코루틴을 안전하게 실행하며 발생할 수 있는 예외를 처리합니다.

        Args:
            coro (Coroutine): 실행할 비동기 코루틴.

        Returns:
            Any: 코루틴 실행 결과.

        Raises:
            TypeError: `coro`가 코루틴이 아닐 경우 발생합니다.
            Exception: 코루틴 실행 중 예외가 발생할 경우 해당 예외를 다시 발생시킵니다.
        """
        def is_in_event_loop(loop):
            try:
                return asyncio.get_running_loop() == loop
            except RuntimeError:
                return False
        if is_in_event_loop(self.bot.loop):
            raise Exception("submit_sync called from within bot.loop")
        if not asyncio.iscoroutine(coro):
            raise TypeError("submit_sync expects a coroutine")
        try:
            future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            res = future.result()
            return res
        except Exception as e:
            print(f"[submit_sync Error] An error occurred: {e}")
            raise e

    @log
    def start(self, token):
        """
        Discord 봇을 별도의 이벤트 루프 스레드에서 실행합니다.
        이를 통해 GUI와 봇의 비동기 작업이 동시에 원활하게 작동할 수 있습니다.

        Args:
            token (str): Discord 봇 토큰.
        """
        def run_bot():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.start(token))

        thread = threading.Thread(target=run_bot, name="DiscordBotThread", daemon=True)
        thread.start()
        self.bot_thread = thread
        self.bot_loop = self.bot.loop

    @log
    def set_data(self, data: dict):
        """
        봇의 내부 데이터를 업데이트하고, 변경된 데이터를 JSON 파일에 저장합니다.
        데이터를 저장한 후, 관련 봇 속성들을 업데이트합니다.

        Args:
            data (dict): 새로 업데이트할 데이터를 포함하는 딕셔너리.
        """
        self.bot.data.update(data)
        with open(self.dataPath, "w", encoding="UTF-8") as f:
            json.dump(self.bot.data, f, indent=2)
        self.update_attributes()


    @staticmethod
    def slugify(text: str) -> str:
        """
        텍스트를 Discord 채널 이름 format에 맞게 변환합니다.

        Args:
            text (str): 변환할 텍스트.

        Returns:
            str: 채널 이름 format에 맞게 변환된 텍스트.
        """
        result = []
        for char in text:
            if char.isalpha() or char.isdecimal():
                result.append(char.lower())
            elif char in SLUGDIFF:
                result.append(SLUGDIFF[char])
            elif not char.isascii():
                result.append(char)
        return "".join(result)

    def get_channel(self, identifier: ChannelIdentifierType, category_identifier: Optional[CategoryIdentifierType] = NOCHANGE) -> None|discord.VoiceChannel|discord.StageChannel|discord.ForumChannel|discord.TextChannel|discord.CategoryChannel:
        """
        제공된 식별자를 사용하여 Discord 채널 객체를 가져옵니다.
        식별자는 채널 ID (정수), 채널 이름 (문자열), 또는 기존 채널 객체일 수 있습니다.
        카테고리 식별자가 제공되면 해당 카테고리 내에서 채널을 검색합니다.

        Args:
            identifier (ChannelIdentifierType): 채널의 ID, 이름 또는 채널 객체.
            category_identifier (Optional[CategoryIdentifierType]): 채널이 속한 카테고리의 ID, 이름 또는 카테고리 객체.
                                                                  기본값은 NOCHANGE로, 카테고리 필터링을 하지 않습니다.

        Returns:
            None | discord.VoiceChannel | discord.StageChannel | discord.ForumChannel | discord.TextChannel | discord.CategoryChannel:
                찾은 채널 객체 또는 찾지 못한 경우 None을 반환합니다.
        """
        match identifier:
            case int():
                return self.mainGuild.get_channel(identifier)
            case str():
                kwargs = {}
                if not category_identifier == NOCHANGE:
                    kwargs["category"] = self.get_category(category_identifier)
                return discord.utils.get(self.mainGuild.channels, name=identifier, **kwargs)
            case discord.abc.GuildChannel():
                return identifier

    def get_category(self, identifier: CategoryIdentifierType) -> None|discord.CategoryChannel:
        """
        제공된 식별자를 사용하여 Discord 카테고리 채널 객체를 가져옵니다.
        식별자는 카테고리 ID (정수), 카테고리 이름 (문자열), 또는 기존 카테고리 객체일 수 있습니다.

        Args:
            identifier (CategoryIdentifierType): 카테고리의 ID, 이름 또는 카테고리 객체.

        Returns:
            None | discord.CategoryChannel: 찾은 카테고리 객체 또는 찾지 못한 경우 None을 반환합니다.
        """
        match identifier:
            case int():
                return self.mainGuild.get_channel(identifier)
            case str():
                return discord.utils.get(self.mainGuild.categories, name=identifier)
            case discord.CategoryChannel():
                return identifier

    def get_member(self, identifier: MemberIdentifierType) -> None | discord.Member:
        """
        제공된 식별자를 사용하여 Discord 멤버 객체를 가져옵니다.
        식별자는 멤버 ID (정수), 멤버 이름/닉네임/글로벌 이름 (문자열), 또는 기존 User/Member 객체일 수 있습니다.

        Args:
            identifier (MemberIdentifierType): 멤버의 ID, 이름, 닉네임 또는 User/Member 객체.

        Returns:
            None | discord.Member: 찾은 멤버 객체 또는 찾지 못한 경우 None을 반환합니다.
        """
        match identifier:
            case int():
                return self.mainGuild.get_member(identifier)
            case str():
                return discord.utils.get(self.mainGuild.members, name=identifier) or discord.utils.get(self.mainGuild.members, nick=identifier) or discord.utils.get(self.mainGuild.members, global_name=identifier)
            case discord.User():
                return self.mainGuild.get_member(identifier.id)
            case discord.Member():
                return identifier

    def get_members(self, identifier: str, exact: bool = False) -> list[Member]:
        """
        주어진 식별자와 일치하는 Discord 멤버 리스트를 가져옵니다.
        이름 또는 닉네임을 기준으로 멤버를 검색합니다.

        Args:
            identifier (str): 검색할 멤버의 이름 또는 닉네임.
            exact (bool): True인 경우 정확히 일치하는 멤버만 반환하고, False인 경우 부분적으로 일치하는 멤버도 반환합니다.

        Returns:
            list[Member]: 검색 조건에 해당하는 멤버 객체들의 리스트.
        """
        check = lambda a, b: a == b if exact else a in b
        match identifier:
            case str():
                return [member for member in self.mainGuild.members if check(member.nick, identifier) or check(member.name, identifier)]
            case _:
                return []

    def get_role(self, identifier: RoleIdentifierType) -> None | discord.Role:
        """
        제공된 식별자를 사용하여 Discord 역할 객체를 가져옵니다.
        식별자는 역할 ID (정수), 역할 이름 (문자열), 또는 기존 역할 객체일 수 있습니다.

        Args:
            identifier (RoleIdentifierType): 역할의 ID, 이름 또는 역할 객체.

        Returns:
            None | discord.Role: 찾은 역할 객체 또는 찾지 못한 경우 None을 반환합니다.
        """
        match identifier:
            case int():
                return self.mainGuild.get_role(identifier)
            case str():
                return discord.utils.get(self.mainGuild.roles, name=identifier)
            case discord.Role():
                return identifier

    @log
    def create_invite(self, identifier: Optional[ChannelIdentifierType] = None, max_age: int = 0, max_uses: int = 0, reason: str = None, unique: bool = True, **kwargs) -> discord.Invite:
        """
        특정 채널에 대한 초대 코드를 생성합니다.

        Args:
            identifier (Optional[ChannelIdentifierType]): 초대 코드를 생성할 채널의 식별자.
                                                        기본값은 `self.mainChannel`입니다.
            max_age (int): 초대 링크의 유효 기간 (초). 0은 무한대입니다.
            max_uses (int): 초대 링크의 최대 사용 횟수. 0은 무한대입니다.
            reason (str): 감사 로그에 표시될 이유.
            unique (bool): True인 경우 고유한 초대 링크를 생성합니다.
            **kwargs: `discord.TextChannel.create_invite` 메서드에 전달될 추가 키워드 인자.

        Returns:
            discord.Invite: 생성된 초대 객체.
        """
        if identifier is None:
            identifier = self.mainChannel
        res = self.submit_sync(self.get_channel(identifier).create_invite(reason=reason, max_age=max_age, max_uses=max_uses, unique=unique, **kwargs))
        return res

    @log
    def send_message(self, identifier: ChannelIdentifierType, content, embed: Optional[discord.Embed] = None, **kwargs):
        """
        특정 채널에 문자열 메시지를 전송합니다.

        Args:
            identifier (ChannelIdentifierType): 메시지를 전송할 채널의 식별자.
            content (str): 전송할 메시지 내용.
            embed (Optional[discord.Embed]): 메시지와 함께 전송할 임베드 객체.
            **kwargs: `discord.TextChannel.send` 메서드에 전달될 추가 키워드 인자.
        """
        return self.submit_sync(self.get_channel(identifier).send(content, embed=embed, **kwargs))

    @log
    def create_text_channel(self, name: str, category_identifier: Optional[CategoryIdentifierType] = None, topic: Optional[str] = None, reason: Optional[str] = None) -> discord.TextChannel:
        """
        새로운 텍스트 채널을 생성합니다.

        Args:
            name (str): 생성할 텍스트 채널의 이름.
            category_identifier (Optional[CategoryIdentifierType]): 채널이 속할 카테고리의 식별자.
            topic (Optional[str]): 채널의 주제.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

        Returns:
            discord.TextChannel: 생성된 텍스트 채널 객체.
        """
        return self.submit_sync(self.mainGuild.create_text_channel(name, reason=reason or self.defaultReason, category=self.get_category(category_identifier), topic=topic))

    @log
    def edit_text_channel(self, channel_identifier: int|str|discord.TextChannel, name: Optional[str] = NOCHANGE, category_identifier: Optional[CategoryIdentifierType] = NOCHANGE, topic: Optional[str] = NOCHANGE, position: Optional[int] = NOCHANGE, reason: Optional[str] = None):
        """
        기존 텍스트 채널의 속성을 편집합니다.

        Args:
            channel_identifier (int | str | discord.TextChannel): 편집할 텍스트 채널의 식별자.
            name (Optional[str]): 채널의 새 이름. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
            category_identifier (Optional[CategoryIdentifierType]): 채널을 이동시킬 새 카테고리의 식별자.
                                                                  변경하지 않으려면 `NOCHANGE`를 사용합니다.
            topic (Optional[str]): 채널의 새 주제. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
            position (Optional[int]): 채널의 새 위치. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        options = {}
        if not name == NOCHANGE:
            options["name"] = name
        if not category_identifier == NOCHANGE:
            options["category"] = self.get_category(category_identifier)
        if not topic == NOCHANGE:
            options["topic"] = topic
        if not position == NOCHANGE:
            options["position"] = position
        options["reason"] = reason or self.defaultReason
        return self.submit_sync(self.get_channel(channel_identifier).edit(**options))

    @log
    def create_category(self, name: str, position: Optional[int] = None, reason: Optional[str] = None) -> discord.CategoryChannel:
        """
        새로운 카테고리 채널을 생성합니다.

        Args:
            name (str): 생성할 카테고리 채널의 이름.
            position (Optional[int]): 카테고리의 위치.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

        Returns:
            discord.CategoryChannel: 생성된 카테고리 채널 객체.
        """
        return self.submit_sync(self.mainGuild.create_category_channel(name, position=position, reason=reason or self.defaultReason))

    @log
    def edit_category(self, identifier: CategoryIdentifierType, name: Optional[str] = NOCHANGE, position: Optional[int] = NOCHANGE, reason: Optional[str] = None):
        """
        기존 카테고리 채널의 속성을 편집합니다.

        Args:
            identifier (CategoryIdentifierType): 편집할 카테고리 채널의 식별자.
            name (Optional[str]): 카테고리의 새 이름. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
            position (Optional[int]): 카테고리의 새 위치. 변경하지 않으려면 `NOCHANGE`를 사용합니다.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        options = {}
        if not name == NOCHANGE:
            options["name"] = name
        if not position == NOCHANGE:
            options["position"] = position
        return self.submit_sync(self.get_category(identifier).edit(**options, reason=reason or self.defaultReason))

    @log
    def create_role(self, name: str, members: Optional[Iterable[MemberIdentifierType]] = None, reason: Optional[str] = None) -> discord.Role:
        """
        새로운 역할을 생성하고, 선택적으로 멤버들에게 해당 역할을 부여합니다.

        Args:
            name (str): 생성할 역할의 이름.
            members (Optional[Iterable[MemberIdentifierType]]): 새로 생성된 역할을 부여할 멤버들의 식별자 리스트.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.

        Returns:
            discord.Role: 생성된 역할 객체.
        """
        role = self.submit_sync(self.mainGuild.create_role(name=name, reason=reason or self.defaultReason))
        if members is not None:
            for member in members:
                member = self.get_member(member)
                self.submit_sync(member.add_roles(role, reason=reason or self.defaultReason))
        return role

    @log
    def edit_role(self, role_identifier: RoleIdentifierType, name: Optional[str] = None, reason: Optional[str] = None):
        """
        기존 역할의 속성을 편집합니다.

        Args:
            role_identifier (RoleIdentifierType): 편집할 역할의 식별자.
            name (Optional[str]): 역할의 새 이름.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        role = self.get_role(role_identifier)
        return self.submit_sync(role.edit(name=name, reason=reason or self.defaultReason))

    @log
    def add_role(self, member_identifier: MemberIdentifierType, role_identifier: RoleIdentifierType, reason: Optional[str] = None):
        """
        특정 유저에게 역할을 부여합니다.

        Args:
            member_identifier (MemberIdentifierType): 역할을 부여할 멤버의 식별자.
            role_identifier (RoleIdentifierType): 멤버에게 부여할 역할의 식별자.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        return self.submit_sync(self.get_member(member_identifier).add_roles(self.get_role(role_identifier), reason=reason or self.defaultReason))

    @log
    def remove_role(self, member_identifier: MemberIdentifierType, role_identifier: RoleIdentifierType, reason: Optional[str] = None):
        """
        특정 유저로부터 역할을 제거합니다.

        Args:
            member_identifier (MemberIdentifierType): 역할을 제거할 멤버의 식별자.
            role_identifier (RoleIdentifierType): 멤버로부터 제거할 역할의 식별자.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        return self.submit_sync(self.get_member(member_identifier).remove_roles(self.get_role(role_identifier), reason=reason or self.defaultReason))

    @log
    def grant_admin(self, member_identifier: MemberIdentifierType, reason: Optional[str] = None):
        """
        특정 유저에게 관리자 역할을 부여합니다.

        Args:
            member_identifier (MemberIdentifierType): 관리자 역할을 부여할 멤버의 식별자.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        return self.add_role(member_identifier=member_identifier, role_identifier=self.adminRole, reason=reason or self.defaultReason)

    @log
    def grant_executive(self, member_identifier: MemberIdentifierType, reason: Optional[str] = None):
        """
        특정 유저에게 회장단 역할을 부여합니다.

        Args:
            member_identifier (MemberIdentifierType): 회장단 역할을 부여할 멤버의 식별자.
            reason (Optional[str]): 감사 로그에 표시될 이유. 기본값은 `self.defaultReason`입니다.
        """
        return self.add_role(member_identifier=member_identifier, role_identifier=self.executiveRole, reason=reason or self.defaultReason)

    @log
    def create_sig(self, name: str, members: Iterable[MemberIdentifierType], topic: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]:
        """
        주어진 이름과 구성원 리스트를 기반으로 새로운 SIG를 생성합니다.
        이는 새로운 텍스트 채널과 역할을 생성하고, 멤버들에게 해당 역할을 부여합니다.

        Args:
            name (str): SIG의 이름. 채널 이름과 역할 이름으로 사용됩니다.
            members (Iterable[MemberIdentifierType]): SIG에 참여할 멤버들의 식별자 리스트.
            topic (Optional[str]): SIG의 주제(설명). 채널 주제로 사용됩니다.

        Returns:
            tuple[discord.TextChannel, discord.Role]: 생성된 텍스트 채널과 역할 객체.
        """
        channelName = self.slugify(name)
        channel = self.create_text_channel(channelName, category_identifier=self.sigCategory, topic=topic)
        role = self.create_role(name, members)
        return channel, role

    @log
    def archive_sig(self, name: str, previous_semester: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]:
        """
        특정 SIG를 아카이브 처리하고 관련 채널을 이동시킵니다.
        SIG 역할의 이름을 변경하고, 채널을 아카이브 카테고리로 이동시킵니다.

        Args:
            name (str): 아카이브할 SIG의 이름.
            previous_semester (Optional[str]): 이전 학기 정보. 역할 이름에 추가됩니다.
                                             제공되지 않으면 `self.previousSemester` 값이 사용됩니다.

        Returns:
            tuple[discord.TextChannel, discord.Role]: 이동된 텍스트 채널과 이름이 변경된 역할 객체.
        """
        channelName = name.strip().lower().replace(" ", "-")
        channel = self.get_channel(channelName, category_identifier=self.sigCategory)
        if previous_semester is None:
            previous_semester = self.previousSemester
        role = self.edit_role(role_identifier=name, name=f"{name}-{previous_semester}")
        return self.edit_text_channel(channel, category_identifier=self.sigArchiveCategory), role

    @log
    def update_sig_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel:
        """
        SIG 카테고리를 업데이트합니다.
        필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.

        Args:
            identifier (CategoryIdentifierType): SIG 카테고리의 ID, 이름 또는 카테고리 객체.
            create (bool): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다.
                           `False`인 경우, 기존 카테고리를 가져옵니다.

        Returns:
            discord.CategoryChannel: 업데이트되거나 생성된 카테고리 채널 객체.
        """
        category = self.create_category(name=identifier) if create else self.get_category(identifier=identifier)
        self.set_data({"sigCategoryID": category.id})
        return category

    @log
    def update_sig_archive_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel:
        """
        SIG 아카이브 카테고리를 업데이트합니다.
        필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.

        Args:
            identifier (CategoryIdentifierType): SIG 아카이브 카테고리의 ID, 이름 또는 카테고리 객체.
            create (bool): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다.
                           `False`인 경우, 기존 카테고리를 가져옵니다.

        Returns:
            discord.CategoryChannel: 업데이트되거나 생성된 카테고리 채널 객체.
        """
        category = self.create_category(name=identifier) if create else self.get_category(identifier=identifier)
        self.set_data({"sigArchiveCategoryID": category.id})
        return category
    
    @log
    def create_pig(self, name: str, members: Iterable[MemberIdentifierType], topic: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]:
        """
        주어진 이름과 구성원 리스트를 기반으로 새로운 PIG를 생성합니다.
        이는 새로운 텍스트 채널과 역할을 생성하고, 멤버들에게 해당 역할을 부여합니다.

        Args:
            name (str): PIG의 이름. 채널 이름과 역할 이름으로 사용됩니다.
            members (Iterable[MemberIdentifierType]): PIG에 참여할 멤버들의 식별자 리스트.
            topic (Optional[str]): PIG의 주제(설명). 채널 주제로 사용됩니다.


        Returns:
            tuple[discord.TextChannel, discord.Role]: 생성된 텍스트 채널과 역할 객체.
        """
        channelName = self.slugify(name)
        channel = self.create_text_channel(channelName, category_identifier=self.pigCategory, topic=topic)
        role = self.create_role(name, members)
        return channel, role

    @log
    def archive_pig(self, name: str, previous_semester: Optional[str] = None) -> tuple[discord.TextChannel, discord.Role]:
        """
        특정 PIG를 아카이브 처리하고 관련 채널을 이동시킵니다.
        PIG 역할의 이름을 변경하고, 채널을 아카이브 카테고리로 이동시킵니다.

        Args:
            name (str): 아카이브할 PIG의 이름.
            previous_semester (Optional[str]): 이전 학기 정보. 역할 이름에 추가됩니다.
                                             제공되지 않으면 `self.previousSemester` 값이 사용됩니다.

        Returns:
            tuple[discord.TextChannel, discord.Role]: 이동된 텍스트 채널과 이름이 변경된 역할 객체.
        """
        channelName = name.strip().lower().replace(" ", "-")
        channel = self.get_channel(channelName, category_identifier=self.pigCategory)
        if previous_semester is None:
            previous_semester = self.previousSemester
        role = self.edit_role(role_identifier=name, name=f"{name}-{previous_semester}")
        return self.edit_text_channel(channel, category_identifier=self.pigArchiveCategory), role

    @log
    def update_pig_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel:
        """
        PIG 카테고리를 업데이트합니다.
        필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.

        Args:
            identifier (CategoryIdentifierType): PIG 카테고리의 ID, 이름 또는 카테고리 객체.
            create (bool): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다.
                           `False`인 경우, 기존 카테고리를 가져옵니다.

        Returns:
            discord.CategoryChannel: 업데이트되거나 생성된 카테고리 채널 객체.
        """
        category = self.create_category(name=identifier) if create else self.get_category(identifier=identifier)
        self.set_data({"pigCategoryID": category.id})
        return category

    @log
    def update_pig_archive_category(self, identifier: CategoryIdentifierType, create: bool = False) -> discord.CategoryChannel:
        """
        SIG 아카이브 카테고리를 업데이트합니다.
        필요에 따라 새로운 카테고리를 생성하거나 기존 카테고리를 가져와 설정합니다.

        Args:
            identifier (CategoryIdentifierType): PIG 아카이브 카테고리의 ID, 이름 또는 카테고리 객체.
            create (bool): `True`인 경우, 해당 이름의 카테고리를 새로 생성합니다.
                           `False`인 경우, 기존 카테고리를 가져옵니다.

        Returns:
            discord.CategoryChannel: 업데이트되거나 생성된 카테고리 채널 객체.
        """
        category = self.create_category(name=identifier) if create else self.get_category(identifier=identifier)
        self.set_data({"pigArchiveCategoryID": category.id})
        return category
