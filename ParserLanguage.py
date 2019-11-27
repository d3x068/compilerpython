#//////////////////////////////////////////////////////////////////////////////////////////////////////#

# VERSI : 25 NOVEMBER 2019

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

#   135 18 068 - WILDAN ZAIM SYADDAD
#   135 18 071 - MUHAMMAD ANGGA RISFANANI

#//////////////////////////////////////////////////////////////////////////////////////////////////////#

import itertools

#//////////////////////////////////////////////////////////////////////////////////////////////////////#
# HELPER #
#//////////////////////////////////////////////////////////////////////////////////////////////////////#

left, right = 0, 1

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def loadModel(modelPath):
	file = open(modelPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)
#Make production easy to work with
def cleanProduction(expression):
	result = []
	#remove spaces and explode on ";"
	rawRulse = expression.replace('\n','').split(';')
	
	for rule in rawRulse:
		#Explode evry rule on "->" and make a couple
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerms = rule.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			ereased.append(production)
			
	return trash, ereased
 
def setupDict(productions, variables, terms):
	result = {}
	for production in productions:
		#
		if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
			result[production[right][0]] = production[left]
	return result


def rewrite(target, production):
	result = []
	#get positions corresponding to the occurrences of target in production right side
	#positions = [m.start() for m in re.finditer(target, production[right])]
	positions = [i for i,x in enumerate(production[right]) if x == target]
	#for all found targets in production
	for i in range(len(positions)+1):
 		#for all combinations of all possible lenght phrases of targets
 		for element in list(itertools.combinations(positions, i)):
 			#Example: if positions is [1 4 6]
 			#now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
 			#erease position corresponding to the target in production right side
 			tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
 			if tadan != []:
 				result.append((production[left], tadan))
	return result

def dict2Set(dictionary):
	result = []
	for key in dictionary:
		result.append( (dictionary[key], key) )
	return result

def pprintRules(rules):
	for rule in rules:
		tot = ""
		for term in rule[right]:
			tot = tot +" "+ term
		print(rule[left]+" -> "+tot)

def prettyForm(rules):
	dictionary = {}
	for rule in rules:
		if rule[left] in dictionary:
			dictionary[rule[left]] += ' | '+' '.join(rule[right])
		else:
			dictionary[rule[left]] = ' '.join(rule[right])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result

#//////////////////////////////////////////////////////////////////////////////////////////////////////#
# CFG TO CNF CONVERTER #
#//////////////////////////////////////////////////////////////////////////////////////////////////////#

K, V, Productions = [],[],[]
variablesJar = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CW', 'CX', 'CY', 'CZ', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DW', 'DX', 'DY', 'DZ', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EW', 'EX', 'EY', 'EZ', 'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FU', 'FW', 'FX', 'FY', 'FZ', 'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GX', 'GY', 'GZ', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HU', 'HW', 'HX', 'HY', 'HZ', 'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL', 'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IW', 'IX', 'IY', 'IZ', 'JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ', 'JR', 'JS', 'JT', 'JU', 'JW', 'JX', 'JY', 'JZ', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KW', 'KX', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK', 'LL', 'LM', 'LN', 'LO', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LU', 'LW', 'LX', 'LY', 'LZ', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NW', 'NX', 'NY', 'NZ', 'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ', 'OK', 'OL', 'OM', 'ON', 'OO', 'OP', 'OQ', 'OR', 'OS', 'OT', 'OU', 'OW', 'OX', 'OY', 'OZ', 'PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PU', 'PW', 'PX', 'PY', 'PZ', 'QA', 'QB', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK', 'QL', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU', 'QW', 'QX', 'QY', 'QZ', 'RA', 'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ', 'RR', 'RS', 'RT', 'RU', 'RW', 'RX', 'RY', 'RZ', 'SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SU', 'SW', 'SX', 'SY', 'SZ', 'TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TU', 'TW', 'TX', 'TY', 'TZ', 'UA', 'UB', 'UC', 'UD', 'UE', 'UF', 'UG', 'UH', 'UI', 'UJ', 'UK', 'UL', 'UM', 'UN', 'UO', 'UP', 'UQ', 'UR', 'US', 'UT', 'UU', 'UW', 'UX', 'UY', 'UZ', 'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WW', 'WX', 'WY', 'WZ', 'XA', 'XB', 'XC', 'XD', 'XE', 'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XW', 'XX', 'XY', 'XZ', 'YA', 'YB', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YJ', 'YK', 'YL', 'YM', 'YN', 'YO', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YU', 'YW', 'YX', 'YY', 'YZ', 'ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZG', 'ZH', 'ZI', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZQ', 'ZR', 'ZS', 'ZT', 'ZU', 'ZW', 'ZX', 'ZY', 'ZZ']


