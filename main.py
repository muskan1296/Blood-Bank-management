CREATE TABLE Patient
    (Patient_ID         INT         NOT NULL,
     Patient_Name       VARCHAR(30) NOT NULL,
     Blood_Group        VARCHAR(4)  NOT NULL,
     Disease            CHAR(2)
                CHECK (Disease IN('A','B','AB','O')),
     Patient_Contact    NUMBER(10,0),
     Patient_Address    VARCHAR(45),
CONSTRAINT Patient_PK PRIMARY KEY (Patient_ID));

CREATE TABLE Donor
    (Donor_ID           INT         NOT NULL,
     Donor_Name         VARCHAR(30) NOT NULL,
     Medical_Report     VARCHAR(20) NOT NULL
                CHECK (Medical_Report IN('Satisfactory','Not Satisfactory')),
     Donor_Addresss     VARCHAR(45),
     Donor_Contact      NUMBER(10,0),
CONSTRAINT Donor_PK PRIMARY KEY (Donor_ID));

CREATE TABLE Blood_Bank
    (Blood_Bank_ID      INT             NOT NULL,
     Blood_Bank_Name    VARCHAR(50)     NOT NULL,
     Blood_Bank_Address VARCHAR(45),
     Blood_Bank_Contact Number(10,0),
     Donor_ID           INT,
     Patient_ID         INT,
CONSTRAINT Blood_Bank_PK PRIMARY KEY (Blood_Bank_ID),
CONSTRAINT Blood_Bank_FK1 FOREIGN KEY (Donor_ID)  REFERENCES Donor(Donor_ID),
CONSTRAINT Blood_Bank_FK2 FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID));

INSERT INTO Patient VALUES (101,'Jose Adams','AB+','O',7778889999,'101 Melborne') ;
INSERT INTO Patient VALUES (102,'Rose Clara','B+','AB',8889999777,'102 Austria') ;
INSERT INTO Patient VALUES (103,'Ray Spencer','0-','A',6669999777,'103 Naple') ;
INSERT INTO Patient VALUES (104,'Sara Crux','AO','B',8885559777,'104 Paris') ;
INSERT INTO Patient VALUES (105,'Nate Zara','A+','O',1119999777,'105 London') ;


INSERT INTO Donor VALUES (201,'Lara Croft','Satisfactory','201 Meru',1112223333);
INSERT INTO Donor VALUES (202,'Manuel Ladder','Not Satisfactory','202 Lamu',2223334444);
INSERT INTO Donor VALUES (203,'Zain Orange','Satisfactory','203 Nairobi',3334445555);
INSERT INTO Donor VALUES (204,'Anne Gibbs','Not Satisfactory','204 Narok',4445556666);
INSERT INTO Donor VALUES (205,'Reign Stomy','Satisfactory','205 Vasha',5556667777);

INSERT INTO Blood_Bank Values (301,'Meru Blood Bank','301 Meru','6667778888',201,101);
INSERT INTO Blood_Bank Values (302,'Lamu Blood Bank','302 Lamu','7778889999',203,102);
INSERT INTO Blood_Bank Values (303,'Nairobi Blood Bank','303 Nairobi','8889991111',205,103);
INSERT INTO Blood_Bank Values (304,'Narok Blood Bank','304 Narok','9991112222',205,104);
INSERT INTO Blood_Bank Values (305,'Vasha Blood Bank','305 Vasha','1112223333',203,105);

SELECT Patient_Name,Blood_Group,Disease
FROM Patient
WHERE Patient_ID = 101;


SELECT Donor_Name,Donor_Addresss,Donor_Contact,Medical_Report
FROM Donor
WHERE Medical_Report = 'Satisfactory';


SELECT Patient_Name,Blood_Group,Blood_Bank_Name,blood_bank.patient_id,patient.patient_id
FROM Patient, Blood_Bank
WHERE blood_bank.patient_id = patient.patient_id;


SELECT Donor_Name,Medical_Report,Donor_Addresss,donor.donor_id,Blood_Bank_Name
FROM Donor,Blood_Bank
WHERE blood_bank.donor_id = donor.donor_id;


SELECT Blood_Bank_Name, Blood_Bank_Contact,Patient_Name,Patient.Patient_id
FROM Blood_Bank, Patient
WHERE patient.patient_id = blood_bank.patient_id;


SELECT Patient_Name, Donor_Name, Blood_Bank_Name, Blood_Group, Medical_Report
FROM Blood_Bank,Patient,Donor
WHERE blood_bank.patient_id = patient.patient_id AND blood_bank.donor_id = donor.donor_id;


SELECT Donor_Name, Donor.Donor_ID, Blood_Bank.Donor_ID
FROM Donor LEFT OUTER JOIN  Blood_Bank
ON Blood_Bank.Donor_ID = donor.donor_id
GROUP BY blood_bank.donor_id;


