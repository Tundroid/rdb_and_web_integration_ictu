import React, { useEffect, useState } from 'react';
import { API_URL } from '../util/contants';
import { Table, Form, FormGroup, Label, Input, Button, Col, Row } from 'reactstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const Admissions = () => {
	const [admissions, setAdmissions] = useState([]);
	const [filteredAdmissions, setFilteredAdmissions] = useState([]);
	const [status, setStatus] = useState('');

	const fetchData = async () => {
		try {
			const response = await fetch(`${API_URL}get_list_admission`); // Replace with actual API URL
			const data = await response.json();
			data.sort((a: any, b: any) =>
				b.AdmissionID - a.AdmissionID
			);
			setAdmissions(data);
			setFilteredAdmissions(data);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	};

	useEffect(() => {
		// Simulating an API request (replace with actual fetch call)
		fetchData();
	}, []);

	useEffect(() => {
		if (status === '') {
			setFilteredAdmissions(admissions);
		} else {
			const filtered = admissions.filter((admission: any) => admission.ApplicationStatus === status);
			setFilteredAdmissions(filtered);
		}
	}, [status, admissions]);

	const handleAction = async (admission: any, isAccepted: boolean) => {
		console.log("Admission ID:", admission.AdmissionID);
		console.log("Action:", isAccepted ? "Accept" : "Reject");
		try {
			const admissionPayload = {
				ApplicationStatus: isAccepted ? 'Accepted' : 'Rejected'
			};

			const params = {
				AdmissionID: admission.AdmissionID
			};

			const queryString = new URLSearchParams(params).toString();

			const admissionResponse = await fetch(`${API_URL}update/admission?${queryString}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(admissionPayload)
			});

			if (admissionResponse.ok) {
				console.log('Admission updated successfully');
				fetchData();
			} else {
				console.error('Failed to update admission');
			}

		} catch (error) {
			console.error('Error submitting applicant and admission:', error);
		}

		// You can then call an API or update the state based on the action taken.
	};

	return (
		<div className="container mt-4">
			<h2>Admissions</h2>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Form className="mb-4">
				<Row form>

					{/* Department */}
					<Col md={3}>
						<FormGroup>
							<Label for="status">Status Filter</Label>
							<Input
								required
								type="select"
								name="status"
								id="status"
								value={status}
								onChange={(event) => setStatus(event.target.value)}
							>
								<option value="">No filter</option>
								<option value="Pending">Pending</option>
								<option value="Accepted">Accepted</option>
								<option value="Rejected">Rejected</option>
							</Input>
						</FormGroup>
					</Col>
				</Row>
			</Form>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Table striped bordered hover responsive>
				<thead>
					<tr>
						<th>ID</th>
						<th>Applicant</th>
						<th>Program</th>
						<th>Department</th>
						<th>Date</th>
						<th>Status</th>
					</tr>
				</thead>
				<tbody>
					{filteredAdmissions.map((admission: any) => (
						<tr key={admission.AdmissionID}>
							<td>{admission.AdmissionID}</td>
							<td>{admission.FullName}</td>
							<td>{admission.ProgramName}</td>
							<td>{admission.DepartmentName}</td>
							<td>{new Date(admission.ApplicationDate).toLocaleDateString('en-US', { dateStyle: 'medium' })}</td>
							<td>
								<span className={`badge ${admission.ApplicationStatus === "Accepted" ? "badge-success" : "badge-danger"}`}>
									{admission.ApplicationStatus}
								</span>
								{admission.ApplicationStatus === "Pending" ? (
									<div>
										<button className="btn btn-success"
											onClick={() => handleAction(admission, true)}>Accept</button>
										<button className="btn btn-danger"
											onClick={() => handleAction(admission, false)}>Reject</button>
									</div>
								) : (""
								)}</td>
						</tr>
					))}
				</tbody>
			</Table>
		</div>
	);
};

export default Admissions;
