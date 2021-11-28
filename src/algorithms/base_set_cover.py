"""Base Set Covering class"""

from src.utils import BaseLogger


class SetCovering(BaseLogger):
    
    
    def __init__(self, subsets: List, costs: List) -> None:
        """ Set convering initialization
        """
        super().__init__()
        self.subsets = subsets
        self.costs   = costs
        self.universe = self.__identify_unique_items()
        self.total_set_elements = len(self.universe)
        self.total_subsets      = len(subsets)
    
    def __identify_unique_items(self) -> Set:
        """Find all unique elements of data structure
        
        """
        return { item for instance in self.subsets for item in instance }
    
    def random_cover(self):
        """ Create a set covering random solution
        
        """
        covered = set()
        selected_subsets = []
        cost = 0
        while covered != self.universe:
            
            subset_idx = random.randint(0, self.total_subsets - 1 )
            subset     = set( self.subsets[subset_idx] )
            
            selected_subsets.append(subset_idx)
            covered |= subset
            
            cost += self.costs[subset_idx]
        
        self.logger.info(f">>> Total covering cost: {cost}")
        self.logger.info(f">>> Total subsets selected: {len(selected_subsets)}")
        
        return selected_subsets, cost
            
        
            
            
            
        