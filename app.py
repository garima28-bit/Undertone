#Undertone — minimal Flask app.


import io
from flask import Flask, render_template, request, send_file, abort
from PIL import Image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 24 * 1024 * 1024  # 24MB upload cap


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

    try:
        encoded_image = encoding(source_image, message)
    except ValueError as e:
        abort(400, str(e))

    buffer = io.BytesIO()
    encoded_image.save(buffer, format="PNG")  # PNG: lossless, keeps hidden bits intact
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="undertone_encoded.png",
    )


def check_and_flip(binary_input, bit_input):  # Defininf a Fucntion that takes in a Binary and a Single Bit
    if binary_input[7] == bit_input:  # and changes the LSB of the Binary to match the Single Bit
        return binary_input
    else:
        flipped_bit = "1" if binary_input[7] == "0" else "0"
        result = binary_input[:7] + flipped_bit
        return result


def encoding(image: Image.Image, word: str) -> Image.Image:

    pixels = image.load()

    channels = []  # Creates an empty array for the RGB channels of the pixels
    modified = []  # Cretes and empty array for the modified bits
    modified_channels = []
    word_to_bit = ""  # Creates an empty string for the Binary of the words





    for i in range(0, image.width):  # Gets the RGB Channels of each pixel and appends it to the Channels Array
        for j in range(0, image.height):
            r, g, b = pixels[i, j]
            channels.append(r)
            channels.append(g)
            channels.append(b)

    for i in word:  # Creates the Binary for the phrase/words using the Char_to_Bin Function
        word_to_bit = word_to_bit + f"{ord(i):08b}"

    word_to_bit += "00000000"  # null-character delimiter so decoding knows where the message ends

    if len(word_to_bit) > len(channels):
        raise ValueError("Message is too long to fit in this image.")

    for val, bit_input in zip(channels, word_to_bit):
        modified.append(check_and_flip(f"{val:08b}", bit_input))

    for i in modified:
        modified_channels.append(int(i, 2))

    index = 0
    for i in range(image.width):
        for j in range(image.height):
            r = modified_channels[index] if index < len(modified_channels) else channels[index]
            g = modified_channels[index + 1] if index + 1 < len(modified_channels) else channels[index + 1]
            b = modified_channels[index + 2] if index + 2 < len(modified_channels) else channels[index + 2]
            pixels[i, j] = (r, g, b)
            index += 3

    return image


if __name__ == "__main__":
    app.run(debug=True)
