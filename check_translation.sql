-- check_translation.sql
SELECT * FROM translations WHERE original_sentence = ? AND german_translation = ? AND dutch_translation = ? AND spanish_translation = ? AND french_translation = ?;


