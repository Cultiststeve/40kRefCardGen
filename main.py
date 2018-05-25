from PIL import Image, ImageDraw, ImageFont

# Define Strings
cardTypes = ['Order', 'Stratagem']
textOrders = [
    ["Bring it Down!", "Re-roll wound rolls of 1 for all the models in the ordered unit until the end of the phase."],
    ["Fix Bayonets!", "This order can only be issued to units that are within 1\" of an enemy unit. The ordered unit immediately fights as if it were the Fight phase."]]
textStratagem = [["Preliminary Bombardment", "Do a shoot"],
                 ["Defensive Gunners", "Do a defensive shoot"]]

backgroundFilePath = "KriegGrenadierBackground.jpg"
background = Image.open(backgroundFilePath).convert('RGBA')

fontSize = {'cardType': 50, 'title': 70}
font = ImageFont.truetype("40kFont.TTF", fontSize['cardType'])

typeYPos = 50

# Colors
black = (0, 0, 0)
transparent = (255, 255, 255, 0)

def get_total_card_count():
    #TODO group card types
    #TODO use cardTypes text + dynamicaly gen name for dicts
    return len(textOrders) + len(textStratagem)

def get_text_midpoint_width(text_width):
    return background.size[0] / 2 - text_width / 2


def main():

    # For each card to make
    for i in range(0,len(cardTypes)):
        print("For Card Type: " + cardTypes[i])

        # Create card type title
        text = Image.new('RGBA', background.size, (225, 225, 225, 200))
        title = ImageDraw.Draw(text)


        # title = Image.new('RGBA', background.size, black)


    width = font.getsize(cardTypes[0])[0]
    cardtype_x_pos = get_text_midpoint_width(width)

    # Make an blank image and get an ImageDraw Context
    text = Image.new('RGBA', background.size, (225, 225, 225, 200))
    d = ImageDraw.Draw(text)

    # Draw the title
    d.text((cardtype_x_pos, typeYPos), cardTypes[0], font=font, fill=(0, 0, 0))
    # Draw Body Text
    d.text((200, 200), textOrders[0][1], font=font, fill=(0, 0, 0))

    # Combine background and text, and output
    final = Image.alpha_composite(background, text)
    final.save(fp="marked.png")


# draw = ImageDraw.Draw(background)
# draw.text((50,50), "hello world", fill=(255,255,255), font=font)  # Draw text on a blank
# draw = ImageDraw.Draw(background)
#
# background.save("marked.png")

if __name__ == '__main__':
    main()
