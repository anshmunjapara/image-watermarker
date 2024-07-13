from tkinter import Label, Tk, Canvas, Button, filedialog, Text
from PIL import Image, ImageTk, ImageDraw, ImageFont


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.minsize(width=1000, height=700)
        self.mouse_x = None
        self.mouse_y = None
        self.text = None
        self.original_image = None
        self.full_quality_image = None
        self.image_file = self.original_image
        self.img = None
        self.image_path = None
        self.font_color = "white"

        self.title = Label(text="Add watermark to your Images", font=("Arial", 24, "bold"))
        self.title.pack()

        self.canvas = Canvas(self, width=800, height=500, bg="white")
        self.canvas.create_text(400, 250, text="Press to add Image", fill="black")
        self.canvas.pack()

        self.place_watermark = Button(text="Place watermark", command=self.track_mouse)
        self.place_watermark.pack()

        self.add_image_btn = Button(text="Add Image", command=self.open_image)
        self.add_image_btn.pack()

        self.text_area = Text(self, height=2, width=20)
        self.text_area.pack()

        self.save_btn = Button(self, text="Save Image", command=self.save_image)
        self.save_btn.pack()

    def set_image_by_path(self, path):
        self.full_quality_image = Image.open(path)
        self.original_image = Image.open(path).resize(
            (700, 400))
        self.img = ImageTk.PhotoImage(self.original_image)

        self.set_image()

    def set_image(self):

        self.canvas.create_image(400, 250, image=self.img)

    def track_mouse(self):
        self.mouse_position_captured = False
        self.canvas.bind("<Button-1>", self.get_mouse_pos)
        self.wait_for_mouse_pos()

    def get_mouse_pos(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        print(self.mouse_x, self.mouse_y)
        self.canvas.unbind("<Button-1>")
        self.mouse_position_captured = True

    def wait_for_mouse_pos(self):
        if not self.mouse_position_captured:
            self.after(100, self.wait_for_mouse_pos)
        else:
            self.place_watermark_at_position()

    def place_watermark_at_position(self):
        self.image_file = self.original_image.copy()
        self.text = self.text_area.get("1.0", 'end-1c')
        if self.text is not None:
            self.draw = ImageDraw.Draw(self.image_file)
            self.font = ImageFont.truetype(font="Arial", size=25)
            self.draw.text((self.mouse_x - 75, self.mouse_y - 70), self.text, font=self.font)
            self.img = ImageTk.PhotoImage(self.image_file)

            self.set_image()

    def open_image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.set_image_by_path(self.image_path)

    def save_image(self):
        self.draw = ImageDraw.Draw(self.full_quality_image)
        self.font = ImageFont.truetype("Arial", 25)
        self.draw.text((self.mouse_x - 75, self.mouse_y - 70), self.text, font=self.font)
        self.full_quality_image.save('water Marked Image.jpg')


main_window = MainWindow()
main_window.mainloop()
