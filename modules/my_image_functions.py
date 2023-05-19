''' Example Usage:
from displayio import Group
from my_image_functions import draw_background_color, draw_text, draw_image
image_buffer = Group()
image_buffer.append(draw_background_color(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, color=0xff0000))
image_buffer.append(draw_image('/display-ruler.bmp', x=20, y=20))
image_buffer.append(draw_text(string="Hello World!", scale=3, x=20, y=int(DISPLAY_HEIGHT/2), color=0x000000))
display.show(image_buffer)
display.refresh()
'''

# Set a background
def draw_background_color(width=None, height=None, color=0xffffff):
    from displayio import Bitmap, Palette, TileGrid
    background_bitmap = Bitmap(width, height, 1)
    palette = Palette(1)  # Map colors in a palette
    palette[0] = color    # Background Color
    return TileGrid(background_bitmap, pixel_shader=palette)  # Create a Tilegrid with the background


# Draw simple text using the built-in font into a displayio group
def draw_text(string='No Text', scale=2, x=20, y=20, color=0x000000, font=None):
    from displayio import Group
    from adafruit_display_text import label
    if font:
        from adafruit_bitmap_font import bitmap_font
        font_library = bitmap_font.load_font(font)  # i.e. font="/Helvetica-Bold-16.bdf"
    else:
        from terminalio import FONT
        font_library = FONT
    text_group = Group(scale=scale, x=x, y=y)
    text_area = label.Label(font_library, text=string, color=color)
    text_group.append(text_area)  # Add this text to the text group
    return text_group

# Display Image
def draw_image(filename=None, x=0, y=0):
    from displayio import OnDiskBitmap, TileGrid
    f = open(filename, "rb")
    pic = OnDiskBitmap(f)
    return TileGrid(pic, pixel_shader=pic.pixel_shader, x=x, y=y)
    
