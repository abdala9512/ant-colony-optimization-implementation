""""Data process"""

class DataReader:


    def __init__(self, file):
        """
        DataReader Initialization
        
        Args:
            file (str): filepath 
        """
        self.file = file
        self.data = self._readTXT()
        self.universe, self.sets = tuple( int(i) for i in self.data[0].split() ) 
        self.sets, self.costs  = self._processTXT(self.data)

    def _readTXT(self):
        """
        Reads filepath.
        """
        with open(self.file) as f:
            data = f.readlines()
        return data

    def _processTXT(self, data):
        """
        Generate sets and costs
        
        Args:
            data (List): List of lines of data read
        
        """
        
        sets = [ [ int(j) for j in i.split()[1: ] ] for i in data[1:] ]
        costs = [ int(i.split()[0])  for i in data[1:] ]
        return  sets, costs
