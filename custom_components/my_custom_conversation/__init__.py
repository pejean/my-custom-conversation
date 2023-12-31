"""The My Custom Conversation integration."""
from __future__ import annotations

from typing import Literal

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.util import ulid

import aiohttp
import asyncio


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize your integration."""
    agent = MyCustomConversationAgent(hass, entry)
    conversation.async_set_agent(hass, entry, agent)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenAI."""
    conversation.async_unset_agent(hass, entry)
    return True


async def send_message_to_api_async(conversation_id, message):
    url = 'http://super:8555'
    payload = {'conversation_id': conversation_id, 'message': message}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    result = response_data['message']
                else:
                    result = f"Communication Error: {response.status}"
    except aiohttp.ClientError as e:
        result = f"HTTP client error: {e}"
    except asyncio.TimeoutError:
        result = "Request timed out"
    except Exception as e:
        result = f"An unexpected error occurred: {e}"

    return result


class MyCustomConversationAgent(conversation.AbstractConversationAgent):
    """My Custom Conversation Agent"""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[dict]] = {}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(self, user_input: conversation.ConversationInput) -> conversation.ConversationResult:
        """Process a sentence."""

        conversation_id = user_input.conversation_id
        if conversation_id is None:
            conversation_id = ulid.ulid()

        user_message = user_input.text

        api_response = await send_message_to_api_async(conversation_id, user_message)

        input_response = intent.IntentResponse(language=user_input.language)
        input_response.async_set_speech(api_response)
        return conversation.ConversationResult(response=input_response, conversation_id=conversation_id)
