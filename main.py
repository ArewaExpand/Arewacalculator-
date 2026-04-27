from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView

class ProfitCalculator(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.history_list = []

        # AppBar
        self.toolbar = MDTopAppBar(
            title="Profit/Loss Calculator",
            pos_hint={"top": 1},
            elevation=10,
        )
        self.add_widget(self.toolbar)

        # Layout
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15, pos_hint={"top": 0.9})

        # Pair buttons
        pair_buttons = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        for pair in ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"]:
            btn = MDRaisedButton(text=pair, on_release=lambda x, p=pair: self.set_pair(p))
            pair_buttons.add_widget(btn)
        self.layout.add_widget(pair_buttons)

        # Show selected pair
        self.selected_pair = MDTextField(
            hint_text="Pair da aka zaɓa",
            readonly=True,
            mode="rectangle"
        )
        self.layout.add_widget(self.selected_pair)

        # Input fields
        self.entry_price = MDTextField(hint_text="Entry Price", input_filter="float", mode="rectangle")
        self.tp_price = MDTextField(hint_text="Take Profit (TP)", input_filter="float", mode="rectangle")
        self.sl_price = MDTextField(hint_text="Stop Loss (SL)", input_filter="float", mode="rectangle")
        self.lot_size = MDTextField(hint_text="Lot Size (e.g., 0.01)", input_filter="float", mode="rectangle")

        # Result label
        self.result_label = MDLabel(
            text="Saka bayanai don lissafi",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=100
        )

        # Button
        self.calculate_button = MDRaisedButton(
            text="Lissafa",
            on_release=self.calculate_profit_loss,
            pos_hint={"center_x": 0.5}
        )

        # History
        self.history_view = MDScrollView()
        self.history_box = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.history_box.bind(minimum_height=self.history_box.setter('height'))
        self.history_view.add_widget(self.history_box)

        # Add widgets
        for widget in [
            self.entry_price, self.tp_price,
            self.sl_price, self.lot_size, self.calculate_button,
            self.result_label, self.history_view
        ]:
            self.layout.add_widget(widget)

        self.add_widget(self.layout)

    def set_pair(self, pair):
        self.selected_pair.text = pair

    def calculate_profit_loss(self, instance):
        try:
            pair = self.selected_pair.text
            entry = float(self.entry_price.text)
            tp = float(self.tp_price.text)
            sl = float(self.sl_price.text)
            lot = float(self.lot_size.text)

            # Pip calculation logic
            if "JPY" in pair:
                pip_multiplier = 100  # 1 pip = 0.01
            elif "BTC" in pair:
                pip_multiplier = 1    # Crypto: use price diff as is
            else:
                pip_multiplier = 10000  # 1 pip = 0.0001

            profit_pips = abs(tp - entry) * pip_multiplier
            loss_pips = abs(entry - sl) * pip_multiplier
            pip_value = 10 * lot

            profit_usd = profit_pips * pip_value / 10
            loss_usd = loss_pips * pip_value / 10
            rr_ratio = round(profit_usd / loss_usd, 2) if loss_usd != 0 else "∞"

            result_text = (
                f"[b]Riba:[/b] ${profit_usd:.2f}\n"
                f"[b]Asara:[/b] ${loss_usd:.2f}\n"
                f"[b]Risk/Reward:[/b] {rr_ratio}"
            )
            self.result_label.text = result_text

            # Add to history
            item_text = f"{pair} | Entry: {entry}, TP: {tp}, SL: {sl}, Lot: {lot} → RR: {rr_ratio}"
            self.history_box.add_widget(
                OneLineListItem(text=item_text)
            )
        except Exception:
            self.result_label.text = "⚠️ Kuskure a bayanan da ka shigar."

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        return ProfitCalculator()

MainApp().run()
