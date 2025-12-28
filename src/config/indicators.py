from dataclasses import dataclass
from typing import List

@dataclass
class Indicator:
    name: str          # Indicator name
    unit: str          # Measurement unit
    keywords: List[str] # Keywords/aliases for heuristic routing

INDICATORS = [
    Indicator("Total Scope 1 GHG Emissions", "tCO2e", ["scope 1", "direct emissions", "ghg"]),
    Indicator("Total Scope 2 GHG Emissions", "tCO2e", ["scope 2", "indirect emissions", "market-based"]),
    Indicator("Total Scope 3 GHG Emissions", "tCO2e", ["scope 3", "value chain", "financed emissions"]),
    Indicator("GHG Emissions Intensity", "tCO2e/€M", ["emissions intensity", "carbon intensity", "intensity ratio"]),
    Indicator("Total Energy Consumption", "MWh", ["energy consumption", "total energy use", "gigajoules"]),
    Indicator("Renewable Energy Percentage", "%", ["renewable energy", "renewable electricity", "green energy"]),
    Indicator("Net Zero Target Year", "Year", ["net zero", "carbon neutral", "2030", "2050"]),
    Indicator("Green Financing Volume", "€ Millions", ["green financing", "sustainable bonds", "green loan"]),
    
    Indicator("Total Employees", "FTE", ["total employees", "full time equivalent", "workforce size"]),
    Indicator("Female Employees", "%", ["gender diversity", "women employees", "female workforce"]),
    Indicator("Gender Pay Gap", "%", ["gender pay gap", "pay equity", "remuneration gap"]),
    Indicator("Training Hours per Employee", "Hours", ["training hours", "learning hours", "development hours"]),
    Indicator("Employee Turnover Rate", "%", ["turnover rate", "attrition", "voluntary departure"]),
    Indicator("Work-Related Accidents", "Count", ["accidents", "injuries", "lost time", "safety incidents"]),
    Indicator("Collective Bargaining Coverage", "%", ["collective bargaining", "union coverage", "social dialogue"]),
    
    Indicator("Board Female Representation", "%", ["board diversity", "women on board", "female directors"]),
    Indicator("Board Meetings", "Count", ["board meetings", "number of meetings"]),
    Indicator("Corruption Incidents", "Count", ["corruption", "bribery", "whistleblowing", "ethics"]),
    Indicator("Avg Payment Period to Suppliers", "Days", ["payment practices", "payment period", "supplier payments"]),
    Indicator("Suppliers Screened for ESG", "%", ["suppliers screened", "supply chain audit", "esg screening"]),
]