SELECT_DATA_DEDUPLICATION = """
SELECT * FROM translations
WHERE id NOT IN (
    SELECT MIN(id)
    FROM translations
    GROUP BY lower(original_sentence)
);"""

DELETE_DATA_DEDUPLICATION = """
-- This SQL query deletes duplicate rows from the 'translations' table based on the 'original_sentence' column.
-- It keeps the row with the lowest 'id' value for each unique 'original_sentence'.
-- Any duplicate rows are removed, ensuring data integrity.

DELETE FROM translations
WHERE id NOT IN (
    SELECT MIN(id)
    FROM translations
    GROUP BY lower(original_sentence)
);

"""
SELECT_EMPTY_ROWS = """
SELECT * FROM translations
WHERE original_sentence IS NULL OR TRIM(original_sentence) = '';
"""

DELETE_EMPTY_ROWS = """
DELETE FROM translations
WHERE original_sentence IS NULL OR TRIM(original_sentence) = '';
"""


