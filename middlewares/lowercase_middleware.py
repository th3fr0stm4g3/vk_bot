from vkbottle.dispatch.middlewares import BaseMiddleware


class LowercaseMiddleware(BaseMiddleware):

    async def pre(self):

        if self.event.text:
            self.event.text = (
                self.event.text
                .lower()
                .strip()
            )