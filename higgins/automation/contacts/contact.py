import uuid
from dataclasses import dataclass, field


@dataclass
class Contact:
    name: str
    alias: str = None
    email: str = None
    phone: str = None
    default_messaging_app: str = None
    contact_id: str = field(default_factory=lambda: str(uuid.uuid1()))
