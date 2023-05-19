

# Set a background
def draw_background_color(width=None, height=None, color=0xffffff):
    from displayio import Bitmap, Palette, TileGrid
    background_bitmap = Bitmap(width, height, 1)
    palette = Palette(1)  # Map colors in a palette
    palette[0] = color    # Background Color
    return TileGrid(background_bitmap, pixel_shader=palette)  # Create a Tilegrid with the background


# Draw simple text using the built-in font into a displayio group
def draw_text(string='No Text', scale=2, x=20, y=20, color=0x000000):
    from displayio import Group
    from adafruit_display_text import label
    from terminalio import FONT
    text_group = Group(scale=scale, x=x, y=y)
    text_area = label.Label(FONT, text=string, color=color)
    text_group.append(text_area)  # Add this text to the text group
    return text_group

# Display Image
def draw_image(filename=None, x=0, y=0):
    from displayio import OnDiskBitmap, TileGrid
    f = open(filename, "rb")
    pic = OnDiskBitmap(f)
    return TileGrid(pic, pixel_shader=pic.pixel_shader, x=x, y=y)
    
