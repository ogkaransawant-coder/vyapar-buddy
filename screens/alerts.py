import flet as ft


class AlertsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page = page

        # In real app, these will be loaded from backend via a service
        self.alerts_data = self._mock_alerts()

        self.controls = [
            self._top_bar(),
            self._summary_header(),
            self._filters_row(),
            self._alerts_list(),
        ]

    # ------------- Top bar -------------

    def _top_bar(self) -> ft.Control:
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=4, vertical=4),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Alerts & Anomalies",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Real-time signals for stock, demand and fraud",
                                size=12,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Refresh alerts",
                                on_click=self.refresh_alerts,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SEARCH,
                                tooltip="Search alerts",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS,
                                icon_color="#F87171",  # RED_ACCENT-ish
                                tooltip="Notifications",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Header / Stats -------------

    def _summary_header(self) -> ft.Control:
        total = len(self.alerts_data)
        critical = sum(1 for a in self.alerts_data if a["severity"] == "critical")
        warning = sum(1 for a in self.alerts_data if a["severity"] == "warning")

        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 4},
                    padding=16,
                    bgcolor="#020617",
                    border_radius=16,
                    border=ft.border.all(1, "#1E293B"),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "Active Alerts",
                                size=16,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                f"{total} alerts currently monitored",
                                size=12,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "md": 4},
                    padding=16,
                    bgcolor="#0F172A",
                    border_radius=16,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        "Critical",
                                        size=13,
                                        color="#FCA5A5",  # RED_300
                                    ),
                                    ft.Icon(
                                        ft.Icons.ERROR,
                                        color="#F87171",  # RED_400
                                        size=20,
                                    ),
                                ],
                            ),
                            ft.Text(
                                str(critical),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "md": 4},
                    padding=16,
                    bgcolor="#0F172A",
                    border_radius=16,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        "Warnings",
                                        size=13,
                                        color="#FCD34D",  # AMBER_200-ish
                                    ),
                                    ft.Icon(
                                        ft.Icons.WARNING_AMBER,
                                        color="#FBBF24",  # AMBER_300-ish
                                        size=20,
                                    ),
                                ],
                            ),
                            ft.Text(
                                str(warning),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
            ]
        )

    # ------------- Filters / Search -------------

    def _filters_row(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=8,
            controls=[
                ft.TextField(
                    col={"xs": 12, "md": 4},
                    label="Search by product or alert type",
                    prefix_icon=ft.Icons.SEARCH,
                    dense=True,
                    border_radius=20,
                    on_change=self._on_search_change,
                ),
                ft.Dropdown(
                    col={"xs": 6, "md": 2},
                    label="Severity",
                    dense=True,
                    border_radius=20,
                    options=[
                        ft.dropdown.Option("all"),
                        ft.dropdown.Option("critical"),
                        ft.dropdown.Option("warning"),
                        ft.dropdown.Option("info"),
                    ],
                    value="all",
                    on_change=self._on_filter_change,
                ),
                                ft.Dropdown(
                    col={"xs": 6, "md": 2},
                    label="Type",
                    dense=True,
                    border_radius=20,
                    options=[
                        ft.dropdown.Option("all"),
                        ft.dropdown.Option("Low Stock"),
                        ft.dropdown.Option("Overstock"),
                        ft.dropdown.Option("Demand Spike"),
                        ft.dropdown.Option("Mismatch"),
                    ],
                    value="all",
                    on_change=self._on_filter_change,
                ),
                ft.Row(
                    col={"xs": 12, "md": 4},
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.FilledButton(
                            "Acknowledge all",
                            icon=ft.Icons.DONE_ALL,
                            on_click=self._acknowledge_all,
                        ),
                        ft.OutlinedButton(
                            "Clear resolved",
                            icon=ft.Icons.CLEAR_ALL,
                            on_click=self._clear_resolved,
                        ),
                    ],
                ),
            ],
        )

    # ------------- Alerts list -------------

    def _alerts_list(self) -> ft.Control:
        self.alerts_column = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )
        self._render_alerts(self.alerts_data)
        return self.alerts_column

    def _render_alerts(self, alerts):
        self.alerts_column.controls.clear()
        if not alerts:
            self.alerts_column.controls.append(
                ft.Container(
                    padding=32,
                    border_radius=16,
                    bgcolor="#020617",
                    border=ft.border.all(1, "#1E293B"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE_OUTLINE,
                                color="#4ADE80",  # GREEN_400-ish
                            ),
                            ft.Text(
                                "No active alerts. Inventory looks good!",
                                size=14,
                                color="#D1D5DB",  # GREY_300
                            ),
                        ],
                    ),
                )
            )
        else:
            for alert in alerts:
                self.alerts_column.controls.append(self._alert_card(alert))
        # don’t call update() during __init__; page.update() is used after actions

    def _alert_card(self, data: dict) -> ft.Control:
        severity = data.get("severity", "warning")
        bg_map = {
            "critical": "#1F2937",
            "warning": "#FEF3C7",
            "info": "#E0F2FE",
        }
        border_map = {
            "critical": "#EF4444",
            "warning": "#F59E0B",
            "info": "#0EA5E9",
        }

        bgcolor = bg_map.get(severity, "#020617")
        border_color = border_map.get(severity, "#1E293B")

        text_on_light = "#111827"
        text_on_dark = "#F3F4F6"

        return ft.Container(
            padding=16,
            border_radius=16,
            bgcolor=bgcolor,
            border=ft.border.all(1.5, border_color),
            ink=True,
            on_click=lambda _: self._open_details(data),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        spacing=10,
                        expand=True,
                        controls=[
                            ft.Row(
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        padding=10,
                                        border_radius=12,
                                        bgcolor="#FFFFFF10",
                                        content=ft.Icon(
                                            data["icon"],
                                            color=border_color,
                                            size=24,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                data["type"],
                                                size=16,
                                                weight=ft.FontWeight.W_600,
                                                color=text_on_dark
                                                if bgcolor in ("#020617", "#1F2937")
                                                else text_on_light,
                                            ),
                                            ft.Text(
                                                data.get("product", ""),
                                                size=12,
                                                color="#9CA3AF",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Text(
                                data["message"],
                                size=13,
                                color=text_on_light
                                if bgcolor not in ("#020617", "#1F2937")
                                else "#F9FAFB",
                            ),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.FilledButton(
                                        "Take action",
                                        icon=ft.Icons.ROCKET_LAUNCH,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                        ),
                                        on_click=lambda e, d=data: self._handle_action(d),
                                    ),
                                    ft.OutlinedButton(
                                        "Dismiss",
                                        icon=ft.Icons.CLOSE,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                        ),
                                        on_click=lambda e, d=data: self._dismiss_alert(d),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text(
                                data["time"],
                                size=11,
                                color="#4B5563",  # GREY_600
                            ),
                            ft.Container(height=8),
                            ft.Chip(
                                label=ft.Text(
                                    severity.capitalize(),
                                    size=11,
                                ),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Actions / callbacks -------------

    def refresh_alerts(self, e):
        self._render_alerts(self.alerts_data)
        self.page.update()

    def _acknowledge_all(self, e):
        self.alerts_data = []
        self._render_alerts(self.alerts_data)
        self.page.update()

    def _clear_resolved(self, e):
        self.alerts_data = [
            a for a in self.alerts_data if not a.get("resolved", False)
        ]
        self._render_alerts(self.alerts_data)
        self.page.update()

    def _handle_action(self, alert):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Action triggered for: {alert['type']}"),
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _dismiss_alert(self, alert):
        self.alerts_data = [a for a in self.alerts_data if a is not alert]
        self._render_alerts(self.alerts_data)
        self.page.update()

    def _open_details(self, alert):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(alert["type"]),
            content=ft.Text(alert["message"]),
            actions= ft.TextButton("Close", on_click=lambda e: self._close_dialog()),
            
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    # ------------- Filtering logic -------------

    def _on_search_change(self, e: ft.ControlEvent):
        query = (e.control.value or "").lower()
        filtered = [
            a
            for a in self.alerts_data
            if query in a["type"].lower()
            or query in a["message"].lower()
            or query in a.get("product", "").lower()
        ]
        self._render_alerts(filtered)
        self.page.update()

    def _on_filter_change(self, e: ft.ControlEvent):
        # Placeholder for combined severity/type filters; re-render with current data
        self._render_alerts(self.alerts_data)
        self.page.update()

    # ------------- Mock data (replace with backend) -------------

    def _mock_alerts(self):
        return [
            {
                "id": "a1",
                "type": "Low Stock Warning",
                "product": "Wireless Mouse",
                "message": "Wireless Mouse stock has dropped below minimum threshold (5 units remaining).",
                "icon": ft.Icons.WARNING_AMBER,
                "severity": "critical",
                "time": "2 hours ago",
            },
            {
                "id": "a2",
                "type": "Demand Spike Prediction",
                "product": "Monitor Arms",
                "message": "Monitor Arms expected to see 45% increase in demand over next 2 weeks.",
                "icon": ft.Icons.SHOW_CHART,
                "severity": "warning",
                "time": "4 hours ago",
            },
            {
                "id": "a3",
                "type": "Overstock Alert",
                "product": "Keyboard Cases",
                "message": "Keyboard Cases inventory is 3x above optimal level (156 units).",
                "icon": ft.Icons.INVENTORY_2,
                "severity": "warning",
                "time": "5 hours ago",
            },
            {
                "id": "a4",
                "type": "Low Stock Warning",
                "product": "USB Cable",
                "message": "USB Cable inventory below reorder point (12 units remaining).",
                "icon": ft.Icons.WARNING,
                "severity": "critical",
                "time": "1 hour ago",
            },
            {
                "id": "a5",
                "type": "Stock Mismatch Detected",
                "product": "Desk Lamp",
                "message": "Potential discrepancy in Desk Lamp count - physical audit recommended.",
                "icon": ft.Icons.ERROR_OUTLINE,
                "severity": "critical",
                "time": "6 hours ago",
            },
        ]


