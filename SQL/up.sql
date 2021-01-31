-- Table: q_manager.task_table
-- DROP TABLE q_manager.task_table;
CREATE TABLE q_manager.task_table
(
    id integer NOT NULL DEFAULT nextval('q_manager.task_table_id_seq'::regclass),
    task_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    pid character varying(10) COLLATE pg_catalog."default",
    status character varying(15) COLLATE pg_catalog."default",
    guid character varying(50) COLLATE pg_catalog."default",
    file_name character varying(255) COLLATE pg_catalog."default",
    args character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT task_table_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
ALTER TABLE q_manager.task_table
    OWNER to postgres;


-- Table: q_manager.logs_table
-- DROP TABLE q_manager.logs_table;
CREATE TABLE q_manager.logs_table
(
    id integer NOT NULL DEFAULT nextval('q_manager.logs_table_id_seq'::regclass),
    pid integer,
    task_id integer,
    message text COLLATE pg_catalog."default",
    CONSTRAINT logs_table_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE q_manager.logs_table
    OWNER to postgres;