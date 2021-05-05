<div class="container">
<script src="https://weex.ciaceperu.com/function.js"></script>
<div class="currency">
    
<input type="number" id="amount-one" placeholder="0" value="100" />
  <select id="currency-one">
        <option value="PEN">SOLES</option>
        <option value="USD" selected>DÓLARES</option>

    </select>

</div>

<div class="swap-rate-container">
   
  <button class="btn" id="swap">
        <img draggable="false" role="img" class="emoji" alt="↕️" src="https://cdn.kambista.com/svg/change.svg">️
    </button>
    
</div>

<div class="currency">
<input type="number" id="amount-two" placeholder="0" />
    <select id="currency-two">
        <option value="PEN" selected>SOLES</option>
        <option value="USD">DÓLARES</option>

    </select>
    
    

</div>
<div class="rate" id="rate"></div> 
</div>


<script>
const currencyElement_one = document.getElementById("currency-one");
const amountElement_one = document.getElementById("amount-one");
const currencyElement_two = document.getElementById("currency-two");
const amountElement_two = document.getElementById("amount-two");
const rateElement = document.getElementById("rate");
const swap = document.getElementById("swap");


currencyElement_one
PEN
USD

currencyElement_two
PEN
USD


https://api.exchangerate-api.com/v4/latest/USD

// Calculate Exchance Rate & Update DOM
function calcuate() {
const currency_one = currencyElement_one.value;
const currency_two = currencyElement_two.value;

fetch(`http://demo.weex.pe/weex/tasa-cambio/v1`)
.then((res) => res.json())
.then((data) => {
const rate = data.rates[currency_two];
rateElement.innerText = `1 ${currency_one} = ${rate} ${currency_two}`;
amountElement_two.value = (amountElement_one.value * rate).toFixed(3);
});
}

// Event Listeners
currencyElement_one.addEventListener("change", calcuate);
amountElement_one.addEventListener("input", calcuate);
currencyElement_two.addEventListener("change", calcuate);
amountElement_two.addEventListener("input", calcuate);

swap.addEventListener("click", function () {
const temp = currencyElement_one.value;
currencyElement_one.value = currencyElement_two.value;
currencyElement_two.value = temp;
calcuate();
});

calcuate();
</script>
