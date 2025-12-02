import flet as ft


class ChatPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=0,
        )
        self.page = page

        # Chat messages list
        self.chat_column = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            padding=ft.padding.only(left=16, right=16, top=16, bottom=8),
        )

        # Input field
        self.user_input = ft.TextField(
            hint_text="Ask me anything about your inventory...",
            expand=True,
            border_radius=24,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor="#020617",
            color="#F5F5F5",  # GREY_100-ish
            hint_style=ft.TextStyle(color="#6B7280"),
            border_color="transparent",
            multiline=True,
            min_lines=1,
            max_lines=4,
            # remove shift_enter for compatibility
            on_submit=self.send_message,
        )

        # Layout: top bar, chat list, typing indicator placeholder, input bar
        self.controls = [
            self._top_bar(),
            ft.Container(
                expand=True,
                bgcolor="#020617",
                content=self.chat_column,
            ),
            ft.Container(),  # placeholder for typing indicator
            self._input_bar(),
        ]
        self.typing_indicator = self._typing_indicator(visible=False)
        self.controls[2] = self.typing_indicator  # replace placeholder

        # Initial assistant message
        self.add_message(
            "Hello! I'm your AI inventory assistant. I can help you check stock levels, analyze trends, manage alerts, and answer questions about your inventory. How can I help you today?",
            is_user=False,
        )

    # ------------- Top bar -------------

    def _top_bar(self) -> ft.Control:
        return ft.Container(
            bgcolor="#020617",
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border=ft.border.only(bottom=ft.BorderSide(1, "#1E293B")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=32,
                                height=32,
                                border_radius=16,
                                bgcolor="#22C55E20",
                                content=ft.Icon(
                                    ft.Icons.SUPPORT_AGENT,
                                    size=20,
                                    color="#34D399",  # EMERALD_400-ish
                                ),
                            ),
                            ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Text(
                                        "Vyapaar Buddy Assistant",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Ask about stock, sales, alerts and more",
                                        size=11,
                                        color="#6B7280",  # GREY_500
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.HISTORY,
                                tooltip="Conversation history",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SETTINGS_OUTLINED,
                                tooltip="Chat settings",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Typing indicator -------------

    def _typing_indicator(self, visible: bool) -> ft.Control:
        self.typing_dots = ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(width=6, height=6, border_radius=3, bgcolor="#9CA3AF"),
                ft.Container(width=6, height=6, border_radius=3, bgcolor="#9CA3AF"),
                ft.Container(width=6, height=6, border_radius=3, bgcolor="#9CA3AF"),
            ],
        )

        return ft.Container(
            visible=visible,
            padding=ft.padding.only(left=20, right=20, bottom=4, top=4),
            bgcolor="#020617",
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=8,
                        border_radius=999,
                        bgcolor="#1F2937",
                        content=self.typing_dots,
                    ),
                    ft.Text(
                        "Vyapaar Buddy is thinking...",
                        size=11,
                        color="#6B7280",  # GREY_500
                    ),
                ],
            ),
        )

    # ------------- Input bar -------------

    def _input_bar(self) -> ft.Control:
        return ft.Container(
            bgcolor="#020617",
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border=ft.border.only(top=ft.BorderSide(1, "#1E293B")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ATTACH_FILE,
                        icon_color="#9CA3AF",
                        tooltip="Attach file (coming soon)",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.IMAGE_OUTLINED,
                        icon_color="#9CA3AF",
                        tooltip="Upload image (coming soon)",
                    ),
                    self.user_input,
                    ft.IconButton(
                        icon=ft.Icons.MIC,
                        icon_color="#9CA3AF",
                        tooltip="Voice input (coming soon)",
                    ),
                    ft.FilledButton(
                        content=ft.Icon(ft.Icons.SEND, size=18),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            bgcolor="#6366F1",  # INDIGO_500-ish
                            padding=ft.padding.all(10),
                        ),
                        on_click=self.send_message,
                    ),
                ],
            ),
        )

    # ------------- Message bubble builder -------------

    def _message_bubble(self, text: str, is_user: bool) -> ft.Control:
        bubble_color = "#2563EB" if is_user else "#111827"
        text_color = "#F9FAFB"  # GREY_50-ish
        align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START

        return ft.Row(
            alignment=align,
            controls=[
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    margin=ft.margin.only(bottom=8, left=4, right=4),
                    bgcolor=bubble_color,
                    border_radius=ft.border_radius.only(
                        top_left=18,
                        top_right=18,
                        bottom_left=6 if is_user else 18,
                        bottom_right=18 if is_user else 6,
                    ),
                    content=ft.Text(
                        text,
                        size=14,
                        color=text_color,
                    ),
                    width=600,
                )
            ],
        )

    # ------------- Public method to add message -------------

    def add_message(self, text: str, is_user: bool):
        bubble = self._message_bubble(text, is_user)
        self.chat_column.controls.append(bubble)
        # page.update() is handled in send_message / backend reply

    # ------------- Sending / backend hook -------------

    def send_message(self, e: ft.ControlEvent):
        user_text = (self.user_input.value or "").strip()
        if not user_text:
            return

        self.add_message(user_text, is_user=True)

        self.user_input.value = ""
        self.user_input.update()

        self._set_typing(True)
        self.page.update()

        self.page.run_task(self._fake_backend_reply, user_text)

    async def _fake_backend_reply(self, user_text: str):
        import asyncio

        await asyncio.sleep(1.2)

        reply = (
            "This is a demo reply. Soon this will connect to your inventory AI backend "
            "to fetch real-time stock, sales and forecast insights."
        )
        self.add_message(reply, is_user=False)
        self._set_typing(False)
        self.page.update()

    def _set_typing(self, value: bool):
        self.typing_indicator.visible = value
        self.typing_indicator.update()
