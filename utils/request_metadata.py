from pathlib import Path
import itertools
from dataclasses import dataclass

@dataclass 
class RequestsMetadata:
    proxies: itertools.cycle
    curr_proxy: str
    user_agents: itertools.cycle
    odir_pages: Path
    odir_properties: Path
