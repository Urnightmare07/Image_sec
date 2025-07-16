from PIL import Image, ImageDraw
import os
import random
import argparse
from numpy import mean

"""
Terms used:
payload - Image that will be split into 2
key     - Image that will be used to aid in the process of splitting
seed    - A string value that will be used in the process of sample selecting within splitting
"""

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--payload', '-p', required=True)
    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--seed', '-s', required=True)
    return parser.parse_args()

def main():
    args = get_options()

    payload_file = args.payload
    key_file = args.key
    seed = args.seed

    # Same seed will result in same random behavior
    # Arbitrary - but must be consistent in production use
    # Should be less than total pixels in payload image
    SAMPLE_PIXEL_COUNT = 10

    # Checking if payload file exists
    if not os.path.isfile(payload_file):
        print("The splittable file does not exist.")
        exit()
    if not os.path.isfile(key_file):
        print("The key file does not exist.")
        exit()

    payload_image = Image.open(payload_file)
    key_image = Image.open(key_file)

    f, _ = os.path.splitext(payload_file)
    out_filename_A = "A.png"
    out_filename_B = "B.png"

    payload_image = payload_image.convert('1')  # convert image to 1 bit
    key_image_greyscale = key_image.convert('LA')

    greyscale_pixel_values = list(key_image_greyscale.getdata())

    # pixel_values is an array of tuples (2D), we flatten it to get an array (1D)
    greyscale_pix_values_flat = [
        x for sets in greyscale_pixel_values for x in sets
    ]

    mean_pixel_value_key_image = mean(greyscale_pix_values_flat)

    print("Image size: {}".format(payload_image.size))

    # Prepare two empty slider images for drawing
    width = payload_image.size[0] * 2
    height = payload_image.size[1] * 2

    print("Output size: {} x {}".format(width, height))

    out_image_A = Image.new('1', (width, height))
    out_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(out_image_A)
    draw_B = ImageDraw.Draw(out_image_B)

    # Two possible patterns to choose from
    patterns = ((1, 0, 1, 0), (0, 1, 0, 1))

    # Cycle through pixels
    for x in range(0, int(width / 2)):
        for y in range(0, int(height / 2)):  # Pattern selection
            # This is done by selecting picking a sample of pixels from payload image's greyscale version
            # Selection is done based on seed provided so same seed results in same selections
            key_array_len = len(greyscale_pix_values_flat)
            pixels_to_sample = (SAMPLE_PIXEL_COUNT + x + y) % key_array_len

            # Making sure the value isn't 0
            if pixels_to_sample == 0:
                pixels_to_sample = SAMPLE_PIXEL_COUNT

            sampleMean = mean(random.sample(
                greyscale_pix_values_flat, pixels_to_sample))

            # Core decisional logic to choosing which pattern goes
            if sampleMean > mean_pixel_value_key_image:
                pat = patterns[0]
            else:
                pat = patterns[1]

            pixel = payload_image.getpixel((x, y))  # A will always get the pattern
            draw_A.point((x * 2, y * 2), pat[0])
            draw_A.point((x * 2 + 1, y * 2), pat[1])
            draw_A.point((x * 2, y * 2 + 1), pat[2])
            draw_A.point((x * 2 + 1, y * 2 + 1), pat[3])

            if pixel == 0:  # Dark pixel so B gets the anti pattern
                draw_B.point((x * 2, y * 2), 1 - pat[0])
                draw_B.point((x * 2 + 1, y * 2), 1 - pat[1])
                draw_B.point((x * 2, y * 2 + 1), 1 - pat[2])
                draw_B.point((x * 2 + 1, y * 2 + 1), 1 - pat[3])
            else:
                draw_B.point((x * 2, y * 2), pat[0])
                draw_B.point((x * 2 + 1, y * 2), pat[1])
                draw_B.point((x * 2, y * 2 + 1), pat[2])
                draw_B.point((x * 2 + 1, y * 2 + 1), pat[3])

    out_image_A.save(out_filename_A, 'PNG')
    out_image_B.save(out_filename_B, 'PNG')
    print("Done.")

if __name__ == '__main__':
    main()
