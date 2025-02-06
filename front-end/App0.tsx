import React, { useState, useEffect, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Form from './components/Form'
import SaleDetail from './components/SaleDetail'
import ItemDetail from './components/ItemDetail'
import ItemTable from './components/ItemTable';
import SideMenu from './components/SideMenu';
import { Util } from './util/Util';
import { Cart } from './util/Cart'
import { API_URL } from './util/contants'
import { v4 as uuidv4 } from 'uuid';
import './App.css';



function App() {
	const navigate = useNavigate();
	const [carts, setCarts] = useState<Cart[]>([]);
	const [activeCartId, setActiveCartId] = useState<string | null>(null);

	const activeCart = carts?.find((cart) => cart.active);

	const addNewCart = () => {
		const newCart: Cart = {
			id: uuidv4(),
			items: {},
			active: true,
			createdAt: new Date(),
			updatedAt: new Date(),
			total: 0,
			saleDate: new Date(),
			ref: Util.getInvoiceNumber(),
			receiver: 1,
			rec_desc: ""
		};
		setCarts((prevCarts) =>
			prevCarts.map((cart) => ({ ...cart, active: false })).concat(newCart)
		);
		setActiveCartId(newCart.id);
	};

	const handleDeleteCart = (cartId: string) => {
		setCarts((prevCarts) => prevCarts.filter((cart) => cart.id !== cartId));
	};

	const handleValidateClick = async () => {
		if (!activeCart) return;
		const details = {
			batch: activeCart.id,
			operation: 2,
			receiver: activeCart.receiver,
			source_depot: 5,
			dest_depot: 2,
			rec_date: activeCart.saleDate.toISOString().slice(0, 10),
			ref: activeCart.ref,
			app_user: 2,
			rec_desc: activeCart.rec_desc
		};
		const records = Object.values(activeCart.items).map(({ id, amount, quantity }) => ({ item: id, amount, quantity, batch: activeCart.id }));
		const payload = {
			details: details,
			records: records
		}
		console.log(payload);
		// try {
		// 	const response = await fetch(`${API_URL}sell`, {
		// 		method: 'POST',
		// 		headers: {
		// 			'Content-Type': 'application/json',
		// 			'Authorization': `Bearer ${JWT_TOKEN}`
		// 		},
		// 		body: JSON.stringify(payload),
		// 	});

		// 	if (response.ok) {
		// 		console.log('Order sent successfully!');
		// 		handleDeleteCart(activeCart.id);
		// 	} else {
		// 		console.error('Error sending order:', response.status);
		// 	}
		// } catch (error) {
		// 	console.error('Error sending order:', error);
		// }
	};

	useEffect(() => {
		if (!carts.length)
			addNewCart();
	}, [carts]);

	const handleNoteChange = (rec_desc: string) => {
		setCarts((prevCarts) =>
			prevCarts.map((cart) =>
				cart.active
					? {
						...cart,
						rec_desc,
						updatedAt: new Date(),
					}
					: cart
			)
		);
	};

	const buttonStyle: React.CSSProperties = {
		display: 'block',
		width: '200px',
		padding: '20px',
		margin: '20px auto',
		fontSize: '18px',
		fontWeight: 'bold',
		color: '#fff',
		backgroundColor: '#007bff',
		border: 'none',
		borderRadius: '10px',
		cursor: 'pointer',
		boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
		transition: 'background-color 0.3s ease',
	};

	const containerStyle: React.CSSProperties = {
		display: 'flex',
		flexDirection: 'column',
		justifyContent: 'center',
		alignItems: 'center',
		height: '100vh',
		backgroundColor: '#f0f0f0',
	};

	const handleApplicantClick = () => {
		navigate('/applicant');
	};

	const handleAdminClick = () => {
		navigate('/admin');
	};

	// const LandingPage =
	// 	<>

	// 	</>;

	const LandingPage: React.FC = () => {
		return (
			<div style={containerStyle}>
				<button style={buttonStyle} onClick={handleApplicantClick}>
					Applicant
				</button>
				<button style={{ ...buttonStyle, backgroundColor: '#28a745' }} onClick={handleAdminClick}>
					Admin
				</button>
			</div>
		);
	};

	// Applicant Page Component
	const ApplicantPage = () => {
		return (
			<div style={{ textAlign: 'center', padding: '20px' }}>
				<h1>Welcome, Applicant!</h1>
				<p>This is the applicant page.</p>
			</div>
		);
	};

	// Admin Page Component
	const AdminPage = () => {
		return (
			<div style={{ textAlign: 'center', padding: '20px' }}>
				<h1>Welcome, Admin!</h1>
				<p>This is the admin page.</p>
			</div>
		);
	};

	const app =
		<Router>
			<Routes>
				<Route path="/" element={<LandingPage />} />
				<Route path="/applicant" element={<ApplicantPage />} />
				<Route path="/admin" element={<AdminPage />} />
			</Routes>
		</Router>;
	return app;


	// const app =
	// 	<>
	// 		<h1>POS System</h1>
	// 		<div className="row">
	// 			<div className="col-md-8">
	// 				<Form carts={carts} setCarts={setCarts} />
	// 				<h2>Cart</h2>
	// 				<SaleDetail carts={carts} setCarts={setCarts}/>
	// 				<ItemDetail carts={carts} setCarts={setCarts}/>
	// 				<ItemTable carts={carts} setCarts={setCarts} />
	// 				<label>
	// 					Note(s) / Detail(s):
	// 					<input
	// 						type="text"
	// 						value={activeCart?.rec_desc}
	// 						onChange={(e) => handleNoteChange(e.target.value)}
	// 					/>
	// 				</label>
	// 				<h3>Grand Total: {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'XAF' }).format(activeCart ? activeCart.total : 0)}</h3>
	// 				<button className="btn btn-success" disabled={(activeCart ? activeCart.total : 0) === 0} onClick={handleValidateClick}>Validate</button>
	// 			</div>
	// 			<div className="col-md-4">
	// 				<SideMenu
	// 					carts={carts}
	// 					activeCartId={activeCartId}
	// 					setActiveCartId={setActiveCartId}
	// 					setCarts={setCarts}
	// 					addNewCart={addNewCart}
	// 				/>
	// 			</div>
	// 		</div>
	// 	</>;
	// return app;
}

export default App;
