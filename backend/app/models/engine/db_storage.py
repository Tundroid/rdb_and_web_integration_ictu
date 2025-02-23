#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.applicant import Applicant
from models.department import Department
from models.program import Program
from models.admission import Admission
from models.notification import Notification
from os import getenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import scoped_session, sessionmaker


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

classes = {
    "applicant": Applicant,
    "department": Department,
    "program": Program,
    "admission": Admission,
    "notification": Notification
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        APP_MYSQL_USER = getenv("APP_MYSQL_USER")
        APP_MYSQL_PWD = getenv("APP_MYSQL_PWD")
        APP_MYSQL_HOST = getenv("APP_MYSQL_HOST")
        APP_MYSQL_DB = getenv("APP_MYSQL_DB")
        APP_ENV = getenv("APP_ENV")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(
                    APP_MYSQL_USER,
                    APP_MYSQL_PWD,
                    APP_MYSQL_HOST,
                    APP_MYSQL_DB)
            )
        if APP_ENV == "test":
            pass

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        class_dict = classes
        if cls:
            class_dict = {key: val for key, val in class_dict.items() if val == cls}
        for my_class in class_dict.values():
            objs = self.__session.query(my_class).all()
            for obj in objs:
                obj_id = ("-".join([str(getattr(obj, k.name))
                                    for k in inspect(cls).primary_key]))
                key = f"{obj.__class__.__name__}.{obj_id}"
                new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
        # pk_name = inspect(obj).primary_key[0].name  # Get the primary key column name
        # print("Before: ", getattr(obj, pk_name))  # Print before flush
        self.__session.flush()  # Assigns the autogenerated ID
        # print("After: ", getattr(obj, pk_name))  # Print after flush

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        # TODO try to create all db with the following
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, ids):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        return (self.__session.query(cls)
                        .filter_by(**ids).first())

    def count(self, cls=None):
        """
        count the number of objects in storage
        """

        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def clean(self, cls):
        """
        clear all records in given table represented by @cls
        """
        # Disable foreign key checks
        self.__session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        # Truncate the table
        self.__session.execute(text(f"TRUNCATE TABLE {cls.__tablename__}"))

        # Re-enable foreign key checks
        self.__session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        self.save()
    @property
    def session(self):
        """
        Getter for the private __session attribute.
        Provides controlled access to the database session.
        """
        return self.__session

    def send_mail(self):
        # Sender email credentials
        SMTP_SERVER = "moleculesoft.net"  # Change this for other email providers
        SMTP_PORT = 465
        EMAIL_SENDER = "admissions@moleculesoft.net"
        EMAIL_PASSWORD = "Admissions.25"  # Use App Password if 2FA is enabled
        EMAIL_RECEIVER = ""
        
        # Connect to SMTP server and send email
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        notifications = self.all(Notification)
        for notification in notifications.values():
            try:
                if notification.NotificationStatus == "Unsent":
                    admission = self.get(Admission, {"AdmissionID": notification.AdmissionID})
                    if admission:
                        applicant = self.get(Applicant, {"ApplicantID": admission.ApplicantID})
                        if applicant:
                            EMAIL_RECEIVER = applicant.Email
                            
                            # Create the email
                            msg = MIMEMultipart()
                            msg["From"] = EMAIL_SENDER
                            msg["To"] = EMAIL_RECEIVER
                            msg["Subject"] = "Application Status"
                            body = notification.Message
                            msg.attach(MIMEText(body, "plain"))

                            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
                            
                            setattr(notification, "NotificationStatus", "Sent")
                            print("Email sent successfully!")
                        else:
                            print("Could not retrieve applicant")
                    else:
                        print("Could not retrieve admission")
            except Exception as e:
                print(f"Error: {e}")
        self.save()
        server.quit