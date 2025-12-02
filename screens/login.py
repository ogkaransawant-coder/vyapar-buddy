import flet as ft


class LoginPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.bgcolor = "#020617"
        self.padding = 16

        # ---------- Form fields ----------
        self.email_field = ft.TextField(
            label="Email address",
            hint_text="you@example.com",
            border_radius=16,
            bgcolor="#020617",
            color="#E5E7EB",  # GREY_100
            border_color="#1E293B",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            width=360,
            autofocus=True,
        )

        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            border_radius=16,
            bgcolor="#020617",
            color="#E5E7EB",  # GREY_100
            border_color="#1E293B",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            width=360,
            on_submit=self._do_login,
        )

        self.remember_me = ft.Checkbox(
            label="Remember this device",
            value=True,
            label_style=ft.TextStyle(color="#9CA3AF", size=12),  # GREY_400
        )

        self.error_text = ft.Text(
            "",
            size=12,
            color="#F87171",  # RED_400
            visible=False,
        )

        # ---------- Buttons ----------
        login_button = ft.FilledButton(
            text="Sign in",
            icon=ft.Icons.LOGIN,
            width=360,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.Padding(0, 14, 0, 14),
            ),
            on_click=self._do_login,
        )

        google_button = ft.OutlinedButton(
            width=360,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=18),
                    ft.Text("Continue with Google", size=13),
                ],
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            on_click=lambda e: self._social_login("google"),
        )

        forgot_password = ft.TextButton(
            "Forgot password?",
            style=ft.ButtonStyle(color="#A5B4FC"),  # INDIGO_300-ish
            on_click=self._forgot_password,
        )

        # ---------- Layout (mobile + desktop friendly) ----------
        # Single centered column scales nicely on small screens.
        self.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Logo + title
                ft.Image(src="assets/logo.png", width=72, height=72),
                ft.Text(
                    "Vyapaar Buddy",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#F9FAFB",
                ),
                ft.Text(
                    "AI-powered inventory assistant for your business",
                    size=13,
                    color="#9CA3AF",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=24),

                # Card with form (looks good on mobile too)
                ft.Container(
                    width=420,
                    padding=20,
                    bgcolor="#020617",
                    border_radius=20,
                    border=ft.border.all(1, "#1E293B"),
                    content=ft.Column(
                        spacing=16,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Sign in to your account",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#F9FAFB",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Use your work email to access Vyapaar Buddy.",
                                size=12,
                                color="#6B7280",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            self.email_field,
                            self.password_field,
                            ft.Row(
                                width=360,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.remember_me, forgot_password],
                            ),
                            self.error_text,
                            login_button,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        width=110,
                                        height=1,
                                        bgcolor="#1E293B",
                                    ),
                                    ft.Text(
                                        "or",
                                        size=11,
                                        color="#6B7280",
                                    ),
                                    ft.Container(
                                        width=110,
                                        height=1,
                                        bgcolor="#1E293B",
                                    ),
                                ],
                            ),
                            google_button,
                        ],
                    ),
                ),
                ft.Container(height=24),
                ft.Text(
                    "© 2025 Vyapaar Buddy · All rights reserved",
                    size=11,
                    color="#4B5563",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    # ---------- Actions / validation ----------

    def _do_login(self, e):
        email = (self.email_field.value or "").strip()
        password = (self.password_field.value or "").strip()

        if not email or not password:
            self.error_text.value = "Please enter both email and password."
            self.error_text.visible = True
            self.error_text.update()

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Please fill in all fields."),
                bgcolor="#B91C1C",  # RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # TODO: call auth backend here
        self.page.session.set("user_email", email)
        self.page.session.set("screen", "dashboard")
        self.page.go("/dashboard")

    def _forgot_password(self, e):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Password reset flow coming soon."),
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _social_login(self, provider: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Sign in with {provider.title()} coming soon."),
        )
        self.page.snack_bar.open = True
        self.page.update()
