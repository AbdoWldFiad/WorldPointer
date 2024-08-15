from tkinter import Tk, Label
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = None
class MapViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Viewer")
        
        # Load the image
        image = Image.open('map.jpg')

        photo = ImageTk.PhotoImage(image)
        
        # Create a Label widget to display the image
        label = Label(root, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

if __name__ == "__main__":
    root = Tk()
    viewer = MapViewer(root)
    root.mainloop()
