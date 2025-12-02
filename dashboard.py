import flet as ft
from flet.canvas import Canvas, Arc
from flet import Paint, PaintingStyle


class DashboardPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page = page

        # In real app, these values should be fetched from backend APIs
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self.sales_data = [4200, 3800, 5200, 4600, 6000, 6500]

        self.fast = 58
        self.slow = 32
        self.dead = 10

        self.controls = [
            self._top_bar(),
            self._header_section(),
            self._kpi_section(),
            self._charts_section(),
        ]

    # ---------------- Top bar ----------------

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
                                "Dashboard",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Inventory health and performance at a glance",
                                size=12,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Refresh dashboard",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SEARCH,
                                icon_color="#9CA3AF",
                                tooltip="Search",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS,
                                icon_color="#EF4444",
                                tooltip="Notifications",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---------------- Header section ----------------

    def _header_section(self) -> ft.Control:
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
                                "Vyapaar Buddy overview",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Monitor stock risk, sales momentum, and demand signals.",
                                size=12,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Chip(
                                label=ft.Text("Today", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                            ft.Chip(
                                label=ft.Text("Store: All", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---------------- KPI section ----------------

    def _kpi_section(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=12,
            controls=[
                self._kpi_card(
                    icon=ft.Icons.ARROW_DOWNWARD,
                    icon_color="#FBBF24",  # AMBER_300
                    value="12",
                    title="Low stock items",
                    subtitle="+3 from last week",
                    chip_text="Restock",
                    chip_color="#FBBF24",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    icon_color="#A5B4FC",  # INDIGO_300
                    value="5",
                    title="Overstock alerts",
                    subtitle="-2 from last week",
                    chip_text="Review",
                    chip_color="#6366F1",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.REPORT_GMAILERRORRED,
                    icon_color="#FCA5A5",  # RED_300
                    value="8",
                    title="Dead stock items",
                    subtitle="No change",
                    chip_text="Liquidate",
                    chip_color="#F87171",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.SHOW_CHART,
                    icon_color="#6EE7B7",  # GREEN_300
                    value="+18%",
                    title="Predicted demand",
                    subtitle="Next 30 days",
                    chip_text="Forecast",
                    chip_color="#22C55E",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.ATTACH_MONEY,
                    icon_color="#6EE7B7",  # EMERALD_300-ish
                    value="$91,000",
                    title="Total revenue",
                    subtitle="+12.5%",
                    chip_text="Sales",
                    chip_color="#22C55E",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    icon_color="#93C5FD",  # BLUE_300
                    value="1,247",
                    title="Orders processed",
                    subtitle="+8.2%",
                    chip_text="Orders",
                    chip_color="#60A5FA",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                    icon_color="#67E8F9",  # CYAN_300
                    value="3,892",
                    title="Items sold",
                    subtitle="+15.3%",
                    chip_text="Volume",
                    chip_color="#22D3EE",
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.TRENDING_UP,
                    icon_color="#D9F99D",  # LIME_300
                    value="18.4%",
                    title="Growth rate",
                    subtitle="+3.1% vs last period",
                    chip_text="Growth",
                    chip_color="#A3E635",
                    col={"xs": 12, "md": 3},
                ),
            ],
        )

    def _kpi_card(
        self,
        icon,
        icon_color,
        value: str,
        title: str,
        subtitle: str,
        chip_text: str,
        chip_color,
        col,
    ) -> ft.Control:
        return ft.Container(
            col=col,
            padding=16,
            bgcolor="#0F172A",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(icon, size=24, color=icon_color),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=999,
                                bgcolor="#111827",
                                content=ft.Text(
                                    chip_text,
                                    size=10,
                                    color=chip_color,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#F9FAFB",
                    ),
                    ft.Text(
                        title,
                        size=13,
                        color="#9CA3AF",
                    ),
                    ft.Text(
                        subtitle,
                        size=11,
                        color="#6B7280",
                    ),
                ],
            ),
        )

    # ---------------- Charts section ----------------

    def _charts_section(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=16,
            controls=[
                ft.Container(
                    col={"xs": 12, "lg": 7},
                    content=self._sales_trend_chart(),
                ),
                ft.Container(
                    col={"xs": 12, "lg": 5},
                    content=self._inventory_distribution(),
                ),
            ],
        )

    # ---------------- Sales LineChart ----------------

    def _sales_trend_chart(self) -> ft.Control:
        points = [
            ft.LineChartDataPoint(i, self.sales_data[i])
            for i in range(len(self.sales_data))
        ]

        max_y = max(self.sales_data) if self.sales_data else 0
        step = max(1000, int(max_y / 4)) if max_y else 1000

        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Sales trends",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#F9FAFB",
                            ),
                            ft.Chip(
                                label=ft.Text("Last 6 months", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                    ft.Text(
                        "Recent sales velocity across months.",
                        size=11,
                        color="#6B7280",
                    ),
                    ft.Container(
                        height=260,
                        content=ft.LineChart(
                            data_series=[
                                ft.LineChartData(
                                    data_points=points,
                                    curved=True,
                                    color="#3B82F6",
                                    stroke_width=3,
                                )
                            ],
                            interactive=True,
                            border=ft.border.all(1, "#1E293B"),
                            left_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(
                                        value=i * step,
                                        label=ft.Text(
                                            str(i * step),
                                            size=10,
                                            color="#9CA3AF",
                                        ),
                                    )
                                    for i in range(0, 5)
                                ],
                                labels_size=32,
                            ),
                            bottom_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(
                                        value=i,
                                        label=ft.Text(
                                            self.months[i],
                                            size=11,
                                            color="#9CA3AF",
                                        ),
                                    )
                                    for i in range(len(self.months))
                                ],
                                labels_size=32,
                            ),
                        ),
                    ),
                ],
            ),
        )

    # ---------------- Inventory distribution (pie-like) ----------------    

    def _inventory_distribution(self) -> ft.Control:
        total = self.fast + self.slow + self.dead
        fast_deg = (self.fast / total) * 360
        slow_deg = (self.slow / total) * 360
        dead_deg = 360 - fast_deg - slow_deg

        canvas = Canvas(
            [
                Arc(
                    150,
                    150,
                    300,
                    300,
                    0,
                    fast_deg,
                    paint=Paint(
                        style=PaintingStyle.FILL,
                        color="#10B981",
                    ),
                ),
                Arc(
                    150,
                    150,
                    300,
                    300,
                    fast_deg,
                    slow_deg,
                    paint=Paint(
                        style=PaintingStyle.FILL,
                        color="#FBBF24",
                    ),
                ),
                Arc(
                    150,
                    150,
                    300,
                    300,
                    fast_deg + slow_deg,
                    dead_deg,
                    paint=Paint(
                        style=PaintingStyle.FILL,
                        color="#EF4444",
                    ),
                ),
            ]
        )

        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(
                        "Inventory distribution",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#F9FAFB",
                    ),
                    ft.Text(
                        "Share of fast, slow and dead moving items.",
                        size=11,
                        color="#6B7280",
                    ),
                    ft.Container(
                        height=260,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Stack(
                                    width=220,
                                    height=220,
                                    controls=[
                                        ft.Container(
                                            width=220,
                                            height=220,
                                            content=canvas,
                                        ),
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    f"{self.fast + self.slow}%",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#F9FAFB",
                                                ),
                                                ft.Text(
                                                    "Active stock",
                                                    size=11,
                                                    color="#9CA3AF",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        self._legend_item(
                                            "Fast moving",
                                            f"{self.fast}%",
                                            "#10B981",
                                        ),
                                        self._legend_item(
                                            "Slow moving",
                                            f"{self.slow}%",
                                            "#FBBF24",
                                        ),
                                        self._legend_item(
                                            "Dead stock",
                                            f"{self.dead}%",
                                            "#EF4444",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _legend_item(self, label: str, value: str, color: str) -> ft.Control:
        return ft.Row(
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=5,
                    bgcolor=color,
                ),
                ft.Text(
                    label,
                    size=12,
                    color="#E5E7EB",  # GREY_300-ish
                ),
                ft.Text(
                    value,
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color="#F9FAFB",
                ),
            ],
        )
                