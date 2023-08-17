import os
import pathlib
from PIL import Image
import argparse
from transformers import CLIPProcessor, CLIPModel

def load_vocab(path):
    # Load vocabulary
    with open(path, "r") as f:
        vocab = [l.strip() for l in f.readlines()]

    vocab = [l for l in vocab if l and not l.startswith("#")]
    vocab = vocab[:MAX_VOCAB_SIZE]
    return vocab


def main():
    # Load model, processor and image
    image = Image.open(FILE_PATH)
    model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
    processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

    for f in os.listdir(VOCAB_DIR):
        file_path = os.path.join(VOCAB_DIR, f)
        if os.path.isfile(file_path):  # Ensure it's a file and not a directory
            vocab = load_vocab(file_path)

            inputs = processor(
                text=vocab,
                images=image,
                return_tensors="pt",
                padding=True,
            )

            outputs = model(**inputs)
            logits_per_image = (
                outputs.logits_per_image
            )  # this is the image-text similarity score

            # Convert logits to softmax probabilities
            probs = logits_per_image.softmax(dim=1)[0]

            # Map output to vocabulary
            probs = [float(p) for p in probs]
            classes = zip(probs, vocab)
            classes = sorted(classes, reverse=True)
            print("###########")
            print(file_path)
            # Print the top n classes
            for c in classes[:TOP_N_CLASSES]:
                print(f"{c[0]:.3f},\t {c[1]}")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Process and classify images using CLIP."
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="path",
        help="Specify path to image file.",
        metavar="IMG",
        required=True,
    )
    parser.add_argument(
        "-v",
        "--maxvocab",
        action="store",
        dest="max_vocab",
        help="Maximum number of words per category. Default: 600.",
        default=600,
        type=int,
    )
    parser.add_argument(
        "-d",
        "--dir",
        action="store",
        dest="vocab_dir",
        help="Path to vocabulary directory. Default: vocab/",
        default="vocab",
        metavar="DIR",
        type=pathlib.Path,
    )
    parser.add_argument(
        "-n",
        "--number",
        action="store",
        dest="number",
        help="Number of top classes to be printed per category. Default: 5.",
        default=5,
        type=int,
    )


    args = parser.parse_args()

    FILE_PATH = args.path
    MAX_VOCAB_SIZE = args.max_vocab
    VOCAB_DIR = args.vocab_dir
    TOP_N_CLASSES = args.number

    main()
