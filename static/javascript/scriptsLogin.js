const mModal = document.querySelector('.modal-sobre')
const btSobre = document.querySelector('#bt-sobre')


function openSobre(){
    mModal.classList.add('active-modal')

    mModal.onclick = e => {
        if (e.target.className.indexOf('modal-sobre') !== -1) {
            mModal.classList.remove('active-modal')
        }
    }
}
