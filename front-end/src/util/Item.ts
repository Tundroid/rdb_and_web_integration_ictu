export class Item {
	constructor(
		public id: number,
		public item: string,
		public prevAmount: number = 0,
		public amount: number = 0,
		public quantity: number = 1
	) { }

	static getTotal(item: Item): number {
		return item.quantity * item.amount;
	}

	static getUniqueId = (item: Item) => {
		return `${item.id}-${item.amount}`;
	};
}