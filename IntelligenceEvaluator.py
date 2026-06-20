class IntelligenceEvaluator:
    def __init__(self, asset, report):
        self.asset = asset
        self.report = report

    def calculate_desperation_penalty(self):
        # Count the number of desperation flags triggered (0 to 4)
        flags_active = sum(value for value in self.asset["desperation_flags"].values())
        return flags_active * 0.15  # 15% penalty per desperation flag

    def evaluate(self):
        # Base Score Calculation (Max 100)
        # Weights: Reliability (30%), Access (20%), Corroboration (30%), Plausibility (20%)
        base_score = (
            (self.asset["historical_reliability"] / 5) * 30 +
            (self.asset["access_capability"] / 5) * 20 +
            (self.report["corroboration_level"] / 5) * 30 +
            (self.report["plausibility"] / 5) * 20
        )

        penalty_multiplier = 1.0

        # DECISION TREE RULES
        
        # Rule 1: The "Too Good To Be True" Bias Trap
        if self.report["aligns_with_handler_bias"] and self.report["corroboration_level"] <= 2:
            penalty_multiplier -= 0.25

        # Rule 2: The Desperation / Urgency Loop
        if self.report["urgency_demand"]:
            desperation_penalty = self.calculate_desperation_penalty()
            penalty_multiplier -= desperation_penalty

        # Rule 3: Uncorroborated Exfiltration Demand (High Risk of Fabrication)
        if self.asset["desperation_flags"]["flight_risk_exfiltration_demanded"] and self.report["corroboration_level"] == 1:
            penalty_multiplier -= 0.40

        # Apply penalties (Floor at 0)
        final_score = max(0, base_score * penalty_multiplier)
        return self.generate_action_plan(final_score)

    def generate_action_plan(self, score):
        if score >= 80:
            return {"score": score, "status": "ACTIONABLE", "directive": "Proceed with operational planning."}
        elif 50 <= score < 80:
            return {"score": score, "status": "QUARANTINE", "directive": "Hold action. Mandate independent SIGINT/OSINT corroboration."}
        else:
            return {"score": score, "status": "FABRICATION RISK", "directive": "Reject intelligence. Initiate counterintelligence review of asset."}
