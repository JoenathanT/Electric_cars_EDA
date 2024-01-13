-- Create Database 
CREATE DATABASE milestone_3;

-- Create a table
CREATE TABLE IF NOT EXISTS table_m3 (
    "VIN (1-10)" VARCHAR(10),
    "County" VARCHAR(255),
    "City" VARCHAR(255),
    "State" VARCHAR(255),
	"Postal Code" FLOAT,
    "Model Year" INT,
    "Make" VARCHAR(255),
    "Model" VARCHAR(255),
    "Electric Vehicle Type" VARCHAR(255),
    "Clean Alternative Fuel Vehicle (CAFV) Eligibility" VARCHAR(255),
    "Electric Range" INT,
    "Base MSRP" INT,
    "Legislative District" FLOAT,
	"DOL Vehicle ID" VARCHAR(255),
    "Vehicle Location" VARCHAR(255),
    "Electric Utility" VARCHAR(255),
    "2020 Census Tract" FLOAT
);

-- check the column that we make before
SELECT * FROM table_m3;

-- LOAD data from CSV files.
COPY table_m3("VIN (1-10)","County", "City", "State", "Postal Code", "Model Year", "Make", "Model", "Electric Vehicle Type", 
			  "Clean Alternative Fuel Vehicle (CAFV) Eligibility", "Electric Range", "Base MSRP", "Legislative District", 
			  "DOL Vehicle ID", "Vehicle Location", "Electric Utility", "2020 Census Tract")
FROM 'C:\Users\Jonathan T\Downloads\Electric_Vehicle_Population_Data.csv'
DELIMITER ','
CSV HEADER ;
