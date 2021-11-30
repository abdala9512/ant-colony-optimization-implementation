"""Base Set Covering class"""

from collections import Counter
import numpy as np
from typing import Dict, List, Set



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
        self.set_scores         = self.__calculate_set_scores()
        self.set_probabilities  = self.__calculate_set_probabilities()
        self.max_len_set        = max([len(subset) for subset in self.subsets])
    
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

    def __calculate_set_probabilities(self):
        """Return the average score for each subset"""
        scores = [np.mean([self.item_scores[i] for i in subset])   for subset in self.subsets]
        
        return  self.__calculate_probabilities(scores)
    
    
    def __calculate_probabilities(self, vals):
        total_sum     = sum(vals)
        return [ val / total_sum  for val in vals ]
    
    def __calculate_set_scores(self):
        
        total_subsets = []
        for subset in self.subsets:
            subset_scores = [self.item_scores[i] for i in subset]
            subset_overall_score = np.average(subset_scores, weights= [item / sum(subset_scores) for item in subset_scores])
            total_subsets.append(subset_overall_score)
        return total_subsets
        
    
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

            subset_idx = self.__select_set(set_list = all_available_subsets)
            subset     = set( self.subsets[subset_idx] )
            
            selected_subsets.append(subset_idx)
            covered |= subset
            
            cost += self.costs[subset_idx]
            all_available_subsets.remove(subset_idx)
            
        
        self.logger.info(f">>> Total covering cost: {cost}")
        self.logger.info(f">>> Total subsets selected: {len(selected_subsets)}")
        
        return selected_subsets, cost

        
    def __select_set(self, set_list: List, probs = None):
        """Select a set index, regarding if the set already have appended to a subset_list"""
        subset_idx = random.randint(0, len(set_list) - 1)
        return set_list[subset_idx]
    
    @staticmethod
    def max_min_normalizer(num, max_val, min_val):
        return (num - min_val) / (max_val - min_val)

            