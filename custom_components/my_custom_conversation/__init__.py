"""The My Custom Conversation integration."""
from __future__ import annotations

from typing import Literal

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import intent

import voluptuous as vol

CONFIG_SCHEMA = vol.Schema(
    {
        "my_custom_conversation": vol.Schema({
            vol.Optional("name", default="my_custom_conversation_agent"): cv.string
        })
    },
    extra=vol.ALLOW_EXTRA
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize your integration."""
    agent = MyCustomConversationAgent(hass, entry)
    conversation.async_set_agent(hass, entry, agent)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenAI."""
    conversation.async_unset_agent(hass, entry)
    return True


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
        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech("Test response")
        return conversation.ConversationResult(
            conversation_id=None,
            response=response
        )
