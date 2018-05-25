from PIL import Image, ImageDraw, ImageFont

# Define Strings
# cardTypes = ['Order', 'Stratagem']

contentOrders = [
    {"title": "Bring it Down!", "rules": "Re-roll wound rolls of 1 for all the models in the ordered unit until the end of the phase."},
    {"title": "Fix Bayonets!", "rules": "This order can only be issued to units that are within 1\" of an enemy unit. The ordered unit immediately fights as if it were the Fight phase."}]
orders = {"name": "Order", "content": contentOrders}


contentStratagem = [{"title": "Preliminary Bombardment", "rules": "Do a shoot"},
                   {"title": "Defensive Gunners", "rules": "Do a defensive shoot"}]
stratagem = {"name": "Stratagem", "content": contentStratagem}

cards = [orders, stratagem]

# Define other constants
backgroundFilePath = "KriegGrenadierBackground.jpg"
background = Image.open(backgroundFilePath).convert('RGBA')

fontFile = "40kFont.TTF"
fontCardType = ImageFont.truetype(fontFile, 70)
fontRules = ImageFont.truetype(fontFile, 50)

cardTypeTextYPos = 50
rulesTextYPos = 200

# Colors
black = (0, 0, 0)
transparent = (255, 255, 255, 0)


def get_total_card_count():
    #TODO group card types
    #TODO use cardTypes text + dynamicaly gen name for dicts
    return len(contentOrders) + len(contentStratagem)


def get_card_type_x_pos(string):
    width = fontCardType.getsize(string)[0]
    return get_text_midpoint_width(width)


def get_text_midpoint_width(text_width):
    return background.size[0] / 2 - text_width / 2

def get_text_wrap_num_lines(string):
    return 2


def main():

    # For each card to make
    for i in range(0,len(cards)):
        cardType = cards[i]
        print("Card type name : " + cardType["name"])

        # For each card of that type

        # Make blank image for text, sets color of background inc transparance
        image = Image.new('RGBA', background.size, (225, 225, 225, 200))
        imageDrawObject = ImageDraw.Draw(image)
        # Draw title
        string = cardType["name"]
        imageDrawObject.text((get_card_type_x_pos(string), cardTypeTextYPos), string, font=fontCardType, fill=black)
        # Add card type text to final
        final = Image.alpha_composite(background, image)


        for j in range (0, len(cardType["content"])):
            content = cardType["content"][j]
            print("Card content title: " + content["title"])

            string_rules = content["rules"]

            # TODO workout text wrapping, and do FOR each line
            for k in range (0, get_text_wrap_num_lines(string_rules)):
                print (k)

            imageDrawObject.text((get_card_type_x_pos(string_rules), rulesTextYPos), string_rules, font=fontRules, fill=black)
            final = Image.alpha_composite(final, image)



            # Finaly, save file
            final.save(fp="output/" + cardType["name"] + content["title"].replace(' ','') + '.png')


        # title = Image.new('RGBA', background.size, black)

    #
    # width = fontCardType.getsize(cardTypes[0])[0]
    # cardtype_x_pos = get_text_midpoint_width(width)
    #
    # # Make an blank image and get an ImageDraw Context
    # text = Image.new('RGBA', background.size, (225, 225, 225, 200))
    # d = ImageDraw.Draw(text)
    #
    # # Draw the title
    # d.text((cardtype_x_pos, typeTextYPos), cardTypes[0], font=fontCardType, fill=(0, 0, 0))
    # # Draw Body Text
    # d.text((200, 200), textOrders[0][1], font=fontCardType, fill=(0, 0, 0))
    #
    # # Combine background and text, and output
    # final = Image.alpha_composite(background, text)
    # final.save(fp="marked.png")


# draw = ImageDraw.Draw(background)
# draw.text((50,50), "hello world", fill=(255,255,255), font=font)  # Draw text on a blank
# draw = ImageDraw.Draw(background)
#
# background.save("marked.png")

if __name__ == '__main__':
    main()
