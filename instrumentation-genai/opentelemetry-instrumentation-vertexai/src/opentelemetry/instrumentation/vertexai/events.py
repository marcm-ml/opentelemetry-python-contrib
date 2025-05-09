# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Factories for event types described in
https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-events.md#system-event.

Hopefully this code can be autogenerated by Weaver once Gen AI semantic conventions are
schematized in YAML and the Weaver tool supports it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Literal

from opentelemetry._events import Event
from opentelemetry.semconv._incubating.attributes import gen_ai_attributes
from opentelemetry.util.types import AnyValue


def user_event(
    *,
    role: str = "user",
    content: AnyValue = None,
) -> Event:
    """Creates a User event
    https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/gen-ai/gen-ai-events.md#user-event
    """
    body: dict[str, AnyValue] = {
        "role": role,
    }
    if content is not None:
        body["content"] = content
    return Event(
        name="gen_ai.user.message",
        attributes={
            gen_ai_attributes.GEN_AI_SYSTEM: gen_ai_attributes.GenAiSystemValues.VERTEX_AI.value,
        },
        body=body,
    )


def assistant_event(
    *,
    role: str = "assistant",
    content: AnyValue = None,
) -> Event:
    """Creates an Assistant event
    https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/gen-ai/gen-ai-events.md#assistant-event
    """
    body: dict[str, AnyValue] = {
        "role": role,
    }
    if content is not None:
        body["content"] = content
    return Event(
        name="gen_ai.assistant.message",
        attributes={
            gen_ai_attributes.GEN_AI_SYSTEM: gen_ai_attributes.GenAiSystemValues.VERTEX_AI.value,
        },
        body=body,
    )


def system_event(
    *,
    role: str = "system",
    content: AnyValue = None,
) -> Event:
    """Creates a System event
    https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/gen-ai/gen-ai-events.md#system-event
    """
    body: dict[str, AnyValue] = {
        "role": role,
    }
    if content is not None:
        body["content"] = content
    return Event(
        name="gen_ai.system.message",
        attributes={
            gen_ai_attributes.GEN_AI_SYSTEM: gen_ai_attributes.GenAiSystemValues.VERTEX_AI.value,
        },
        body=body,
    )


def tool_event(
    *,
    role: str | None,
    id_: str,
    content: AnyValue = None,
) -> Event:
    """Creates a Tool message event
    https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/gen-ai/gen-ai-events.md#event-gen_aitoolmessage
    """
    if not role:
        role = "tool"

    body: dict[str, AnyValue] = {
        "role": role,
        "id": id_,
    }
    if content is not None:
        body["content"] = content
    return Event(
        name="gen_ai.tool.message",
        attributes={
            gen_ai_attributes.GEN_AI_SYSTEM: gen_ai_attributes.GenAiSystemValues.VERTEX_AI.value,
        },
        body=body,
    )


@dataclass
class ChoiceMessage:
    """The message field for a gen_ai.choice event"""

    content: AnyValue = None
    role: str = "assistant"


@dataclass
class ChoiceToolCall:
    """The tool_calls field for a gen_ai.choice event"""

    @dataclass
    class Function:
        name: str
        arguments: AnyValue = None

    function: Function
    id: str
    type: Literal["function"] = "function"


FinishReason = Literal[
    "content_filter", "error", "length", "stop", "tool_calls"
]


def choice_event(
    *,
    finish_reason: FinishReason | str,
    index: int,
    message: ChoiceMessage,
    tool_calls: Iterable[ChoiceToolCall] = (),
) -> Event:
    """Creates a choice event, which describes the Gen AI response message.
    https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/gen-ai/gen-ai-events.md#event-gen_aichoice
    """
    body: dict[str, AnyValue] = {
        "finish_reason": finish_reason,
        "index": index,
        "message": _asdict_filter_nulls(message),
    }

    tool_calls_list = [
        _asdict_filter_nulls(tool_call) for tool_call in tool_calls
    ]
    if tool_calls_list:
        body["tool_calls"] = tool_calls_list

    return Event(
        name="gen_ai.choice",
        attributes={
            gen_ai_attributes.GEN_AI_SYSTEM: gen_ai_attributes.GenAiSystemValues.VERTEX_AI.value,
        },
        body=body,
    )


def _asdict_filter_nulls(instance: Any) -> dict[str, AnyValue]:
    return asdict(
        instance,
        dict_factory=lambda kvs: {k: v for (k, v) in kvs if v is not None},
    )
