# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:21:17 2020

@author: kbzg512
"""



import unittest

from tatsu import parse, compile, to_python_model
from tatsu.util import asjson

import tatsu
import json


GRAMMAR_DIR = "..\\"


#
#
#   Things to be aware of... 
#       The granmar is case insensitive; it's munching stuff to upper case. 
#
#


class TestGrammar(unittest.TestCase):
    



    def setUp(self):    
        
        # Load the grammar in from a reference file. 
        with open(GRAMMAR_DIR + "HANA_SQL_Grammar.bnf") as f:
            grammar = f.read()
        
        self.debug = False
        
        self.model = compile(grammar)


    def generate_ast(self, input):
        
        munged_input = input.replace(',', '  ,  ')
        
        self.ast = self.model.parse(munged_input)

        result = str(json.dumps(asjson(self.ast), sort_keys=True))
    
        return result        


    def test_simple_select_from(self):

        input = "SELECT * FROM MARA;"
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        result = self.generate_ast(input)

        if self.debug:
            print()
            print(target)
            print(result)
                
        self.assertEqual(result, target)
        



    def test_simple_select_from_alias(self):

        input = "SELECT * FROM MARA AS A;"
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        result = self.generate_ast(input)
        
        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)
        

    def test_simple_select_single_column(self):

        input = "SELECT ZSID FROM MARA AS A;"
        
        result = self.generate_ast(input)
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": {"column_name": "ZSID"}}]}, ";"]"""

        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)
        
        
        
        
    def test_simple_select_column_list(self):

        input = "SELECT MATNR,ZSID FROM MARA AS A;"
        
        result = self.generate_ast(input)
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": [{"column_name": "MATNR"}, {"column_name": "ZSID"}]}]}, ";"]"""

        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)
        
        
        
        
        
    def test_simple_select_column_list_column_alias(self):

        input = "SELECT MATNR,ZSID,TXT40 AS Short_Desc FROM MARA AS A;"
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": [{"column_name": "MATNR"}, {"column_name": "ZSID"}, {"column_alias": {"identifier": "Short_Desc"}, "column_name": "TXT40"}]}]}, ";"]"""
        
        result = self.generate_ast(input)

        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)
                



    def test_simple_join(self):

        input = "SELECT * FROM MARA AS A LEFT OUTER JOIN MAKT AS B ON A.ZSID = B.ZSID;"
        
        result = self.generate_ast(input)
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "joined_table": {"join_predicate": {"comparison_predicate": {"comparison_operator": "=", "expression": [{"identifier": ["A", "ZSID"]}, {"identifier": ["B", "ZSID"]}]}}, "join_type": [["LEFT"], "OUTER"], "table_ref": {"table_alias": "B", "table_name": {"identifier": "MAKT"}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)





    def test_simple_where(self):

        input = "SELECT * FROM MARA AS A WHERE 4 = 4;"
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_alias": "A", "table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": "*"}], "where_clause": {"condition": {"predicate": {"comparison_predicate": {"comparison_operator": "=", "expression": [{"constant": ["4", []]}, {"constant": ["4", []]}]}}}}}, ";"]"""
        
        result = self.generate_ast(input)

        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(str(result), str(target))



    def test_real_world_from(self):

        # This one is a bit clunky. 
        # Need to ensure the expected result escapes the backslash used to escape the quote... !

        input = """SELECT * FROM masterdata."DataIngestion.SDI.FLATFILE.MDM::APO_LOCATION" ;"""
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_name": {"identifier": ["\\"", ["DataIngestion.SDI.FLATFILE.MDM::APO_LOCATION"], "\\""], "schema_name": "masterdata"}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        result = self.generate_ast(input)

        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)




    def test_column_alias_multiple_wheres(self):

        # This one is a bit clunky. 
        # Need to ensure the expected result escapes the backslash used to escape the quote... !

        input = """SELECT ZSID,matnr,mara.fED AS blah FROM MARA WHERE ZSID = 'EU3' AND ID = 4; """
        
        target = """[{"from_clause": {"table_expression": {"table_ref": {"table_name": {"identifier": "MARA"}}}}, "select_clause": ["SELECT", {"selectitem": [{"column_name": "ZSID"}, {"column_name": "matnr"}, {"column_alias": {"identifier": "blah"}, "column_name": "fED", "table_alias": "mara"}]}], "where_clause": {"condition": {"and": "AND", "condition": [{"predicate": {"comparison_predicate": {"comparison_operator": "=", "expression": [{"identifier": "ZSID"}, {"constant": ["'", ["EU3"], "'"]}]}}}, {"predicate": {"comparison_predicate": {"comparison_operator": "=", "expression": [{"identifier": "ID"}, {"constant": ["4", []]}]}}}]}}}, ";"]"""
        
        result = self.generate_ast(input)
        
        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)



    def test_simple_nested_subquery(self):


        input = """SELECT * FROM (SELECT ZSID FROM (SELECT * FROM (SELECT 1 FROM DUNCE)));"""
        
        target = """[{"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"table_ref": {"table_name": {"identifier": "DUNCE"}}}}, "select_clause": ["SELECT", {"selectitem": {"expression": {"constant": ["1", []]}}}]}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}}}}, "select_clause": ["SELECT", {"selectitem": {"column_name": "ZSID"}}]}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        result = self.generate_ast(input)
        
        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)



    def test_complicated_nested_subquery(self):


        input = """SELECT * FROM (SELECT ZSID FROM (SELECT B.* FROM (SELECT A.ID FROM DUNCE AS A) B ) C);"""
        
        target = """[{"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"subquery": {"select_statement": {"from_clause": {"table_expression": {"table_ref": {"table_name": {"identifier": "DUNCE"}}}}, "select_clause": ["SELECT", {"selectitem": {"expression": {"constant": ["1", []]}}}]}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}}}}, "select_clause": ["SELECT", {"selectitem": {"column_name": "ZSID"}}]}}}}, "select_clause": ["SELECT", {"selectitem": "*"}]}, ";"]"""
        
        result = self.generate_ast(input)
        
        if self.debug:
            print()
            print(target)
            print(result)
        
        self.assertEqual(result, target)






if __name__ == '__main__':
    unittest.main()
