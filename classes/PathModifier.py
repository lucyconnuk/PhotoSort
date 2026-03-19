from dataclasses import dataclass


@dataclass(frozen=True)
class PathModifier: # pragma: no cover # no point in testing this

    def modify_path( any, template: str ) -> str:
        return template