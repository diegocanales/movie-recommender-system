from hydra_zen import store
from hydra_zen.third_party.pydantic import pydantic_parser

from typing import Literal
from pydantic import PositiveInt


from dataclasses import dataclass


@dataclass
class ProcessingConfig:
    age: PositiveInt = 22
    name: str = "Bobby"


def main(character: Character, gear: tuple[str, ...] = (), mode: Literal["easy", "hard"] = "easy",):
    print(f"{character=!r} {gear=!r}  {mode=!r}")


if __name__ == "__main__":
    from hydra_zen import zen

    store(main, hydra_defaults=["_self_", {"character": "base"}])
    store(Character, group="character", name="base")
    store.add_to_hydra_store()

    zen(
        main,
        # This is the key ingredient
        instantiation_wrapper=pydantic_parser,
    ).hydra_main(
        config_name="main",
        config_path=None,
        version_base="1.3",
    )
