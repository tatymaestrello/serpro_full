// Below Function Executes On Form Submit
function customerValidation() {
    // Storing Field Values In Variables
    var name = document.getElementById("name").value;
    var fileName = document.getElementById("file").value;
    // Conditions
    if (name === '' && fileName === '') {
    alert("Ao menos um dos campos: Nome do Cliente ou Inserção em Lote devem estar preenchidos");
    return false;
    } 
    if (name != '' && fileName != '') {
        alert("Ao escolher Inserção em Lote, a inserção indivual fica desabilitada, favor inserir o cliente no arquivo e tentar novamente");
        return false;
        } 
    else {
    return true;
    }
    }