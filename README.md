# Undertone

A web-based steganography tool that hides text messages inside PNG images using LSB (Least Significant Bit) encoding — invisible to the eye, recoverable with the right key.

Built with Flask and Pillow.

---

## What it does

Undertone lets you embed a secret text message into the pixel data of a PNG image. The image looks completely unchanged, but the message is encoded bit-by-bit into the least significant bits of the pixel color values. Anyone with the encoded image (and Undertone) can extract the hidden message back out.

- **Encode** — hide a text message inside a PNG image
- **Decode** — extract a hidden message from an encoded PNG
- Preserves spacing and special characters in the original message
- Uses a null-byte delimiter to mark the end of the hidden message, so decoding stops cleanly without needing to know the message length in advance

## Tech stack

| Layer | Tool |
|---|---|
| Backend | Flask |
| Image processing | Pillow (PIL) |
| Frontend | HTML / CSS / JS — dark theme, cipher-teal & signal-amber palette |
| Typography | Space Grotesk (headings), IBM Plex Mono (body/code) |
| Deployment | Gunicorn (WSGI server) |

## Getting started

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# clone the repo
git clone https://github.com/<your-username>/undertone.git
cd undertone

# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run the app
flask run
```

The app will be available at `http://127.0.0.1:5000`.

## Project structure

```
undertone/
├── app.py                 # Flask app entry point and routes
├── static/                 # CSS, JS, cursor-reactive canvas background
├── templates/               # Jinja2 HTML templates
├── requirements.txt
└── README.md
```

## Roadmap

- [ ] `/decode` route — extract hidden messages from uploaded images
- [x] LSB encoding logic
- [x] Null-byte delimiter for clean message boundaries
- [x] Multi-page frontend
- [ ] Deployment (Render / DigitalOcean)

## How LSB steganography works

Each pixel in an image is made of color channels (R, G, B), each stored as an 8-bit value (0–255). Changing just the *last* bit of each channel alters the color so slightly that it's invisible to the human eye — but that bit can be repurposed to store a bit of your hidden message. String enough of these bits together across enough pixels, and you can hide an entire message inside a picture that looks completely untouched.

## Contributors

Built by [Veshesh](https://github.com/<your-username>) and [Garima](https://github.com/<garima-username>).

## License

MIT License — feel free to fork, learn from, and build on this project.
