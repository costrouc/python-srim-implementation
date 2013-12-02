import pandas as pd

class Element:
    """
    Representation of an element
    """
    def __init__(self, symbol, atomicNumber, mass):
        self.symbol = symbol
        self.atomicNumber = atomicNumber
        self.mass = mass

class ElementTable:
    """
    Table that stores relavent element information
    """
    def __init__(self):
        self.element_table = pd.read_csv('element.csv')

    def get_elementbysymbol(self, element):
        for i, symbol in enumerate(self.element_table['Symbol']):
            if (element == symbol):
                name =  self.element_table.Name[i]
                symbol = self.element_table.Symbol[i]
                atomicNumber =  self.element_table.Atomic_Number[i]
                atomicMass =  self.element_table.Atomic_Mass[i]
                
                return Element(symbol, atomicNumber, atomicMass)
        return None