def isUnitary(rule, variables):
	if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
		return True
	return False

def isSimple(rule):
	if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
		return True
	return False


for nonTerminal in V:
	if nonTerminal in variablesJar:
		variablesJar.remove(nonTerminal)

#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, variables):
	variables.append('S0')
	return [('S0', [variables[0]])] + productions
#Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def TERM(productions, variables):
	newProductions = []
	#create a dictionari for all base production, like A->a, in the form dic['a'] = 'A'
	dictionary = setupDict(productions, variables, terms=K)
	for production in productions:
		#check if the production is simple
		if isSimple(production):
			#in that case there is nothing to change
			newProductions.append(production)
		else:
			for term in K:
				for index, value in enumerate(production[right]):
					if term == value and not term in dictionary:
						#it's created a new production vaiable->term and added to it 
						dictionary[term] = variablesJar.pop()
						#Variables set it's updated adding new variable
						V.append(dictionary[term])
						newProductions.append( (dictionary[term], [term]) )
						
						production[right][index] = dictionary[term]
					elif term == value:
						production[right][index] = dictionary[term]
			newProductions.append( (production[left], production[right]) )
			
	#merge created set and the introduced rules
	return newProductions

#Eliminate non unitry rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, variables):
	result = []
	for production in productions:
		k = len(production[right])
		#newVar = production[left]
		if k <= 2:
			result.append( production )
		else:
			newVar = variablesJar.pop(0)
			variables.append(newVar+'1')
			result.append( (production[left], [production[right][0]]+[newVar+'1']) )
			i = 1
#TODO
			for i in range(1, k-2 ):
				var, var2 = newVar+str(i), newVar+str(i+1)
				variables.append(var2)
				result.append( (var, [production[right][i], var2]) )
			result.append( (newVar+str(k-2), production[right][k-2:k]) ) 
	return result
	

#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
	newSet = []
	#seekAndDestroy throw back in:
	#        – outlaws all left side of productions such that right side is equal to the outlaw
	#        – productions the productions without outlaws 
	outlaws, productions = seekAndDestroy(target='e', productions=productions)
	#add new reformulation of old rules
	for outlaw in outlaws:
		#consider every production: old + new resulting important when more than one outlaws are in the same prod.
		for production in productions + [e for e in newSet if e not in productions]:
			#if outlaw is present in the right side of a rule
			if outlaw in production[right]:
				#the rule is rewrited in all combination of it, rewriting "e" rather than outlaw
				#this cycle prevent to insert duplicate rules
				newSet = newSet + [e for e in  rewrite(outlaw, production) if e not in newSet]

	#add unchanged rules and return
	return newSet + ([productions[i] for i in range(len(productions)) 
							if productions[i] not in newSet])

def unit_routine(rules, variables):
	unitaries, result = [], []
	#controllo se una regola è unaria
	for aRule in rules:
		if isUnitary(aRule, variables):
			unitaries.append( (aRule[left], aRule[right][0]) )
		else:
			result.append(aRule)
	#altrimenti controllo se posso sostituirla in tutte le altre
	for uni in unitaries:
		for rule in rules:
			if uni[right]==rule[left] and uni[left]!=rule[left]:
				result.append( (uni[left],rule[right]) )
	
	return result

def UNIT(productions, variables):
	i = 0
	result = unit_routine(productions, variables)
	tmp = unit_routine(result, variables)
	while result != tmp and i < 1000:
		result = unit_routine(tmp, variables)
		tmp = unit_routine(result, variables)
		i+=1
	return result


def run_converter():
	global K, V, Productions

	modelPath = str(input('Masukkan Nama File Grammar : '))
	
	K, V, Productions = loadModel( modelPath )

	Productions = START(Productions, variables=V)
	Productions = TERM(Productions, variables=V)
	Productions = BIN(Productions, variables=V)
	Productions = DEL(Productions)
	Productions = UNIT(Productions, variables=V)

	Productions = convert_form(Productions)
	
	open('CNF_out.txt', 'w').write(	prettyForm(Productions) )

def convert_form(Products):
	length = len(Products)
	fix_form = [ [] for i in range(length) ]
	for i,Product in enumerate(Products):
		fix_form[i] += [Product[left]]
		if (len(Product[right])==1 and Product[right][0] in K):
			fix_form[i] += ["'"+Product[right][0]+"'"]
		else:
			fix_form[i] += Product[right]

	return fix_form

#//////////////////////////////////////////////////////////////////////////////////////////////////////#
# LEXER #
#//////////////////////////////////////////////////////////////////////////////////////////////////////#

def scan(nama_file):

    f = open(nama_file,'r')

    if(f.mode == 'r'):
        string = f.read()

    f.close()

    return string

