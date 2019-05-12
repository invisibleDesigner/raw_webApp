import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()

    def translate(self, _escape_table):
        return self.name


class RoleEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(self, o)


def role_decode(d):
    if RoleEncoder.prefix in d:
        name = d[RoleEncoder.prefix]
        return UserRole[name]
    else:
        return d
