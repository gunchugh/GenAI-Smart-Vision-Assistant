from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch
import gc

# Lazy Load
processor = None
model = None


def get_vilt():

    global processor, model

    if processor is None or model is None:

        processor = ViltProcessor.from_pretrained(
            "dandelin/vilt-b32-finetuned-vqa"
        )

        model = ViltForQuestionAnswering.from_pretrained(
            "dandelin/vilt-b32-finetuned-vqa"
        )

    return processor, model


def answer_question(image_path, question):

    processor, model = get_vilt()

    image = Image.open(image_path).convert("RGB")

    with torch.inference_mode():

        encoding = processor(
            image,
            question,
            return_tensors="pt"
        )

        outputs = model(**encoding)

    logits = outputs.logits

    idx = logits.argmax(-1).item()

    answer = model.config.id2label[idx]

    image.close()

    del encoding
    del outputs

    gc.collect()

    return answer