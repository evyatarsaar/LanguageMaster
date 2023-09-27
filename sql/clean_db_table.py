from logger_config import logger
from db import DatabaseManager
from data_integrity import SELECT_DATA_DEDUPLICATION, SELECT_EMPTY_ROWS, DELETE_DATA_DEDUPLICATION, DELETE_EMPTY_ROWS


def process_deletion(cursor, select_query, delete_query):
    cursor.execute(select_query)
    rows_to_delete = cursor.fetchall()

    # Log the rows to be deleted
    for row in rows_to_delete:
        logger.info(f"Row to be deleted: {row}")

    confirmation = input("Do you want to delete the listed rows? (yes/no): ").lower()
    if confirmation == "yes":
        # Perform the actual deletion
        cursor.execute(delete_query)
        logger.info("Deletion completed.")
    else:
        logger.info("Deletion canceled.")


def main():
    with DatabaseManager('../translations.db') as cursor:
        process_deletion(cursor, SELECT_DATA_DEDUPLICATION, DELETE_DATA_DEDUPLICATION)
        process_deletion(cursor, SELECT_EMPTY_ROWS, DELETE_EMPTY_ROWS)


if __name__ == '__main__':
    main()
