from PIL import Image, ImageDraw, ImageFont
import textwrap

# Define Strings
# cardTypes = ['Order', 'Stratagem']
contentOrders = [
    {"title": "Duty unto death!",
     "rules": "Any Infantry or Cavalry model in the unit that is killed in the Fight phase immediately makes a single attack."},
    {"title": "Without Mercy",
     "rules": "All lasguns and all hot-shot lasguns in the ordered unit change their Type to Pistol 2 until the end of the turn."},
    {"title": "Bring it Down!",
     "rules": "Re-roll wound rolls of 1 for all the models in the ordered unit until the end of the phase."},
    {"title": "Forwards, for the Emperor!",
     "rules": "The ordered unit can shoot this phase even if it Advanced in its Movement phase"},
    {"title": "Get Back in the Fight!",
     "rules": "The ordered unit can shoot this phase, even if it Fell Back in its Movement phase"},
    {"title": "Move! Move! Move!",
     "rules": "Instead of shooting this phase, the ordered unit immediately moves as if it were the Movement phase. It must Advance as part of this move, and cannot declare a charge during this turn."},
    {"title": "Fix Bayonets!",
     "rules": "This order can only be issued to units that are within 1\" of an enemy unit. The ordered unit immediately fights as if it were the Fight phase."}
]
orders = {"name": "Order", "content": contentOrders}
#
# {"title": "",
#  "rules": "",
#  "cost": ""},

contentStratagem = [
    {"title": "Crush them!",
     "rules": "Start of the Charge Phase:\t Select an AM Vehicle unit from your army. This unit can charge even if it Advanced this turn. In the following Fight phase, attacks made by this unit hit on a 2+.",
     "cost": "1 CP"},
    {"title": "Jury Rigging",
     "rules": "Start of your turn:\t\t Select an AM Vehicle from your army. It cannot move, charge or pile in this turn, but immediately heals 1 wound",
     "cost": "1 CP"},
    {"title": "Preliminary Bombardment",
     "rules": "Before first battle round:\t Roll a dice for each enemy unit on the battlefield. On a 6, that unit suffers 1 mortal wound. You can only use this Stratagem once per battle.",
     "cost": "2 CP"},
    {"title": "Inspired Tactics",
     "rules": "After an Officer issued an order:\t\t\t That officer may immediately issue an additional order.",
     "cost": "1 CP"},
    {"title": "Defensive Gunners",
     "rules": "When charge against AM Vehicle:\t When that unit fires Overwatch this phase, they successfully hit on a roll of 5 or 6, instead of only 6.",
     "cost": "1 CP"},
    {"title": "Take Cover!",
     "rules": "In opponent's Shooting phase, when unit targeted:\t\t\t You can add 1 to the saving throws you make for this unit until the end of the phase.",
     "cost": "1 CP"},
    {"title": "Grenadiers",
     "rules": "Before an AM infantry unit shoots or fires Overwatch:\t\t\t Up to ten models in the unit that are armed with grenades can throw a grenade this phase, instead of onlly one model being able to do so.",
     "cost": "1 CP"},
    {"title": "Fight to the Death",
     "rules": "Start of the moral phase: Pick an AM Infantry unit from your army that is required to take a Moral test. You can roll a D3 for the unit, rather than a D6, when taking this test.",
     "cost": "1 CP"},
    {"title": "Vengeance for Cadia!",
     "rules": "When an AM unit shoots of fires Overwatch:\t\t\t Re-roll failed hit and wound rolls for models in this unit that target CHAOS units untill the end of the phase.",
     "cost": "1 CP"},
    {"title": "Command Re-Roll",
     "rules": "You can re-roll any single dice.",
     "cost": "1 CP"},
    {"title": "Counter-Offensive",
     "rules": "After an enemy unit that charged has fought:\t\t\t Select one of your own eligible units and fight with it next.",
     "cost": "2 CP"},
    {"title": "Insane Bravery",
     "rules": "Before taking a Moral test:\t You can automatically pass a single Moral test.",
     "cost": "2 CP"},
]
stratagem = {"name": "Stratagem", "content": contentStratagem}

contentPsychic = [
    {"title": "Smite",
     "rules": "The closest visible enemy unit within 18\" of the psyker suffers D3 mortal wounds. If the result of the Psychic test was more than 10, the target suffers D6 mortal wounds instead.",
     "cost": "5 WC"},
    {"title": "Psychic Barrier",
     "rules": "Select a friendly AM unit within 12\" of the psyker. Until the start of your next Psychic phase, add 1 to that unit's saving throws.",
     "cost": "6 WC"},
    {"title": "Nightshroud",
     "rules": "Choose a friendly AM unit within 12\" of the psyker. Until the start of your next turn, any enemy unit that targets the chosen unit with a ranged weapon suffers a -1 penalty to its hit rolls.",
     "cost": "6 WC"},
]
psychic = {"name": "Psychic Power", "content": contentPsychic}

