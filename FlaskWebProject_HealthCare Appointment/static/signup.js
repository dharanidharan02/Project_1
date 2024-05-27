document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm'); // Corrected form ID
    const messageContainer = document.getElementById('message-container');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(signupForm);
        const xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    messageContainer.innerHTML = '<p class="success-message">' + response.message + '</p>';
                    // Redirect to login page after successful signup
                    window.location.href = '/login';
                } else {
                    messageContainer.innerHTML = '<p class="error-message">Error: ' + xhr.statusText + '</p>';
                }
            }
        };

        xhr.open('POST', '/signup', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(formData);
    });
});
