-- Create Identifiers table
CREATE TABLE Identifiers (
    identifier_name VARCHAR(255) PRIMARY KEY,
    description TEXT,
    identifier_type VARCHAR(255)
);

-- Insert data into Identifiers table
INSERT INTO Identifiers (identifier_name, description, identifier_type)
VALUES
    ('88823141', 'Shampoo Product', 'Finished Product Part'),
    ('88823142', 'Packaging Carton', 'Packaging Material Part'),
    ('88823143', 'Packaging Box', 'Packaging Material Part'),
    ('88823144', 'Chemical Substance', 'Assembled Product Part'),
    ('88823145', 'Water', 'Assembled Product Part'),
    ('88823146', 'Shampoo Bottle', 'Material Part');
-- Create Countries table
CREATE TABLE Countries (
    name VARCHAR(255) PRIMARY KEY,
    iso_code VARCHAR(255),
    short_code VARCHAR(255)
);

-- Insert data into Countries table
INSERT INTO Countries (name, iso_code, short_code)
VALUES
    ('Luxembourg', 'LU', '442'),
    ('France', 'FR', '250'),
    ('Germany', 'DE', '276'),
    ('Belgium', 'BE', '056'),
    ('Netherlands', 'NL', '528'),
    ('Sweden', 'SE', '752'),
    ('Norway', 'NO', '578');

-- Create ConsumerUnits table
CREATE TABLE ConsumerUnits (
    number_of_consumers INT,
    country_name VARCHAR(255),
    PRIMARY KEY (number_of_consumers, country_name),
    FOREIGN KEY (country_name) REFERENCES Countries(name)
);

-- Insert data into ConsumerUnits table
INSERT INTO ConsumerUnits (number_of_consumers, country_name)
VALUES
    ( 150, 'Luxembourg'),  -- Shampoo product used by 150 consumers in Luxembourg
    ( 200, 'France'),      -- Shampoo product used by 200 consumers in France
    ( 100, 'Germany'),     -- Packaging Carton used by 100 consumers in Germany
    ( 120, 'Belgium'),     -- Packaging Box used by 120 consumers in Belgium
    ( 80, 'Netherlands'), -- Chemical Substance used by 80 consumers in Netherlands
    ( 60, 'Sweden'),      -- Water used by 60 consumers in Sweden
    ( 90, 'Norway');      -- Shampoo Bottle used by 90 consumers in Norway

-- Create Ownership table
CREATE TABLE Ownership (
    identifier_name VARCHAR(255),
    originator_first_name VARCHAR(255),
    originator_last_name VARCHAR(255),
    user_id_tnumber VARCHAR(255),
    user_id_intranet VARCHAR(255),
    email VARCHAR(255),
    owner_first_name VARCHAR(255),
    owner_last_name VARCHAR(255),
    PRIMARY KEY (identifier_name, user_id_tnumber),
    FOREIGN KEY (identifier_name) REFERENCES Identifiers(identifier_name)
);

-- Insert data into Ownership table
INSERT INTO Ownership (identifier_name, originator_first_name, originator_last_name, user_id_tnumber, user_id_intranet, email, owner_first_name, owner_last_name)
VALUES
    ('88823141', 'Andrea', 'Meier', 'AP5065', 'meier.a.1', 'andrea@example.com', 'Andrea', 'Meier'),
    ('88823142', 'John', 'Doe', 'JD1234', 'doe.j.1', 'john@example.com', 'John', 'Doe'),
    ('88823143', 'Jane', 'Smith', 'JS5678', 'smith.j.2', 'jane@example.com', 'Jane', 'Smith'),
    ('88823144', 'Michael', 'Brown', 'MB9101', 'brown.m.3', 'michael@example.com', 'Michael', 'Brown'),
    ('88823145', 'Emily', 'Davis', 'ED1123', 'davis.e.4', 'emily@example.com', 'Emily', 'Davis'),
    ('88823146', 'David', 'Wilson', 'DW1456', 'wilson.d.5', 'david@example.com', 'David', 'Wilson');

