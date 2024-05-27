// Function to handle form submission for adding a new reminder
document.getElementById('reminderForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the reminder input value
    const reminder = document.getElementById('reminder').value.trim();

    // Validate reminder input
    if (reminder === '') {
        alert('Please enter a reminder.');
        return;
    }

    // Add the reminder to the table
    addReminder(reminder);

    // Clear the input field
    document.getElementById('reminder').value = '';
});

// Function to handle form submission for sending a new message
document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the message input value
    const message = document.getElementById('message').value.trim();

    // Validate message input
    if (message === '') {
        alert('Please enter a message.');
        return;
    }

    // Send the message
    sendMessage(message);

    // Clear the input field
    document.getElementById('message').value = '';
});

// Function to add a reminder to the table
function addReminder(reminder) {
    const table = document.getElementById('reminderTable');
    const row = table.insertRow();
    const cell = row.insertCell();
    cell.textContent = reminder;
}

// Function to send a message
function sendMessage(message) {
    // Simulate sending message (replace with actual logic)
    alert('Message sent: ' + message);
}
