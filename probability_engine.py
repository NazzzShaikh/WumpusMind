class ProbabilityEngine:
    def __init__(self, kb, pit_prob, wumpus_count=1):
        self.kb = kb
        self.pit_prob = pit_prob
        self.wumpus_count = wumpus_count

    def calculate_risks(self):
        """
        Calculates a rough Bayesian risk for each unknown cell based on known breezes and stenches.
        Returns a dict: { (x,y): risk_score (0.0 to 1.0) }
        Where 0.0 is definitely safe, 1.0 is definitely death.
        """
        risks = {}
        for x in range(self.kb.size):
            for y in range(self.kb.size):
                p = (x, y)
                if p in self.kb.safe:
                    risks[p] = 0.0
                elif p in self.kb.pits or p in self.kb.wumpus:
                    risks[p] = 1.0
                else:
                    # Very simplified probabilistic calculation for performance:
                    # Count how many adjacent breezes / stenches are unresolved
                    breeze_count = sum(1 for adj in self.kb._get_adjacent(p) if adj in self.kb.breezes)
                    stench_count = sum(1 for adj in self.kb._get_adjacent(p) if adj in self.kb.stenches)
                    
                    pit_risk = self.pit_prob
                    if breeze_count > 0:
                        pit_risk += breeze_count * 0.2
                    if p in self.kb.no_pits:
                        pit_risk = 0.0
                        
                    wumpus_risk = 0.1 # Base prior
                    if stench_count > 0:
                        wumpus_risk += stench_count * 0.4
                    if p in self.kb.no_wumpus:
                        wumpus_risk = 0.0
                        
                    # Joint probability of hazard (either pit or wumpus)
                    joint_risk = 1 - ((1 - min(pit_risk, 0.99)) * (1 - min(wumpus_risk, 0.99)))
                    risks[p] = joint_risk
        
        return risks

    def get_best_guess(self):
        """
        Returns the least risky unvisited cell and its reasoning.
        """
        risks = self.calculate_risks()
        
        reachable_unknowns = set()
        for safe_cell in self.kb.safe:
            for adj in self.kb._get_adjacent(safe_cell):
                if adj not in self.kb.safe and adj not in self.kb.visited:
                    reachable_unknowns.add(adj)
                    
        unvisited = [p for p in reachable_unknowns if p in risks and risks[p] < 1.0]
        
        if not unvisited:
            return None, "No available guesses.", 0.0
            
        best_cell = min(unvisited, key=lambda p: risks[p])
        confidence = 1 - risks[best_cell]
        
        reasoning = f"Bayesian Inference: Calculated joint risk. Chose {best_cell} with {confidence*100:.1f}% confidence."
        return best_cell, reasoning, confidence
