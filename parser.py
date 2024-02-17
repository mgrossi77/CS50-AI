import nltk
import sys
import string

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | CS
PP -> P NP
NP -> N | Det N | Det AJP NP | N PP | Det N PP | N AP | Det N AP
VP -> V | V PP | V NP | V NP PP | Det V | V AP
AP -> Adv | Adv AP
AJP -> Adj | Adj AJP
CS -> S Conj S | S Conj VP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    words = nltk.word_tokenize(sentence)

    final_words = []

    for word in words:
        if word_has_alphabet(word):
            final_words.append(word.lower())

    return final_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    ans = []

    def traverse_tree(tree):

        if tree.label() == "NP":
            flag = True

            stack = [tree]

            i = 0
            while stack:
                node = stack.pop()

                if i == 0:
                    i += 1

                else:
                    if node.label() == "NP":
                        flag = False
                        break

                for sub in node:

                    if type(sub) == nltk.tree.Tree:
                        stack.append(sub)

            if flag == True:
                ans.append(tree)

        for subtree in tree:

            if type(subtree) == nltk.tree.Tree:
                traverse_tree(subtree)

    traverse_tree(tree)

    return ans


def word_has_alphabet(word):

    for i in word:
        if i.isalpha():
            return True

    return False


if __name__ == "__main__":
    main()
