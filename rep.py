# Replace
# This script reads the CRD from a file and replaces words in a given text with words from the CRD.

# $ python3 -m venv ./venv
# $ source ./venv/bin/activate
# $ python3 -m pip install nltk
# $ python3 rep.py

import pickle
import random
import nltk
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

from crd import MIN_WORD_LENGTH, make_key

TEXT = """I must not fear. Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain."""

def match_case(original, replacement):
    og_chars = list(original)
    rep_chars = list(replacement)

    for i, c in enumerate(og_chars):
        if c.isupper():
            rep_chars[i] = rep_chars[i].upper()
        else:
            rep_chars[i] = rep_chars[i].lower()

    return "".join(rep_chars)

def replace_text(text, crd):
    original_tokens = nltk.word_tokenize(text)
    original_tagged = nltk.pos_tag(original_tokens)
    tokens = original_tokens.copy()
    replacements = {}

    for i, token in enumerate(original_tokens):
        if len(token) < MIN_WORD_LENGTH:
            continue

        key = make_key(token)
        if key not in crd:
            continue

        random.shuffle(crd[key])
        for c, candidate in enumerate(crd[key]):
            candidate = match_case(token, candidate)
            if candidate == token:
                continue
            tokens[i] = candidate
            tagged = nltk.pos_tag(tokens)
            if tagged[i][1] == original_tagged[i][1]:
                replacements[token] = candidate

                crd[key].pop(c)
                if len(crd[key]) == 0:
                    del crd[key]

                break
    
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

def main():
    # read crd from file
    crd = {}
    with open('crd.pkl', 'rb') as f:
        crd = pickle.load(f)

    replaced = replace_text(TEXT, crd)
    print(replaced)

if __name__ == "__main__":
   main()



