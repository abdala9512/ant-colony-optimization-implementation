
"""Ant System Metaherustic"""

import multiprocessing
import numpy as np
from typing import Dict, List, Set


from src.algorithms.base_set_cover import SetCovering
from src.utils import BaseLogger



class ACOptimizer(BaseLogger):
    
    def __init__(self, 
                 set_cover: SetCovering,
                 ants: int = 10,
                 evaporation_rate: float = 0.0,
                 alpha: float = 1.0,
                 beta:float = 0.0) -> None:
        
        """
        ACO algorithm initialization
        
        Args:
            saet_cover (SetCovering): set cover class with the subsets and costs
            ants (int): Number of ants in the instance
            evaporation_date (float):  pheromone's evaporation speed for each iteration
            
        """
        super().__init__()
        self.set_cover = set_cover
        self.ants = ants
        self.evaporation_rate = evaporation_rate
        self.heuristic_alpha = alpha
        self.heuristic_beta = beta
        self.set_initial_pheromones = self.__calc_pheromone()
        self.set_pheromones = [ 1 / self.set_cover.total_subsets for pheromone in self.set_initial_pheromones]
        self.initialized = False
        
    def __str__(self):
        return "ACO(ants = {ants}, evaporation_rate = {evaporation_rate})".format(ants = self.ants, evaporation_rate = self.evaporation_rate)
    
    
    def __calc_obj_function(self):
        pass
    
    def __calc_pheromone(self):
        
        """Calculates pheromone level by each set based on the length of the set
        
        """
        
        pheromones = []
        for i, subset in enumerate(self.set_cover.subsets):
                
            length_score =  len(subset) / self.set_cover.max_len_set
            rarity_score =  self.set_cover.set_probabilities[i]
            cost_score   =  self.set_cover.costs[i]
                
            metaheuristic_information = length_score * 0.1 + rarity_score * 0.6 + (1 / cost_score) * 0.3
            pheromones.append(metaheuristic_information)
            
        return pheromones
            
    
    def __initialize(self):
        
        pool = ACOptimizer.make_pool()
        result = pool.map(self.set_cover.cover, [ ant for ant in range(self.ants) ])
        pool.close()
        return result
    
    def __update_probabilities(self, solutions) -> None:
        """Update probabilities based on past solutions and evaporation rate"""
        
        self.set_pheromones = [pheromone * (1 - self.evaporation_rate)  for pheromone in self.set_pheromones]
        
        for solution in solutions:
            for i, subset in enumerate(solution[0]):
                self.set_pheromones[i] += self.set_initial_pheromones[i]
        
        
    def build_ant_solution(self, ant):
        
        #pool = ACOptimizer.make_pool()
        solutions = self.__set_cover_ant_solution()
        #pool.close()
        return solutions
    
    def __set_cover_ant_solution(self):
        
        probabilities = self.__weight_pheromones(self.set_pheromones)
        all_sets = [*range(self.set_cover.total_subsets)]
        
        covered = set()
        selected_subsets = []
        cost = 0
        while covered != self.set_cover.universe:

            subset_idx = np.random.choice(a = all_sets , p = probabilities)
            subset     = set( self.set_cover.subsets[subset_idx] )

            if subset_idx in selected_subsets:
                continue

            selected_subsets.append(subset_idx)
            covered |= subset

            cost += self.set_cover.costs[subset_idx]
    
        
        self.logger.info(f">>> Total covering cost: {cost}")
        self.logger.info(f">>> Total subsets selected: {len(selected_subsets)}")
        
        return selected_subsets, cost
    
    def __weight_pheromones(self, pheromones):
        total_sum     = sum(pheromones)
        return [ val / total_sum  for val in pheromones ]
    
    
    def __local_search(self):
        pass
    
    
    @staticmethod
    def make_pool():
        
        AVAILABLE_CORES = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(AVAILABLE_CORES)
        
        return pool
        
    
    def execute(self, iterations=2, mode='min', early_stopping_count=20, verbose=True) :
        
        
        # 1. Inicialization
        # Calculate pheromones, 
        #self.__initialize()
        
        for _ in range(iterations):
            print(f" iteratcio {_}: ")
            pool = ACOptimizer.make_pool()
            # Ant solutions
            solutions = pool.map(self.build_ant_solution, [1 for i in range(self.ants)])
            pool.close() 
            # local search
            self.__local_search()
            # Global update pheromones
            self.__update_probabilities(solutions)
            
        pool.close() 
        return solutions
        
        
