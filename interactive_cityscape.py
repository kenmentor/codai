import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Interactive City")
root.geometry("600x400")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=600, height=400, bg="#87CEEB")
canvas.pack()

# Function to move the sun
def move_sun(event):
    canvas.coords(sun, event.x - 25, event.y - 25, event.x + 25, event.y + 25)

# Function to change building color when clicked
def change_color(event):
    item = canvas.find_closest(event.x, event.y)
    current_color = canvas.itemcget(item, "fill")
    new_color = "#FF6347" if current_color != "#FF6347" else "#8B4513"
    canvas.itemconfig(item, fill=new_color)

# Draw buildings
building1 = canvas.create_rectangle(50, 250, 150, 400, fill="#8B4513", outline="black")
building2 = canvas.create_rectangle(200, 200, 300, 400, fill="#A0522D", outline="black")
building3 = canvas.create_rectangle(350, 300, 450, 400, fill="#D2691E", outline="black")

# Bind click event to buildings
canvas.tag_bind(building1, '<Button-1>', change_color)
canvas.tag_bind(building2, '<Button-1>', change_color)
canvas.tag_bind(building3, '<Button-1>', change_color)

# Draw windows on buildings
for x in range(60, 150, 30):
    for y in range(260, 400, 30):
        canvas.create_rectangle(x, y, x+20, y+20, fill="yellow", outline="black")

for x in range(210, 300, 30):
    for y in range(210, 400, 30):
        canvas.create_rectangle(x, y, x+20, y+20, fill="yellow", outline="black")

for x in range(360, 450, 30):
    for y in range(310, 400, 30):
        canvas.create_rectangle(x, y, x+20, y+20, fill="yellow", outline="black")

# Draw the sun
sun = canvas.create_oval(500, 50, 550, 100, fill="#FFD700", outline="#FFD700")

# Bind movement event to sun
canvas.tag_bind(sun, '<B1-Motion>', move_sun)

# Draw clouds
canvas.create_oval(100, 50, 170, 80, fill="white", outline="white")
canvas.create_oval(130, 30, 200, 70, fill="white", outline="white")
canvas.create_oval(400, 70, 470, 100, fill="white", outline="white")
canvas.create_oval(430, 50, 500, 90, fill="white", outline="white")

# Run the Tkinter event loop
root.mainloop()
