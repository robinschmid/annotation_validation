import re

from pandera import DataFrameSchema, Column, Check
from chemformula import ChemFormula
from molmass import Formula


def harmonize_formula(input):
    try:
        # harmonize to sorted formula
        # O2H4C2+  -->  [C2H4O2]+
        # O2H4C2   -->  C2H4O2
        return Formula(input).formula
    except:
        raise ValueError(f"Cannot parse {input} as formula")


def is_valid_formula(input):
    try:
        # harmonize to sorted formula
        # O2H4C2+  -->  [C2H4O2]+
        # O2H4C2   -->  C2H4O2
        f = Formula(input)
        if f is None:
            raise ValueError(f"Cannot parse {input} as formula")
        return f.formula
    except:
        raise ValueError(f"Cannot parse {input} as formula")


schema = DataFrameSchema(
    columns={
        "compound": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(min_value=0),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
        ),
        "filename": Column(
            dtype="str",
            checks=[
                Check.str_length(1)
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=False,
        ),
        "rt_min": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(min_value=0),
                Check.less_than_or_equal_to(max_value=100),
            ],
            nullable=True,
            unique=False,
            coerce=False,
            required=False,
        ),
        "precursor_mz": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(min_value=50),
                Check.less_than_or_equal_to(max_value=10000),
            ],
            nullable=True,
            unique=False,
            coerce=False,
            required=False,
        ),
        "challenge_class": Column(
            dtype="str",
            checks=[
                Check.str_length(1)
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=False,
        ),
        "annotation_rank": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(min_value=1),
                Check.less_than_or_equal_to(max_value=25),
            ],
            nullable=False,
            unique=False,
            coerce=True,
            required=True,
        ),
        "monoisotopic_mass": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(min_value=50),
                Check.less_than_or_equal_to(max_value=10000),
            ],
            nullable=True,
            unique=False,
            coerce=True,
            required=False,
        ),
        "formula_neutral": Column(
            dtype="str",
            checks=[
                Check(lambda s: isinstance(harmonize_formula(s), str), element_wise=True)
            ],
            nullable=True,
            unique=False,
            coerce=True,
            required=True,
            regex=True,  # all formula columns
        ),
        "formula_ion": Column(
            dtype="str",
            checks=[
                Check(lambda s: isinstance(harmonize_formula(s), str), element_wise=True)
            ],
            nullable=True,
            unique=False,
            coerce=True,
            required=True,
            regex=True,  # all formula columns
        ),
        "adduct": Column(
            dtype="str",
            checks=[
                Check.str_contains(re.compile("M[+-]"))
            ],
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
        ),
        "smiles": Column(
            dtype="str",
            checks=None,
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
        ),
        "inchi": Column(
            dtype="str",
            checks=None,
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
        ),
        "inchikey": Column(
            dtype="str",
            checks=[
                Check.str_length(14, 27)
            ],
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
        ),
        "compound_class": Column(
            dtype="str",
            checks=None,
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
        ),
    },
    checks=None,
    dtype=None,
    coerce=True,
    strict=True,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=True,
    title="Validate",
    description=None,
)
