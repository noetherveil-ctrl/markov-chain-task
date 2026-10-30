import argparse
import random
from pathlib import Path


def generate(words, length, order):
    chains = {}
    for i in range(len(words) - order):
        key = tuple(words[i:i + order])
        chains.setdefault(key, []).append(words[i + order])

    starts = [key for key in chains if key[0][0].isupper()]
    if not starts:
        raise ValueError("В тексте нет подходящего начала")

    result = list(random.choice(starts))[:length]
    while len(result) < length:
        key = tuple(result[-order:])
        if key not in chains:
            result.extend(random.choice(starts)[:length - len(result)])
        else:
            result.append(random.choice(chains[key]))
    return " ".join(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("length", type=int)
    parser.add_argument("--order", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    if args.length < 1:
        parser.error("Длина должна быть положительной")
    words = Path(args.file).read_text(encoding="utf-8-sig").split()
    if len(words) <= args.order:
        parser.error("Слишком короткий исходный текст")
    try:
        print(generate(words, args.length, args.order))
    except ValueError as error:
        parser.error(str(error))
