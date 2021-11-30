""""Data process"""

from src.algorithms.ac_optimizer import ACOptimizer

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

    def __init__(self, aco_instance: ACOptimizer) -> None:
        self.aco_instance = aco_instance
        self.solutions = aco_instance.solutions
        self.total_iterations = len(aco_instance.solutions)
        self.iter_df = self.__prepare_data()
        
    def generate_report(self, filename = "iteration_history.csv") -> None:
         self.iter_df.to_csv(filename, index=False)
            
    @staticmethod  
    def save_image(img, filename):
        img.get_figure().savefig(filename)
    
    def pheromones_distribution(self):
        return sns.histplot(self.aco_instance.set_pheromones)
        
    def aco_algorithm_visuals(self):
        return sns.lineplot(x = 'iteration', y = 'avg_cost', data = self.iter_df)
    
    def __prepare_data(self):
        costs =  [[ant_solution[1] for ant_solution in iter_solution ] for iter_solution in self.solutions]
        iterations = [(i+1, np.mean(cost)) for i, cost in enumerate(costs)]
        df = pd.DataFrame(iterations, columns = ['iteration', 'avg_cost'])
        return df
    

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

