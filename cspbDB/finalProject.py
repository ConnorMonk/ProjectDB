# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

my_host = 'dbmonk.cw1d6mk1vb7h.us-east-2.rds.amazonaws.com'
my_user = 'connormonk'
my_password = 'connormonk'
my_database = 'dbmonk'

connection = pymysql.connect(host=my_host, user=my_user, password=my_password, database=my_database)
db = connection.cursor()
# Avoid errors when re-running page
# CREATION OF TABLES AND TRIGGERS
db.execute('''DROP TABLE IF EXISTS employee, department, schedule''')

db.execute('''CREATE TABLE employee(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    phone VARCHAR(15),
    position VARCHAR(30) NOT NULL,
    salary INT NOT NULL,
    department_id INT NOT NULL
    );''')

db.execute('''CREATE TABLE department(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    location VARCHAR(30) NOT NULL,
    avg_salary INT NOT NULL
    );''')

db.execute('''CREATE TABLE schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    mon_start INT CHECK (mon_start >= 0 AND mon_start <= 23),
    tue_start INT CHECK (tue_start >= 0 AND tue_start <= 23),
    wed_start INT CHECK (wed_start >= 0 AND wed_start <= 23),
    thu_start INT CHECK (thu_start >= 0 AND thu_start <= 23),
    fri_start INT CHECK (fri_start >= 0 AND fri_start <= 23),
    sat_start INT CHECK (sat_start >= 0 AND sat_start <= 23),
    sun_start INT CHECK (sun_start >= 0 AND sun_start <= 23),
    mon_hours INT CHECK (mon_hours >= 0 AND mon_hours <= 8),
    tue_hours INT CHECK (tue_hours >= 0 AND tue_hours <= 8),
    wed_hours INT CHECK (wed_hours >= 0 AND wed_hours <= 8),
    thu_hours INT CHECK (thu_hours >= 0 AND thu_hours <= 8),
    fri_hours INT CHECK (fri_hours >= 0 AND fri_hours <= 8),
    sat_hours INT CHECK (sat_hours >= 0 AND sat_hours <= 8),
    sun_hours INT CHECK (sun_hours >= 0 AND sun_hours <= 8),
    CONSTRAINT hours_per_week CHECK (40 <= mon_hours + tue_hours + wed_hours + thu_hours + fri_hours + sat_hours + sun_hours <= 42),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
    );''')

db.execute('''ALTER TABLE employee
    ADD CONSTRAINT fk_department 
    FOREIGN KEY (department_id) 
    REFERENCES department(id)
    ;''')

db.execute('''
    CREATE TRIGGER after_employee_insert
    AFTER INSERT ON employee
    FOR EACH ROW
    BEGIN
    DECLARE sum_salary DECIMAL;
    DECLARE num_employees INT;
    SELECT SUM(salary), COUNT(*) INTO sum_salary, num_employees
    FROM employee
    WHERE department_id = NEW.department_id;
    UPDATE department
    SET avg_salary = sum_salary / num_employees
    WHERE id = NEW.department_id;
    END;''')

db.execute('''
    CREATE TRIGGER before_employee_delete
    BEFORE DELETE ON employee
    FOR EACH ROW
    BEGIN
    DELETE FROM schedule
    WHERE employee_id = OLD.id;
    END;''')

db.execute('''
    CREATE TRIGGER after_employee_delete
    AFTER DELETE ON employee
    FOR EACH ROW
    BEGIN
    DECLARE sum_salary DECIMAL;
    DECLARE num_employees INT;
    SELECT SUM(salary), COUNT(*) INTO sum_salary, num_employees
    FROM employee
    WHERE department_id = OLD.department_id;
    UPDATE department
    SET avg_salary = sum_salary / num_employees
    WHERE id = OLD.department_id;
    END;''')

db.execute('''CREATE INDEX i_employee ON employee (last_name, first_name);''')

    
# SHOW SQL statements and accompanying code for all table creation, 
# INSERT INITIAL DATA
db.execute('''
    INSERT INTO department (name, location)
    VALUES ('Management', 'Colorado');
    ''')
db.execute('''
    INSERT INTO department (name, location)
    VALUES ('Development', 'Colorado');
    ''')
db.execute('''
    INSERT INTO department (name, location)
    VALUES ('Sales', 'California');
    ''')

# insertion functions  
def create_employee(first_name,last_name,phone,position,salary=80000,department_id=2):
    db.execute(f'''
        INSERT INTO employee (first_name,last_name,phone,position,salary,department_id)
        VALUES ('{first_name}','{last_name}',{phone},'{position}',{salary},{department_id});
        ''')
    
