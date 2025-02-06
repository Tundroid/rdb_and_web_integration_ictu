import React, { useEffect, useState } from 'react';
import { API_URL } from '../util/contants';
import { Table, Form, FormGroup, Label, Input, Button, Col, Row } from 'reactstrap';

const Departments = () => {
	const [departments, setDepartments] = useState([]);
	const [departmentName, setDepartmentName] = useState('');

	const fetchData = async () => {
		try {
			const response = await fetch(`${API_URL}get/department`); // Replace with actual API URL
			const data = await response.json();
			data.sort((a: any, b: any) =>
				a.DepartmentName.localeCompare(b.DepartmentName)
			);
			setDepartments(data);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	};

	useEffect(() => {
		fetchData();
	}, []);

	const handleAddDepartment = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			const response = await fetch(`${API_URL}create/department`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ DepartmentName: departmentName }),
			});
			const data = await response.json();
			fetchData();
			setDepartmentName('');
		} catch (error) {
			console.error('Error adding department:', error);
		}
	};

	const handleDelete = async (department: any) => {
		try {

			const params = {
				DepartmentID: department.DepartmentID
			};

			const queryString = new URLSearchParams(params).toString();

			const response = await fetch(`${API_URL}delete/department?${queryString}`, {
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
			<h2>Departments</h2>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Form onSubmit={handleAddDepartment}>
				<Row form>
					{/* Program Code */}
					<Col md={3}>
						<FormGroup>
							<Label for="departmentName">Department Name:</Label>
							<Input
								required
								type="text"
								name="departmentName"
								id="departmentName"
								value={departmentName}
								onChange={(event) => setDepartmentName(event.target.value)}
							/>
						</FormGroup>
					</Col>
					<Col md={1} className="d-flex align-items-end">
						<Button type="submit" color="primary">
							Add Department
						</Button>
					</Col>
				</Row>
			</Form>
			<hr style={{ borderTop: "4px solid #007bff" }} />
			<Table striped bordered hover responsive>
				<thead>
					<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{departments.map((department: any) => (
						<tr key={department.DepartmentID}>
							<td>{department.DepartmentID}</td>
							<td>{department.DepartmentName}</td>
							<td><button className="btn btn-danger"
								onClick={() => handleDelete(department)}>Delete</button></td>
						</tr>
					))}
				</tbody>
			</Table>
		</div>
	);
};

export default Departments;
