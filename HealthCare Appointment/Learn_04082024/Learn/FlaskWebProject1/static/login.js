// Function to handle login form submission
function handleLogin(event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve form data
    const formData = new FormData(event.target);

    // Perform form validation
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
        alert('Please enter both username and password.');
        return;
    }

    // Perform authentication with the backend
    authenticateUser(username, password)
        .then(response => {
            if (response === 'success') {
                // Redirect to the dashboard or homepage
                window.location.href = '/dashboard.html';
            } else {
                alert('Incorrect username or password. Please try again.');
            }
        })
        .catch(error => {
            alert('An error occurred during login. Please try again later.');
            console.error(error);
        });
}

// Function to authenticate user with the backend
function authenticateUser(username, password) {
    // Replace this with the actual endpoint of your Flask login route
    const url = '/login';

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .catch(error => {
            console.error('Error:', error);
            throw new Error('An error occurred while communicating with the server');
        });
}

// Attach form submission event listener to login form
document.getElementById('loginForm').addEventListener('submit', handleLogin);
