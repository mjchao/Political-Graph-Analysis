"""Test cases for node manager.
"""
import os
import unittest
import numpy as np
import pandas as pd
import nodes

class TestNodes(unittest.TestCase):

    def setUp(self):
        self._SAVE_DIR = os.path.join("tmp", "test")
        nodes.Reset()

    def testReset(self):
        nodes.AddLegislator({"id": 1})
        nodes.Reset()

        legislators = nodes.GetLegislators()
        expected = pd.DataFrame()
        self.assertTrue(expected.equals(legislators))

    def testAddBills(self):
        nodes.AddBillProperties(["id", "name", "date"])
        nodes.AddBill({"id": 1})	
        nodes.AddBill({"id": 2, "name": "Bill 2"})
        nodes.AddBill({"id": 3, "name": "Bill 3", "date": "25-10-2016"})

        bills = nodes.GetBills()
        expected = pd.DataFrame([[1, None, None],
                                [2, "Bill 2", None],
                                [3, "Bill 3", "25-10-2016"]],
                                columns=["id", "name", "date"], dtype=object)

        self.assertTrue(expected.equals(bills))

    def testAddLegislators(self):
        nodes.AddLegislatorProperties(["id", "name", "state"])
        nodes.AddLegislator({"id": 231, "name": "Alice", "state": "MO"})
        nodes.AddLegislator({"id": 423, "name": "Bob", "state": None})
        nodes.AddLegislator({"id": 23, "name": None, "state": "MI"})
        nodes.AddLegislator({"id": -12, "name": None, "state": None})

        legislators = nodes.GetLegislators()
        expected = pd.DataFrame([[231, "Alice", "MO"],
                                [423, "Bob", None],
                                [23, None, "MI"],
                                [-12, None, None]],
                                columns=["id", "name", "state"], dtype=object)
        self.assertTrue(expected.equals(legislators))

    def testAddCompanies(self):
        nodes.AddCompanyProperties(["id", "name", "ceo"])
        nodes.AddCompany({})
        nodes.AddCompany({"name": "Company 1", "ceo": "Bob"})
        nodes.AddCompany({"ceo": "Carl"})
        nodes.AddCompany({"id": 1, "name": "Company 3", "ceo": "David"})

        companies = nodes.GetCompanies()
        expected = pd.DataFrame([[None, None, None],
                                [None, "Company 1", "Bob"],
                                [None, None, "Carl"],
                                [1, "Company 3", "David"]],
                                columns=["id", "name", "ceo"], dtype=object)
        self.assertTrue(expected.equals(companies))

	
    def testLoadSave(self):
        nodes.AddBillProperties(["id", "name", "date"])
        nodes.AddBill({"id": 1})	
        nodes.AddBill({"id": 2, "name": "Bill 2"})
        nodes.AddBill({"id": 3, "name": "Bill 3", "date": "25-10-2016"})
        
        nodes.AddLegislatorProperties(["id", "name", "state"])
        nodes.AddLegislator({"id": 231, "name": "Alice", "state": "MO"})
        nodes.AddLegislator({"id": 423, "name": "Bob", "state": None})
        nodes.AddLegislator({"id": 23, "name": None, "state": "MI"})
        nodes.AddLegislator({"id": -12, "name": None, "state": None})

        nodes.AddCompanyProperties(["id", "name", "ceo"])
        nodes.AddCompany({})
        nodes.AddCompany({"name": "Company 1", "ceo": "Bob"})
        nodes.AddCompany({"ceo": "Carl"})
        nodes.AddCompany({"id": 1, "name": "Company 3", "ceo": "David"})

        bills = nodes.GetBills()
        legislators = nodes.GetLegislators()
        companies = nodes.GetCompanies()
        
        nodes.Save(self._SAVE_DIR)
        nodes.Load(self._SAVE_DIR)
        
        loaded_bills = nodes.GetBills()
        self.assertTrue(loaded_bills.equals(bills))
        loaded_legislators = nodes.GetLegislators()
        self.assertTrue(loaded_legislators.equals(legislators))
        loaded_companies = nodes.GetCompanies()
        self.assertTrue(loaded_companies.equals(companies))


if __name__ == "__main__":
	unittest.main()
