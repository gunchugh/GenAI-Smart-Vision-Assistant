from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

processor = None
model = None


def get_blip():

    global processor, model

    if processor is None or model is None:

        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    return processor, model


def generate_caption(image_path):

    processor, model = get_blip()

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    )

    output = model.generate(**inputs)

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption