import os

from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import argparse

# Constants
FONT_FILE = "40kFont.TTF"
FONT_CARD_TYPE = ImageFont.truetype(FONT_FILE, 60)
FONT_RULES = ImageFont.truetype(FONT_FILE, 70)
FONT_TITLE = ImageFont.truetype(FONT_FILE, 100)
FONT_COST = ImageFont.truetype(FONT_FILE, 80)
FONTS_DICT = {"cardType": FONT_CARD_TYPE,
              "rules": FONT_RULES,
              "title": FONT_TITLE,
              "cost": FONT_COST}

Y_CARD_POS = 50
Y_RULES_POS = 250
Y_TITLE_POS = 130
MARGINS = 40
MAX_WIDTH_RULES = 32

X_COST = 820
Y_COST = Y_CARD_POS - 10

# Colors
COLOR_TRANSPARENT = (255, 255, 255, 0)
TITLE_COLORS = {
    "Strategem": "purple",
    "Psychic": "darkBlue",
    "Order": "darkorange",
    "Act of Faith": "gold"
}

# Values
BACKGROUND_TRANSPARENCY = 160
BORDER_SIZE_VERTICAL = 30  # Larger = smaller proportion is border
BORDER_SIZE_HORIZONTAL = 35


def get_data(file_path):
    data_file = open(file_path)
    json_data = json.load(data_file)
    return json_data


def get_card_types(json_data):
    card_types = []
    for item in json_data:
        if item != "faction":
            card_types.append(item)
    return card_types


def get_total_card_count(json_data):
    total = 0
    card_types = get_card_types(json_data)
    for card_type in card_types:
        card_type_data = (json_data[card_type])
        total += len(card_type_data)
    return total


def get_text_x_pos(background_img, text_type, string):
    width = FONTS_DICT[text_type].getsize(string)[0]
    return get_text_midpoint_width(background_img, width)


def get_text_midpoint_width(background_img, text_width):
    return background_img.size[0] / 2 - text_width / 2


def get_background_image(file_path):
    background = Image.open(file_path).convert('RGBA')
    return background


def draw_text_border(draw_obj, x, y, text, font, fill, border_fill, thickness):
    draw_obj.text((x - thickness, y - thickness), text, font=font, fill=border_fill)
    draw_obj.text((x + thickness, y - thickness), text, font=font, fill=border_fill)
    draw_obj.text((x - thickness, y + thickness), text, font=font, fill=border_fill)
    draw_obj.text((x + thickness, y + thickness), text, font=font, fill=border_fill)
    draw_obj.text((x, y), text, font=font, fill=fill)


