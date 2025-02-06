import React, { useState, useEffect } from 'react';
import { API_URL } from '../util/contants';
import 'bootstrap/dist/css/bootstrap.min.css';

const ApplicantPage = () => {
	const [fullName, setFullName] = useState('');
	const [email, setEmail] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');
	const [dateOfBirth, setDateOfBirth] = useState('');
	const [programs, setPrograms] = useState([]);
	const [programCode, setProgramCode] = useState('');
	const [departments, setDepartments] = useState([]);
	const [departmentId, setDepartmentId] = useState('');
	const [filteredPrograms, setFilteredPrograms] = useState([]);
	const [admissionSubmitted, setAdmissionSubmitted] = useState(false);
	const [showAlert, setShowAlert] = useState(false);

	useEffect(() => {
		const fetchItems = async () => {
			try {
				const response = await fetch(`${API_URL}get/program`);
				if (!response.ok) throw new Error('Failed to fetch items');
				const data = await response.json();
				setPrograms(data);
			} catch (error) {
				console.error('Error fetching items:', error);
			}
		};
		fetchItems();
	}, []);

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
		if (departmentId) {
			const filtered = programs.filter((program: any) => program.DepartmentID === parseInt(departmentId));
			setFilteredPrograms(filtered);
		} else {
			setFilteredPrograms([]);
		}
	}, [departmentId, programs]);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const applicantPayload = {
			FullName: fullName,
			Email: email,
			PhoneNumber: phoneNumber,
			DateOfBirth: dateOfBirth
		};

		try {
			const applicantResponse = await fetch(`${API_URL}create/applicant`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(applicantPayload)
			});

			if (!applicantResponse.ok) {
				throw new Error('Failed to create applicant');
			}

			const applicantData = await applicantResponse.json();

			const currentDate = new Date();
			const applicationDate = currentDate.toISOString().split('T')[0];

			const admissionPayload = {
				ApplicantID: applicantData.ApplicantID,
				ProgramCode: programCode,
				ApplicationDate: applicationDate
			};

			const admissionResponse = await fetch(`${API_URL}create/admission`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(admissionPayload)
			});

			if (!admissionResponse.ok) {
				throw new Error('Failed to create admission');
			} else {
				setShowAlert(true);
				setAdmissionSubmitted(true);
				setTimeout(() => {
					setShowAlert(false);
					setAdmissionSubmitted(false);
					resetForm();
				}, 5000);
			}

			setShowAlert(true);
			setAdmissionSubmitted(true);
		} catch (error) {
			console.error('Error submitting applicant and admission:', error);
		}
	};



	const resetForm = () => {
		setFullName('');
		setEmail('');
		setPhoneNumber('');
		setDateOfBirth('');
		setProgramCode('');
		setDepartmentId('');
	};

	return (
		<div className="container d-flex justify-content-center align-items-center vh-100 bg-light">
			<div className="card p-4 shadow-lg" style={{ width: '40rem' }}>
				<h2 className="text-center mb-2">Applicant Registration</h2>
				<hr style={{ borderTop: "4px solid #007bff" }} />
				{showAlert && <div className="alert alert-success">Your application has been received and is pending review.</div>}
				<form onSubmit={handleSubmit}>
					<div className="mb-1">
						<label className="form-label">Full Name</label>
						<input type="text" className="form-control" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
					</div>
					<div className="mb-1">
						<label className="form-label">Email</label>
						<input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} required />
					</div>
					<div className="mb-1">
						<label className="form-label">Phone Number</label>
						<input type="tel" className="form-control" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required />
					</div>
					<div className="mb-1">
						<label className="form-label">Date of Birth</label>
						<input type="date" className="form-control" value={dateOfBirth} onChange={(e) => setDateOfBirth(e.target.value)} required />
					</div>
					<div className="mb-1">
						<label className="form-label">Department</label>
						<select className="form-select" value={departmentId} onChange={(e) => setDepartmentId(e.target.value)} required>
							<option value="">Select a department</option>
							{departments.map((department: any) => (
								<option key={department.DepartmentID} value={department.DepartmentID}>{department.DepartmentName}</option>
							))}
						</select>
					</div>
					<div className="mb-1">
						<label className="form-label">Program</label>
						<select className="form-select" value={programCode} onChange={(e) => setProgramCode(e.target.value)} required disabled={!departmentId}>
							<option value="">Select a program</option>
							{filteredPrograms.map((program: any) => (
								<option key={program.ProgramCode} value={program.ProgramCode}>{program.ProgramName}</option>
							))}
						</select>
					</div>
					<button type="submit" className="btn btn-primary w-100">Submit</button>
				</form>
			</div>
		</div>
	);
};

export default ApplicantPage;
