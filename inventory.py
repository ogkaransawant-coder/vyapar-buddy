import flet as ft


class InventoryPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page = page

        # In real app, these will be loaded from Firestore / API
        self.items = self._mock_items()

        self.search_field = ft.TextField(
            hint_text="Search products or categories...",
            expand=True,
            height=46,
            bgcolor="#020617",
            color="#F5F5F5",  # GREY_100-ish
            border_radius=24,
            prefix_icon=ft.Icons.SEARCH,
            hint_style=ft.TextStyle(color="#6B7280", size=12),
            border_color="transparent",
            on_change=self._on_search_change,
        )

        self.table_column = ft.Column(
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        self.controls = [
            self._top_bar(),
            self._header_section(),
            self._table_card(),
        ]

        self._render_table(self.items)

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
                                "Inventory",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Browse, search and manage product stock.",
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
                                tooltip="Refresh inventory",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                tooltip="Add product",
                                on_click=self._open_add_dialog,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---------------- Header / filters ----------------

    def _header_section(self) -> ft.Control:
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
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Inventory management",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Chip(
                                label=ft.Text("Live sync", size=11),
                                bgcolor="#111827",
                                disabled=True,
                            ),
                        ],
                    ),
                    ft.Text(
                        "Use search, filters and quick actions to manage stock across all categories.",
                        size=11,
                        color="#6B7280",  # GREY_500
                    ),
                    ft.ResponsiveRow(
                        run_spacing=8,
                        controls=[
                            ft.Container(
                                col={"xs": 12, "md": 6},
                                content=self.search_field,
                            ),
                            ft.Container(
                                col={"xs": 6, "md": 2},
                                content=ft.Dropdown(
                                    label="Status",
                                    dense=True,
                                    border_radius=20,
                                    bgcolor="#020617",
                                    options=[
                                        ft.dropdown.Option("All"),
                                        ft.dropdown.Option("Low"),
                                        ft.dropdown.Option("OK"),
                                        ft.dropdown.Option("Overstock"),
                                        ft.dropdown.Option("Dead Stock"),
                                    ],
                                    value="All",
                                    on_change=self._on_filter_change,
                                ),
                            ),
                            ft.Container(
                                col={"xs": 6, "md": 2},
                                content=ft.Dropdown(
                                    label="Category",
                                    dense=True,
                                    border_radius=20,
                                    bgcolor="#020617",
                                    options=[
                                        ft.dropdown.Option("All"),
                                        ft.dropdown.Option("Electronics"),
                                        ft.dropdown.Option("Furniture"),
                                        ft.dropdown.Option("Accessories"),
                                        ft.dropdown.Option("Lighting"),
                                        ft.dropdown.Option("Stationery"),
                                    ],
                                    value="All",
                                    on_change=self._on_filter_change,
                                ),
                            ),
                            ft.Container(
                                col={"xs": 12, "md": 2},
                                content=ft.FilledButton(
                                    "Add product",
                                    icon=ft.Icons.ADD,
                                    on_click=self._open_add_dialog,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---------------- Table container ----------------

    def _table_card(self) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=16,
            bgcolor="#020617",
            border_radius=16,
            border=ft.border.all(1, "#1E293B"),
            content=ft.Column(
                spacing=8,
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Products",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"{len(self.items)} items",
                                size=11,
                                color="#6B7280",  # GREY_500
                            ),
                        ],
                    ),
                    ft.Divider(height=1, color="#1E293B"),
                    ft.Container(
                        expand=True,
                        content=self.table_column,
                    ),
                ],
            ),
        )

    # ---------------- Table rendering ----------------

    def _render_table(self, items):
        self.table_column.controls.clear()

        # Header
        self.table_column.controls.append(self._table_header())

        if not items:
            self.table_column.controls.append(
                ft.Container(
                    padding=24,
                    border_radius=12,
                    bgcolor="#020617",
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.INVENTORY_2_OUTLINED,
                                color="#4B5563",  # GREY_600
                            ),
                            ft.Text(
                                "No products match your filters.",
                                size=13,
                                color="#9CA3AF",  # GREY_400
                            ),
                        ],
                    ),
                )
            )
        else:
            for item in items:
                self.table_column.controls.append(self._inventory_row(item))

        # no update() here; page.update() is called after actions

    def _table_header(self) -> ft.Control:
        return ft.Container(
            padding=ft.padding.symmetric(vertical=6, horizontal=8),
            content=ft.Row(
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self._header_cell("Product name"),
                    self._header_cell("Category"),
                    self._header_cell("Qty", align_end=True, fixed_width=70),
                    self._header_cell("Status", fixed_width=110),
                    self._header_cell("Last updated", fixed_width=110),
                    self._header_cell("", fixed_width=70),
                ],
            ),
        )

    def _header_cell(
        self, label: str, align_end: bool = False, fixed_width: int | None = None
    ) -> ft.Control:
        return ft.Container(
            width=fixed_width,
            alignment=ft.alignment.center_right if align_end else ft.alignment.center_left,
            content=ft.Text(
                label,
                size=11,
                weight=ft.FontWeight.W_600,
                color="#6B7280",  # GREY_500
            ),
        )

    def _inventory_row(self, item: dict) -> ft.Control:
        return ft.Container(
            padding=ft.padding.symmetric(vertical=10, horizontal=8),
            border_radius=10,
            bgcolor="#0F172A",
            margin=ft.margin.only(bottom=6),
            content=ft.Row(
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            item["name"],
                            size=14,
                            color="#F9FAFB",
                        ),
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Text(
                            item["category"],
                            size=13,
                            color="#D1D5DB",
                        ),
                        expand=True,
                    ),
                    ft.Container(
                        alignment=ft.alignment.center_right,
                        content=ft.Text(
                            str(item["quantity"]),
                            size=13,
                            color="#F9FAFB",
                        ),
                        width=70,
                    ),
                    ft.Container(
                        content=self._status_chip(item["status"]),
                        width=110,
                    ),
                    ft.Container(
                        content=ft.Text(
                            item["updated"],
                            size=12,
                            color="#6B7280",
                        ),
                        width=110,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=4,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_size=18,
                                tooltip="Edit",
                                on_click=lambda e, i=item: self._open_edit_dialog(i),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_size=18,
                                tooltip="Delete",
                                on_click=lambda e, i=item: self._delete_item(i),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def _status_chip(self, status: str) -> ft.Control:
        colors = {
            "Low": ("#FEE2E2", "#EF4444"),
            "OK": ("#DCFCE7", "#22C55E"),
            "Overstock": ("#FEF3C7", "#F59E0B"),
            "Dead Stock": ("#E2E8F0", "#475569"),
        }
        bg, text_color = colors.get(status, ("#E5E7EB", "#374151"))
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=20,
            bgcolor=bg,
            content=ft.Text(
                status,
                size=12,
                weight=ft.FontWeight.W_600,
                color=text_color,
            ),
        )

    # ---------------- Dialogs / actions ----------------

    def _open_add_dialog(self, e):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add product"),
            content=ft.Text("Product creation form will go here."),
            actions=[ft.TextButton("Close", on_click=lambda ev: self._close_dialog())],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _open_edit_dialog(self, item: dict):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit {item['name']}"),
            content=ft.Text("Product edit form will go here."),
            actions=[ft.TextButton("Close", on_click=lambda ev: self._close_dialog())],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _delete_item(self, item: dict):
        # Remove item from list and refresh table
        self.items = [i for i in self.items if i is not item]
        self._render_table(self.items)
        self.page.update()

    # ---------------- Filters / search ----------------

    def _on_search_change(self, e: ft.ControlEvent):
        self._apply_filters()

    def _on_filter_change(self, e: ft.ControlEvent):
        self._apply_filters()

    def _apply_filters(self):
        q = (self.search_field.value or "").lower()
        filtered = [
            i
            for i in self.items
            if q in i["name"].lower()
            or q in i["category"].lower()
            or q in i["status"].lower()
        ]
        self._render_table(filtered)
        self.page.update()

    # ---------------- Mock data (replace with backend) ----------------

    def _mock_items(self):
        return [
            {
                "name": "Wireless Mouse",
                "category": "Electronics",
                "quantity": 5,
                "status": "Low",
                "updated": "2 hours ago",
            },
            {
                "name": "Ergonomic Chair",
                "category": "Furniture",
                "quantity": 45,
                "status": "OK",
                "updated": "1 day ago",
            },
            {
                "name": "Laptop Stand",
                "category": "Accessories",
                "quantity": 8,
                "status": "Low",
                "updated": "3 hours ago",
            },
            {
                "name": "Keyboard Case",
                "category": "Accessories",
                "quantity": 156,
                "status": "Overstock",
                "updated": "5 hours ago",
            },
            {
                "name": "USB Cable",
                "category": "Electronics",
                "quantity": 12,
                "status": "Low",
                "updated": "1 hour ago",
            },
            {
                "name": "Monitor Arm",
                "category": "Furniture",
                "quantity": 34,
                "status": "OK",
                "updated": "2 days ago",
            },
            {
                "name": "Desk Lamp",
                "category": "Lighting",
                "quantity": 2,
                "status": "Dead Stock",
                "updated": "1 week ago",
            },
            {
                "name": "Notebook Pack",
                "category": "Stationery",
                "quantity": 89,
                "status": "OK",
                "updated": "4 hours ago",
            },
        ]

