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
        self.item_scores        = self.__calculate_item_scores()
        self.set_probabilities  = self.__calculate_set_scores()
    
    def __identify_unique_items(self) -> Set:
        """Find all unique elements of data structure
        
        """
        return { item for instance in self.subsets for item in instance }
    
    def __calculate_item_scores(self):
        item_counts  = dict(
            Counter([item for sublist in self.subsets for item in sublist])
        )
        
        item_values = {}
        for key, value in item_counts.items():
            item_values[key] = 1 / (value / self.total_subsets)
        
        SCORE_MAX = max(item_values.values())
        SCORE_MIN = min(item_values.values())
        
        item_scores = {}
        for key, value in item_values.items():
            item_scores[key] = SetCovering.max_min_normalizer(value, max_val = SCORE_MAX, min_val = SCORE_MIN)
            
        return item_scores

    def __calculate_set_scores(self):
        """Return the average score for each subset"""
        scores = [np.mean([self.item_scores[i] for i in subset])   for subset in self.subsets]
        
        return  self.__calculate_probabilities(scores)
    
    
    def __calculate_probabilities(self, vals):
        total_sum     = sum(vals)
        return [ val / total_sum  for val in vals ]
        
    
    def cover(self, probs = None):
        """ Create a set covering solution
        """
        
        if not probs:
            prob_dist = self.set_probabilities
        
        all_available_subsets = [*range(self.total_subsets)]
        
        
        
        covered = set()
        selected_subsets = []
        cost = 0
        while covered != self.universe:
            
            scores_ = zip(all_available_subsets, self.__calculate_probabilities(prob_dist))
            scores_ = dict(scores_)
            
            subset_idx = self.__select_set(set_list = list( scores_.keys() ),
                                           probs = list( scores_.values() ))
            subset     = set( self.subsets[subset_idx] )
            #print(f"selected set: {subset_idx}")
            
            selected_subsets.append(subset_idx)
            covered |= subset
            
            cost += self.costs[subset_idx]
            
            del scores_[subset_idx]
            
            print(f"total cost: {cost}")
            print(f"total subsets used: {len(selected_subsets)}")
            print(f"elements covered {len(covered)}")
        
        self.logger.info(f">>> Total covering cost: {cost}")
        self.logger.info(f">>> Total subsets selected: {len(selected_subsets)}")
        
        return selected_subsets, cost

        
    def __select_set(self, set_list: List, probs = None):
        """Select a set index, regarding if the set already have appended to a subset_list"""
        subset_idx = np.random.choice( set_list, 
                                       size = 1, 
                                       p = probs)[0]
        return subset_idx
    
    @staticmethod
    def max_min_normalizer(num, max_val, min_val):
        return (num - min_val) / (max_val - min_val)

            