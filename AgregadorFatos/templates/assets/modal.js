document.addEventListener('DOMContentLoaded', (event) => {
    const openModalBtn = document.getElementById('openModalBtn');
    const modal = document.getElementById('modal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modalBody = document.getElementById('modalBody');

    openModalBtn.addEventListener('click', () => {
        fetchContentIntoModal('/addSource/');
        modal.style.display = 'block';
    });

    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    function fetchContentIntoModal(url) {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                modalBody.innerHTML = data;
                attachFormSubmitHandler();
            })
            .catch(error => {
                modalBody.innerHTML = '<p>Failed to load content.</p>';
                console.error('Error fetching content:', error);
            });
    }

    function attachFormSubmitHandler() {
        const form = modalBody.querySelector('formOption3'); // ID of Source Add Form
        if (form) {
            form.onsubmit = (event) => {
                event.preventDefault(); // Prevent the default form submission
                const formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken') // Ensure you include the CSRF token
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        modal.style.display = 'none';
                    } else {
                        alert('There was an error with your submission.');
                    }
                })
                .catch(error => console.error('Error:', error));
            };
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