-- Create Relationships table
CREATE TABLE Relationships (
    from_identifier_name VARCHAR(255),
    to_identifier_name VARCHAR(255),
    relationship_name VARCHAR(255),
    PRIMARY KEY (from_identifier_name, to_identifier_name),
    FOREIGN KEY (from_identifier_name) REFERENCES Identifiers(identifier_name),
    FOREIGN KEY (to_identifier_name) REFERENCES Identifiers(identifier_name)
);

-- Insert data into Relationships table
INSERT INTO Relationships (from_identifier_name, to_identifier_name, relationship_name)
VALUES
    ('88823141', '88823142', 'Contains'),
    ('88823141', '88823143', 'Contains'),
    ('88823141', '88823144', 'Contains'),
    ('88823141', '88823145', 'Contains'),
    ('88823141', '88823146', 'Contains');

-- Create Characteristics table
CREATE TABLE Characteristics (
    master_name VARCHAR(255),
    name VARCHAR(255),
    specifics VARCHAR(255),
    action_required VARCHAR(255),
    report_type VARCHAR(255),
    data_type VARCHAR(255),
    lower_routine_release_limit DECIMAL(10, 2),
    lower_limit DECIMAL(10, 2),
    lower_target DECIMAL(10, 2),
    target DECIMAL(10, 2),
    upper_target DECIMAL(10, 2),
    upper_limit DECIMAL(10, 2),
    upper_routine_release_limit DECIMAL(10, 2),
    test_frequency INT,
    precision INT,
    engineering_unit VARCHAR(255),
    PRIMARY KEY (master_name,name)
);

-- Insert data into Characteristics table
-- Shampoo Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES
    ('CM-10001', 'Volume', 'Shampoo Bottle Volume', 'CONTROL', 'VARIABLE', 'Decimal', 490.0, 490.0, 500.0, 505.0, 510.0, 520.0, 520.0, 1, 2, 'ml'),
    ('CM-10002', 'pH Level', 'Shampoo pH Level', 'CONTROL', 'VARIABLE', 'Decimal', 4.0, 4.0, 5.0, 5.5, 6.0, 7.0, 7.0, 1, 2, 'pH'),
    ('CM-10003', 'Viscosity', 'Shampoo Viscosity', 'CONTROL', 'VARIABLE', 'Decimal', 10.0, 10.0, 15.0, 20.0, 25.0, 30.0, 30.0, 1, 2, 'Pa.s'),
    ('CM-10004', 'Color', 'Shampoo Color', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-10005', 'Fragrance', 'Shampoo Fragrance', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-10006', 'Foam Height', 'Shampoo Foam Height', 'CONTROL', 'VARIABLE', 'Decimal', 10.0, 10.0, 15.0, 20.0, 25.0, 30.0, 30.0, 1, 2, 'cm'),
    ('CM-10007', 'Density', 'Shampoo Density', 'CONTROL', 'VARIABLE', 'Decimal', 0.9, 0.9, 1.0, 1.1, 1.2, 1.3, 1.3, 1, 3, 'g/cm^3'),
    ('CM-10008', 'Ingredient A Concentration', 'Concentration of Ingredient A', 'CONTROL', 'VARIABLE', 'Decimal', 0.5, 0.5, 1.0, 1.5, 2.0, 2.5, 2.5, 1, 2, '%'),
    ('CM-10009', 'Ingredient B Concentration', 'Concentration of Ingredient B', 'CONTROL', 'VARIABLE', 'Decimal', 1.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.0, 1, 2, '%'),
    ('CM-10010', 'Shelf Life', 'Shelf Life of Shampoo', 'CONTROL', 'VARIABLE', 'Decimal', 12.0, 12.0, 18.0, 24.0, 30.0, 36.0, 36.0, 1, 1, 'months');

