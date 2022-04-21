const modal = document.querySelector('.modal-container')
const tbody = document.querySelector('tbody')
const sNome = document.querySelector('#m-desc')
const sValor = document.querySelector('#m-valor')
const btnSalvar = document.querySelector('#btnSalvar')

var save = true;
var ID = ''

function openModal(edit = false, desc, valor) {
    modal.classList.add('active')
  
    modal.onclick = e => {
      if (e.target.className.indexOf('modal-container') !== -1) {
        modal.classList.remove('active')
      }
    }
  
    if (edit) {
      sNome.value = desc
      sValor.value = valor
      save = false
    } else {
      sNome.value = ''
      sValor.value = ''
      save = true
    }
    
}

function saveAction(){
    document.myform.action = `${window.saveURL}`;
    document.myform.submit();
}


function updateAction(){
  document.myform.action = 'update/'+ID;
  document.myform.submit();
}

function deleteAction(i){
    ID = i['index']
    document.formDelete.action = 'delete/'+ID;
    document.formDelete.submit();
}

function editItem(id, desc, valor) {
    ID = id
    openModal(true, desc, valor)
}

btnSalvar.onclick = e => {
  
  if (sNome.value == '' || sValor.value == '') {
    return
  }

  e.preventDefault();

  if(save){
      saveAction()
  }
  else{
      updateAction()
  }

  modal.classList.remove('active')
}