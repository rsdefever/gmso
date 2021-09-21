from typing import Optional, Tuple

import unyt as u
from pydantic import Field

from gmso.core.parametric_potential import ParametricPotential
from gmso.utils._constants import PAIRPOTENTIAL_TYPE_DICT


class PairPotentialType(ParametricPotential):
    __base_doc__ = """A description of custom pairwise potential between 2 AtomTypes that does not follow combination rule.

    This is a subclass of the gmso.core.ParametricPotential superclass.

    PairPotentialType represents a type of pairwise potential between two
    Atomtypes that does not follow a specific combination rule, and includes the functional
    form describing its interactions. The functional form of the potential is
    stored as a `sympy` expression and the parameters, with units, are stored
    explicitly.  The AtomTypes that are used to define the dihedral type are
    stored as `member_types`.


    Notes
    -----
    Inherits many functions from gmso.ParametricPotential:
        __eq__, _validate functions
    """

    member_types_: Optional[Tuple[str, str]] = Field(
        None,
        description="List-like of strs, referring to gmso.Atomtype.name or gmso.Atomtype.atomclass, "
        "defining the members of this pair potential type",
    )

    def __init__(
        self,
        name="PairPotentialType",
        expression=None,
        parameters=None,
        independent_variables=None,
        potential_expression=None,
        member_types=None,
        topology=None,
        tags=None,
    ):
        if potential_expression is None:
            if expression is None:
                expression = "4 * eps * ((sigma / r)**12 - (sigma / r)**6)"
            if parameters is None:
                parameters = {"eps": 1 * u.Unit("kJ / mol"), "sigma": 1 * u.nm}
            if independent_variables is None:
                independent_variables = {"r"}

        super(PairPotentialType, self).__init__(
            name=name,
            expression=expression,
            parameters=parameters,
            independent_variables=independent_variables,
            topology=topology,
            member_types=member_types,
            potential_expression=potential_expression,
            set_ref=PAIRPOTENTIAL_TYPE_DICT,
            tags=tags,
        )

    @property
    def member_types(self):
        return self.__dict__.get("member_types_")

    class Config:
        fields = {"member_types_": "member_types"}

        alias_to_fields = {"member_types": "member_types_"}
