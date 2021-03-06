const modalBtn = document.querySelectorAll('[data-modal]');
const body = document.body;
const modalClose = document.querySelectorAll('.modal-close');
const modal = document.querySelectorAll('.modal');
const chooseTypeBtn = document.querySelectorAll('.search-choose-type-block');
console.log('qqqqqqqq')

chooseTypeBtn.forEach(item => {
    item.addEventListener('click', event => {
        let $this = event.currentTarget;


        $this.classList.add('chosen-type');


    });
});


modalBtn.forEach(item => {
    item.addEventListener('click', event => {
        let $this = event.currentTarget;
        let modalId = $this.getAttribute('data-modal');
        let modal = document.getElementById(modalId);
        let modalContent = modal.querySelector('.modal-content');

        modalContent.addEventListener('click', event => {
            event.stopPropagation();
        });
        console.log('qqqqqqqq')

        modal.classList.add('show');
        body.classList.add('no-scroll');

        setTimeout(() => {
            modalContent.style.transform = 'none';
            modalContent.style.opacity = '1';
        }, 1);

    });
});


modalClose.forEach(item => {
    item.addEventListener('click', event => {
        let currentModal = event.currentTarget.closest('.modal');

        closeModal(currentModal);
    });
});


modal.forEach(item => {
    item.addEventListener('click', event => {
        let currentModal = event.currentTarget;

        closeModal(currentModal);
    });
});


function closeModal(currentModal) {
    let modalContent = currentModal.querySelector('.modal-content');
    modalContent.removeAttribute('style');

    setTimeout(() => {
        currentModal.classList.remove('show');
        body.classList.remove('no-scroll');
    }, 200);
}


