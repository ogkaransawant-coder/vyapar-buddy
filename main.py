import flet as ft
from screens.login import LoginPage
from screens.dashboard import DashboardPage
from screens.chat import ChatPage
from screens.inventory import InventoryPage
from screens.alerts import AlertsPage
from screens.analytics import AnalyticsPage
from screens.settings import SettingsPage


NAV_ITEMS = [
    {"label": "Chat", "target": "chat", "icon": ft.Icons.CHAT_BUBBLE_OUTLINE},
    {"label": "Dashboard", "target": "dashboard", "icon": ft.Icons.DASHBOARD_OUTLINED},
    {"label": "Inventory", "target": "inventory", "icon": ft.Icons.INVENTORY_2_OUTLINED},
    {"label": "Alerts", "target": "alerts", "icon": ft.Icons.WARNING_AMBER_OUTLINED},
    {"label": "Analytics", "target": "analytics", "icon": ft.Icons.SHOW_CHART},
    {"label": "Settings", "target": "settings", "icon": ft.Icons.SETTINGS_OUTLINED},
]


def main(page: ft.Page):
    # Global page config
    page.title = "Vyapaar Buddy"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(use_material3=True)
    page.adaptive = True
    page.window_maximized = True
    page.padding = 0
    page.scroll = "auto"

    # Initial route / session
    page.session.set("screen", "login")

    # ----------------- Navigation helpers -----------------

    def set_screen(target: str):
        page.session.set("screen", target)
        if target == "login":
            page.go("/login")
        else:
            page.go(f"/{target}")

    def load_screen(name: str, page: ft.Page) -> ft.Control:
        return {
            "dashboard": DashboardPage(page=page),
            "chat": ChatPage(page=page),
            "inventory": InventoryPage(page=page),
            "alerts": AlertsPage(page=page),
            "analytics": AnalyticsPage(page=page),
            "settings": SettingsPage(page=page),
        }.get(name, ft.Column(controls=[ft.Text("Page not found")]))

    # ----------------- Layout builder -----------------

    def build_shell(content: ft.Control) -> ft.Control:
        """
        Shell layout that adapts to screen size:
        - Desktop / tablet: persistent left sidebar
        - Mobile: top app bar + bottom navigation bar
        """
        is_mobile = page.width is not None and page.width < 800

        if is_mobile:
            # Mobile layout: content + bottom navigation
            return ft.View(
                route=page.route,
                padding=0,
                bgcolor="#000000",
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            # Top app bar
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                                bgcolor="#020617",
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Row(
                                            spacing=10,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Image(
                                                    src="assets/logo.png",
                                                    width=32,
                                                    height=32,
                                                    fit=ft.ImageFit.CONTAIN,
                                                ),
                                                ft.Text(
                                                    "Vyapaar Buddy",
                                                    size=18,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.LOGOUT,
                                            tooltip="Logout",
                                            on_click=lambda _: set_screen("login"),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Divider(height=1, color="#1E293B"),
                            # Page content
                            ft.Container(
                                expand=True,
                                padding=16,
                                bgcolor="#020617",
                                content=content,
                            ),
                        ],
                    ),
                ],
                bottom_appbar=ft.Container(
                    bgcolor="#020617",
                    content=ft.NavigationBar(
                        selected_index=_get_nav_index(page.session.get("screen")),
                        destinations=[
                            ft.NavigationDestination(
                                icon=item["icon"], label=item["label"]
                            )
                            for item in NAV_ITEMS
                        ],
                        on_change=lambda e: set_screen(
                            NAV_ITEMS[e.control.selected_index]["target"]
                        ),
                    ),
                ),
            )

        # Desktop / tablet layout: persistent sidebar
        return ft.View(
            route=page.route,
            padding=0,
            bgcolor="#020617",
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Container(
                            width=260,
                            bgcolor="#020617",
                            padding=16,
                            content=NavigationMenu(
                                page=page,
                                active_screen=page.session.get("screen"),
                                on_change=set_screen,
                            ),
                        ),
                        ft.VerticalDivider(width=1, color="#1E293B"),
                        ft.Container(
                            expand=True,
                            padding=16,
                            bgcolor="#020617",
                            content=content,
                        ),
                    ],
                )
            ],
        )

    # ----------------- Route handling -----------------

    def route_change(route):
        page.views.clear()
        current_screen = page.session.get("screen") or "login"

        if current_screen == "login":
            page.views.append(
                ft.View(
                    "/login",
                    padding=0,
                    controls=[LoginPage(page=page)],
                )
            )
        else:
            page.views.append(build_shell(load_screen(current_screen, page)))

        page.update()

    def view_pop(view):
        # Basic back-navigation behavior
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # React to window resize to re-build adaptive layout
    def on_resize(e):
        if page.session.get("screen") != "login":
            route_change(page.route)

    page.on_resize = on_resize

    # Initial entry
    page.go("/login")


# ----------------- Navigation menu component -----------------


class NavigationMenu(ft.Column):
    def __init__(self, page: ft.Page, active_screen: str, on_change):
        super().__init__(
            spacing=10,
            expand=True,
        )
        self.page = page
        self.active_screen = active_screen
        self.on_change = on_change

        header = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="assets/logo.png",
                    width=40,
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(
                            "Vyapaar Buddy",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Smart Inventory Assistant",
                            size=11,
                            color="#9CA3AF",  # GREY-ish
                        ),
                    ],
                ),
            ],
        )

        nav_list = ft.Column(
            spacing=4,
            controls=[
                self._nav_button(item["label"], item["target"], item["icon"])
                for item in NAV_ITEMS
            ],
        )

        logout_btn = self._nav_button("Logout", "login", ft.Icons.LOGOUT)

        self.controls = [
            header,
            ft.Divider(color="#1F2937"),
            nav_list,
            ft.Container(expand=True),  # spacer
            ft.Divider(color="#1F2937"),
            logout_btn,
        ]

    def _nav_button(self, label: str, target: str, icon):
        is_active = target == self.active_screen
        return ft.Container(
            padding=6,
            border_radius=8,
            bgcolor="#0B1220" if is_active else None,
            ink=True,
            on_click=lambda _: self.on_change(target),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        icon,
                        color="#FBBF24" if is_active else "#D1D5DB",  # AMBER / GREY_300
                        size=20,
                    ),
                    ft.Text(
                        label,
                        size=15,
                        weight=ft.FontWeight.W_500
                        if is_active
                        else ft.FontWeight.NORMAL,
                    ),
                ],
            ),
        )


def _get_nav_index(screen: str) -> int:
    for i, item in enumerate(NAV_ITEMS):
        if item["target"] == screen:
            return i
    return 0


ft.app(target=main, assets_dir="assets")
