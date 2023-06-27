import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import re

list_stock_codes = []
df_hose_tickers = pd.read_csv('../data/tickers/hose_tickers.csv')
df_hnx_tickers = pd.read_csv('../data/tickers/hnx_tickers.csv')
df_uc_tickers = pd.read_csv('../data/tickers/uc_tickers.csv')
list_stock_codes.extend(df_hose_tickers['Stock Code'].tolist())
list_stock_codes.extend(df_hnx_tickers['Stock Code'].tolist())
list_stock_codes.extend(df_uc_tickers['Stock Code'].tolist())
print('qcg'.upper() in list_stock_codes)


def predict_label(text, tags):
    # if tag contain stock code then return it
    for tag in tags:
        if tag.upper() in list_stock_codes:
            return str(tag).upper()
    matches = re.findall(r"\(Mã: ([A-Z]{3})\)", text)
    print(matches)
    if len(matches) > 3:
        return ""
    for match in matches:
        if match in list_stock_codes:
            return str(match).upper()
    return ""


class DataVisualizer:
    def __init__(self, data, root):
        self.data = data
        self.index = 0
        self.root = root
        self.init_text = "VIC"

        self.title_text = Text(height=2, width=100, font=("Times New Roman", 12), state=DISABLED)
        self.content_text = ScrolledText(height=20, width=100, font=("Times New Roman", 12), state=DISABLED)
        self.tag_text = Text(height=1, width=100, font=("Times New Roman", 12), state=DISABLED)
        self.label_entry = Entry(width=50)

        self.setup_gui()
        self.load_item()

    def setup_gui(self):
        self.root.title("Hand label")
        self.root.geometry("800x600+160+10")  # Change the numbers as needed

        title_frame = Frame(self.root)
        title_frame.pack(fill=BOTH, expand=True)
        Label(title_frame, text="Title").pack()
        self.title_text.pack()

        content_frame = Frame(self.root)
        content_frame.pack(fill=BOTH, expand=True)
        Label(content_frame, text="Content").pack()
        self.content_text.pack()

        tag_frame = Frame(self.root)
        tag_frame.pack(fill=X, expand=True)
        Label(tag_frame, text="Tags").pack()
        self.tag_text.pack(fill=X, expand=True)

        label_frame = Frame(self.root)
        label_frame.pack(fill=BOTH, expand=True)
        Label(label_frame, text="Label").pack(side=LEFT)
        self.label_entry.pack(pady=(0, 40))

        Button(label_frame, text="Save Changes", command=self.save_changes).pack(side=RIGHT)

        self.root.bind('<Return>', lambda event: self.save_changes())
        self.root.bind('<Right>', lambda event: self.next_item())
        self.root.bind('<Left>', lambda event: self.previous_item())  # Bind left arrow to go back to the previous item

    def load_item(self):
        item = self.data[self.index]
        self.title_text.config(state=NORMAL)
        self.title_text.delete('1.0', END)
        self.title_text.insert('1.0', item["Title"])
        self.title_text.config(state=DISABLED)

        self.content_text.config(state=NORMAL)
        self.content_text.delete('1.0', END)
        self.content_text.insert('1.0', item["Content"])
        self.content_text.config(state=DISABLED)

        self.tag_text.config(state=NORMAL)
        self.tag_text.delete('1.0', END)
        self.tag_text.insert('1.0', ', '.join(item["Tags"]))
        self.tag_text.config(state=DISABLED)

        self.label_entry.delete(0, END)
        self.label_entry.insert(0, str(predict_label(item["Content"], item["Tags"])))

    def save_changes(self):
        self.data[self.index]["Label"] = self.label_entry.get()
        print("Saved changes")

    def next_item(self):
        self.index += 1
        if self.index < len(self.data):
            self.load_item()
        return "break"

    def previous_item(self):  # This method will load the previous item
        if self.index > 0:
            self.index -= 1
            self.load_item()
        return "break"


with open('../data/contents/data_vietnambiz_1_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

root = Tk()
app = DataVisualizer(data, root)
root.mainloop()
