import psycopg2
import pathlib
import os
from dotenv import load_dotenv

from .logs.logger import Logger

CURRENT_FILE_PATH = pathlib.Path(__file__).parent.resolve()

load_dotenv(dotenv_path=f'{CURRENT_FILE_PATH}\\..\\.env')

def load_queries() -> dict:
    """
    Function to load all queries to get data from database
    queries path -> /SQLQueries/*
    :return: list
    """
    path = f"{CURRENT_FILE_PATH}\\sql" # path of the sql Queries folder
    queries = {} # store all queries

    # SQL files
    sql_files = os.listdir(path)
    for file in sql_files:

        if file.endswith('.sql'): # check if it is a .sql file

            filename = file.split('.')[0] # get the name of the file
            sql_content = str()

            # Get the content from the sql file.
            with open(f"{path}\\{file}", 'r') as sql_file_content:
                sql_content = sql_file_content.read()


            queries[filename] = sql_content

    return queries


class DatabaseConnection(object):

    """
    Database object to access the database
    Tips:
        always close the connection when you finished your job.
    """

    def __init__(self) -> None:

        # Credentials
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

        # Init. connection
        self.conn = None

        # Init. loggers
        self.access_logger = Logger(f"{CURRENT_FILE_PATH}/logs/access.log")
        self.error_logger = Logger(f"{CURRENT_FILE_PATH}/logs/errors.log")

        # Init. queries
        self.sql_queries = load_queries()

        self.connect()


    # Create connection to the database
    def connect(self) ->  None:
        """
        Method to establish connection to the database
        :return: None
        """
        try:
            # Try to establish a connection with the database
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )

            self.access_logger.create_success_log("Successfully connected to the database." + " [object] DatabaseConnection [method] connect()")

        # Error handling
        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)}" + " [object] DatabaseConnection [method] connect()")

    # Get the insert query and create a new cursor
    def get_insert_query_and_create_cursor(self, query: str) -> list:

        insert_query = None
        cursor = None

        try:
            insert_query = self.sql_queries[query]
            self.access_logger.create_info_log("Successfully loaded addPexelsVideo query.")
        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)}. [object] DatabaseConnection [method] add_pexels_video()")

        try:

            cursor = self.conn.cursor()
            self.access_logger.create_info_log("Successfully created cursor for database querying.")
        except Exception as error:
            self.error_logger.create_error_log(f"Exception: {str(error)}. [object] DatabaseConnection [method] add_pexels_video()")

        return [insert_query, cursor]

    def request_pexels_video(self, id_: bool = False,
                             video_link: bool = False,
                             download_link: bool = False,
                             key_word_search: bool = False,
                             conditions: dict | None = None) -> list:

        insert_query, cursor = self.get_insert_query_and_create_cursor('getPexelsVideos')

        # Columns map for pexels_videos
        col_map = {
            "id": id_,
            "video_link": video_link,
            "download_link": download_link,
            "key_word_search" : key_word_search
        }

        # Check selected columns
        selected_cols = [col for col, include in col_map.items() if include]

        if not selected_cols:
            selected_cols = list(col_map.keys())

        col_str = ", ".join(selected_cols)

        # Add selected columns into query
        insert_query = insert_query.format(columns = col_str)


        # Check for conditions
        condition_query = ''

        if conditions:

            insert_query += " WHERE "
            for condition in conditions:
                if type(conditions[condition]) == str:
                    condition_query += f"{condition} = '{conditions[condition]}' "
                if type(conditions[condition]) == int:
                    condition_query += f"{condition} = {conditions[condition]} "
                condition_query += "AND "

        # Remove last "AND" Added
        condition_query = condition_query[:-5]

        # Concatenate SELECTION query with CONDITION query
        insert_query = insert_query + condition_query
        insert_query += ';'

        try:

            # Execute SELECT query
            cursor.execute(insert_query)

            # Fetch all results
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            results = [dict(zip(col_names, row)) for row in rows]

            cursor.close() # Close the cursor

            return results # Return result

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] DatabaseConnection [method] request_pexels_video()")

            # If error return empty list
            return []

    def add_pexels_video(self, data: list) -> None:
        """
        Method to add a video data into pexels_videos table
        """
        insert_query, cursor = self.get_insert_query_and_create_cursor('addPexelsVideo')

        try:

            if data:


                for item in data:

                    self.access_logger.create_info_log("Attempt to insert new data.")
                    cursor.execute(insert_query, (
                        item["video_link"],
                        item["download_link"],
                        item["key_word_search"],
                        item["video_path"]
                    ))
                    self.conn.commit()

                cursor.close()

                self.access_logger.create_success_log("Successfully submitted data into database.")

            else:
                self.error_logger.create_error_log("No data was provided. [object] DatabaseConnection [method] add_pexels_video()")

        except Exception as error:
            self.error_logger.create_error_log(
                f"Exception: {str(error)}. [object] DatabaseConnection [method] add_pexels_video()")
