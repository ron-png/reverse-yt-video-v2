'''# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Open an Image
img = Image.open('RYeb4C_zyro-HD.jpg')

# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

# Custom font style and font size
myFont = ImageFont.truetype('impact.ttf', 150)

# Add Text to an image
I1.text((10, 10), "but backwards", font=myFont, fill =(255, 255, 255))

# Display edited image
img.show()

# Save the edited image
img.save("edited_image.jpg")
'''


# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Open an Image
img = Image.open('RYeb4C_zyro-HD.jpg')

# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

# Custom font style and font size
myFont = ImageFont.truetype('impact.ttf', 150)

# Define text position
text_position = (10, 10)
text = "but backwards"

# Outline color and fill color
outline_color = (0, 0, 0)  # Black
fill_color = (255, 255, 255)  # White

# Draw outline by drawing text multiple times with slight offsets
offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
for offset in offsets:
    I1.text((text_position[0] + offset[0], text_position[1] + offset[1]), text, font=myFont, fill=outline_color)

# Draw the text in the desired fill color
I1.text(text_position, text, font=myFont, fill=fill_color)

# Display edited image
img.show()

# Save the edited image
img.save("edited_image.jpg")