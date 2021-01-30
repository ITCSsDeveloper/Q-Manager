create schema q_manager;

-- q_manager.task_table definition
CREATE TABLE q_manager.task_table (
	id serial NOT NULL,
	task_name varchar(50) NOT NULL,
	pid varchar(50) NULL,
	status varchar(50) NULL,
	create_by varchar(50) NULL,
	create_time timestamp NULL,
	start_time timestamp NULL,
	end_time timestamp NULL,
	guid varchar(50) NULL,
	args varchar(1000) NULL,
	CONSTRAINT task_table_pkey PRIMARY KEY (id)
);

create table q_manager.logs_table (
    id serial primary key,
    task_id int,
    create_time timestamp,
    message varchar(255)
);