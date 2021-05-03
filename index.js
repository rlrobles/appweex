

console.log(`Convertidor`)


//const currency_one = currencyElement_one.value;
const currency_one = 'PEN'; //USD PEN
const amountElement_one = 200;
//const currency_two = currencyElement_two.value;
const currency_two = 'USD'; //PEN USD
let amountElement_two = 0;

let data = {
    rates: {
        USD: {
            compra: 1,
            venta: 1
        },
        PEN: {
            compra: 3.428,
            venta: 3.442
        }
    }
}

const rate = data.rates[currency_two];

console.log(rate);

//convertResult = 
//rateElement.innerText = `1 ${currency_one} = ${rate} ${currency_two}`;

amountElement_two = amountElement_one * rate.venta;
amountFixed = amountElement_two.toFixed(3);
console.log(`ConvertResult: ${amountElement_two}`);


