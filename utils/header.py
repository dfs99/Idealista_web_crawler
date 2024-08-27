from typing import ClassVar, Dict

#TODO: Pendiente de incorporar.

class RequestHeader:

    USER_AGENT_LABEL: ClassVar[str] = "User-Agent"

    def __init__(self,  user_agent, **kwars):
        self._user_agent = user_agent
        # attributes set dynamically.
        for key, val in kwars.items():
            setattr(self, key, val)

    @property
    def user_agent(self):
        return self.user_agent
    
    @user_agent.setter
    def user_agent(self, new_user_agent):
        self._user_agent = new_user_agent
    
    def model_dump(self) -> Dict[str, str]:
        dump = dict()
        for key, value in vars(self).items():
            if key=="_user_agent":
                dump[RequestHeader.USER_AGENT_LABEL] = value 
            else:
                dump[key.replace("_", "-")] = value
        return dump 
"""
HEADERS: ClassVar[str] = {
        "User-Agent": None,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    } """


if __name__ == "__main__":

    t = RequestHeader(
        user_agent=None, 
        accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
        accept_language="en-US;en;q=0.9",
        accept_encoding="gzip, deflate, br"
    )

    print(vars(t))
    print(t.model_dump())

    #print([cvar for cvar in dir(t) if not callable(getattr(t, cvar)) and not cvar.startswith("__") and cvar.isupper()])