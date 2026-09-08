"""Rules engine and template parser"""

from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
import re

class RuleType(str, Enum):
    """Rule types"""
    CASE = "case"
    PINYIN = "pinyin"
    NUMBER = "number"
    SYMBOL = "symbol"
    COMBINE = "combine"
    FILTER = "filter"

@dataclass
class Rule:
    """Rule definition"""
    id: str
    type: RuleType
    name: str
    description: str
    config: Dict[str, Any]
    enabled: bool = True
    order: int = 0

class RuleParser:
    """Template parser for complex rules"""
    
    TEMPLATE_PATTERN = re.compile(r'\{([^}]+)\}')
    
    def __init__(self):
        self.variables: Dict[str, List[str]] = {}
    
    def parse_template(self, template: str) -> List[str]:
        """Parse template string and return possible combinations"""
        # Extract variables
        vars_found = self.TEMPLATE_PATTERN.findall(template)
        
        if not vars_found:
            return [template]
        
        # Build combinations
        results = []
        self._build_combinations(template, vars_found, 0, "", results)
        return results
    
    def _build_combinations(self, template: str, vars_list: List[str], 
                           index: int, current: str, results: List[str]):
        """Recursively build combinations"""
        if index == len(vars_list):
            results.append(current or template)
            return
        
        var = vars_list[index]
        if var in self.variables:
            for value in self.variables[var]:
                placeholder = "{" + var + "}"
                new_template = template.replace(placeholder, str(value), 1)
                self._build_combinations(
                    new_template, vars_list, index + 1, new_template, results
                )
        else:
            self._build_combinations(template, vars_list, index + 1, current, results)
    
    def register_variable(self, name: str, values: List[str]):
        """Register a variable for template substitution"""
        self.variables[name] = values

class PresetLibrary:
    """Password pattern presets"""
    
    PRESETS = {
        "company": {
            "name": "Company Pattern",
            "description": "Company-style passwords",
            "templates": [
                "{company}{year}",
                "{company_abbr}{number}",
                "{department}{emp_id}"
            ]
        },
        "personal": {
            "name": "Personal Pattern",
            "description": "Personal-style passwords",
            "templates": [
                "{name}{birthday}",
                "{nickname}{year}",
                "{hobby}{number}"
            ]
        },
        "mixed": {
            "name": "Mixed Pattern",
            "description": "Mixed-style passwords",
            "templates": [
                "{name}{place}{date}",
                "{brand}{number}{symbol}",
                "{keyword}{year}{emoji}"
            ]
        },
        "keyboard": {
            "name": "Keyboard Pattern",
            "description": "Keyboard trace patterns",
            "templates": [
                "qwerty",
                "1q2w3e4r",
                "asdfgh"
            ]
        }
    }
    
    @classmethod
    def get_preset(cls, name: str) -> Dict[str, Any]:
        """Get preset by name"""
        return cls.PRESETS.get(name)
    
    @classmethod
    def list_presets(cls) -> List[Dict[str, str]]:
        """List all presets"""
        return [
            {"name": k, "title": v["name"], "description": v["description"]}
            for k, v in cls.PRESETS.items()
        ]

class RuleEngine:
    """Rule execution engine"""
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.parser = RuleParser()
    
    def add_rule(self, rule: Rule):
        """Add a rule"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.order)
    
    def execute(self, seeds: List[str], variables: Dict[str, List[str]] = None) -> List[str]:
        """Execute rules chain"""
        if variables:
            for name, values in variables.items():
                self.parser.register_variable(name, values)
        
        results = seeds.copy()
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            # Rule execution logic here
        
        return results
    
    def preview(self, seeds: List[str], limit: int = 5) -> List[str]:
        """Preview rule results"""
        results = self.execute(seeds)
        return results[:limit]

# Global rule engine instance
rule_engine = RuleEngine()
