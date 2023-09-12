CREATE TABLE IF NOT EXISTS llm_generations (
    llm_generation_id integer PRIMARY KEY AUTOINCREMENT,
    course_id integer NOT NULL,
    assignment_id integer NOT NULL,
    exercise_id integer NOT NULL,
    comment text,
    generated_code text,
    llm_interaction_type text,
    lines_used_before_edit integer,
    date_created DATETIME NOT NULL,
    user_id text
);
