import { createContext, useState, useEffect } from 'react';
import { API_URL } from './util/contants'

interface TokenContextProps {
	jwtToken: string | null;
	refreshJWTToken: () => void;
}

const TokenContext = createContext<TokenContextProps>({
	jwtToken: null,
	refreshJWTToken: () => { },
});

interface TokenProviderProps {
	children: React.ReactNode;
}

const TokenProvider: React.FC<TokenProviderProps> = ({ children }) => {
	const [jwtToken, setJWTToken] = useState<string | null>(null);

	const refreshJWTToken = async () => {		
		console.log("Refreshing token...", new Date());
		try {
			const username = 'skfn';
			const password = 'skfn';

			const basicAuth = `Basic ${btoa(`${username}:${password}`)}`;

			const response = await fetch(`${API_URL}login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: basicAuth,
				},
				body: JSON.stringify({ /* your refresh token data */ }),
			});

			if (response.ok) {
				const newToken: any = await response.json();
				setJWTToken(`Bearer ${newToken.access_token}`);
			} else {
				// Token refresh failed, retry after a short delay
				await retryRefreshToken();
			}
		} catch (error) {
			// Token refresh failed, retry after a short delay
			await retryRefreshToken();
		}
	};

	const retryRefreshToken = async () => {
		// Wait for 5 seconds (5000 ms) before retrying		
		console.log("Retrying token...", new Date());
		await new Promise((resolve) => setTimeout(resolve, 5000));
		await refreshJWTToken();
	};

	useEffect(() => {
		const startTokenRefresh = async () => {
			await refreshJWTToken();
			setInterval(refreshJWTToken, 180000); // Refresh token every 30 minutes
		};
		startTokenRefresh();
	}, []);

	return (
		<TokenContext.Provider value={{ jwtToken, refreshJWTToken }}>
			{children}
		</TokenContext.Provider>
	);
};

export { TokenProvider, TokenContext };