"""Transform/mutation processing"""

from typing import List, Set
from abc import ABC, abstractmethod
import re

class Transform(ABC):
    """Base transform class"""
    
    @abstractmethod
    def apply(self, text: str) -> List[str]:
        """Apply transformation and return variants"""
        pass

class CaseTransform(Transform):
    """Case transformations"""
    
    def apply(self, text: str) -> List[str]:
        """Generate case variants"""
        results = []
        results.append(text)  # original
        results.append(text.lower())  # lowercase
        results.append(text.upper())  # UPPERCASE
        
        if len(text) > 0:
            results.append(text[0].upper() + text[1:])  # Capitalize
        
        # Mixed case (limit to avoid explosion)
        if len(text) <= 10:
            for i in range(2 ** min(len(text), 4)):
                mixed = ""
                for j, ch in enumerate(text[:4]):
                    if (i >> j) & 1:
                        mixed += ch.upper()
                    else:
                        mixed += ch.lower()
                mixed += text[4:]
                results.append(mixed)
        
        return list(set(results))

class NumberTransform(Transform):
    """Number transformations"""
    
    DIGIT_MAP = {
        "0": ["O", "零"],
        "1": ["I", "L", "l", "一"],
        "3": ["E"],
        "5": ["S"],
        "8": ["B"],
    }
    
    HOMOPHONE_MAP = {
        "爱": ["1314", "A"],
        "好": ["88", "好"],
        "发": ["8", "发"],
        "死": ["4", "死"],
    }
    
    def apply(self, text: str) -> List[str]:
        """Generate number variants"""
        results = [text]
        
        # Replace digits
        for digit, replacements in self.DIGIT_MAP.items():
            if digit in text:
                for replacement in replacements:
                    results.append(text.replace(digit, replacement))
        
        return results

class SymbolTransform(Transform):
    """Symbol transformations"""
    
    SYMBOLS = ["@", "#", "!", "$", "%", "^"]
    
    def apply(self, text: str) -> List[str]:
        """Generate symbol variants"""
        results = [text]
        
        for symbol in self.SYMBOLS:
            results.append(f"{symbol}{text}")      # prefix
            results.append(f"{text}{symbol}")      # suffix
            if len(text) > 1:
                results.append(f"{text[0]}{symbol}{text[1:]}")  # middle
        
        return results[:100]  # Limit to avoid explosion

class FilterProcessor:
    """Filter and validation"""
    
    def __init__(self, min_length: int = 6, max_length: int = 32):
        self.min_length = min_length
        self.max_length = max_length
    
    def filter_by_length(self, items: List[str]) -> List[str]:
        """Filter by length"""
        return [
            item for item in items
            if self.min_length <= len(item) <= self.max_length
        ]
    
    def filter_by_charset(self, items: List[str], 
                         require_digit: bool = False,
                         require_upper: bool = False,
                         require_lower: bool = False) -> List[str]:
        """Filter by character set"""
        results = []
        for item in items:
            valid = True
            if require_digit and not any(c.isdigit() for c in item):
                valid = False
            if require_upper and not any(c.isupper() for c in item):
                valid = False
            if require_lower and not any(c.islower() for c in item):
                valid = False
            if valid:
                results.append(item)
        return results
    
    def filter_by_entropy(self, items: List[str], min_entropy: float = 30.0) -> List[str]:
        """Filter by entropy (password strength)"""
        results = []
        for item in items:
            if self.calculate_entropy(item) >= min_entropy:
                results.append(item)
        return results
    
    @staticmethod
    def calculate_entropy(password: str) -> float:
        """Calculate password entropy"""
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(not c.isalnum() for c in password):
            charset_size += 32
        
        if charset_size == 0:
            return 0.0
        
        import math
        return math.log2(charset_size) * len(password)

class DeduplicateProcessor:
    """Deduplication using Bloom filter"""
    
    def __init__(self, size: int = 1000000, hash_count: int = 3):
        self.size = size
        self.hash_count = hash_count
        self.bits = [False] * size
    
    def _hash(self, item: str, seed: int) -> int:
        """Generate hash"""
        h = hash((item, seed)) % self.size
        return abs(h)
    
    def add(self, item: str):
        """Add item to filter"""
        for i in range(self.hash_count):
            idx = self._hash(item, i)
            self.bits[idx] = True
    
    def contains(self, item: str) -> bool:
        """Check if item exists"""
        for i in range(self.hash_count):
            idx = self._hash(item, i)
            if not self.bits[idx]:
                return False
        return True
    
    def deduplicate(self, items: List[str]) -> List[str]:
        """Deduplicate items"""
        results = []
        for item in items:
            if not self.contains(item):
                self.add(item)
                results.append(item)
        return results
