# Numeric-Array-Navigation-As-Kolor-Image

I turned source code into images.

Numeric Array Navigation as a Color Image — Byte Splitting Algorithm


## How To Run

1. Run the python file with the path to the file you want to generate an image of. Example "python .\image_byte.py C:\Users\M\Work_pojects\code_to_pic\Code-to-Image\image_byte.py "

This algorithm takes a word, converts it into its UTF-8 byte representation, and transforms those bytes into two byte-sized values.

The basic idea is:

Convert the word into bytes.
Calculate an original_byte value from the entire word.
Determine whether the word has an even or odd number of bytes.
If the length is even, split the bytes directly into two halves.
If the length is odd, use the final byte differently by splitting it into two 4-bit nibbles.
Add the resulting values together.
Use % 256 so every resulting value stays within the the color range.


For example:

"the" → [116, 104, 101]

1. Original Byte

original_byte is a simple byte-sized summary of the entire word.

original_byte = sum(word_bytes) % 256


For "the":

116 + 104 + 101 = 321
321 % 256 = 65


So:

original_byte = 65


It is not one of the original bytes. It is the sum of all the bytes wrapped back into the 0–255 range.

2. Even-Length Words

If the word has an even number of bytes, split it directly in half and sum each half.

Example:

"test" → [116, 101, 115, 116]

[116, 101] | [115, 116]

half_a = 116 + 101 = 217
half_b = 115 + 116 = 231


Both values are wrapped with % 256 so they stay within a byte.

3. Odd-Length Words

If the word has an odd number of bytes, the final byte is handled separately.

For "the":

[116, 104, 101]


The last byte is 101, which in binary is:

01100101


Split it into two 4-bit nibbles:

0110 | 0101
  6  |  5


The remaining bytes are:

[116] | [104]


Add each nibble to its corresponding side:

half_a = 116 + 6 = 122
half_b = 104 + 5 = 109


So "the" produces:

original_byte = 65
half_a        = 122
half_b        = 109

In Short
Word
 ↓
UTF-8 bytes
 ↓
Calculate original_byte from all bytes
 ↓
Even? ──→ Split bytes in half → sum each half
 ↓
Odd? ───→ Split final byte into two nibbles
             ↓
          add each nibble to each side
 ↓
% 256
 ↓
half_a, original_byte, half_b


The important distinction is that original_byte summarizes the whole word, while half_a and half_b are the two values produced by splitting the word's bytes.