CREATE TABLE Researcher (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100)
);

CREATE TABLE Expertise (
    ID VARCHAR(255) PRIMARY KEY
);

CREATE TABLE ResearcherExpertise (
    ID INT ,
    Expertise VARCHAR(255),
    PRIMARY KEY (ID, Expertise),
    FOREIGN KEY (ID) REFERENCES Researcher(ID)
    -- FOREIGN KEY (Expertise) REFERENCES Expertise(ID)
);

CREATE TABLE ResearchPaper (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    PublicationDate DATE,
    CitationCount INT,
    Conference INT
);

CREATE TABLE Authorship (
    Paper INT,
    Author INT,
    PRIMARY KEY (Paper, Author),
    FOREIGN KEY (Paper) REFERENCES ResearchPaper(ID),
    FOREIGN KEY (Author) REFERENCES Researcher(ID)
);

CREATE TABLE Conference (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Date DATE,
    Location VARCHAR(255)
);

CREATE TABLE Review (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Paper INT,
    Title VARCHAR(255),
    FOREIGN KEY (Paper) REFERENCES ResearchPaper(ID)
);

INSERT INTO Expertise (ID)
VALUES
    ('Machine Learning'),
    ('Quantum Physics'),
    ('Environmental Science'),
    ('Artificial Intelligence'),
    ('Biomedical Engineering'),
    ('Cultural Anthropology'),
    ('Climate Change Policy'),
    ('Astrophysics'),
    ('Bioinformatics'),
    ('Linguistic Analysis'),
    ('Materials Science'),
    ('Epidemiology'),
    ('Urban Planning'),
    ('Renewable Energy Technology'),
    ('Game Theory'),
    ('Cognitive Neuroscience'),
    ('Political Economy'),
    ('Organic Chemistry'),
    ('Social Psychology'),
    ('Cybersecurity');


/*INSERT INTO Researcher (Name, Email, Age)
VALUES
    ('John Doe', 'john.doe@example.com', 35),
    ('Alice Smith', 'alice.smith@example.com', 28),
    ('Bob Johnson', 'bob.johnson@example.com', 32),
    ('Emily Davis', 'emily.davis@example.com', 29),
    ('Michael Wilson', 'michael.wilson@example.com', 40);
    -- ('Olivia Lee', 'olivia.lee@example.com', 37),
    -- ('David Brown', 'david.brown@example.com', 31),
    -- ('Sophia Taylor', 'sophia.taylor@example.com', 42),
    -- ('James Anderson', 'james.anderson@example.com', 34),
    -- ('Ella Martinez', 'ella.martinez@example.com', 27);


INSERT INTO ResearchPaper (Title, PublicationDate, CitationCount, Conference)
VALUES
    ('Paper 1', '2023-01-15', 20, 1),
    ('Paper 2', '2022-08-10', 15, 2),
    ('Paper 3', '2023-03-22', 30, 1),
    ('Paper 4', '2022-12-05', 12, 3),
    ('Paper 5', '2023-05-30', 25, 2),
    ('Paper 6', '2022-09-17', 18, 1),
    ('Paper 7', '2023-02-14', 22, 3),
    ('Paper 8', '2023-06-11', 28, 2),
    ('Paper 9', '2022-11-03', 14, 1),
    ('Paper 10', '2023-04-25', 16, 2);

-- Researcher IDs 1 to 5
-- Paper IDs 1 to 10
INSERT INTO Authorship (Paper, Author)
VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 3),
    (3, 4),
    (4, 5),
    (4, 1),
    (5, 2),
    (5, 3),
    (6, 4),
    (6, 5),
    (7, 1),
    (7, 2),
    (8, 3),
    (8, 4),
    (9, 5),
    (9, 1),
    (10, 2),
    (10, 3);

INSERT INTO Conference (Title, Date, Location, Organiser)
VALUES
    ('Conference 1', '2023-08-15', 'New York', 'Organizer 1'),
    ('Conference 2', '2022-11-20', 'San Francisco', 'Organizer 2'),
    ('Conference 3', '2023-04-05', 'London', 'Organizer 3');
    -- ('Conference 4', '2022-10-10', 'Tokyo', 'Organizer 4'),
    -- ('Conference 5', '2023-03-25', 'Berlin', 'Organizer 5'),
    -- ('Conference 6', '2022-09-30', 'Sydney', 'Organizer 6'),
    -- ('Conference 7', '2023-07-10', 'Paris', 'Organizer 7'),
    -- ('Conference 8', '2022-12-15', 'Toronto', 'Organizer 8'),
    -- ('Conference 9', '2023-06-20', 'Singapore', 'Organizer 9'),
    -- ('Conference 10', '2022-11-05', 'Barcelona', 'Organizer 10');

INSERT INTO Review (Paper, Title, Rating)
VALUES
    (1, 'Review of Paper 1', 4.5),
    (1, 'Second Review of Paper 1', 4.0),
    (2, 'Review of Paper 2', 3.8),
    (2, 'Second Review of Paper 2', 4.2),
    (3, 'Review of Paper 3', 4.6),
    (3, 'Second Review of Paper 3', 3.9),
    (4, 'Review of Paper 4', 3.6),
    (5, 'Review of Paper 5', 4.8),
    (6, 'Review of Paper 6', 4.0),
    (7, 'Review of Paper 7', 4.4),
    (8, 'Review of Paper 8', 4.2),
    (8, 'Second Review of Paper 8', 3.7),
    (9, 'Review of Paper 9', 4.1),
    (9, 'Second Review of Paper 9', 4.5),
    (10, 'Review of Paper 10', 3.9),
    (10, 'Second Review of Paper 10', 4.3);*/
