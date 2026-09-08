"""Seed management service"""

from typing import List, Optional, Dict
from uuid import UUID, uuid4
from dataclasses import dataclass, asdict
from enum import Enum

class SeedCategory(str, Enum):
    """Seed categories"""
    NAME = "name"
    DATE = "date"
    PLACE = "place"
    ANIMAL = "animal"
    WEBSITE = "website"
    SLANG = "slang"
    MEME = "meme"
    KEYBOARD = "keyboard"
    LUCKY_NUMBER = "lucky_number"
    HOMOPHONE = "homophone"
    HOBBY = "hobby"
    BRAND = "brand"
    CUSTOM = "custom"

class SeedSource(str, Enum):
    """Seed sources"""
    BUILTIN = "builtin"
    IMPORTED = "imported"
    API = "api"

@dataclass
class Seed:
    """Seed data model"""
    id: UUID
    value: str
    category: SeedCategory
    source: SeedSource
    tags: List[str]
    enabled: bool = True
    metadata: Dict = None
    
    def to_dict(self):
        return asdict(self)

class SeedManager:
    """Seed management"""
    
    def __init__(self):
        self.seeds: Dict[UUID, Seed] = {}
        self.categories: Dict[str, List[UUID]] = {cat.value: [] for cat in SeedCategory}
    
    def add_seed(self, value: str, category: SeedCategory, source: SeedSource, 
                 tags: List[str] = None, metadata: Dict = None) -> Seed:
        """Add a seed"""
        seed_id = uuid4()
        seed = Seed(
            id=seed_id,
            value=value,
            category=category,
            source=source,
            tags=tags or [],
            metadata=metadata or {}
        )
        self.seeds[seed_id] = seed
        self.categories[category.value].append(seed_id)
        return seed
    
    def get_seed(self, seed_id: UUID) -> Optional[Seed]:
        """Get a seed by ID"""
        return self.seeds.get(seed_id)
    
    def list_seeds(self, category: Optional[SeedCategory] = None) -> List[Seed]:
        """List seeds by category"""
        if category:
            return [self.seeds[sid] for sid in self.categories[category.value]]
        return list(self.seeds.values())
    
    def search_seeds(self, query: str, category: Optional[SeedCategory] = None) -> List[Seed]:
        """Search seeds"""
        results = []
        seeds = self.list_seeds(category)
        for seed in seeds:
            if query.lower() in seed.value.lower():
                results.append(seed)
        return results
    
    def import_from_file(self, filepath: str, category: SeedCategory) -> int:
        """Import seeds from file"""
        count = 0
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    value = line.strip()
                    if value:
                        self.add_seed(value, category, SeedSource.IMPORTED)
                        count += 1
        except Exception as e:
            print(f"Error importing from {filepath}: {e}")
        return count
    
    def get_statistics(self) -> Dict:
        """Get seed statistics"""
        stats = {"total": len(self.seeds)}
        for category in SeedCategory:
            stats[category.value] = len(self.categories[category.value])
        return stats

# Global seed manager instance
seed_manager = SeedManager()
