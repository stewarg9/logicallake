
GRAMMAR_DIR = "..\\"


def main():
    import pprint
    import json
    from tatsu import parse, compile, to_python_model
    from tatsu.util import asjson
    
    import tatsu
    
    input =  """SELECT * FROM masterdata."DataIngestion.SDI.FLATFILE.MDM::APO_LOCATION" ;"""

    #input = "SELECT * FROM MARA;"
    

    # Load the grammar in from a reference file. 
    with open(GRAMMAR_DIR + "HANA_SQL_Grammar.bnf") as f:
        grammar = f.read()
    
    model = compile(grammar)

    munged_input = input.replace(',', ' , ')

    ast = model.parse(munged_input)

    #print(ast)
    
    result = str(json.dumps(asjson(ast), sort_keys = True))

    print(result)

if __name__ == '__main__':
    main()


