from dataclasses import dataclass


@dataclass(frozen=True)
class PathModifier:

    def modify_path( any, template: str ) -> str:
        return template    