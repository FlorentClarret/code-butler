from typing import List, Type

from code_butler.rules.github.save_state import SaveStateRule
from code_butler.rules.github.set_output import SetOutputRule
from code_butler.rules.common.rule import Rule

ALL_RULES: List[Type[Rule]] = [SaveStateRule, SetOutputRule]