def main():
    # Take input for data
    parser = argparse.ArgumentParser(description="Creates 40k reminder cards")
    parser.add_argument('input_data', type=str, help="input json file")
    parser.add_argument('background_image', type=str, help="background image")
    args = parser.parse_args()
    print(args)

    data_file_path = args.input_data
    background_file_path = args.background_image

    image_background = get_background_image(background_file_path)
    json_data = get_data(data_file_path)
    faction = json_data["faction"]
    output_dir = faction.replace(' ', '') + "_output/"
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass
    card_types = get_card_types(json_data)

    # For each card type to make
    for card_type in card_types:
        print("\n\nCard type name : {}".format(card_type))

        # Make blank image for text, sets color of background inc transparance
        image_card_type_text = Image.new('RGBA', image_background.size, (255, 255, 255, BACKGROUND_TRANSPARENCY))
        image_draw_obj_card_type_text = ImageDraw.Draw(image_card_type_text)

        # Draw card type text
        x_pos = get_text_x_pos(background_img=image_background, text_type="cardType", string=card_type)
        fill = TITLE_COLORS[card_type]


        image_draw_obj_card_type_text.text((x_pos, Y_CARD_POS), card_type, font=FONT_CARD_TYPE, fill=fill)
        # Add card type text to final
        card_outline = Image.alpha_composite(image_background, image_card_type_text)

        # Draw borders
        image_borders = Image.new('RGBA', image_background.size, COLOR_TRANSPARENT)
        image_draw_object_borders = ImageDraw.Draw(image_borders)
        image_draw_object_borders.rectangle(
            ((0, 0), (image_background.size[0] / BORDER_SIZE_VERTICAL, image_background.size[1])),
            fill="black")
        image_draw_object_borders.rectangle(
            (
            (image_background.size[0] * ((BORDER_SIZE_VERTICAL - 1) / BORDER_SIZE_VERTICAL), 0), image_background.size),
            fill="black")
        image_draw_object_borders.rectangle(
            ((0, 0), (image_background.size[0], image_background.size[1] / BORDER_SIZE_HORIZONTAL)),
            fill="black")
        image_draw_object_borders.rectangle(
            ((0, image_background.size[1] * (BORDER_SIZE_HORIZONTAL - 1) / BORDER_SIZE_HORIZONTAL),
             (image_background.size[0], image_background.size[1])), fill="black")
        card_outline = Image.alpha_composite(card_outline, image_borders)

        # For each card of that type
        for card_title in json_data[card_type]:
            current_card_outline = card_outline.copy()

            print("Card title: {}".format(card_title))
            card_data = json_data[card_type][card_title]
            print("Card data: {}".format(card_data))
            print("Card data type: {}".format(type(card_data)))
            if type(card_data) is list:
                card_content = card_data[0]
                card_cost = card_data[1]
                print("Card cost: {}".format(card_cost))
            else:
                card_content = card_data
                card_cost = None
            print("Card content: {}".format(card_content))

            # Add name of card
            lines = textwrap.wrap(card_title, width=18)
            y_text = Y_TITLE_POS
            num_title_lines = len(lines)
            assert num_title_lines > 0
            for line in lines:
                height = FONTS_DICT["title"].getsize(line)[1]
                x_text = get_text_x_pos(background_img=image_background, text_type="title", string=line)
                image_title_text = Image.new('RGBA', image_background.size, COLOR_TRANSPARENT)
                imageDrawObject_title_text = ImageDraw.Draw(image_title_text)

                draw_text_border(draw_obj=imageDrawObject_title_text, x=x_text, y=y_text, font=FONT_TITLE,
                                 thickness=3, text=line, border_fill="black", fill="white")
                # imageDrawObject_title_text.text((x_text, y_text), line, font=FONT_TITLE, fill="black")
                current_card_outline = Image.alpha_composite(current_card_outline, image_title_text)
                y_text += height

            current_card_outline = Image.alpha_composite(current_card_outline, image_title_text)

            # Print rules on card
            lines = textwrap.wrap(card_content, width=MAX_WIDTH_RULES)
            y_text = Y_RULES_POS
            if num_title_lines > 1:
                y_text += FONTS_DICT["title"].getsize("example")[1]
            for line in lines:
                print("Line: " + line)
                height = FONTS_DICT["rules"].getsize(line)[1]
                x_text = get_text_x_pos(background_img=image_background, text_type="rules", string=line)
                image_rules_text_line = Image.new('RGBA', image_background.size, COLOR_TRANSPARENT)
                imageDrawObject_rules_text = ImageDraw.Draw(image_rules_text_line)
                imageDrawObject_rules_text.text((x_text, y_text), line, font=FONTS_DICT["rules"], fill="black")
                current_card_outline = Image.alpha_composite(current_card_outline, image_rules_text_line)
                y_text += height

            # Print cost
            if card_cost:
                image_cost = Image.new('RGBA', image_background.size, COLOR_TRANSPARENT)
                image_draw_object_cost = ImageDraw.Draw(image_cost)
                image_draw_object_cost.text((X_COST, Y_COST), card_cost, font=FONTS_DICT["cost"], fill="darkRed")
                current_card_outline = Image.alpha_composite(current_card_outline, image_cost)

            # Finally, save file
            current_card_outline.save(fp=output_dir + card_type + card_title.replace(' ', '') + '.png')


if __name__ == '__main__':
    main()
