import React, { useEffect, useState } from 'react';
import { API_URL } from '../util/contants';
import { Table } from 'reactstrap';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Simulating an API request (replace with actual fetch call)
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}get/notification`); // Replace with actual API URL
        const data = await response.json();
		data.sort((a: any, b: any) =>
			b.NotificationID - a.NotificationID
		  );
        setNotifications(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mt-4">
      <h2>Notifications</h2>
	  <hr style={{ borderTop: "4px solid #007bff" }} />
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Admission ID</th>
            <th>Message</th>
			<th>NotificationStatus</th>
			<th>CreatedAt</th>
          </tr>
        </thead>
        <tbody>
          {notifications.map((notification : any)  => (
            <tr key={notification.NotificationID}>
              <td>{notification.AdmissionID}</td>
              <td>{notification.Message}</td>
			  <td>{notification.NotificationStatus}</td>
			  <td>{notification.CreatedAt}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Notifications;
