from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path


class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")


class PushNotificationTool(BaseTool):
    """A custom tool: notifies the user about the chosen stock.

    In production this would call a push service (e.g. Pushover, Slack,
    WhatsApp). For the course it appends to output/notifications.md so you
    can see exactly when (and with what) the agent decided to use the tool.
    """

    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        print(f"Push: {message}")
        notifications = Path("output") / "notifications.md"
        notifications.parent.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with notifications.open("a", encoding="utf-8") as f:
            f.write(f"- **{timestamp}** — {message}\n")
        return '{"notification": "ok"}'
