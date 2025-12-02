import flet as ft


class AnalyticsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page = page

        # In real app, these will come from backend via api_service / forecasting_service
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self.revenue = [12000, 11500, 15500, 15000, 18000, 19500]
        self.profit = [9000, 8200, 10000, 9600, 12000, 13500]

        self.category_labels = [
            "Electronics",
            "Furniture",
            "Accessories",
            "Lighting",
            "Stationery",
        ]
        self.category_values = [4200, 3600, 2800, 1500, 2400]

        self.controls = [
            self._top_bar(),
            self._header(),
            self._kpi_section(),
            self._charts_row(),
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
                                "Analytics",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Trends, performance and forecasts",
                                size=12,
                                color="#9CA3AF",
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.SegmentedButton(
                                selected=["6M"],
                                segments=[
                                    ft.Segment(value="7D", label=ft.Text("7D")),
                                    ft.Segment(value="30D", label=ft.Text("30D")),
                                    ft.Segment(value="6M", label=ft.Text("6M")),
                                    ft.Segment(value="1Y", label=ft.Text("1Y")),
                                ],
                                on_change=self._on_range_change,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                                tooltip="Export report",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Header / description -------------

    def _header(self) -> ft.Control:
        return ft.Container(
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text(
                        "Analytics Dashboard",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Understand revenue, profit and category performance at a glance.",
                        size=12,
                        color="#9CA3AF",
                    ),
                ],
            ),
        )

    # ------------- KPI cards -------------

    def _kpi_section(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=12,
            controls=[
                self._kpi_card(
                    icon=ft.Icons.ATTACH_MONEY,
                    title="Total revenue",
                    value="$91,000",
                    change="+12.5%",
                    change_positive=True,
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    title="Orders processed",
                    value="1,247",
                    change="+8.2%",
                    change_positive=True,
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    title="Items sold",
                    value="3,892",
                    change="+15.3%",
                    change_positive=True,
                    col={"xs": 12, "md": 3},
                ),
                self._kpi_card(
                    icon=ft.Icons.TRENDING_UP,
                    title="Growth rate",
                    value="18.4%",
                    change="+3.1% vs last period",
                    change_positive=True,
                    col={"xs": 12, "md": 3},
                ),
            ],
        )

    def _kpi_card(
        self,
        icon,
        title: str,
        value: str,
        change: str,
        change_positive: bool,
        col,
    ) -> ft.Control:
        return ft.Container(
            col=col,
            padding=16,
            bgcolor="#0F172A",
            border_radius=16,
            border=ft.border.all(1, "#1F2937"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(icon, size=26, color="#FBBF24"),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=12,
                                bgcolor="#111827",
                                content=ft.Text(
                                    "Live",
                                    size=10,
                                    color="#4ADE80",
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        title,
                        size=13,
                        color="#9CA3AF",
                    ),
                    ft.Row(
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.ARROW_DROP_UP
                                if change_positive
                                else ft.Icons.ARROW_DROP_DOWN,
                                color="#4ADE80" if change_positive else "#F87171",
                            ),
                            ft.Text(
                                change,
                                size=11,
                                color="#4ADE80" if change_positive else "#F87171",
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ------------- Charts row -------------

    def _charts_row(self) -> ft.Control:
        return ft.ResponsiveRow(
            run_spacing=16,
            controls=[
                ft.Container(
                    col={"xs": 12, "lg": 7},
                    content=self._revenue_chart_card(),
                ),
                ft.Container(
                    col={"xs": 12, "lg": 5},
                    content=self._category_chart_card(),
                ),
            ],
        )

    # ------------- Revenue / profit chart -------------

    def _revenue_chart_card(self) -> ft.Control:
        revenue_points = [
            ft.LineChartDataPoint(i, self.revenue[i])
            for i in range(len(self.months))
        ]
        profit_points = [
            ft.LineChartDataPoint(i, self.profit[i])
            for i in range(len(self.months))
        ]

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
                                "Revenue & profit trends",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Chip(
                                label=ft.Text("Last 6 months", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                    ft.Text(
                        "Track how revenue and profit evolve over time.",
                        size=11,
                        color="#6B7280",
                    ),
                    ft.Container(
                        height=260,
                        content=ft.LineChart(
                            data_series=[
                                ft.LineChartData(
                                    data_points=revenue_points,
                                    curved=True,
                                    color="#3B82F6",
                                    stroke_width=3,
                                ),
                                ft.LineChartData(
                                    data_points=profit_points,
                                    curved=True,
                                    color="#22C55E",
                                    stroke_width=3,
                                ),
                            ],
                            interactive=True,
                            border=ft.border.all(1, "#1E293B"),
                            left_axis=ft.ChartAxis(labels_size=32),
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

    # ------------- Category bar chart -------------

    def _category_chart_card(self) -> ft.Control:
        bars = [
            ft.BarChartRod(
                from_y=0,
                to_y=self.category_values[i],
                width=22,
                color="#A78BFA",
                border_radius=4,
            )
            for i in range(len(self.category_values))
        ]

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
                                "Category performance",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Chip(
                                label=ft.Text("By revenue", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                    ft.Text(
                        "Which categories contribute most to your sales.",
                        size=11,
                        color="#6B7280",   # FIXED INVALID COLOR
                    ),
                    ft.Container(
                        height=260,
                        content=ft.BarChart(
                            bar_groups=[
                                ft.BarChartGroup(x=i, bar_rods=[bars[i]])
                                for i in range(len(self.category_values))
                            ],
                            interactive=True,
                            left_axis=ft.ChartAxis(labels_size=32),
                            bottom_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(
                                        value=i,
                                        label=ft.Text(
                                            self.category_labels[i],
                                            size=10,
                                            color="#9CA3AF",
                                        ),
                                    )
                                    for i in range(len(self.category_labels))
                                ],
                                labels_size=40,
                            ),
                            border=ft.border.all(1, "#1E293B"),
                            horizontal_grid_lines=ft.ChartGridLines(
                                color="#1E293B",
                                width=1,
                            ),
                        ),
                    ),
                ],
            ),
        )

    # ------------- Callbacks -------------

    def _on_range_change(self, e: ft.ControlEvent):
        selected_values = list(e.control.selected or [])
        current = selected_values[0] if selected_values else ""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Time range changed to: {current}"),
        )
        self.page.snack_bar.open = True
        self.page.update()
