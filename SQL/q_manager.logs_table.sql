-- Table: q_manager.logs_table

-- DROP TABLE q_manager.logs_table;

CREATE TABLE q_manager.logs_table
(
    id bigint NOT NULL DEFAULT nextval('q_manager.logs_table_id_seq'::regclass),
    pid integer,
    task_id integer NOT NULL,
    message text COLLATE pg_catalog."default",
    date date,
    "time" timestamp with time zone,
    CONSTRAINT logs_table_pkey PRIMARY KEY (id, task_id)
)

TABLESPACE pg_default;

ALTER TABLE q_manager.logs_table
    OWNER to postgres;