import flet as ft


class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page = page

        self.controls = [
            self._top_bar(),
            self._header(),
            self._sections_grid(),
        ]

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
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "Settings",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Manage your account, security and app preferences.",
                                size=12,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.HELP_OUTLINE,
                                tooltip="Help & support",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.PERSON_OUTLINE,
                                tooltip="Profile",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Header -------------

    def _header(self) -> ft.Control:
        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "Vyapaar Buddy settings",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Fine-tune notifications, security, language and data controls.",
                                size=11,
                                color="#6B7280",  # GREY_500
                            ),
                        ],
                    ),
                    ft.Chip(
                        label=ft.Text("Workspace: Default", size=11),
                        bgcolor="#111827",
                        disabled=True,
                    ),
                ],
            ),
        )

    # ------------- Sections grid -------------

    def _sections_grid(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=16,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=self._profile_settings_card(),
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=self._notifications_card(),
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=self._security_card(),
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=self._preferences_card(),
                ),
                ft.Container(
                    col={"xs": 12, "md": 12},
                    content=self._data_management_card(),
                ),
            ],
        )

    # ------------- Generic section card -------------

    def _section_card(self, icon, title: str, rows: list, button_text: str, on_click):
        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=8,
                                border_radius=12,
                                bgcolor="#111827",
                                content=ft.Icon(icon, color="#A5B4FC", size=22),  # INDIGO_300-ish
                            ),
                            ft.Text(
                                title,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        row_title,
                                        size=13,
                                        color="#9CA3AF",  # GREY_400
                                    ),
                                    ft.Text(
                                        row_value,
                                        size=13,
                                        color="#F5F5F5",  # GREY_100-ish
                                    ),
                                ],
                            )
                            for row_title, row_value in rows
                        ],
                    ),
                    ft.Container(
                        alignment=ft.alignment.center_right,
                        content=ft.OutlinedButton(
                            button_text,
                            icon=ft.Icons.EDIT_OUTLINED,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=18),
                                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                            ),
                            on_click=on_click,
                        ),
                    ),
                ],
            ),
        )

    # ------------- Individual cards -------------

    def _profile_settings_card(self) -> ft.Control:
        rows = [
            ("Full name", "John Doe"),
            ("Email", "john@example.com"),
            ("Role", "Inventory Manager"),
        ]
        return self._section_card(
            ft.Icons.PERSON,
            "Profile",
            rows,
            "Edit profile",
            self._on_edit_profile,
        )

    def _notifications_card(self) -> ft.Control:
        rows = [
            ("Low stock alerts", "Enabled"),
            ("Demand predictions", "Enabled"),
            ("Weekly reports", "Disabled"),
        ]
        return self._section_card(
            ft.Icons.NOTIFICATIONS,
            "Notifications",
            rows,
            "Edit notifications",
            self._on_edit_notifications,
        )

    def _security_card(self) -> ft.Control:
        rows = [
            ("Two-factor authentication", "Enabled"),
            ("Session timeout", "30 minutes"),
            ("Last login", "Today at 9:24 AM"),
        ]
        return self._section_card(
            ft.Icons.LOCK,
            "Security",
            rows,
            "Manage security",
            self._on_edit_security,
        )

    def _preferences_card(self) -> ft.Control:
        rows = [
            ("Language", "English (US)"),
            ("Time zone", "GMT-5 (EST)"),
            ("Date format", "MM/DD/YYYY"),
        ]
        return self._section_card(
            ft.Icons.LANGUAGE,
            "Preferences",
            rows,
            "Edit preferences",
            self._on_edit_preferences,
        )

    def _data_management_card(self) -> ft.Control:
        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=8,
                                border_radius=12,
                                bgcolor="#111827",
                                content=ft.Icon(
                                    ft.Icons.STORAGE,
                                    color="#FBBF24",  # AMBER_300-ish
                                    size=22,
                                ),
                            ),
                            ft.Text(
                                "Data & storage",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Text(
                                                "Export your data, clear local cache or request account deletion.",
                        size=12,
                        color="#9CA3AF",  # GREY_400
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.FilledButton(
                                "Export data",
                                icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=18),
                                ),
                                on_click=self._on_export_data,
                            ),
                            ft.OutlinedButton(
                                "Clear cache",
                                icon=ft.Icons.DELETE_OUTLINE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=18),
                                ),
                                on_click=self._on_clear_cache,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Callbacks / backend hooks -------------

    def _show_snack(self, message: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def _on_edit_profile(self, e):
        # TODO: open profile edit dialog and call user profile API
        self._show_snack("Profile editing coming soon.")

    def _on_edit_notifications(self, e):
        # TODO: open notifications preferences and save to backend
        self._show_snack("Notification settings coming soon.")

    def _on_edit_security(self, e):
        # TODO: open security dialog (password change, 2FA config)
        self._show_snack("Security settings coming soon.")

    def _on_edit_preferences(self, e):
        # TODO: open language/timezone preferences and sync to backend
        self._show_snack("Preferences editing coming soon.")

    def _on_export_data(self, e):
        # TODO: trigger backend export job and send link/email
        self._show_snack("Data export request submitted (placeholder).")

    def _on_clear_cache(self, e):
        # TODO: clear local cache_service and maybe remote sessions
        self._show_snack("Local cache cleared (placeholder).")