cards = [orders, stratagem, psychic]

# Define other constants
# backgroundFilePath = "KriegGrenadierBackground.jpg"
backgroundFilePath = "KriegPlatoonBackground.jpg"
background = Image.open(backgroundFilePath).convert('RGBA')

fontFile = "40kFont.TTF"
fontCardType = ImageFont.truetype(fontFile, 60)
fontRules = ImageFont.truetype(fontFile, 70)
MaxWidthRules = 32
fontTitle = ImageFont.truetype(fontFile, 100)
fontCost = ImageFont.truetype(fontFile, 80)
fontsDict = {"cardType": fontCardType,
             "rules": fontRules,
             "title": fontTitle,
             "cost": fontCost}

y_card_pos = 50
y_rules_pos = 250
y_title_pos = 130
margins = 40

x_cost = 820
y_cost = y_card_pos - 10

# Colors
black = (0, 0, 0)
grey = (50, 50, 50)
darkRed = (255, 50, 50)
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
        if "Psychic" in type_string:
            fill = "darkBlue"
        elif "Order" in type_string:
            fill = "darkorange"
        elif "Stratagem" in type_string:
            fill = "purple"
        else:
            fill = "black"
        imageDrawObject_card_type_text.text((x_pos, y_card_pos), type_string, font=fontCardType, fill=fill)
        # Add card type text to final
        card_outline = Image.alpha_composite(background, image_card_type_text)

        # Draw borders
        image_borders = Image.new('RGBA', background.size, (255, 255, 255, 0))
        imageDrawObject_borders = ImageDraw.Draw(image_borders)
        imageDrawObject_borders.rectangle(((0, 0), (background.size[0] / borderSizeVertical, background.size[1])),
                                          fill="black")
        imageDrawObject_borders.rectangle(
            ((background.size[0] * ((borderSizeVertical - 1) / borderSizeVertical), 0), background.size), fill="black")
        imageDrawObject_borders.rectangle(((0, 0), (background.size[0], background.size[1] / borderSizeHorizontal)),
                                          fill="black")
        imageDrawObject_borders.rectangle(((0, background.size[1] * (borderSizeHorizontal - 1) / borderSizeHorizontal),
                                           (background.size[0], background.size[1])), fill="black")
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
            num_title_lines = len(lines)
            for line in lines:
                height = fontsDict["title"].getsize(line)[1]
                x_text = get_text_x_pos(line, "title")
                image_title_text = Image.new('RGBA', background.size, (255, 255, 255, 0))
                imageDrawObject_title_text = ImageDraw.Draw(image_title_text)

                imageDrawObject_title_text.text((x_text, y_text), line, font=fontTitle, fill="black")
                current_card = Image.alpha_composite(current_card, image_title_text)
                y_text += height

            current_card = Image.alpha_composite(current_card, image_title_text)

            # Print rules on card
            string_rules = content["rules"]
            lines = textwrap.wrap(string_rules, width=MaxWidthRules)
            y_text = y_rules_pos
            if num_title_lines > 1:
                y_text += fontsDict["title"].getsize("example")[1]
            print("old y " + str(y_text))
            # y_text = y_title_pos + fontsDict["title"].getsize("example")[1]
            print("new y " + str(y_text))
            for line in lines:
                print("Line: " + line)
                height = fontsDict["rules"].getsize(line)[1]
                x_text = get_text_x_pos(line, "rules")
                image_rules_text_line = Image.new('RGBA', background.size, (255, 255, 255, 0))
                imageDrawObject_rules_text = ImageDraw.Draw(image_rules_text_line)
                imageDrawObject_rules_text.text((x_text, y_text), line, font=fontsDict["rules"], fill="black")
                current_card = Image.alpha_composite(current_card, image_rules_text_line)
                y_text += height

            # Print cost
            if "cost" in content.keys():
                string_cost = content["cost"]
                image_cost = Image.new('RGBA', background.size, (255, 255, 255, 0))
                imageDrawObject_cost = ImageDraw.Draw(image_cost)
                imageDrawObject_cost.text((x_cost, y_cost), string_cost, font=fontsDict["cost"], fill="darkRed")
                current_card = Image.alpha_composite(current_card, image_cost)

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
