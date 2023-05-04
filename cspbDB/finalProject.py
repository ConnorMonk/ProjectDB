# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

my_host = 'dbmonk.cw1d6mk1vb7h.us-east-2.rds.amazonaws.com'
my_user = 'connormonk'
my_password = 'connormonk'
my_database = 'dbmonk'

connection = pymysql.connect(host=my_host, user=my_user, password=my_password, database=my_database)
with connection:
    db = connection.cursor()
    # Avoid errors when re-running page
    db.execute('''DROP TABLE IF EXISTS employee, department, schedule''')
    
    db.execute('''CREATE TABLE employee(
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        phone VARCHAR(15),
        position VARCHAR(30) NOT NULL,
        salary INT NOT NULL,
        department_id INT NOT NULL,
        manager_id INT,
        schedule_id INT,
        CONSTRAINT fk_manager
        FOREIGN KEY (manager_id)
        REFERENCES employee(id)
        );''')
    
    db.execute('''CREATE TABLE department(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        location VARCHAR(30) NOT NULL,
        avg_salary DECIMAL NOT NULL
        );''')
    
    db.execute('''CREATE TABLE schedule(
        id INT AUTO_INCREMENT PRIMARY KEY,
        hours INT CHECK (hours BETWEEN 40 AND 45),
        location VARCHAR(30) NOT NULL
        );''')
    
    db.execute('''ALTER TABLE employee
        ADD CONSTRAINT fk_department 
        FOREIGN KEY (department_id) 
        REFERENCES department(id)
        ;''')
    
    db.execute('''ALTER TABLE employee
        ADD CONSTRAINT fk_schedule 
        FOREIGN KEY (schedule_id) 
        REFERENCES schedule(id)
        ;''')
    
    db.execute('''
        CREATE TRIGGER after_employee_insert
        AFTER INSERT ON employee
        FOR EACH ROW
        BEGIN
        DECLARE sum_salary DECIMAL(6, 2);
        DECLARE num_employees INT;

        SELECT SUM(salary), COUNT(*) INTO sum_salary, num_employees
        FROM employee
        WHERE department_id = NEW.department_id;

        UPDATE department
        SET avg_salary = sum_salary / num_employees
        WHERE id = NEW.department_id;
        END;''')
    
    db.execute('''
        CREATE TRIGGER after_employee_delete
        AFTER DELETE ON employee
        FOR EACH ROW
        BEGIN
        DELETE FROM schedule
        WHERE id = OLD.schedule_id;
        END;''')
    
    db.execute('''CREATE INDEX i_employee ON employee (last_name, first_name);''')

    
    # TODO
    # SHOW SQL statements and accompanying code for all table creation, 
    # insertion of initial data, updates, and queries.
    
    # TODO
    # INSERT INITIAL DATA
    db.execute('''
        INSERT INTO employee (first_name,last_name,phone,position,salary,department_id,manager_id,schedule_id)
        VALUES ('Bob', 'Smith', '12345678', 'bob@example.com', 1);''')
    
    
    # TODO
    # QUERIES
    db.execute('''
        SELECT *
        FROM employee
        INNER JOIN schedule
        ON employee.schedule_id = schedule.id
        INNER JOIN department
        ON employee.department_id = department.id
        ;''')
    
    # TODO
    # GROUPING RESULTS
    
    # TODO
    # SHOW TRIGGERS BEING EXCECUTED
    
