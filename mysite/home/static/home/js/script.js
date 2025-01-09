// script.js

const modal = document.getElementById('transactionModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeBtn = document.querySelector('.close-btn');

// Открытие модального окна
openModalBtn.addEventListener('click', (event) => {
    event.preventDefault();  // Чтобы не происходил переход по ссылке
    modal.style.display = 'block';
});

// Закрытие модального окна
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Закрытие при клике вне окна
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
