# Replace
# This script reads the CRD from a file and replaces words in a given text with words from the CRD.

# $ python3 -m venv ./venv
# $ source ./venv/bin/activate
# $ python3 -m pip install nltk
# $ python3 rep.py

import sys
import pickle
import random
import nltk
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

from crd import MIN_WORD_LENGTH, make_key

TEXT = """I must not fear. Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain."""

# assumes original and replacement have the same length
# returns replacement with the same case as original
def match_case(original, replacement):
    og_chars = list(original)
    rep_chars = list(replacement)

    for i, c in enumerate(og_chars):
        if c.isupper():
            rep_chars[i] = rep_chars[i].upper()
        else:
            rep_chars[i] = rep_chars[i].lower()

    return "".join(rep_chars)

# This code assumes that if the original text has 'everywhere' tagged 'NN' and
# we find a replacement 'ecoclimate' with the same tag, then we can replace
# every instance of 'everywhere' (that's tagged 'NN') with 'ecoclimate'.
# Later in the text, 'Everywhere' tagged 'NNP' (proper noun, like someone's name)
# will not be replaced with 'ecoclimate'.

def make_replacement_key(token, tag):
    return token.upper() + "_" + tag

def replace_text(text, crd):
    original_tokens = nltk.word_tokenize(text)
    original_tagged = nltk.pos_tag(original_tokens)
    tokens = original_tokens.copy()
    replacements = {}

    for i, token in enumerate(original_tokens):
        if len(token) < MIN_WORD_LENGTH:
            # too short to replace
            continue

        original_tag = original_tagged[i][1]
        replacement_key = make_replacement_key(token, original_tag)
        if replacement_key in replacements:
            # we've already found a replacement for this token
            continue

        key = make_key(token)
        if key not in crd:
            # no replacement possible
            continue

        random.shuffle(crd[key])
        for c, candidate in enumerate(crd[key]):
            candidate = match_case(token, candidate)
            if candidate == token:
                # don't replace with the same word
                continue
            tokens[i] = candidate
            tagged = nltk.pos_tag(tokens)
            if tagged[i][1] == original_tag:
                replacements[replacement_key] = candidate.upper()

                crd[key].pop(c)
                if len(crd[key]) == 0:
                    del crd[key]

                break

    # found all replacements, now re-build the text using them
    
    r = 0
    text_out = ""
    for i, token in enumerate(original_tokens):
        original_tag = original_tagged[i][1]
        replacement_key = make_replacement_key(token, original_tag)

        new_token = token
        # use replacement if possible
        if replacement_key in replacements:
            new_token = replacements[replacement_key]
            new_token = match_case(token, new_token)

        text_part = text[r:r+len(token)]
        # account for whitespace
        while text_part != token:
            text_out += text[r:r+1]
            r += 1
            if r+len(token) > len(text):
                print("Error: this should never happen")
                sys.exit()
            text_part = text[r:r+len(token)]

        r += len(token)
        text_out += new_token

    return text_out

def main():
    # read crd from file
    crd = {}
    with open('crd.pkl', 'rb') as f:
        crd = pickle.load(f)

    # replace text
    replaced = replace_text(TEXT, crd)
    print(replaced)

if __name__ == "__main__":
   main()



