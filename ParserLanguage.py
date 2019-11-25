#//////////////////////////////////////////////////////////////////////////////////////////////////////#

# VERSI : 25 NOVEMBER 2019

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

#   MUHAMMAD ANGGA RISFANANI
#   WILDAN ZAIM SYADDAD

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

# Global dictionary used for storing the rules.
RULE_DICT = {}


def read_grammar(grammar_file):
    """
    Reads in the given grammar file and splits it into separate lists for each rule.
    :param grammar_file: the grammar file to read in.
    :return: the list of rules.
    """
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]


def add_rule(rule):
    """
    Adds a rule to the dictionary of lists of rules.
    :param rule: the rule to add to the dict.
    """
    global RULE_DICT

    if rule[0] not in RULE_DICT:
        RULE_DICT[rule[0]] = []
    RULE_DICT[rule[0]].append(rule[1:])


def convert_grammar(grammar):
    """
        Converts a context-free grammar in the form of

        S -> NP VP
        NP -> Det ADV N

        and so on into a chomsky normal form of that grammar. After the conversion rules have either
        exactly one terminal symbol or exactly two non terminal symbols on its right hand side.

        Therefore some new non terminal symbols might be created. These non terminal symbols are
        named like the symbol they replaced with an appended index.
    :param grammar: the CFG.
    :return: the given grammar converted into CNF.
    """

    # Remove all the productions of the type A -> X B C or A -> B a.
    global RULE_DICT
    unit_productions, result = [], []
    res_append = result.append
    index = 0

    for rule in grammar:
        new_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Rule is in form A -> X, so back it up for later and continue with the next rule.
            unit_productions.append(rule)
            add_rule(rule)
            continue
        elif len(rule) > 2:
            # Rule is in form A -> X B C or A -> X a.
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                for item in terminals:
                    # Create a new non terminal symbol and replace the terminal symbol with it.
                    # The non terminal symbol derives the replaced terminal symbol.
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    new_rules += [f"{rule[0]}{str(index)}", item[0]]
                index += 1
            while len(rule) > 3:
                new_rules += [f"{rule[0]}{str(index)}", rule[1], rule[2]]
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1
        # Adds the modified or unmodified (in case of A -> x i.e.) rules.
        add_rule(rule)
        res_append(rule)
        if new_rules:
            res_append(new_rules)
    # Handle the unit productions (A -> X)
    while unit_productions:
        rule = unit_productions.pop()
        if rule[1] in RULE_DICT:
            for item in RULE_DICT[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    res_append(new_rule)
                else:
                    unit_productions.append(new_rule)
                add_rule(new_rule)
    return result

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

class Node:
    """
    Used for storing information about a non-terminal symbol. A node can have a maximum of two
    children because of the CNF of the grammar.
    It is possible though that there are multiple parses of a sentence. In this case information
    about an alternative child is stored in self.child1 or self.child2 (the parser will decide
    where according to the ambiguous rule).
    Either child1 is a terminal symbol passed as string, or both children are Nodes.
    """

    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        """
        :return: the string representation of a Node object.
        """
        return self.symbol


class Parser:
    """
    A CYK parser which is able to parse any grammar in CNF. The grammar can be read from a file or
    passed as a string. It either returns a string representation of the parse tree(s) or prints it
    to standard out.
    """

    def __init__(self, grammar, sentence):
        """
        Creates a new parser object which will read in the grammar and transform it into CNF and
        then parse the given sentence with that grammar.
        :param grammar: the file path to the grammar/the string repr. of the grammar to read in
        :param sentence: the file path to the sentence/the string repr. of the sentence to read in
        """
        self.parse_table = None
        self.prods = {}
        self.grammar = None

        self.grammar = convert_grammar(read_grammar(grammar))
        self.__call__(sentence)

    def __call__(self, sentence, parse=False):
        """
        Parse the given sentence (string or file) with the earlier given grammar.
        :param sentence: the sentence to parse with self.grammar
        """
        with open(sentence) as inp:
            self.input = inp.readline().split()
            for inputs in (self.input):
                print(inputs)
            if parse:
                self.parse()

    def parse(self):
        """
        Does the actual parsing according to the CYK algorithm. The parse table is stored in
        self.parse_table.
        """
        length = len(self.input)
        # self.parse_table[y][x] is the list of nodes in the x+1 cell of y+1 row in the table.
        # That cell covers the word below it and y more words after.
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            # Find out which non terminals can generate the terminals in the input string
            # and put them into the parse table. One terminal could be generated by multiple
            # non terminals, therefore the parse table will contain a list of non terminals.
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.parse_table[0][i].append(Node(rule[0], word))
        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size

                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )

    def print_tree(self, output=True):
        """
        Print the parse tree starting with the start symbol. Alternatively it returns the string
        representation of the tree(s) instead of printing it.
        """
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                print("Accepted") # Not Accepted
                print("\nPossible parse(s):")
            trees = [generate_tree(node) for node in final_nodes] # Accepted
            if output:
                for tree in trees:
                    print(tree)
            else:
                return trees
        else:
            print("Syntax Error") # Not Accepted

def generate_tree(node):
    """
    Generates the string representation of the parse tree.
    :param node: the root node.
    :return: the parse tree in string form.
    """
    if node.child2 is None:
        return f"[{node.symbol} '{node.child1}']"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"

if __name__ == '__main__':
    grammar = str(input('Masukkan Nama File Grammar : '))
    sentence = str(input('Masukkan Nama File Input : '))
    CYK = Parser(grammar, sentence)
    CYK.parse()
    CYK.print_tree()
