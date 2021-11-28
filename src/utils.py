""""Data process"""

from src.algorithms.ac_optimizer import ACOptimizer, SetCoverACO

class DataReader:


    def __init__(self, file) -> None:
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


class ACOAnalytics:

    def __init__(self, aco_instance: SetCoverACO) -> None:
        pass

class DataWriter:

    def __init__(self, aco_instance: SetCoverACO) ->None:
        pass

class BaseLogger:
    
    
    def __init__(self, logger_name: str = "Model Logger") -> None:
        
        self.logger_name = logger_name
        self.logger      =  logging.getLogger(self.logger_name)
        self.__logger_settings()
        # TODO: Check if the only handler needed is the StreamHandler
        for handler in self.logger.handlers: self.logger.removeHandler(handler)
        
        
    def __logger_settings(self) -> None:
        
        self.logger.setLevel(logging.INFO)
        logFileHandler = logging.FileHandler("./app.log",mode='w')
        consoleHandler  = logging.StreamHandler()
        logFormatter = logging.Formatter('%(name)s - %(levelname)s - [%(asctime)s] - %(message)s')
        
        consoleHandler.setFormatter(logFormatter)
        logFileHandler.setFormatter(logFormatter)
        
        self.logger.addHandler(logFileHandler)
        self.logger.addHandler(consoleHandler)

