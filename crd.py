# builds the Candidate Replacement Dictionary
# key: xNy, where x is the first letter of the word, y is the last letter of the word, and N is the number of letters in the word - 2
# value: list of words that match the key
# values are pulled Collins Scrabble Words, 2015 (csw.txt)

# $ python3 crd.py

import pickle

MIN_WORD_LENGTH = 10

def make_key(val):
    num = len(val) - 2
    return val[0].lower() + str(num) + val[-1].lower()

def main():
    # read Collins Scrabble Words
    words = []
    with open('csw.txt') as f:
        words = f.readlines()
        words = [x.strip() for x in words]
        words = [x for x in words if len(x) >= MIN_WORD_LENGTH]
        words = [x.upper() for x in words]
        words.sort(key=len)

    # words[0] is the first ten-letter word to appear in csw.txt
    # words[1] is the second ten-letter word to appear in csw.txt
    # words[-1] is the last fifteen-letter word to appear in csw.txt
    # csw.txt happens to be uppercase and sorted alphabetically, but this code doesn't rely on that

    # build dictionary
    crd = {}
    for num in range(MIN_WORD_LENGTH, 16):
        print("working on", num, "...", end="", flush=True)
        for first in range(ord('A'), ord('Z')+1):
            for last in range(ord('A'), ord('Z')+1):
                tmp = []
                for word in words:
                    if len(word) > num:
                        break
                    if len(word) == num and word[0] == chr(first) and word[-1] == chr(last):
                        tmp.append(word)
                if len(tmp) > 0:
                    crd[make_key(tmp[0])] = tmp
        print("done")

    # save dictionary
    with open('crd.pkl', 'wb') as f:
        pickle.dump(crd, f)

if __name__ == "__main__":
   main()

