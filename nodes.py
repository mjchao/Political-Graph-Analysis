"""Manages bill, legislator and company data.

Flow:
0. (Optionally) Specify all the properties you want by calling
	Add<Bill/Legislator/Company>Properties(). The properties will be added
	to the dataframe in order in which they appear in the list.
1. Determine the properties of all your bills/legislators/companies. Store them
	in a dict. E.g. {"id": 1, "Name": "Barack Obama"}
2. Call Add<Bill/Legislator/Company>() on the dicts with the properties.
"""
import os
import pandas as pd

_bills = pd.DataFrame()
_legislators = pd.DataFrame()
_companies = pd.DataFrame()

def Save(save_dir):
    """Saves the bills, legislators, and companies data to the given directory.
    The data are saved in files "bills.csv", "legislators.csv", and
    "companies.csv", respectively.

    Args:
            save_dir: (string) The directory in which to save.
    """
    _bills.to_csv(os.path.join(save_dir, "bills.csv"), index=False)
    _legislators.to_csv(os.path.join(save_dir, "legislators.csv"), index=False)
    _companies.to_csv(os.path.join(save_dir, "companies.csv"), index=False)


def Load(load_dir):
    """Loads the bills, legislators, and companies data from a given directory.
    The data is expected to be in files named "bills.csv", "legislators.csv",
    and "companies.csv", respectively.
    
    Args:
            load_dir: (string) The directory form which to load
    """
    _bills = pd.read_csv(os.path.join(load_dir, "bills.csv"))
    _legislators = pd.read_csv(os.path.join(load_dir, "legislators.csv"))
    _companies = pd.read_csv(os.path.join(load_dir, "companies.csv"))


def Reset():
    """Clears all the data.
    """
    _bills.drop(_bills.index, inplace=True)
    _bills.drop(_bills.columns, axis=1, inplace=True)

    _legislators.drop(_legislators.index, axis=0, inplace=True)
    _legislators.drop(_legislators.columns, axis=1, inplace=True)

    _companies.drop(_companies.index, axis=0, inplace=True)
    _companies.drop(_companies.columns, axis=1, inplace=True)


def _EnsureColumnsExist(df, column_names):
    """Ensures that the given columns exist in the dataframe.

    Args:
            df: (DataFrame) A dataframe.
            column_names: (list of string) A list of column names that should be
                    in the given dataframe.
    """
    for col in column_names:
            if col not in df.columns:
                    df[col] = pd.Series([None for _ in range(len(df))], dtype=object)


def _AddEntryToDf(df, entry_data):
    """Adds an entry to the given dataframe. Any new columns will automatically
    be added to the dataframe.

    Args:
            df: (DataFrame) A dataframe.
            entry_data: (dict) A dictionary mapping columns to values.
    """
    _EnsureColumnsExist(df, entry_data.keys())
    
    # Cannot just set directly to an array. Must be done iteratively
    # or else Pandas will be confused by the data types.
    new_row_idx = len(df)
    for name in df.columns:
            if name in entry_data:
                    df.loc[new_row_idx, name] = entry_data[name]
            else:
                    df.loc[new_row_idx, name] = None


def AddBillProperties(properties):
    """Adds the given properties to the bills dataframe. The properties will
    be added in the order specified by the list.

    Args:
            properties: (list of str) The properties that are relevant to  bills.
                    These get added as the columns of the bills dataframe if they
                    don't already exist.
    """
    _EnsureColumnsExist(_bills, properties)


def AddBill(bill_data):
    """Adds another bill to the dataset. Any new properties will automatically
    be added to the dataframe. Any properties in the dataframe not specified
    will be set to None. There is no guarantee on the order in which new
    properties are added since dict has no ordering. You can use
    AddBillProperties to specify the ordering of your properties up front.

    Args:
            bill_data: (dict) A dictionary that maps bill properties to values. For
                    example, {"id": 12345, "date": "25-09-2016"} will add a bill with
                    its id set to 12345 and date set to "25-09-2016".
    """
    _AddEntryToDf(_bills, bill_data)


def GetBills(copy=False):
    """Returns the bills in the dataset.

    Args:
            copy: (bool) Whether to make a deep copy.

    Returns:
            (DataFrame) The bills dataframe.
    """
    if copy:
            return pd.DataFrame.copy(_bills)
    else:
            return _bills


def AddLegislatorProperties(properties):
    """Adds the given properties to the legislators dataframe.

    Args:
            properties: (list of str) The properties that are relevant to
                    legislators. These get added as the columns of the legislators
                    dataframe if they don't already exist.
    """
    _EnsureColumnsExist(_legislators, properties)


def AddLegislator(legislator_data):
    """Adds another legislator to the dataset. Any new properties will
    automatically be added to the dataframe. Any properties in the dataframe
    not specified will be set to None. There is no guarantee on the order in
    which new properties are added since dict has no ordering. You can use
    AddLegislatorProperties to specify the ordering of your properties up front.

    Args:
            legislator_data: (dict) A dictionary that maps legislator properties to
                    values. For example, {"firstname": Barack, "lastname": "Obama"} will
                    add a legislator with its firstname set to "Barack" and lastname
                    set to "Obama".
    """
    _AddEntryToDf(_legislators, legislator_data)


def GetLegislators(copy=False):
    """Returns the legislators in the dataset.

    Args:
            copy: (bool) Whether to make a deep copy.

    Returns:
            (DataFrame) The legislators dataframe.
    """
    if copy:
            return pd.DataFrame.copy(_legislators)
    else:
            return _legislators


def AddCompanyProperties(properties):
    """Adds the given properties to the companies dataframe.

    Args:
            properties: (list of string) The properties that are relevant to
                    companies. These get added as the columns of the companies
                    dataframe if they don't already exist.
    """
    _EnsureColumnsExist(_companies, properties)


def AddCompany(company_data):
    """Adds another company to the dataset. Any new properties will
    automatically be added to the dataframe. Any properties in the dataframe
    not specified will be set to None. There is no guarantee on the order in
    which new properties are added since dict has no ordering. You can use
    AddCompanyProperties to specify the ordering of your properties up front.

    Args:
            company_data: (dict) A dictionary that maps company properties to
                    values. For example, {"name": Google, "sector": "Technology"} will
                    add a company with its name set to "Google" and sector set to
                    "Technology".
    """
    _AddEntryToDf(_companies, company_data)


def GetCompanies(copy=False):
    """Returns the companies in the dataset.

    Args:
            copy: (bool) Whether to make a deep copy.

    Returns:
            (DataFrame) The companies dataframe.
    """
    if copy:
            return pd.DataFrame.copy(_comapnies)
    else:
            return _companies

