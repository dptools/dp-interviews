#!/usr/bin/env python

import sys
from pathlib import Path

file = Path(__file__).resolve()
parent = file.parent
root = None
for parent in file.parents:
    if parent.name == "av-pipeline-v2":
        root = parent
sys.path.append(str(root))

# remove current directory from path
try:
    sys.path.remove(str(parent))
except ValueError:
    pass

from enum import Enum
from typing import List

from pipeline.helpers import utils, db

console = utils.get_console()


class InterviewRole(Enum):
    """
    Enumerates the roles of interviews.
    """

    INTERVIEWER = "interviewer"
    SUBJECT = "subject"

    @staticmethod
    def init_table_query() -> List[str]:
        """
        Return the SQL query to create the 'interview_roles' table.
        """
        create_sql_query = """
        CREATE TABLE IF NOT EXISTS interview_roles (
            ir_role TEXT NOT NULL UNIQUE
        );
        """

        populate_sql_queries: List[str] = []

        for role in InterviewRole:
            populate_sql_queries.append(
                f"""
                INSERT INTO interview_roles (ir_role)
                VALUES ('{role.value}');
                """
            )

        sql_queries: List[str] = [create_sql_query] + populate_sql_queries

        return sql_queries

    @staticmethod
    def drop_table_query() -> str:
        """
        Return the SQL query to drop the 'interview_roles' table.
        """
        sql_query = """
        DROP TABLE IF EXISTS interview_roles;
        """

        return sql_query


if __name__ == "__main__":
    config_file = utils.get_config_file_path()

    console.log("Initializing 'interview_roles' table...")
    console.log(
        "[red]This will delete all existing data in the 'interview_roles' table![/red]"
    )

    drop_queries = [InterviewRole.drop_table_query()]
    create_queries = InterviewRole.init_table_query()

    sql_queries = drop_queries + create_queries

    db.execute_queries(config_file=config_file, queries=sql_queries)
    console.log("Done!")
