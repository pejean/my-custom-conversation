"""The My Custom Conversation integration."""
from typing import Literal

from homeassistant.components import conversation
from homeassistant.components.conversation import agent
from homeassistant.const import MATCH_ALL
from homeassistant.helpers import intent


async def async_setup_entry(hass, config):
    """Initialize your integration."""
    conversation.async_set_agent(hass, MyCustomConversationAgent())


class MyCustomConversationAgent(agent.AbstractConversationAgent):

    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(self, user_input: agent.ConversationInput) -> agent.ConversationResult:
        """Process a sentence."""
        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech("Test response")
        return agent.ConversationResult(
            conversation_id=None,
            response=response
        )
