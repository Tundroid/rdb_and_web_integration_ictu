CREATE DATABASE IF NOT EXISTS `rdb_web_db`;

USE `rdb_web_db`;

CREATE TABLE Applicant (
    ApplicantID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    DateOfBirth DATE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) UNIQUE NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Program (
    ProgramCode VARCHAR(10) PRIMARY KEY,
    ProgramName VARCHAR(100) UNIQUE NOT NULL,
    Duration INT NOT NULL,
    DepartmentID INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE Admission (    
    AdmissionID INT AUTO_INCREMENT PRIMARY KEY,
    ApplicantID INT NOT NULL,
    ProgramCode VARCHAR(10) NOT NULL,
    ApplicationDate DATE NOT NULL,
    ApplicationStatus ENUM('Accepted', 'Pending', 'Rejected') NOT NULL DEFAULT "Pending",
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ApplicantID) REFERENCES Applicant(ApplicantID),
    FOREIGN KEY (ProgramCode) REFERENCES Program(ProgramCode)
);

CREATE TABLE Notification (    
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    AdmissionID INT NOT NULL,
    Message TEXT NOT NULL,
    NotificationStatus ENUM('Sent', 'Unsent') NOT NULL DEFAULT "Unsent",
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (AdmissionID) REFERENCES Admission(AdmissionID)
);

DELIMITER ;;
CREATE PROCEDURE CreateAdmissionNotification(
    AdmissionID INT,
    ProgramCode VARCHAR(10),
    NewStatus ENUM('Accepted', 'Pending', 'Rejected')
)
BEGIN
    DECLARE notificationMessage TEXT;

    SET notificationMessage = CONCAT(
        'Your application for the program: ', 
         (SELECT ProgramName FROM Program WHERE ProgramCode = ProgramCode),
         ', Application ID: ', 
        admissionID,
        " has been "
    );

    IF NewStatus = "Pending" THEN
        SET notificationMessage = CONCAT(
            notificationMessage,
            " received and is pending review. Keep checking your mail and expect to hear from
            us within the next five (5) working days. Thanks for applying with us.");
    ELSEIF NewStatus = "Accepted" THEN
        SET notificationMessage = CONCAT(
            notificationMessage,
            " accepted. A follow-up mail on how to continue will be sent to you shortly.
            In the mean time, congratulations!");
    ELSE
        SET notificationMessage = CONCAT(
            notificationMessage,
            " rejected. Reply with ""WHY?"" to find out the reason of rejection.Sorry! Better luck next time.");
    END IF;

    INSERT INTO Notification (AdmissionID, Message)
    VALUES (
        AdmissionID, 
        notificationMessage
    );
END ;;
DELIMITER ;

DELIMITER ;;
CREATE DEFINER=`rdb_user`@`%` TRIGGER `CreateNotificationNEW` AFTER INSERT ON `Admission` FOR EACH ROW 
BEGIN
    CALL CreateAdmissionNotification(NEW.AdmissionID, New.ProgramCode, NEW.ApplicationStatus);
END ;;
DELIMITER ;

DELIMITER ;;
CREATE DEFINER=`rdb_user`@`%` TRIGGER `CreateNotificationUPDATE` AFTER UPDATE ON `Admission` FOR EACH ROW 
BEGIN
    IF NEW.ApplicationStatus <> OLD.ApplicationStatus THEN
        CALL CreateAdmissionNotification(NEW.AdmissionID, New.ProgramCode, NEW.ApplicationStatus);
    END IF;
END ;;
DELIMITER ;