# Membaca setiap token berdasarkan keywords
def ReadToken(nama_file):

    symbols = ['(', ')', ':', '[', ']', '=', '"', ',', '\n', "'", '#', '<', '>', '<=', '>=', '!='] # single-char keywords
    other_symbols = ['==', "'''"] # multi-char keywords
    keywords = ['False', 'None', 'True', 'and', 'as', 'break', 'class', 'continue', 'def', 'elif', 'else', 'for', 'from', 'if', 'import', 'in', 'is', 'not', 'or', 'pass', 'raise', 'return', 'while', 'with']
    KEYWORDS = symbols + other_symbols + keywords

    string = scan(nama_file)

    TabSentence = []
    
    white_space = ' '

    lexeme = ''
    for i,char in enumerate(string):
        if char == '=':
            if string[i+1] == '=':
                lexeme += '=='
            elif string[i-1] == '=':
                continue
            else:
                lexeme += '='
        elif char == "'":
            if string[i-1] == "'":
                if string[i+1] == "'":
                    continue
                elif string[i-2] == "'":
                    continue
                else:
                    lexeme += "''"
            elif string[i+1] == "'":
                if string[i+2] == "'":
                    lexeme += "'''"
                elif string[i-1] == "'":
                    continue
                else:
                    continue
            else:
                lexeme += "'"
        else:
            if char != white_space:
                lexeme += char # adding a char each time
        if (i+1 < len(string)): # prevents error
            if string[i+1] == white_space or string[i+1] in KEYWORDS or lexeme in KEYWORDS: # if next char == ' '
                if lexeme != '':
                    TabSentence += [lexeme.replace('\n', '<newline>')]
                    lexeme = ''
    TabSentence += [lexeme.replace('\n', '<newline>')]

    return TabSentence

def convert_Sentence_to_Separate(TabSentence):
	sprt_kword = ['class', 'def','for', 'from', 'if', 'import', 'while', 'with']

	TabIdxToken = []
	TabToken = []
	TabResult = []
	for i,sentence in enumerate(TabSentence):
		if sentence in sprt_kword:
			TabIdxToken += [i]
	TabIdxToken += [len(TabSentence)]
	if 0 in TabIdxToken == False:
		TabIdxToken = [0] + TabIdxToken
	for i in range(len(TabIdxToken)-1):
		for j in range(TabIdxToken[i], TabIdxToken[i+1]):
			TabToken += TabSentence[j].split()
		TabResult += [TabToken]
		TabToken = []

	return TabResult


#//////////////////////////////////////////////////////////////////////////////////////////////////////#
# PARSER #
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

        self.grammar = Productions
        self.__call__(sentence)

    def __call__(self, sentence, parse=False):
        """
        Parse the given sentence (string or file) with the earlier given grammar.
        :param sentence: the sentence to parse with self.grammar
        """
        with open(sentence) as inp:
            #self.input = inp.readline().split()
            self.input = convert_Sentence_to_Separate(ReadToken(sentence))
            #print(self.input)
            if parse:
                self.parse()

    def parse(self, idx):
        """
        Does the actual parsing according to the CYK algorithm. The parse table is stored in
        self.parse_table.
        """
        length = len(self.input[idx])
        # self.parse_table[y][x] is the list of nodes in the x+1 cell of y+1 row in the table.
        # That cell covers the word below it and y more words after.
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]
        #print('self.parse_table',self.parse_table)
        
        for i, word in enumerate(self.input[idx]):
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
        start_symbol = 'S0'
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                IsAccepted = True # Accepted
                #print("\nPossible parse(s):")
                #print("ACCEPTED")

                return IsAccepted

            #trees = [generate_tree(node) for node in final_nodes] # Accepted
            #if output:
                #for tree in trees:
                    #print(tree)
            #else:
                #return trees
        else:
            IsAccepted = False # Not Accepted
            #print("SYNTAX ERROR")
            return IsAccepted

def generate_tree(node):
    """
    Generates the string representation of the parse tree.
    :param node: the root node.
    :return: the parse tree in string form.
    """
    if node.child2 is None:
        return f"[{node.symbol} '{node.child1}']"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"

#///////////////////////////////////////////////////////////////////////////////////////////////#
# MAIN PROGRAM #
#///////////////////////////////////////////////////////////////////////////////////////////////#
def run_main():
    Accepted = True
    run_converter()
    grammar_file = "CNF_out.txt"
    sentence_file = str(input('Masukkan Nama File Input : '))
    CYK = Parser(grammar_file, sentence_file)
    for i in range(len(CYK.input)):
        CYK.parse(i)
        Accepted =  Accepted and CYK.print_tree()

    if Accepted:
        print('A C C E P T E D')
    else :
        print('S Y N T A X   E R R O R')

run_main()