-- Packaging Carton Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES
    ('CM-20001', 'Carton Thickness', 'Thickness of Carton', 'CONTROL', 'VARIABLE', 'Decimal', 1.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.0, 1, 2, 'mm'),
    ('CM-20002', 'Carton Weight', 'Weight of Carton', 'CONTROL', 'VARIABLE', 'Decimal', 50.0, 50.0, 55.0, 60.0, 65.0, 70.0, 70.0, 1, 1, 'g'),
    ('CM-20003', 'Carton Dimensions', 'Dimensions of Carton', 'CONTROL', 'VARIABLE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-20004', 'Carton Material', 'Material of Carton', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-20005', 'Carton Color', 'Color of Carton', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, '');

-- Packaging Box Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES
    ('CM-30001', 'Box Thickness', 'Thickness of Box', 'CONTROL', 'VARIABLE', 'Decimal', 2.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.0, 1, 2, 'mm'),
    ('CM-30002', 'Box Weight', 'Weight of Box', 'CONTROL', 'VARIABLE', 'Decimal', 100.0, 100.0, 110.0, 120.0, 130.0, 140.0, 140.0, 1, 1, 'g'),
    ('CM-30003', 'Box Dimensions', 'Dimensions of Box', 'CONTROL', 'VARIABLE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-30004', 'Box Material', 'Material of Box', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, ''),
    ('CM-30005', 'Box Color', 'Color of Box', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, '');

-- Chemical Substance Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES
    ('CM-40001', 'Chemical Purity', 'Purity of Chemical Substance', 'CONTROL', 'VARIABLE', 'Decimal', 95.0, 95.0, 97.0, 98.0, 99.0, 100.0, 100.0, 1, 1, '%'),
    ('CM-40002', 'Chemical Concentration', 'Concentration of Chemical Substance', 'CONTROL', 'VARIABLE', 'Decimal', 10.0, 10.0, 15.0, 20.0, 25.0, 30.0, 30.0, 1, 1, '%'),
    ('CM-40003', 'Chemical pH', 'pH of Chemical Substance', 'CONTROL', 'VARIABLE', 'Decimal', 2.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.0, 1, 2, 'pH'),
    ('CM-40004', 'Chemical Viscosity', 'Viscosity of Chemical Substance', 'CONTROL', 'VARIABLE', 'Decimal', 5.0, 5.0, 10.0, 15.0, 20.0, 25.0, 25.0, 1, 2, 'Pa.s'),
    ('CM-40005', 'Chemical Color', 'Color of Chemical Substance', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, '');

-- Water Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES 
    ('CM-50002', 'Water pH', 'pH of Water', 'CONTROL', 'VARIABLE', 'Decimal', 6.5, 6.5, 7.0, 7.5, 8.0, 8.5, 8.5, 1, 2, 'pH'),
    ('CM-50003', 'Water Conductivity', 'Conductivity of Water', 'CONTROL', 'VARIABLE', 'Decimal', 0.0, 0.0, 0.1, 0.2, 0.3, 0.5, 0.5, 1, 3, 'µS/cm'),
    ('CM-50004', 'Water Hardness', 'Hardness of Water', 'CONTROL', 'VARIABLE', 'Decimal', 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 4.0, 1, 1, 'dH'),
    ('CM-50005', 'Water Color', 'Color of Water', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, '');

-- Shampoo Bottle Characteristics
INSERT INTO Characteristics (master_name, name, specifics, action_required, report_type, data_type, lower_routine_release_limit, lower_limit, lower_target, target, upper_target, upper_limit, upper_routine_release_limit, test_frequency, precision, engineering_unit)
VALUES 
    ('CM-60001', 'Bottle Volume', 'Capacity of Shampoo Bottle', 'CONTROL', 'VARIABLE', 'Decimal', 490.0, 490.0, 500.0, 505.0, 510.0, 520.0, 520.0, 1, 2, 'ml'),
    ('CM-60002', 'Bottle Weight', 'Weight of Shampoo Bottle', 'CONTROL', 'VARIABLE', 'Decimal', 30.0, 30.0, 35.0, 40.0, 45.0, 50.0, 50.0, 1, 1, 'g'),
    ('CM-60003', 'Bottle Height', 'Height of Shampoo Bottle', 'CONTROL', 'VARIABLE', 'Decimal', 180.0, 180.0, 185.0, 190.0, 195.0, 200.0, 200.0, 1, 1, 'mm'),
    ('CM-60004', 'Bottle Diameter', 'Diameter of Shampoo Bottle', 'CONTROL', 'VARIABLE', 'Decimal', 50.0, 50.0, 55.0, 60.0, 65.0, 70.0, 70.0, 1, 1, 'mm'),
    ('CM-60005', 'Bottle Material', 'Material of Shampoo Bottle', 'INSPECT', 'ATTRIBUTE', 'String', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, '');

-- Create IdentifierCharacteristics table
CREATE TABLE IdentifierCharacteristics (
    identifier_name VARCHAR(255),
    master_name VARCHAR(255),
    characteristic_name VARCHAR(255),
    PRIMARY KEY (identifier_name, master_name, characteristic_name),
    FOREIGN KEY (identifier_name) REFERENCES Identifiers(identifier_name),
    FOREIGN KEY (master_name, characteristic_name) REFERENCES Characteristics(master_name, name)
);
-- Linking Shampoo Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823141', 'CM-10001', 'Volume'),
    ('88823141', 'CM-10002', 'pH Level'),
    ('88823141', 'CM-10003', 'Viscosity'),
    ('88823141', 'CM-10004', 'Color'),
    ('88823141', 'CM-10005', 'Fragrance'),
    ('88823141', 'CM-10006', 'Foam Height'),
    ('88823141', 'CM-10007', 'Density'),
    ('88823141', 'CM-10008', 'Ingredient A Concentration'),
    ('88823141', 'CM-10009', 'Ingredient B Concentration'),
    ('88823141', 'CM-10010', 'Shelf Life');

-- Linking Packaging Carton Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823142', 'CM-20001', 'Carton Thickness'),
    ('88823142', 'CM-20002', 'Carton Weight'),
    ('88823142', 'CM-20003', 'Carton Dimensions'),
    ('88823142', 'CM-20004', 'Carton Material'),
    ('88823142', 'CM-20005', 'Carton Color');

-- Linking Packaging Box Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823143', 'CM-30001', 'Box Thickness'),
    ('88823143', 'CM-30002', 'Box Weight'),
    ('88823143', 'CM-30003', 'Box Dimensions'),
    ('88823143', 'CM-30004', 'Box Material'),
    ('88823143', 'CM-30005', 'Box Color');

-- Linking Chemical Substance Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823144', 'CM-40001', 'Chemical Purity'),
    ('88823144', 'CM-40002', 'Chemical Concentration'),
    ('88823144', 'CM-40003', 'Chemical pH'),
    ('88823144', 'CM-40004', 'Chemical Viscosity'),
    ('88823144', 'CM-40005', 'Chemical Color');

-- Linking Water Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823145', 'CM-50002', 'Water pH'),
    ('88823145', 'CM-50003', 'Water Conductivity'),
    ('88823145', 'CM-50004', 'Water Hardness'),
    ('88823145', 'CM-50005', 'Water Color');

-- Linking Shampoo Bottle Characteristics
INSERT INTO IdentifierCharacteristics (identifier_name, master_name, characteristic_name)
VALUES
    ('88823146', 'CM-60001', 'Bottle Volume'),
    ('88823146', 'CM-60002', 'Bottle Weight'),
    ('88823146', 'CM-60003', 'Bottle Height'),
    ('88823146', 'CM-60004', 'Bottle Diameter'),
    ('88823146', 'CM-60005', 'Bottle Material');
