export class Util {

	static getLongNumber(): string {
		return new Date().toISOString().replace(/[-:.TZ]/g, '');
	}

	static getInvoiceNumber(): string {
		return `I${Util.getLongNumber()}`;
	}

}