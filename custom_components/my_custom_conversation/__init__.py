"""The My Custom Conversation integration."""
from __future__ import annotations

from typing import Literal

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent

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


async def send_message_to_api_async(message):
    url = 'http://127.0.0.1:8555'
    payload = {'message': message}

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

        api_response = await send_message_to_api_async(user_input.text)

        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech(api_response)
        return conversation.ConversationResult(
            conversation_id=None,
            response=response
        )