def assign_schedule(employee_id, mon_start = 9, tue_start = 9, wed_start = 9, thu_start = 9, fri_start = 9, sat_start = 9, sun_start = 9, mon_hours = 8, tue_hours = 8, wed_hours = 8, thu_hours = 8, fri_hours = 8, sat_hours = 0, sun_hours = 0):
    db.execute(f'''
                   INSERT INTO schedule (employee_id, mon_start, tue_start, wed_start, thu_start, fri_start, sat_start, sun_start, mon_hours, tue_hours, wed_hours, thu_hours, fri_hours, sat_hours, sun_hours)
                   VALUES ({employee_id},{mon_start},{tue_start},{wed_start},{thu_start},{fri_start},{sat_start},{sun_start},{mon_hours},{tue_hours},{wed_hours},{thu_hours},{fri_hours}, {sat_hours}, {sun_hours});
        ''')

def delete_employee(employee_id):
    db.execute(f'''
        DELETE FROM employee
        WHERE id = {employee_id};
        ''')

#Team 1
#department 1 means John Johnson is the manager.
create_employee('John', 'Johnson', '11111111', 'Manager', 100000, 1) 

# department '2' is development 
create_employee('Bob', 'Brown', '11111112', 'Engineer', 100000, 2)  
create_employee('Bill', 'Williamson', '11111113', 'Developer',85000, 2)
create_employee('Jonah', 'Jameson', '11111114', 'Developer',95000, 2)
create_employee('Peter', 'Porker', '11111115', 'Developer',110000, 2)
create_employee('Lucy', 'Liu', '11111116', 'Developer',105000, 2)
# 3 is sales
create_employee('Mikey', 'Mike', '11111117', 'Salesperson',75000, 3)

# designate schedules with employee ID as the parameter
assign_schedule(1)
assign_schedule(2)
assign_schedule(3)
assign_schedule(4)
assign_schedule(5)
assign_schedule(6)
assign_schedule(7)

# Show trigger firing that updates avg_salary of department
avg_sal = db.execute('''
                     SELECT avg_salary
                     FROM department
                     ''')

print(f'avg_salary by department after first team is created = {db.fetchall()}\n')

# Team 2
create_employee('Jane', 'Jackson', '11111111', 'Manager', 200000, 1) 

# department '2' is development 
create_employee('Beth', 'Brown', '11111112', 'Engineer', 110000, 2)  
create_employee('Clare', 'Clifford', '11111113', 'Developer',90000, 2)
create_employee('Jane', 'Jameson', '11111114', 'Developer',90000, 2)
create_employee('Prim', 'Price', '11111115', 'Developer',180000, 2)
create_employee('Dave', 'Davinsky', '11111116', 'Developer',115000, 2)
# 3 is sales
create_employee('Sarah', 'Smith', '11111117', 'Salesperson',75000, 3)

assign_schedule(8, 7,7,7,7,7,7,7,8,8,8,4,4,4,4)

assign_schedule(9, 17, 17, 17, 17, 17)
assign_schedule(10, 17, 17, 17, 17, 17)
assign_schedule(11, 17, 17, 17, 17, 17)
assign_schedule(12, 17, 17, 17, 17, 17)
assign_schedule(13, 17, 17, 17, 17, 17)
assign_schedule(14, 17, 17, 17, 17, 17)

# Show trigger firing that updates avg_salary of department
avg_sal = db.execute('''
                     SELECT avg_salary
                     FROM department
                     ''')

print(f'avg_salary by department after second team is created= {db.fetchall()}\n')

# Show all the employees with active schedules.

# QUERIES
# JOINS
# GROUPING 

test = db.execute('''
    SELECT COUNT(*)
    FROM employee
    INNER JOIN schedule
    ON employee.id = schedule.employee_id
    INNER JOIN department
    ON employee.department_id = department.id;
    ''')

print(f'Number of employees currently on payroll {db.fetchall()}\n')

delete_employee(12)

avg_sal = db.execute('''
                     SELECT avg_salary
                     FROM department
                     ''')

print(f'avg_salary by department after an overpaid employee in the Development department is fired= {db.fetchall()}\n')

test = db.execute('''
    SELECT COUNT(*)
    FROM employee
    INNER JOIN schedule
    ON employee.id = schedule.employee_id
    INNER JOIN department
    ON employee.department_id = department.id;
    ''')

print(f'Number of employees currently on payroll {db.fetchall()}\n')

# Show all the employees with active schedules.
test = db.execute('''
    SELECT employee.id,first_name
    FROM employee
    INNER JOIN schedule
    ON employee.id = schedule.employee_id
    INNER JOIN department
    ON employee.department_id = department.id;
    ''')

print('\n#######################################################')
print(f'\nAll employees currently on payroll {db.fetchall()}\n')

db.execute('''
    SELECT department.name AS department, COUNT(*) AS num_employees
    FROM employee
    JOIN department ON employee.department_id = department.id
    GROUP BY department.name;
    ''')

print(f'Number of employees in each department = {db.fetchall()}\n')

db.execute('''
           SELECT salary, employee.first_name
           FROM employee
           INNER JOIN schedule
           ON employee.id = schedule.employee_id
           WHERE schedule.sat_hours AND schedule.sun_hours > 0;
           ''')

print(f'Salary of employee\'s who work on weekends = {db.fetchall()}')
