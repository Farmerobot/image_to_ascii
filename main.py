import sys
from PIL import Image
import numpy as np

def average_lightness(image) :
    # convert the grayscale image to a 2-dimensional array
    image_array = np.array(image)

    # get dimensions of the array
    width,height = image_array.shape

    # reshape array to 1D and return its average value
    return np.average(image_array.reshape(width*height))

def get_ascii(image, gray_scale, columns, scale) :
    image_ascii = []

    width, height = image.size[0], image.size[1]
    
    tile_width = width/columns
    tile_height = tile_width/scale

    rows = int(height/tile_height)

    print("Target size in characters: %d x %d" % (columns, rows))
    
    # prevent the tile width from becoming 0
    if columns > width or rows > height :
        print("Error: Image is too small for the specified amount of columns")
        exit(0)

    print("Generating image...")

    # break up the image into tiles and return a character based on the
    # average brightness of each indiviual tile
    for j in range(rows) :
        print("Progress: %d%% done" % ((j+1)*100 / rows))
        # find tile dimensions
        y_start = int(j*tile_height)
        y_end = int((j+1)*tile_height)

        # correct the last tile to prevent stepping out outside the image height
        if j == rows - 1 :
            y_end = height
        
        # add empty string to the array to modify later when dealing with columns 
        image_ascii.append('')

        for i in range(columns) :
            # find dimensions just like above, but horizontally
            x_start = int(i*tile_width)
            x_end = int((i+1)*tile_width)

            if i == columns - 1 :
                x_end = width

            # get a tile from the dimensions by cropping the image 
            tile = image.crop((x_start, y_start, x_end, y_end))

            # append a character based on the lightness of the tile
            image_ascii[j] += gray_scale[int(average_lightness(tile)*69)/255]

    return image_ascii

def main() :
    # argument format: [input] [output] [size]
    arguments = len(sys.argv) - 1
    if arguments == 0 :
        print("Invalid parameters")
        print("Please use one of the folowing input formats:")
        print("\t- img_to_ascii [input file]")
        print("\t- img_to_ascii [input file] [output file]")
        print("\t- img_to_ascii [input file] [output file] [target width in characters]")
        return
    elif arguments > 3 :
        print("Too many arguments")
        return
    else :
        # set the default output file name
        output_file_name = "output.txt"
        print("File name: %s" % sys.argv[1])
        if arguments > 1 :
            output_file_name = sys.argv[2]

        # number of horizontal tiles and their ratio to the number of vertical tiles
        # This number depends on the font one is using:
        # its spacing, width and height in pixles
        if arguments == 3 :
            # columns = ((int(sys.argv[3])/46)*46)
            columns = int(sys.argv[3])
        else :
            columns = 46
        scale = 0.46

    # define a scale proprtional to the average lightness of an image 
    gray_scale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # open image and convert it to grayscale
    image = Image.open(sys.argv[1]).convert('L')

    # get the image dimensiosn
    width, height = image.size[0], image.size[1]

    print("Image size: %d x %d px" % (width, height))

    output = get_ascii(image, gray_scale, columns, scale)

    # get the target file
    output_file = open(output_file_name, 'w')

    # write each line to the file
    for row in output :
        output_file.write(row + "\n")

    output_file.close()

    print("Ascii art succesfully generated")
    print("Output file name: %s" % output_file_name)

if __name__ == "__main__" :
    main()