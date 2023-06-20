import pandas as pd
from pandera.errors import SchemaErrors
import pandas_utils as pu
import data_schema

def validate_submission(df: pd.DataFrame, file=None) -> pd.DataFrame:
    if df is None:
        try:
            df = pu.read_dataframe(file)
        except:
            return pd.DataFrame(
                {
                    "Issues": "Could not read file into pandas dataframe"
                }
            )
    try:
        data_schema.schema.validate(df, lazy=True)
        return pd.DataFrame()  # empty on success
    except SchemaErrors as err:
        return err.failure_cases  # dataframe of schema errors

def check_submission(file, challenge_file="../example_data/casmi2022.tsv"):

    pass

if __name__ == '__main__':
    # file = "../example_data/casmi2022.tsv"
    file = "../example_data/failing.tsv"
    validate_submission(file=file)