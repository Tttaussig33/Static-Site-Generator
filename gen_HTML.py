# Name: Sa'ada Maliha Umaima, Teddy Taussig, William Zhang
# 02/16/25
# COM214 PA1
# This python program takes a text file from the user that contains
# style guide for making a website containing either images or random letters
# The functions used to run this program are:
# wrap(): takes a tag and a text as str and wrap the text into an html tag
# generateHTML(): #parses the text into dictionary
#     # determines if it contains images or letters
#     #compiles the img links/table dimensions into a list
    # returns the dictionary, whether image or letter content, img/dimension list
# create_table(): creates a table for letters or images using wrap() and generate_html() helper functions


import random
import string
import time
from datetime import datetime

def wrap(tag, text):
    # Takes a tag and a text as str and wraps the text into an HTML tag
    return f"{tag}{text}\n</{tag.split()[0].strip('<>')}>"

def generate_html():
    # Parses the text into a dictionary
    # Determines if it contains images or letters
    # Compiles the image links/table dimensions into a list

    file = open("config_file2.txt", "r")  # Read config.txt
    lines = file.readlines()  # Reads file one line at a time with \n at the end
    config = {}  # A dictionary to hold the CSS rules in key-value pairs
    cont_list = []  # A list for all image files or table dimensions (for letters)
    img_sec = False  # Turns true when image section in the file is reached
    letters_sec = False  # Turns true when letters section in the file is reached
    for line in lines:
        new_line = line.strip()  # Remove spaces
        # If image section is reached, set img_sec to true and skip that line
        if new_line == "IMAGES":
            img_sec = True
            continue
        # If letters section is reached, set letters_sec to true and skip that line
        if new_line == "LETTERS":
            letters_sec = True
            continue
        # In the image section split the items (links) into a list
        # Add items into the empty cont_list
        if img_sec:
            items = line.split()
            cont_list.extend(items)
        # In the letters section, extract the dimensions and store in cont_list
        elif letters_sec:
            cont_list.extend(new_line.split('x'))
        else:
            part = new_line.split('\t')
            key, value = part[0], part[-1]
            config[key] = value
    return config, cont_list, img_sec, letters_sec

def create_table():
    # Creates the table
    config, cont_list, img_sec, letters_sec = generate_html()
    table_cont = ""
    if img_sec:
        rows = int(len(cont_list)/5) + (len(cont_list) % 5 > 0)
        for i in range(rows):
            table_cont += "<tr>\n"
            row_img = cont_list[i*5:(i+1)*5]
            for img in row_img:
                table_cont += wrap("<td>", f'<img src="images/{img}" alt="{img}" width="100">')
            table_cont += "</tr>\n"
    elif letters_sec:
        rows, cols = int(cont_list[0]), int(cont_list[1])
        for i in range(rows):
            table_cont += "<tr>\n"
            for j in range(cols):
                letter = random.choice(string.ascii_letters)
                table_cont += wrap("<td>", letter)
            table_cont += "</tr>\n"
    table = wrap("<table>", table_cont)
    return table

def main():
    style_content = generate_html()[0]
    body_bg = style_content['BODY_BACKGROUND']
    cell_bg1 = style_content['CELL_BACKGROUND1']
    cell_bg2 = style_content['CELL_BACKGROUND2']
    table_border_color = style_content['TABLE_BORDER_COLOR']
    table_border_px = style_content['TABLE_BORDER_PX']
    authors = style_content['AUTHORS']
    title = f"-- {style_content['TITLE']} --"  # Adds dashes to the title above the table for better formatting
    
    table_style = f"""
    table {{
        width: 60%;
        margin: auto;
        border-collapse: collapse;
        border: {table_border_px}px solid {table_border_color};
    }}
    td {{
        padding: 10px;
        text-align: center;
        border: 1px solid {table_border_color};
    }}
    tr:nth-child(even) {{
        background-color: {cell_bg1};
    }}
    tr:nth-child(odd) {{
        background-color: {cell_bg2};
    }}
    h1, p {{
        text-align: center;
        color: {table_border_color};
    }}
    .generated-text {{
        text-align: center;
        color: {table_border_color};
        font-weight: bold;
        margin-top: 20px;
    }}
    """
    
    head = wrap("<head>", f"<title>{title}</title>\n"
        f"<style>body {{ background-color: {body_bg}; text-align: center; }} {table_style}</style>\n")
    table = create_table()
    timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")  # Generates a dynamic timestamp for when the page is created
    generated_text = wrap("<p class='generated-text'>", f"Created automatically for COM214HW1 on: {timestamp}")  # Wraps the generated text with an HTML paragraph tag and adds the current timestamp for when the content was created
    authors_text = wrap("<p class='generated-text'>", f"Authors: {authors}")  # Wraps the authors' names with an HTML paragraph tag and includes the authors' names in the content
    body = wrap("<body>", f"<h1>{title}</h1>\n{table}\n{generated_text}\n{authors_text}")
    html_cont = head + body
    
    with open('pa1.html', "w") as html:
        html.write(html_cont)
    
    print(f"HTML file 'pa1.html' has been generated successfully.")

main()
