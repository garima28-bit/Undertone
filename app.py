"""
Undertone — A minimal Steganography Flask app.
"""

import io
from flask import Flask, render_template, request, send_file, abort
from PIL import Image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 24 * 1024 * 1024  # 24MB upload cap

DELIMITER = "\x00\xFF"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == "GET":
        return render_template("encode.html")

    image_file = request.files.get("image")
    message = request.form.get("message", "").strip()

    if not image_file or image_file.filename == "":
        abort(400, "No image was uploaded.")
    if not message:
        abort(400, "No message was provided.")

    try:
        source_image = Image.open(image_file.stream).convert("RGB")
    except Exception:
        abort(400, "That file couldn't be read as an image.")

    encoded_image = encoding(source_image, message)

    buffer = io.BytesIO()
    encoded_image.save(buffer, format="PNG")  # PNG: lossless, keeps hidden bits intact
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="undertone_encoded.png",
    )


@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == "GET":
        return render_template("decode.html")

    image_file = request.files.get("image")

    if not image_file or image_file.filename == "":
        abort(400, "No image was uploaded.")

    try:
        source_image = Image.open(image_file.stream).convert("RGB")
    except Exception:
        abort(400, "That file couldn't be read as an image.")

    try:
        decoded_message = decoding(source_image)
    except ValueError as e:
        return render_template("decode.html", error=str(e))

    return render_template("decode.html", decoded_message=decoded_message)

def check_and_flip(binary_input, bit_input):  # Defining a Function that takes in a Binary and a Single Bit
    if binary_input[7] == bit_input:  # and changes the LSB of the Binary to match the Single Bit
        return binary_input
    else:
        flipped_bit = "1" if binary_input[7] == "0" else "0"
        result = binary_input[:7] + flipped_bit
        return result


def encoding(image: Image.Image, word: str) -> Image.Image:
    encoded = image.copy()          # work on a copy — don't mutate the caller's image
    pixels = encoded.load()

    channels = []  # Creates an empty array for the RGB channels of the pixels
    modified = []  # Creates an empty array for the modified bits
    modified_channels = []
    word_to_bit = ""  # Creates an empty string for the Binary of the words

    for i in range(0, encoded.width):  # Gets the RGB Channels of each pixel and appends it to the Channels Array
        for j in range(0, encoded.height):
            r, g, b = pixels[i, j]
            channels.append(r)
            channels.append(g)
            channels.append(b)

    for i in word:  # Creates the Binary for the phrase/words using ord(), including spaces
        word_to_bit = word_to_bit + f"{ord(i):08b}"

    # Delimiter: a marker appended after the message's bits so decoding
    # knows where the real message ends. "\x00\xFF" is a safe choice —
    # not something people type in a text message, and unlikely to
    # occur by chance in ordinary pixel data.
    delimiter_bits = "".join(f"{ord(c):08b}" for c in DELIMITER)
    bitstream = word_to_bit + delimiter_bits

    if len(bitstream) > len(channels):
        raise ValueError(
            "Message is too long to fit in this image "
            f"({len(bitstream)} bits needed, {len(channels)} available)."
        )

    for val, bit_input in zip(channels, bitstream):
        modified.append(check_and_flip(f"{val:08b}", bit_input))

    for i in modified:
        modified_channels.append(int(i, 2))

    index = 0
    for i in range(encoded.width):
        for j in range(encoded.height):
            r = modified_channels[index] if index < len(modified_channels) else channels[index]
            g = modified_channels[index + 1] if index + 1 < len(modified_channels) else channels[index + 1]
            b = modified_channels[index + 2] if index + 2 < len(modified_channels) else channels[index + 2]
            pixels[i, j] = (r, g, b)
            index += 3

    return encoded


def decoding(image: Image.Image) -> str:
    encoded = image.convert("RGB")
    pixels = encoded.load()

    # Same flattening as encoding: every pixel's R, G, B in order,
    # so the bit positions line up exactly with how they were written.
    channels = []
    for i in range(0, encoded.width):
        for j in range(0, encoded.height):
            r, g, b = pixels[i, j]
            channels.append(r)
            channels.append(g)
            channels.append(b)

    # Pull the least-significant bit out of every channel value —
    # this is the raw bitstream that was hidden during encoding.
    bits = "".join(str(val & 1) for val in channels)

    message_chars = []
    for start in range(0, len(bits), 8):
        byte = bits[start:start + 8]
        if len(byte) < 8:
            # Ran out of pixel data before ever seeing the delimiter —
            # this image almost certainly doesn't contain a message
            # encoded by this app.
            break

        char = chr(int(byte, 2))
        message_chars.append(char)

        if "".join(message_chars).endswith(DELIMITER):
            # Found the end marker — stop here and return what we've
            # collected so far, without the delimiter itself.
            return "".join(message_chars)[:-len(DELIMITER)]

    raise ValueError(
        "No message found — this image doesn't appear to contain an "
        "Undertone message."
    )


if __name__ == "__main__":
    app.run(debug=True)
