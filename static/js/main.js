
$(document).ready(function () {

    var valueTipDoc;
    var valuePersPol;
    var valueTipPers;

    var slcTipDoc = $('#TipoDocumento');
    var slcPersPol = $('#PersonaPolitica');
    var slcTipPers = $('#TipoPersona');

    slcTipDoc.on('change', function () {
        valueTipDoc = slcTipDoc.find(":selected").val();

        //Validación para los tipos de documento
        if(valueTipDoc == "2"){
            document.getElementById("imagenFotoDocFrontal").disabled = true;
            document.getElementById("imagenFotoDocPosterior").disabled = true;
        }else if(valueTipDoc == "3"){
            document.getElementById("imagenFotoDocFrontal").disabled = false;
            document.getElementById("imagenFotoDocPosterior").disabled = true;
        }else if(valueTipDoc == "1"){
            document.getElementById("imagenFotoDocFrontal").disabled = false;
            document.getElementById("imagenFotoDocPosterior").disabled = false;
        }

    });

    slcPersPol.on('change', function () {
        valuePersPol = slcPersPol.find(":selected").val();
    });

    slcTipPers.on('change', function () {
        valueTipPers = slcTipPers.find(":selected").val();
    });

    const btnSave = document.querySelectorAll('.btn-save-client');
    //var tipDocUser =  tipDoc.options[tipDoc.selectedIndex].value;

  
    //#### Validación de campos de registro de cliente (tipo de documento, de persona y persona política) ############
    if (btnSave) {
        const btnArray = Array.from(btnSave);
        btnArray.forEach((btn) => {
            btn.addEventListener('click', (e) => {

                var inputNombre = $('#Nombre').val();
                var inputApellidoPaterno = $('#ApellidoPaterno').val();
                var inputApellidoMaterno = $('#ApellidoMaterno').val();
                var inputCorreo = $('#CorreoElectronico').val();
                var inputPassword = $('#Password').val();
                var inputNumeroDoc = $('#NumeroDocumento').val();

                if (inputNombre == "" || inputApellidoPaterno == "" || inputApellidoMaterno == "" || inputCorreo == "" || 
                    inputPassword == "" || inputNumeroDoc == "" ||
                    valueTipDoc == null || valuePersPol == null || valueTipPers == null) {
                    if(inputNombre == ""){
                        alert('Se requiere completar el campo de Nombre');
                    }

                    if(inputApellidoPaterno == "" ){
                        alert('Se requiere completar el campo del Apellido Paterno');
                    }

                    if(inputApellidoMaterno == ""){
                        alert('Se requiere completar el campo del Apellido Materno');
                    }

                    if(inputCorreo == ""){
                        alert('Se requiere completar el campo del correo');
                    }

                    if(inputPassword == ""){
                        alert('Se requiere completar el campo del Password');
                    }

                    if (valueTipDoc == null) {
                        alert('Se requiere completar el campo de Tipo de Documento');
                    }

                    if(inputNumeroDoc == ""){
                        alert('Se requiere completar el campo del número de documento');
                    }

                    if (valuePersPol == null) {
                        alert('Se requiere completar el campo de Persona Política');
                    }

                    if (valueTipPers == null) {
                        alert('Se requiere completar el campo de Tipo de Persona');
                    }
                    e.preventDefault(); //detiene el proceso
                }
            });
        });
    }

    //################################################################
    //##### Script to prevent pasting into input fields ##############
    const pasteBoxEnviar = document.getElementById("montoEnviar");
    pasteBoxEnviar.onpaste = e => {
        e.preventDefault();
        return false;
    };

    const pasteBoxRecibir = document.getElementById("montoRecibir");
    pasteBoxRecibir.onpaste = e => {
        e.preventDefault();
        return false;
    };

    //################################################################

});


