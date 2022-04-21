const mModal = document.querySelector('.modal-sobre')
const btSobre = document.querySelector('#bt-sobre')
const btCloseSobre = document.querySelector('#btClosedSobre')

function openSobre(){
    mModal.classList.add('active-modal')

    mModal.onclick = e => {
        if (e.target.className.indexOf('modal-sobre') !== -1) {
            mModal.classList.remove('active-modal')
        }
    }
}

btCloseSobre.onclick = e => {
    e.preventDefault()

    mModal.classList.remove('active-modal')
}
