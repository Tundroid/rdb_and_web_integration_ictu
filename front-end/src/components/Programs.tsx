import React, { useEffect, useState } from 'react';
import { API_URL } from '../util/contants';
import { Table, Form, FormGroup, Label, Input, Button, Col, Row } from 'reactstrap';

const Programs = () => {
	const [programs, setPrograms] = useState([]);
	const [departmentID, setDepartmentID] = useState(0);
	const [programName, setProgramName] = useState('');
	const [programCode, setProgramCode] = useState('');
	const [duration, setDuration] = useState(1);
	const [departments, setDepartments] = useState([]);

	const fetchData = async () => {
		try {
			const response = await fetch(`${API_URL}get_list_program`);
			const data = await response.json();
			data.sort((a: any, b: any) =>
				a.ProgramName.localeCompare(b.ProgramName)
			);
			setPrograms(data);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	};

	useEffect(() => {
		const fetchDepartments = async () => {
			try {
				const response = await fetch(`${API_URL}get/department`);
				if (!response.ok) throw new Error('Failed to fetch departments');
				const data = await response.json();
				setDepartments(data);
			} catch (error) {
				console.error('Error fetching departments:', error);
			}
		};
		fetchDepartments();
	}, []);


	useEffect(() => {
		fetchData();
	}, []);

	const handleAddProgram = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			const response = await fetch(`${API_URL}create/program`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					ProgramCode: programCode,
					ProgramName: programName,
					DepartmentID: departmentID,
					Duration: duration
				}),
			});
			let t = JSON.stringify({
				ProgramCode: programCode,
				ProgramName: programName,
				DepartmentID: departmentID,
				Duration: duration
			});
			console.log("Data sent: ", t);
			const data = await response.json();
			fetchData();
			setDepartmentID(0);
			setProgramName('');
			setProgramCode('');
			setDuration(0);
		} catch (error) {
			console.error('Error adding program:', error);
		}
	};

	
	const handleDelete = async (program: any) => {
		try {

			const params = {
				ProgramCode: program.ProgramCode
			};

			const queryString = new URLSearchParams(params).toString();

			const response = await fetch(`${API_URL}delete/program?${queryString}`, {
				method: 'DELETE'
			});

			if (response.ok) {
				window.alert('Delete successful!');
				fetchData();
			} else {
				window.alert('Delete failed!');
			}

		} catch (error) {
			console.error('Error deleting:', error);
		}
	};

	return (
		<div className="container mt-4">
			<h2>Programs</h2>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Form onSubmit={handleAddProgram} className="mb-4">
				<Row form>
					{/* Program Code */}
					<Col md={3}>
						<FormGroup>
							<Label for="programCode">Program Code</Label>
							<Input
								required
								type="text"
								id="programCode"
								value={programCode}
								onChange={(event) => setProgramCode(event.target.value)}
							/>
						</FormGroup>
					</Col>

					{/* Program Name */}
					<Col md={3}>
						<FormGroup>
							<Label for="programName">Program Name</Label>
							<Input
								required
								type="text"
								id="programName"
								value={programName}
								onChange={(event) => setProgramName(event.target.value)}
							/>
						</FormGroup>
					</Col>

					{/* Department */}
					<Col md={3}>
						<FormGroup>
							<Label for="department">Department</Label>
							<Input
								required
								type="select"
								id="department"
								value={departmentID}
								onChange={(event) => setDepartmentID(parseInt(event.target.value))}
							>
								<option value="">Select a department</option>
								{departments.map((department: any) => (
									<option key={department.DepartmentID} value={department.DepartmentID}>
										{department.DepartmentName}
									</option>
								))}
							</Input>
						</FormGroup>
					</Col>

					{/* Duration */}
					<Col md={2}>
						<FormGroup>
							<Label for="duration">Duration (Years)</Label>
							<Input
								required
								type="number"
								id="duration"
								value={duration}
								onChange={(event) => setDuration(parseInt(event.target.value))}
							/>
						</FormGroup>
					</Col>

					{/* Submit Button */}
					<Col md={1} className="d-flex align-items-end">
						<Button type="submit" color="primary">
							Add
						</Button>
					</Col>
				</Row>
			</Form>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Table striped bordered hover responsive>
				<thead>
					<tr>
						<th>Code</th>
						<th>Program</th>
						<th>Department</th>
						<th>Duration</th>
						<th>Action</th>
					</tr>
				</thead>
				<tbody>
					{programs.map((program: any) => (
						<tr key={program.ProgramID}>
							<td>{program.ProgramCode}</td>
							<td>{program.ProgramName}</td>
							<td>{program.DepartmentName}</td>
							<td>{program.Duration}</td>
							<td><button className="btn btn-danger"
								onClick={() => handleDelete(program)}>Delete</button></td>
						</tr>
					))}
				</tbody>
			</Table>
		</div>
	);


};

export default Programs;
