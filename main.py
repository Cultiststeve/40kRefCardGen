from PIL import Image, ImageDraw, ImageFont
import textwrap

# Define Strings
# cardTypes = ['Order', 'Stratagem']

contentOrders = [
    {"title": "Bring it Down!",
     "rules": "Re-roll wound rolls of 1 for all the models in the ordered unit until the end of the phase."},
    {"title": "Fix Bayonets!",
     "rules": "This order can only be issued to units that are within 1\" of an enemy unit. The ordered unit immediately fights as if it were the Fight phase."}]
orders = {"name": "Order", "content": contentOrders}

contentStratagem = [{"title": "Preliminary Bombardment", "rules": "Do a shoot"},
                    {"title": "Defensive Gunners", "rules": "Do a defensive shoot"}]
stratagem = {"name": "Stratagem", "content": contentStratagem}

contentPsychic = [
    {"title": "Wizard Hat",
     "rules": "I put on my robe and wizard hat"}
]
psychic = {"name": "Psychic Power", "content": contentPsychic}

cards = [orders, stratagem, psychic]

# Define other constants
# backgroundFilePath = "KriegGrenadierBackground.jpg"
backgroundFilePath = "KriegPlatoonBackground.jpg"
background = Image.open(backgroundFilePath).convert('RGBA')

fontFile = "40kFont.TTF"
fontCardType = ImageFont.truetype(fontFile, 60)
fontRules = ImageFont.truetype(fontFile, 50)
fontTitle = ImageFont.truetype(fontFile, 100)
fontsDict = {"cardType": fontCardType,
             "rules": fontRules,
             "title": fontTitle}

y_card_pos = 50
y_rules_pos = 400
y_title_pos = 130
margins = 40

# Colors
black = (0, 0, 0)
grey = (50, 50, 50)
transparent = (255, 255, 255, 0)

# Values
background_transparency = 160
borderSizeVertical = 30  # Larger = smaller proportion is border
borderSizeHorizontal = 35


def get_total_card_count():
    # TODO group card types
    # TODO use cardTypes text + dynamicaly gen name for dicts
    return len(contentOrders) + len(contentStratagem)


def get_text_x_pos(string="", text_type=None):
    if text_type is None:
        raise Exception("Need a cardType")

    width = fontsDict[text_type].getsize(string)[0]
    return get_text_midpoint_width(width)


def get_text_midpoint_width(text_width):
    return background.size[0] / 2 - text_width / 2


def main():
    # For each card type to make
    for i in range(0, len(cards)):
        cardType = cards[i]
        print("\n\nCard type name : " + cardType["name"])



        # Make blank image for text, sets color of background inc transparance
        image_card_type_text = Image.new('RGBA', background.size, (255, 255, 255, background_transparency))
        imageDrawObject_card_type_text = ImageDraw.Draw(image_card_type_text)
        # Draw title
        type_string = cardType["name"]
        x_pos = get_text_x_pos(string=type_string, text_type="cardType")
        imageDrawObject_card_type_text.text((x_pos, y_card_pos), type_string, font=fontCardType, fill=grey)
        # Add card type text to final
        card_outline = Image.alpha_composite(background, image_card_type_text)

        #Draw borders
        image_borders = Image.new('RGBA', background.size, (255, 255, 255, 0))
        imageDrawObject_borders = ImageDraw.Draw(image_borders)
        imageDrawObject_borders.rectangle(((0, 0), (background.size[0]/borderSizeVertical, background.size[1])), fill=black)
        imageDrawObject_borders.rectangle(((background.size[0]*((borderSizeVertical-1)/borderSizeVertical), 0), background.size), fill=black)
        imageDrawObject_borders.rectangle(((0,0),(background.size[0],background.size[1]/borderSizeHorizontal)), fill=black)
        imageDrawObject_borders.rectangle(((0, background.size[1]*(borderSizeHorizontal-1)/borderSizeHorizontal),(background.size[0],background.size[1])), fill=black)
        card_outline = Image.alpha_composite(card_outline, image_borders)


        # For each card of that type
        for j in range(0, len(cardType["content"])):
            current_card = card_outline
            content = cardType["content"][j]
            print("Card content title: " + content["title"])

            # Add Title
            string_title = content["title"]
            lines = textwrap.wrap(string_title, width=18)
            print(lines)
            y_text = y_title_pos
            for line in lines:
                height = fontsDict["title"].getsize(line)[1]
                x_text = get_text_x_pos(line, "title")
                image_title_text = Image.new('RGBA', background.size, (255, 255, 255, 0))
                imageDrawObject_title_text = ImageDraw.Draw(image_title_text)
                imageDrawObject_title_text.text((x_text, y_text), line, font=fontTitle, fill=black)
                current_card = Image.alpha_composite(current_card, image_title_text)
                y_text += height

            current_card = Image.alpha_composite(current_card, image_title_text)

            # Print rules on card
            string_rules = content["rules"]
            lines = textwrap.wrap(string_rules, width=40)
            y_text = y_rules_pos
            for line in lines:
                print("Line: " + line)
                height = fontsDict["rules"].getsize(line)[1]
                x_text = get_text_x_pos(line, "rules")
                image_rules_text_line = Image.new('RGBA', background.size, (255, 255, 255, 0))
                imageDrawObject_rules_text = ImageDraw.Draw(image_rules_text_line)
                imageDrawObject_rules_text.text((x_text, y_text), line, font=fontsDict["rules"], fill=black)
                current_card = Image.alpha_composite(current_card, image_rules_text_line)
                y_text += height

            # Finaly, save file
            # final = Image.alpha_composite(card_with_type_text, image_rules_text_line)
            current_card.save(fp="output/" + cardType["name"] + content["title"].replace(' ', '') + '.png')

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
