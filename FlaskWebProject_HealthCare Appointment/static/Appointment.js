// Function to fetch and display user's booked appointments
$(document).ready(function() {
    // Functionality for back button
    $("#backButton").click(function() {
        window.history.back();
    });
});

function fetchUserAppointments() {
    fetch('/api/user_appointments')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user appointments');
            }
            return response.json();
        })
        .then(appointments => {
            const appointmentsContainer = document.getElementById('userAppointmentsContainer');
            appointmentsContainer.innerHTML = '';

            appointments.forEach(appointment => {
                const appointmentElement = document.createElement('div');
                appointmentElement.textContent = `Appointment ID: ${appointment.id}, Time: ${appointment.time}`; // Adjust based on your appointment data structure
                appointmentsContainer.appendChild(appointmentElement);
            });
        })
        .catch(error => {
            console.error('Error fetching user appointments:', error.message);
        });
}

// Call fetchUserAppointments when the page loads or when needed
fetchUserAppointments();

$(document).ready(function() {
    $('#searchButton').click(function() {
        // Get the search input value
        var searchValue = $('#searchInput').val().trim();

        // Perform the search
        searchAppointments(searchValue);
    });
});

function searchAppointments(searchValue) {
    // Send an AJAX request to search for appointments
    $.ajax({
        url: '/search_appointments',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ searchValue: searchValue }),
        success: function(data) {
            // Update the appointments table with the search results
            updateAppointmentsTable(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error searching appointments:', textStatus);
        }
    });
}

function updateAppointmentsTable(appointments) {
    // Clear the existing table
    $('#appointmentTable tbody').empty();

    // Populate the table with the search results
    appointments.forEach(function(appointment) {
        var row = '<tr>';
        row += '<td>' + appointment.id + '</td>';
        row += '<td>' + appointment.time + '</td>';
        row += '<td>' + appointment.doctor_name + '</td>';  // Add doctor name
        row += '<td>' + appointment.category + '</td>';     // Add category
        row += '<td>' + appointment.hospital_name + '</td>'; // Add hospital name
        row += '</tr>';

        $('#appointmentTable tbody').append(row);
    });
}
