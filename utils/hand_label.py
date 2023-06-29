import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText


class DataVisualizer:
    def __init__(self, data, root, filepath):
        self.data = data
        self.index = 0
        self.root = root
        self.filepath = filepath
        self.title_text = Text(height=2, width=100, font=("Times New Roman", 12), state=DISABLED)
        self.content_text = ScrolledText(height=20, width=100, font=("Times New Roman", 12), state=DISABLED, wrap=WORD)
        self.tag_text = Text(height=1, width=100, font=("Times New Roman", 12), state=DISABLED)
        self.index_text = Text(height=1, width=1, font=("Times New Roman", 12), state=DISABLED)
        self.word_count = Text(height=1, width=1, font=("Times New Roman", 12), state=DISABLED)
        self.labeled_item = Text(height=1, width=1, font=("Times New Roman", 12), state=DISABLED)
        self.label_entry = Entry(width=50)
        self.goto_entry = Entry(width=10)  # for inputting the index to go to
        self.goto_button = Button(text="Go to index", command=self.goto_item)  # the button to trigger the jump
        self.save_changes_button = Button(text="Save Change", command=self.save_change)
        self.quit_button = Button(text="Quit", command=self.save_to_file)
        self.setup_gui()
        self.load_item()

    def setup_gui(self):
        self.root.title("Hand label")
        self.root.geometry("1000x600+160+10")

        # self.goto_button.place(x=910, y=120, width=70, height=25)
        # self.goto_entry.place(x=930, y=90, width=30, height=25)
        # self.index_text.place(x=910, y=30, width=80, height=25)
        # Label(text="Word Count").place(x=910, y=250, width=70, height=25)
        # self.word_count.place(x=930, y=280, width=40, height=25)

        # self.goto_button.grid(row=0, column=3)
        # self.root.grid_columnconfigure(3, minsize=100)
        # self.goto_entry.grid(row=1, column=3)
        # self.index_text.grid(row=2, column=3)
        # Label(text="Word Count").grid(row=3, column=3)
        # self.word_count.grid(row=4, column=3)
        main_frame = Frame(self.root, width=850)
        main_frame.pack(side=LEFT, expand=True, fill=BOTH)
        right_frame = Frame(self.root, width=150)  # Added a background color for visibility
        right_frame.pack(side=RIGHT, fill=BOTH)

        index_frame = Frame(right_frame, width=150)
        index_frame.pack(fill=Y, expand=True)
        Label(index_frame, text="Index:", width=20).pack()
        self.index_text = Text(index_frame, height=1, width=5, font=("Times New Roman", 12), state=DISABLED)
        self.index_text.pack()
        Label(index_frame, text="\nGo to index:", width=20).pack()
        self.goto_entry = Entry(index_frame, width=10)
        self.goto_entry.pack()
        self.goto_button = Button(index_frame, text="Go", command=self.goto_item)
        self.goto_button.pack()
        Label(index_frame, text="\n\nWord Count").pack()
        self.word_count = Text(index_frame, height=1, width=5, font=("Times New Roman", 12), state=DISABLED)
        self.word_count.pack()

        Label(index_frame, text="\n\nLabeled Item:").pack()
        self.labeled_item = Text(index_frame, height=1, width=10, font=("Times New Roman", 12), state=DISABLED)
        self.labeled_item.config(state=NORMAL)
        self.labeled_item.insert('1.0', "{}/{}".format(labeled, total_item))
        self.title_text.config(state=DISABLED)
        self.labeled_item.pack()

        title_frame = Frame(main_frame)
        title_frame.pack(fill=BOTH, expand=True)
        Label(title_frame, text="Title").pack()
        self.title_text.pack()

        content_frame = Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True)
        Label(content_frame, text="Content").pack()
        self.content_text.pack()

        tag_frame = Frame(main_frame)
        tag_frame.pack(fill=BOTH, expand=True)
        # Label(tag_frame, text="Tags").pack(side=LEFT)
        self.tag_text.pack(fill=X, expand=True)

        label_frame = Frame(main_frame)
        label_frame.pack(fill=BOTH, expand=True)
        # Label(label_frame, text="Label").pack()
        self.label_entry.pack()
        self.save_changes_button.pack()
        self.quit_button.pack(side=RIGHT)

        self.root.bind('<Return>', lambda event: self.save_change())
        self.root.bind('<Right>', lambda event: self.next_item())
        self.root.bind('<Left>', lambda event: self.previous_item())

    def load_item(self):
        item = self.data[self.index]
        self.title_text.config(state=NORMAL)
        self.title_text.delete('1.0', END)
        self.title_text.insert('1.0', item["Title"])
        self.title_text.config(state=DISABLED)

        self.index_text.config(state=NORMAL)
        self.index_text.delete('1.0', END)
        self.index_text.insert('1.0', str(item["Index"]))
        self.index_text.config(state=DISABLED)

        self.word_count.config(state=NORMAL)
        self.word_count.delete('1.0', END)
        self.word_count.insert('1.0', count_words(item["Content"]))
        self.word_count.config(state=DISABLED)

        self.content_text.config(state=NORMAL)
        self.content_text.delete('1.0', END)
        self.content_text.insert('1.0', item["Content"])
        self.content_text.config(state=DISABLED)

        self.tag_text.config(state=NORMAL)
        self.tag_text.delete('1.0', END)
        self.tag_text.insert('1.0', ', '.join(item["Tags"]))
        self.tag_text.config(state=DISABLED)

        self.label_entry.delete(0, END)
        self.label_entry.insert(0, item['Label'])

    def save_change(self):
        self.data[self.index]["Label"] = self.label_entry.get()
        print("Saved change")

    def save_to_file(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print("Saved data to file")
        self.root.destroy()

    def next_item(self):
        self.index += 1
        if self.index < len(self.data):
            self.load_item()
        return "break"

    def previous_item(self):
        if self.index > 0:
            self.index -= 1
            self.load_item()
        return "break"

    def goto_item(self):
        try:
            index = int(self.goto_entry.get())
            if 0 <= index < len(self.data):
                self.index = index
                self.load_item()
            else:
                print(f"Invalid index: {index}. Please enter a number between 0 and {len(self.data) - 1}.")
        except ValueError:
            print(f"Invalid input: {self.goto_entry.get()}. Please enter a number.")


def count_words(text):
    word_count = 0
    words = text.split()
    for word in words:
        # Exclude punctuation marks from the word count
        if not word.strip(".,;?!-"):
            continue
        word_count += 1
    return word_count


def hand_label(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    global labeled
    global total_item
    for d in data:
        if d['Label'] != "":
            labeled += 1
    total_item = len(data)
    root = Tk()
    app = DataVisualizer(data, root, filepath=filepath)
    root.mainloop()


labeled = 0
total_item = 0
hand_label(filepath="../data/contents/data_vietnambiz_1_1.json")
