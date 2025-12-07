import re
from aiogram.filters import BaseFilter
from aiogram.types import Message




class ChannelIdFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Ищем #число
        return bool(re.search(r"#(\d+)", message.text or ""))