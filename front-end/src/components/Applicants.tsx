import React, { useEffect, useState } from 'react';
import { API_URL } from '../util/contants';
import { Table } from 'reactstrap';

const Applicants = () => {
  const [applicants, setApplicants] = useState([]);

  useEffect(() => {
    // Simulating an API request (replace with actual fetch call)
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}get/applicant`); // Replace with actual API URL
        const data = await response.json();
		data.sort((a: any, b: any) =>
			a.FullName.localeCompare(b.FullName)
		  );
        setApplicants(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mt-4">
      <h2>Applicants</h2>
	  <hr style={{ borderTop: "4px solid #007bff" }} />
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Date of Birth</th>
          </tr>
        </thead>
        <tbody>
          {applicants.map((applicant : any)  => (
            <tr key={applicant.ApplicantID}>
              <td>{applicant.ApplicantID}</td>
              <td>{applicant.FullName}</td>
              <td>{applicant.Email}</td>
              <td>{applicant.PhoneNumber}</td>
              <td>{new Date(applicant.DateOfBirth).toLocaleDateString('en-US', { dateStyle: 'medium' })}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Applicants;
