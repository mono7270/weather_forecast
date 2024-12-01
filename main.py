import json
import requests
import tkinter as tk
from tkinter import ttk


class Main:
    def __init__(self):
        # 全地方
        self.regions = {
            "北海道": {
                "宗谷地方": "011000",
                "上川・留萌地方": "012000",
                "網走・北見・紋別地方": "013000",
                "胆振・日高地方": "014030",
                "釧路・根室地方": "014100",
                "石狩・空知・後志地方": "016000",
                "渡島・檜山地方": "017000",
            },
            "東北地方": {
                "青森県": "020000",
                "岩手県": "030000",
                "宮城県": "040000",
                "秋田県": "050000",
                "山形県": "060000",
                "福島県": "070000",
            },
            "関東地方": {
                "茨城県": "080000",
                "栃木県": "090000",
                "群馬県": "100000",
                "埼玉県": "110000",
                "千葉県": "120000",
                "東京都": "130000",
                "神奈川県": "140000",
            },
            "中部地方": {
                "新潟県": "150000",
                "富山県": "160000",
                "石川県": "170000",
                "福井県": "180000",
                "山梨県": "190000",
                "長野県": "200000",
                "岐阜県": "210000",
                "静岡県": "220000",
                "愛知県": "230000",
            },
            "近畿地方": {
                "三重県": "240000",
                "滋賀県": "250000",
                "京都府": "260000",
                "大阪府": "270000",
                "兵庫県": "280000",
                "奈良県": "290000",
                "和歌山県": "300000",
            },
            "中国地方": {
                "鳥取県": "310000",
                "島根県": "320000",
                "岡山県": "330000",
                "広島県": "340000",
                "山口県": "350000",
            },
            "四国地方": {
                "徳島県": "360000",
                "香川県": "370000",
                "愛媛県": "380000",
                "高知県": "390000",
            },
            "九州地方": {
                "福岡県": "400000",
                "佐賀県": "410000",
                "長崎県": "420000",
                "熊本県": "430000",
                "大分県": "440000",
                "宮崎県": "450000",
                "鹿児島県": "460100",
            },
            "沖縄": {
                "沖縄本島": "471000",
                "大東島": "472000",
                "宮古島": "473000",
                "八重山": "474000",
            },
        }

        self.date = ["今日", "明日", "明後日"]

        self.root = tk.Tk()
        self.root.geometry("2500x1000")
        self.root.resizable(False, False)
        self.root.title("天気予報")

        # スタイルの設定
        style = ttk.Style()

        # 表のスタイル
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="black",
            rowheight=50,
            fieldbackground="white",
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "lightgray")],
            foreground=[("selected", "black")],
        )

        # labelのスタイル
        style.configure("Custom.TLabel", foreground="black")

        # メニュー
        menu_frame = ttk.Frame(self.root, width=300, height=600)

        # 地方のセレクトボックス
        region_text = ttk.Label(menu_frame, text="地方", style="Custom.TLabel")
        self.region_keys = list(self.regions.keys())
        self.regions_combobox = ttk.Combobox(
            menu_frame, values=self.region_keys, width=10, state="readonly"
        )
        self.regions_combobox.set("----------")
        self.regions_combobox.bind("<<ComboboxSelected>>", self.change_region)

        # 都道府県名のセレクトボックス
        prefecture_text = ttk.Label(menu_frame, text="都道府県", style="Custom.TLabel")
        self.prefectures_combobox = ttk.Combobox(menu_frame, width=10, state="readonly")
        self.prefectures_combobox.set("----------")
        self.prefectures_combobox.bind("<<ComboboxSelected>>", self.fetch_weather)

        # 天気予報
        forecast_frame = ttk.Frame(self.root)

        # 地域の表示
        self.area = tk.StringVar()
        display_area = ttk.Label(
            forecast_frame, textvariable=self.area, style="Custom.TLabel"
        )

        # 天気予報一覧表
        self.weather_tree = ttk.Treeview(
            forecast_frame,
            columns=("date", "area", "weather", "wind"),
            show="headings",
            height=12,
            style="Custom.Treeview",
        )

        self.weather_tree.column("date", width=100)
        self.weather_tree.column("area", width=200)
        self.weather_tree.column("weather", width=1000)
        self.weather_tree.column("wind", width=1000)

        self.weather_tree.heading("date", text="日付", anchor=tk.W)
        self.weather_tree.heading("area", text="地域", anchor=tk.W)
        self.weather_tree.heading("weather", text="天気", anchor=tk.W)
        self.weather_tree.heading("wind", text="風", anchor=tk.W)

        # 配置
        self.root.grid_columnconfigure(0, weight=1)

        # 全体
        menu_frame.grid(row=0, column=0, pady=5)
        forecast_frame.grid(row=1, column=0, pady=5)

        # メニュー
        region_text.grid(row=0, column=0, padx=5)
        self.regions_combobox.grid(row=0, column=1)
        prefecture_text.grid(row=0, column=2, padx=5)
        self.prefectures_combobox.grid(row=0, column=3)

        # 天気予報
        display_area.grid(row=0, column=0, pady=5)
        self.weather_tree.grid(row=1, column=0, pady=5)

    def change_region(self, event):
        """
        セレクトボックスで地方を選択する
        """
        self.prefectures_combobox["values"] = list(
            self.regions[event.widget.get()].keys()
        )
        self.prefectures_combobox.set("----------")

    def fetch_weather(self, event):
        """
        セレクトボックスで選択した都市の
        3日間の天気予報を表示する
        """
        for item in self.weather_tree.get_children():
            self.weather_tree.delete(item)

        base_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

        select_code = self.regions[self.regions_combobox.get()][event.widget.get()]

        url = f"{base_url}{select_code}.json"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = json.loads(response.text)

            self.area.set(f"{event.widget.get()}の天気予報")

            for i in range(len(json_data[0]["timeSeries"][0]["timeDefines"])):
                for j in range(len(json_data[0]["timeSeries"][0]["areas"])):
                    self.weather_tree.insert(
                        "",
                        "end",
                        values=(
                            self.date[i],
                            json_data[0]["timeSeries"][0]["areas"][j]["area"]["name"],
                            json_data[0]["timeSeries"][0]["areas"][j]["weathers"][i],
                            json_data[0]["timeSeries"][0]["areas"][j]["winds"][i],
                        ),
                    )
        else:
            self.area.set("情報を取得できませんでした。")


if __name__ == "__main__":
    main = Main()
    main.root.mainloop()
