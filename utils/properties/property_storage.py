from dataclasses import dataclass, field
from typing import Dict, Generator
from utils.properties.property import PropertyData

@dataclass
class PropertyStorage:
    data: Dict[str, PropertyData] = field(default_factory=dict)

    def add(self, item: PropertyData) -> bool:
        if item.id not in self.data.keys():
            self.data[item.id] = item
            return True
        return False
    
    def retrieve(self) -> Generator[PropertyData,None,None]:
        while self.data:
            try:
                key, value = self.data.popitem()
                yield value
            except KeyError:
                return
