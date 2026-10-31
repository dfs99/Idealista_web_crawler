from pathlib import Path
import itertools
from dataclasses import dataclass
from typing import Optional

@dataclass 
class RequestsMetadata:
    proxies: Optional[itertools.cycle]
    curr_proxy: str
    user_agents: itertools.cycle
    odir_pages: Path
    odir_properties: Path
