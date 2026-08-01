from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch

processor = ViltProcessor.from_pretrained(
    "dandelin/vilt-b32-finetuned-vqa"
)

model = ViltForQuestionAnswering.from_pretrained(
    "dandelin/vilt-b32-finetuned-vqa"
)


def answer_question(image_path, question):

    image = Image.open(image_path).convert("RGB")

    encoding = processor(
        image,
        question,
        return_tensors="pt"
    )

    outputs = model(**encoding)

    logits = outputs.logits

    idx = logits.argmax(-1).item()

    answer = model.config.id2label[idx]

    return answer