CREATE TABLE IF NOT EXISTS llm_generations (
    llm_generation_id integer PRIMARY KEY AUTOINCREMENT,
    course_id integer NOT NULL,
    assignment_id integer NOT NULL,
    exercise_id integer NOT NULL,
    generated_code text,
    prompt_code text,
    date_created DATETIME NOT NULL,
    user_id text
);
