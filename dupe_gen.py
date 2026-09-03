# import thing for reading a file path

from dataclasses import dataclass
from typing import Dict
import argparse

from PIL import Image
import math

#

# Numeric Array Navigation As Kolor Image nanaki

# have two versions one for dupes and one for non dupes


# make class for bit cord structure
@dataclass
class BitInfo:
    half_a: int
    original: int
    half_b: int
    word: str


from PIL import Image
import math


def compute_canvas_size(num_entries, padding_factor=1.2):
    """
    finds the dimensions for a square canvas and adds extra space just in case (1.2 = 20% extra space).
    """
    # if no data, return a minimum size of 1x1
    if num_entries <= 0:
        return 1

    # total area needed including the extra padding room
    padded_area = num_entries * padding_factor

    # since Area = Side * Side, the side length is the square root of the area round up to the nearest whole pixel.
    side_length = math.ceil(math.sqrt(padded_area))

    # the side length, ensuring it's at least 1
    return max(side_length, 1)


def image_gen_unique(image_cords: list[tuple[int, int, int, str]]):
    """
    Creates a square image where each item in image_cords is represented by one pixel.
    """
    # finds the canvas dimensions based on how many items are in the list
    canvas_size = compute_canvas_size(len(image_cords))

    # makes a blank image and sets it to black
    img = Image.new("RGB", (canvas_size, canvas_size), color=(0, 0, 0))

    # loads the img
    pixels = img.load()

    # loops through the list of colors.
    # y is just for the word, not used
    for i, (r, g, b, y) in enumerate(image_cords):
        color = (r, g, b)

        # coordinate Math: Convert a 1D index (i) into 2D coordinates (x, y)

        # the column (x) is the remainder of the index divided by the width.
        # this makes x cycle: 0, 1, 2, 0, 1, 2...
        x = i % canvas_size

        # the row (y) is how many full widths we have completed.
        # this stays at 0 for the first row, 1 for the second row, etc.
        y_coord = i // canvas_size

        # assign the color to the calculated pixel position
        pixels[x, y_coord] = color

        # just logging, prints the actual cords
        print(f"Color {color} placed at grid position ({x}, {y_coord})")

    # shows the img, doesnt save it though
    return img.show()


def file_input():
    argparser = argparse.ArgumentParser(description="Enter the full file path")

    argparser.add_argument("file_path", type=str, help="The full file path.")

    args = argparser.parse_args()

    with open(args.file_path):
        print(f"The file path you gave is {args.file_path}")

    return args.file_path


def create_duplicate_with_id(info, word):
    # returns a tuple of the word and its byte info
    return (info.half_a, info.original, info.half_b, word)


def cord_gather():
    # byte dict will look like "String word": (first half of byte, origanl byte value, other half, unique id)
    byte_dict = {}
    result_list = []

    # gets file path
    file_path = file_input()
    # opens the file

    with open(file_path, "r") as file:
        print("i")
        #        unique_id = 0

        # Outer while loop for reading lines
        while True:
            line = file.readline()
            print(line)
            if not line:
                break

            # skip comments and empty lines
            if line.startswith("#") or not line.strip():
                continue

            # removes trailing comments
            clean_line = line.split("#", 1)[0].strip()
            print(clean_line)

            # loops through clean words
            for words in clean_line.split():
                print(f"theis is {words}")
                # look up the word in dict
                info = byte_dict.get(words)

                # if word is in the dict

                if info is not None:
                    continue
                else:
                    # chance word to bytes
                    word_bytes = words.encode("utf-8")
                    # gets len of byte
                    length = len(word_bytes)

                    # the origianl value of the word but wrapped so it can't go past 256
                    original_byte = sum(word_bytes) % 256

                    if length % 2 == 0:
                        # --- EVEN WORDS ---
                        mid = length // 2  # splits in two

                        # word_bytes[:mid] is the first half, word_bytes[mid:] is the second
                        half_a = sum(word_bytes[:mid]) % 256
                        half_b = sum(word_bytes[mid:]) % 256
                    else:
                        # --- ODD WORDS ---
                        # get the last byte
                        last_byte = word_bytes[-1]

                        # breaks the last byte in half and gets the bits
                        high_nibble = (last_byte >> 4) & 0x0F
                        low_nibble = last_byte & 0x0F

                        mid = (length - 1) // 2

                        # basically if the word is an odd len we take the last word and split it in to two bit
                        # ex: "the", e bit value would be 01100101
                        # so we nibble it and take the the first half
                        # split the last byte into two nibbles and add those nibbles to the sums of the preceding byte
                        # You're splitting the last byte into two nibbles and adding those nibble values to the sums of the preceding bytes.

                        # Sum the first half + high nibble
                        half_a = (sum(word_bytes[:mid]) + high_nibble) % 256
                        # Sum the rest (excluding the last byte) + low nibble
                        half_b = (sum(word_bytes[mid : length - 1]) + low_nibble) % 256

                    # store in BitInfo Dataclass
                    new_info = BitInfo(
                        half_a=int(half_a),
                        original=int(original_byte),
                        half_b=int(half_b),
                        word=words,
                    )

                    # add to results and dictionary
                    result_list.append(
                        (new_info.half_a, new_info.original, new_info.half_b, words)
                    )
                    byte_dict[words] = new_info

        return result_list


def main():
    res = cord_gather()
    print(res)
    image_gen_unique(res)


main()