function validate(evt) {
    var theEvent = evt || window.event;
  
    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
    // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }

  function precision(a) {
    if (!isFinite(a)) return 0;
    var e = 1, p = 0;
    while (Math.round(a * e) / e !== a) { e *= 10; p++; }
    return p;
  }

  function getLastWord(words) {
    var wordsF = words.trim();
    var n = wordsF.split(" ");
    return n[n.length - 1];

}

function calcSimulationRecibir(){

    var tcCompra = $('#tcCompra').val();
    var tcVenta = $('#tcVenta').val();

    var montoEnviar = $('#montoEnviar').val();
    var montoEnviarF = parseFloat(montoEnviar);

    var montoRecibir = $('#montoRecibir').val();
    var montoRecibirF = parseFloat(montoRecibir);

    var textCompra = document.querySelector(".data-tc-compra").textContent;
    var textVenta = document.querySelector(".data-tc-venta").textContent;

    var tcCompra = textCompra.slice(textCompra.length - 5, textCompra.length);
    var tcVenta = textVenta.slice(textVenta.length - 5, textVenta.length);

    var tcCompraF = parseFloat(tcCompra);
    var tcVentaF = parseFloat(tcVenta);

    //##### Identificar la moneda para simulación ###################################]

    var textPlaceHolderMtoEnviar =  document.getElementById("montoEnviar").placeholder;
    var textMonedaEnviar = getLastWord(textPlaceHolderMtoEnviar);

    if(textMonedaEnviar == "dólares"){
        var estado = 1;
    }

    if(textMonedaEnviar == "soles"){
        var estado = 2;
    }

    switch(estado){
        case 1:
            var resultado = tcCompraF * montoEnviarF;
            break;
        case 2:
            var resultado = montoEnviarF /  tcVentaF;
            break;
        default:
            console.log('default');    
    }

    //######################################################

    var cantDec = precision(resultado);

    if(cantDec >= 3){
        resultadoF = resultado.toFixed(2);
    }else{
        resultadoF = resultado;
    }

    if (isNaN(resultadoF)) {
        document.getElementById("montoRecibir").value = 0;
    }else{
        document.getElementById("montoRecibir").value = resultadoF;
    }
}

function calcSimulationEnviar(){

    var montoEnviar = $('#montoEnviar').val();
    var montoEnviarF = parseFloat(montoEnviar);

    var montoRecibir = $('#montoRecibir').val();
    var montoRecibirF = parseFloat(montoRecibir);

    var textCompra = document.querySelector(".data-tc-compra").textContent;
    var textVenta = document.querySelector(".data-tc-venta").textContent;

    var tcCompra = textCompra.slice(textCompra.length - 5, textCompra.length);
    var tcVenta = textVenta.slice(textVenta.length - 5, textVenta.length);

    var tcCompraF = parseFloat(tcCompra);
    var tcVentaF = parseFloat(tcVenta);

    //##### Identificar la moneda para simulación ###################################]

    var textPlaceHolderMtoEnviar =  document.getElementById("montoEnviar").placeholder;
    var textMonedaEnviar = getLastWord(textPlaceHolderMtoEnviar);

    if(textMonedaEnviar == "dólares"){
        var estado = 1;
    }

    if(textMonedaEnviar == "soles"){
        var estado = 2;
    }

    switch(estado){
        case 1:
            var resultado = montoRecibirF / tcCompraF;
            break;
        case 2:
            var resultado = montoRecibirF *  tcVentaF;
            break;
        default:
            console.log('default');    
    }


    //var resultado = montoRecibirF / tcCompraF;

    var cantDec = precision(resultado);

    if(cantDec >= 3){
        resultadoF = resultado.toFixed(2);
    }else{
        resultadoF = resultado;
    }

    if (isNaN(resultadoF)) {
        document.getElementById("montoEnviar").value = 0;
    }else{
        document.getElementById("montoEnviar").value = resultadoF;
    }
    
}


function changeCoinCurrency(){
   
    var textPlaceHolder =  document.getElementById("monedaCambio").placeholder;
    
    switch(textPlaceHolder){
        case 'Moneda: Dólares a Soles':
            document.getElementById("monedaCambio").placeholder = "Moneda: Soles a Dólares";
            document.getElementById("montoEnviar").placeholder = "Envías soles";
            document.getElementById("montoRecibir").placeholder = "Recibes dólares";
            break;
        case 'Moneda: Soles a Dólares':
            document.getElementById("monedaCambio").placeholder = "Moneda: Dólares a Soles";
            document.getElementById("montoEnviar").placeholder = "Envías dólares";
            document.getElementById("montoRecibir").placeholder = "Recibes soles";
            break;
        default:
            console.log('default');    
    }


    if (document.getElementById("montoEnviar").value != "" && document.getElementById("montoRecibir").value != ""){
        calcSimulationRecibir();
    }
    


}
/*
const btnSave = document.querySelectorAll('.btn-save')
var tipDoc = document.getElementsByName("TipoDocumento");
//var tipDocUser =  tipDoc.options[tipDoc.selectedIndex].value;
var option = getSelectedOption(tipDoc);

if(btnSave){
    const btnArray = Array.from(btnSave);
    btnArray.forEach((btn) => {
       btn.addEventListener('click', (e) => {
            alert(option);
        });
    });
}


function getSelectedOption(sel) {
    var opt;
    for ( var i = 0, len = sel.options.length; i < len; i++ ) {
        opt = sel.options[i];
        if ( opt.selected === true ) {
            break;
        }
    }
    return opt;
}


 */