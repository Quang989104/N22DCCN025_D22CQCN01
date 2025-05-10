import tkinter as tk

# Hàm vẽ nền gradient
def draw_gradient(canvas, root, color1, color2):
    steps = 100
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    r_ratio = (r2 - r1) / steps
    g_ratio = (g2 - g1) / steps
    b_ratio = (b2 - b1) / steps

    for i in range(steps):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_rectangle(0, i*5, 600, (i+1)*5, outline="", fill=color)

# Hàm tạo nút chung
def create_button(root, text, y_pos, command):
    btn = tk.Button(root, text=text, font=("Helvetica", 16, "bold"),
                    bg="white", fg="#333", width=20, height=2, command=command,
                    relief="raised", bd=4, activebackground="#ff4081", activeforeground="white")
    btn.place(relx=0.5, y=y_pos, anchor="center")
    return btn
