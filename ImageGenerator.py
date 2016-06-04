import copy
from PIL import Image
import colorsys
import random

def convert_palette_to_hsv(palette):
    hsv_palette = []
    for i in range(0, len(palette)):
        hsv_palette.append(colorsys.rgb_to_hsv(palette[i][0]/255.0, palette[i][1]/255.0, palette[i][2]/255.0))
        hsv_palette[i] = (round(hsv_palette[i][0]*360/10, 0)*10, round(hsv_palette[i][1], 2), round(hsv_palette[i][2], 2))
    return hsv_palette

def x_in_palette(x, palette):
    for color in palette:
        if round_color(x) == round_color(color):
            return True
    return False

def round_color(x):
    a = (round(x[0]/10, 0)*10, round(x[1], 2), round(x[2], 2))
    return a

def change_color_skin(values, palette, delta_red, delta_green, delta_blue, mode):
    new_values = copy.deepcopy(values)
    for i in range(0, len(values)):
        for j in range(0, len(values[i])):
            if(mode == 'HSV'):
                x = round_color(values[i][j])
            else:
                x = values[i][j]
            if(x_in_palette(x, palette)):
                new_values[i][j] = ((x[0] + delta_red), (x[1] + delta_green),(x[2] + delta_blue))
            else:
                new_values[i][j] = x
    return new_values

def make_image(values, name):
    image = Image.new('RGB', (len(values[0]), len(values)))
    values = [item for sublist in values for item in sublist]
    image.putdata(values)
    image.save(name + '.png')

def convert_image_to_list(image):
    rgb_image = image.convert('RGB')
    rgb_values = []
    for j in range(0, rgb_image.size[1]):
        rgb_values.append([])
        for i in range(0, rgb_image.size[0]):
            rgb_values[j].append(rgb_image.getpixel((i, j)))
    return rgb_values

def convert_list_to_rgb(values):
    new_values = copy.deepcopy(values)
    for i in range(0, len(values)):
        for j in range(0, len(values[i])):
            a = new_values[i][j]
            new_values[i][j] = colorsys.hsv_to_rgb(float(values[i][j][0]/360),
                                                   float(values[i][j][1]),
                                                   float(values[i][j][2]))
            x = new_values[i][j]
            new_values[i][j] = (int(new_values[i][j][0]*255),int(new_values[i][j][1]*255),int(new_values[i][j][2]*255))

    return new_values

def convert_list_to_hsv(values):
    new_values = copy.deepcopy(values)
    for i in range(0, len(values)):
        for j in range(0, len(values[i])):
            new_values[i][j] = colorsys.rgb_to_hsv(float(values[i][j][0])/255.0,
                                                   float(values[i][j][1])/255.0,
                                                   float(values[i][j][2])/255.0)
            new_values[i][j] = (int(new_values[i][j][0]*360),new_values[i][j][1],new_values[i][j][2])
    return new_values

#Pillow example
'''
image = Image.open('test_original.png')
rgb_values = convert_image_to_list(image)

for i in range(0, len(rgb_values)):
    for j in range(0, len(rgb_values[i])):
        x = rgb_values[i][j]
        if (i%4 == 0 and j%4 == 0) or (i%4 == 1 and j%4 == 1)\
                or (i%4 == 1 and j%4 == 0) or (i%4 == 0 and j%4 == 1):
            rgb_values[i][j] = (x[0], x[1] + 100, x[2])

make_image(rgb_values, 'test')
'''





















#Changing Megaman's color in RGB

image = Image.open('megaman.png')
rgb_values = convert_image_to_list(image)

dark_blue = (4, 50, 100)
med_blue = (4, 66, 212)
light_blue = (4, 138, 244)
dark_teal = (28, 146, 172)
teal = (52, 194, 220)
palette = (dark_blue, med_blue, light_blue, dark_teal, teal)

rgb_new = change_color_skin(rgb_values, palette, 200, -50, -100, 'RGB')
make_image(rgb_new, 'red_megaman')






















#Changing Megaman's color in HSV
hsv_values = convert_list_to_hsv(convert_image_to_list(image))
palette_hsv = convert_palette_to_hsv(palette)

hsv_new = convert_list_to_rgb(change_color_skin(hsv_values, palette_hsv, -180, 0, +.25, 'HSV'))
make_image(hsv_new, 'megaman_hsv')































def get_random_face(num_faces, image, padding):
    face_values = []
    image = Image.open(image)
    image = image.convert('RGB')
    num = random.randrange(0, num_faces)
    width = int(image.size[0]/num_faces)
    height = (image.size[1])
    for i in range(0 + padding, width - padding):
        face_values.append([])
        for j in range(0 + padding, height - padding):
            face_values[i - padding].append(image.getpixel((num*width + i, j)))
    return face_values

def make_random_goomba(face_image, base_image, num_faces, padding_face, padding_base, face_start, palette):
    face = get_random_face(num_faces, face_image, padding_face)

    image = Image.open(base_image)
    rgb_values = convert_image_to_list(image)

    face_image = Image.open(face_image)
    width = int(face_image.size[0]/num_faces - 2*padding_face)
    height = int(face_image.size[1] - 2*padding_face)

    for i in range(face_start[0], face_start[0] + width):
        for j in range(face_start[1], face_start[1] + height):
            if(face[i - face_start[0]][j - face_start[1]] != (255, 255, 255)):
                rgb_values[j + padding_base][i + padding_base] = face[i - face_start[0]][j - face_start[1]]
                x = int(i + 18 + padding_base)
                rgb_values[j + padding_base][x] = face[i - face_start[0]][j - face_start[1]]

    hsv_values = convert_list_to_hsv(rgb_values)
    hsv_palette = convert_palette_to_hsv(palette)

    hue = (random.randrange(1, num_faces*4)/(4*num_faces))*360
    sat = random.randrange(-10, 0)/100
    val = random.randrange(-1, 0)/100

    values = convert_list_to_rgb(change_color_skin(hsv_values, hsv_palette, hue, sat, val, 'HSV'))
    return values

def format_list_to_spritesheet(values, num_per_row, num, sprite_width, sprite_height):
    new_values = [[(255, 255, 255) for x in range(num_per_row*sprite_width)] for y in range((int(num/num_per_row) + 1)*sprite_height)]
    row = 0
    col = 0
    for i in range(0, len(values)):
        if((i+1) % num_per_row == 0):
            row += 1
            col = 0
        for j in range(0, len(values[i])):
            for k in range(0, len(values[i][j])):
                new_values[j + row*sprite_height][k + col*sprite_width] = values[i][j][k]

        col += 1
    return new_values

def create_goombas(num, face_image, base_image, output_name, num_faces, padding_face, padding_base, face_start, palette, num_per_row, sprite_width, sprite_height):
    goomba_values = []
    for i in range(0, num):
        goomba_values.append(make_random_goomba(face_image, base_image, num_faces, padding_face, padding_base, face_start, palette))
    goomba_values = format_list_to_spritesheet(goomba_values, num_per_row, num, sprite_width, sprite_height)
    make_image(goomba_values, output_name)

#Creating many different Goomba enemies

red = (255, 0, 0)
light_red = (255, 105, 105)
dark_red = (200, 0, 0)
palette = [red, light_red, dark_red]
create_goombas(20, 'goomba_faces.png', 'goomba_base.png', 'goomba_sheet', 8, 1, 1, (3, 4), palette, 5, 36, 18)


























