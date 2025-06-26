#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-genai>=1.19.0",
#   "pillow",
# ]
# ///

import argparse
import json
import os
import textwrap

from google import genai
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True, help="The image to upload.")
parser.add_argument("--model", default="models/gemini-2.5-pro-preview-03-25")

API_KEY = os.environ["GEMINI_API_KEY"]


def main(args):
    client = genai.Client(api_key=API_KEY)
    text = textwrap.dedent("""
        This picture is of a moving box with the contents of it taped to the side.
        Can you read the list of items from the picture and tell me what it says?
    """.strip("\n"))
    image = Image.open(args.image)

    response = client.models.generate_content(
        model=args.model,
        contents=[text, image],
        config={
            "response_mime_type": "application/json",
            "response_schema": list[str],
        }
    )
    print(json.dumps(response.parsed, indent=2))


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
