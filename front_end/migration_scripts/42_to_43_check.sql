SELECT COUNT(*) AS count
FROM pragma_table_info("exercises")
WHERE name = "llm_interaction_type";

