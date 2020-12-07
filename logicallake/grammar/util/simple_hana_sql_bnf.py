
GRAMMAR_DIR = "..\\"


def main():
    import pprint
    import json
    from tatsu import parse, compile, to_python_model
    from tatsu.util import asjson
    
    import tatsu
    
    input =  """SELECT * FROM (SELECT ZSID FROM (SELECT B.* FROM (SELECT A.ID FROM DUNCE AS A) B ) C);"""

    #input = "SELECT * FROM MARA;"
    

    # Load the grammar in from a reference file. 
    with open(GRAMMAR_DIR + "HANA_SQL_Grammar.bnf") as f:
        grammar = f.read()
    
    model = compile(grammar, verbose=True)

    munged_input = input.replace(',', ' , ')

    ast = model.parse(munged_input)

    #print(ast)
    
    result = str(json.dumps(asjson(ast), sort_keys = True, indent=2))

    print(result)

if __name__ == '__main__':
    main()



