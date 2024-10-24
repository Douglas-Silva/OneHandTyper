import tkinter as tk

def make_draggable(window):
    window.bind("<ButtonPress-1>", lambda event: on_drag_start(window, event))
    window.bind("<B1-Motion>", lambda event: on_drag_motion(window, event))

def on_drag_start(window, event):
    # position x and y of the cursor relative to the top-left corner of the window:
    window._offset_x = event.x
    window._offset_y = event.y

def on_drag_motion(window, event):
    x = event.x_root - window._offset_x
    y = event.y_root - window._offset_y
    window.geometry(f"+{x}+{y}")

def create_floating_widget(text: str, *, x = 0, y = 0, width = 150, height = 32, text_fill = "white"):
    """ Returns a window with method `set_text(new_text: str)`. """
    
    root = tk.Tk()
    root.overrideredirect(True)
    root.wm_attributes("-toolwindow", 1)  # Hide from Taskbar and Alt+Tab
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.6)
    root.geometry(f'{width}x{height}+{x}+{y}')

    canvas = tk.Canvas(root, bg="black", highlightthickness=1, cursor="fleur")
    canvas.pack(fill="both", expand=True)

    canvas_text = canvas.create_text(8, 16, text=text, fill=text_fill, font=("TkDefaultFont", 14), anchor="w")

    def set_text(new_text):
        canvas.itemconfig(canvas_text, text=new_text)

    make_draggable(root)

    # Add a resize grip (bottom-right corner)
    resize_grip = tk.Label(root, text="⤡", bg="black", fg="white", cursor="size_nw_se")
    resize_grip.place(relx=1.0, rely=1.0, x=-2, y=-2, anchor="se")

    def resize(event):
        w = event.x_root - root.winfo_x()
        h = event.y_root - root.winfo_y()
        if w < 50: w = 50
        if h < 32: h = 32
        root.geometry(f"{w}x{h}")
        return "break"  # Prevent further event propagation

    resize_grip.bind("<B1-Motion>", resize)

    root.set_text = set_text

    return root

def create_problems_window(problems: list[str]):
    """ Returns a window with method `set_problems(problems: list[str])`. """

    root = create_text_window("Problems", problems)
    root.set_problems = root.set_lines
    return root

def create_keys_data_window():
    """ Returns a window with method `prepend_key_data(line: str)`. """

    root = create_text_window("Keys Data", ["Press keys to show their data."])
    root.prepend_key_data = root.prepend_line
    return root

def create_text_window(window_title: str, lines: list[str]):
    """ Returns a window with methods `set_lines(lines: list[str])` and `prepend_line(line: str)`. """

    def set_lines(lines: list[str]):
        lines_text.config(state=tk.NORMAL)
        lines_text.delete("1.0", tk.END)
        lines_text.insert(tk.END, '\n\n'.join(lines))
        lines_text.config(state=tk.DISABLED)

    def prepend_line(line: str):
        lines_text.config(state=tk.NORMAL)
        lines_text.insert("1.0", line + '\n')
        lines_text.config(state=tk.DISABLED)

    def get_content():
        return lines_text.get("1.0", tk.END)

    root = tk.Tk()
    root.geometry('800x400')
    root.title(window_title)

    # Create a Text widget to display lines (set state to DISABLED)
    lines_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
    lines_text.pack(padx=10, pady=10, fill='both', expand=True)

    set_lines(lines)

    root.set_lines = set_lines
    root.prepend_line = prepend_line
    root.get_content = get_content
    root.deiconify()
    root.focus_force()
    
    return root