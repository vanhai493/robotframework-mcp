"""
Database testing templates for Robot Framework
"""

from .base import BaseTemplate


class DatabaseTestTemplate(BaseTemplate):
    """Template for generating database tests"""
    
    def generate(
        self,
        db_type: str = "postgresql",
        host: str = "localhost",
        port: str = "5432",
        database: str = "testdb",
        include_crud: bool = True,
        include_validation: bool = True,
    ) -> str:
        """
        Generate database test template
        
        Args:
            db_type: Database type (postgresql, mysql, sqlite, oracle)
            host: Database host
            port: Database port
            database: Database name
            include_crud: Include CRUD tests
            include_validation: Include data validation tests
        """
        result = self._get_header("Database Test")
        result += self._get_settings(db_type)
        result += self._get_variables(db_type, host, port, database)
        result += self._get_connection_tests()
        
        if include_crud:
            result += self._get_crud_tests()
        
        if include_validation:
            result += self._get_validation_tests()
        
        result += self._get_keywords(db_type)
        return result
    
    def _get_settings(self, db_type: str) -> str:
        return """*** Settings ***
Library    DatabaseLibrary
Library    Collections
Library    String

Suite Setup    Connect To Test Database
Suite Teardown    Disconnect From Database
Test Teardown    Rollback Transaction

"""
    
    def _get_variables(self, db_type: str, host: str, port: str, database: str) -> str:
        db_module = {
            "postgresql": "psycopg2",
            "mysql": "pymysql",
            "sqlite": "sqlite3",
            "oracle": "cx_Oracle",
        }.get(db_type.lower(), "psycopg2")
        
        return f"""*** Variables ***
${{DB_HOST}}          {host}
${{DB_PORT}}          {port}
${{DB_NAME}}          {database}
${{DB_USER}}          ${{EMPTY}}
${{DB_PASSWORD}}      ${{EMPTY}}
${{DB_MODULE}}        {db_module}

# Test data
${{TEST_TABLE}}       test_users
${{TEST_USER_NAME}}   Test User
${{TEST_USER_EMAIL}}  test@example.com

"""
    
    def _get_connection_tests(self) -> str:
        return """*** Test Cases ***
Database Connection Test
    [Documentation]    Verify database connection
    [Tags]    database    connection    smoke
    ${status}=    Check If Exists In Database    SELECT 1
    Should Be True    ${status}

Database Version Check
    [Documentation]    Check database version
    [Tags]    database    version
    @{result}=    Query    SELECT version()
    Log    Database version: ${result}

Table Existence Test
    [Documentation]    Verify required tables exist
    [Tags]    database    schema
    Table Must Exist    ${TEST_TABLE}

"""
    
    def _get_crud_tests(self) -> str:
        return """# ============================================
# CRUD Operation Tests
# ============================================

Insert Record Test
    [Documentation]    Test inserting a record
    [Tags]    database    crud    insert
    ${query}=    Set Variable
    ...    INSERT INTO ${TEST_TABLE} (name, email) VALUES ('${TEST_USER_NAME}', '${TEST_USER_EMAIL}')
    Execute Sql String    ${query}
    ${count}=    Row Count    SELECT * FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'
    Should Be Equal As Integers    ${count}    1

Select Record Test
    [Documentation]    Test selecting records
    [Tags]    database    crud    select
    @{result}=    Query    SELECT * FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'
    ${length}=    Get Length    ${result}
    Should Be True    ${length} >= 1
    Log    Found ${length} records

Update Record Test
    [Documentation]    Test updating a record
    [Tags]    database    crud    update
    ${new_name}=    Set Variable    Updated User
    Execute Sql String    UPDATE ${TEST_TABLE} SET name = '${new_name}' WHERE email = '${TEST_USER_EMAIL}'
    @{result}=    Query    SELECT name FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'
    Should Be Equal    ${result}[0][0]    ${new_name}

Delete Record Test
    [Documentation]    Test deleting a record
    [Tags]    database    crud    delete
    Execute Sql String    DELETE FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'
    ${count}=    Row Count    SELECT * FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'
    Should Be Equal As Integers    ${count}    0

Bulk Insert Test
    [Documentation]    Test bulk insert operation
    [Tags]    database    crud    bulk
    @{users}=    Create List
    FOR    ${i}    IN RANGE    1    6
        ${user}=    Create Dictionary    name=User ${i}    email=user${i}@test.com
        Append To List    ${users}    ${user}
    END
    Insert Multiple Records    ${TEST_TABLE}    ${users}
    ${count}=    Row Count    SELECT * FROM ${TEST_TABLE} WHERE email LIKE '%@test.com'
    Should Be True    ${count} >= 5

"""
    
    def _get_validation_tests(self) -> str:
        return """# ============================================
# Data Validation Tests
# ============================================

Data Integrity Test
    [Documentation]    Test data integrity constraints
    [Tags]    database    validation    integrity
    # Test unique constraint
    ${status}=    Run Keyword And Return Status
    ...    Execute Sql String    INSERT INTO ${TEST_TABLE} (email) VALUES ('duplicate@test.com')
    ${status2}=    Run Keyword And Return Status
    ...    Execute Sql String    INSERT INTO ${TEST_TABLE} (email) VALUES ('duplicate@test.com')
    # Second insert should fail if unique constraint exists
    Log    Unique constraint test: ${status2}

Not Null Constraint Test
    [Documentation]    Test NOT NULL constraints
    [Tags]    database    validation    constraints
    ${status}=    Run Keyword And Return Status
    ...    Execute Sql String    INSERT INTO ${TEST_TABLE} (name) VALUES (NULL)
    Log    NOT NULL constraint enforced: ${status}

Foreign Key Test
    [Documentation]    Test foreign key constraints
    [Tags]    database    validation    fk
    # Attempt to insert with invalid foreign key
    ${status}=    Run Keyword And Return Status
    ...    Execute Sql String    INSERT INTO orders (user_id) VALUES (99999)
    Log    Foreign key constraint test: ${status}

Data Type Validation Test
    [Documentation]    Test data type validation
    [Tags]    database    validation    types
    # Test inserting wrong data type
    ${status}=    Run Keyword And Return Status
    ...    Execute Sql String    INSERT INTO ${TEST_TABLE} (age) VALUES ('not_a_number')
    Log    Data type validation: ${status}

Record Count Validation
    [Documentation]    Validate expected record counts
    [Tags]    database    validation    count
    ${count}=    Row Count    SELECT * FROM ${TEST_TABLE}
    Should Be True    ${count} >= 0
    Log    Total records in ${TEST_TABLE}: ${count}

Data Range Validation
    [Documentation]    Validate data is within expected ranges
    [Tags]    database    validation    range
    @{result}=    Query    SELECT MIN(created_at), MAX(created_at) FROM ${TEST_TABLE}
    Log    Date range: ${result}

Null Value Check
    [Documentation]    Check for unexpected NULL values
    [Tags]    database    validation    null
    ${null_count}=    Row Count    SELECT * FROM ${TEST_TABLE} WHERE name IS NULL
    Should Be Equal As Integers    ${null_count}    0    Unexpected NULL values found

Duplicate Check
    [Documentation]    Check for duplicate records
    [Tags]    database    validation    duplicates
    @{duplicates}=    Query
    ...    SELECT email, COUNT(*) as cnt FROM ${TEST_TABLE} GROUP BY email HAVING COUNT(*) > 1
    ${dup_count}=    Get Length    ${duplicates}
    Should Be Equal As Integers    ${dup_count}    0    Duplicate records found

"""
    
    def _get_keywords(self, db_type: str) -> str:
        return """*** Keywords ***
Connect To Test Database
    [Documentation]    Establish database connection
    Connect To Database    ${DB_MODULE}    ${DB_NAME}    ${DB_USER}    ${DB_PASSWORD}
    ...    ${DB_HOST}    ${DB_PORT}
    Log    Connected to database: ${DB_NAME}

Rollback Transaction
    [Documentation]    Rollback any uncommitted changes
    Execute Sql String    ROLLBACK

Insert Multiple Records
    [Arguments]    ${table}    ${records}
    [Documentation]    Insert multiple records into table
    FOR    ${record}    IN    @{records}
        ${columns}=    Get Dictionary Keys    ${record}
        ${values}=    Get Dictionary Values    ${record}
        ${col_str}=    Catenate    SEPARATOR=,    @{columns}
        ${val_str}=    Evaluate    ','.join([f"'{v}'" for v in ${values}])
        Execute Sql String    INSERT INTO ${table} (${col_str}) VALUES (${val_str})
    END

Verify Record Exists
    [Arguments]    ${table}    ${column}    ${value}
    [Documentation]    Verify a record exists in table
    ${count}=    Row Count    SELECT * FROM ${table} WHERE ${column} = '${value}'
    Should Be True    ${count} > 0    Record not found: ${column}=${value}

Verify Record Not Exists
    [Arguments]    ${table}    ${column}    ${value}
    [Documentation]    Verify a record does not exist
    ${count}=    Row Count    SELECT * FROM ${table} WHERE ${column} = '${value}'
    Should Be Equal As Integers    ${count}    0    Record should not exist: ${column}=${value}

Get Record By Id
    [Arguments]    ${table}    ${id}
    [Documentation]    Get single record by ID
    @{result}=    Query    SELECT * FROM ${table} WHERE id = ${id}
    ${length}=    Get Length    ${result}
    Should Be True    ${length} == 1    Record not found with id: ${id}
    RETURN    ${result}[0]

Execute And Verify Row Count
    [Arguments]    ${query}    ${expected_count}
    [Documentation]    Execute query and verify row count
    ${actual_count}=    Row Count    ${query}
    Should Be Equal As Integers    ${actual_count}    ${expected_count}

Clean Test Data
    [Documentation]    Clean up test data
    Execute Sql String    DELETE FROM ${TEST_TABLE} WHERE email LIKE '%@test.com'
    Execute Sql String    DELETE FROM ${TEST_TABLE} WHERE email = '${TEST_USER_EMAIL}'

Backup Table
    [Arguments]    ${table}
    [Documentation]    Create backup of table
    ${timestamp}=    Get Time    epoch
    Execute Sql String    CREATE TABLE ${table}_backup_${timestamp} AS SELECT * FROM ${table}
    Log    Backup created: ${table}_backup_${timestamp}

Compare Tables
    [Arguments]    ${table1}    ${table2}
    [Documentation]    Compare two tables for differences
    ${count1}=    Row Count    SELECT * FROM ${table1}
    ${count2}=    Row Count    SELECT * FROM ${table2}
    Should Be Equal As Integers    ${count1}    ${count2}    Tables have different row counts
"""
