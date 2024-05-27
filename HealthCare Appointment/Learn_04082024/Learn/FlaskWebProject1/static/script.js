// script.js
// script.js

$(document).ready(function() {
    // Functionality for back button
    $("#backButton").click(function() {
        window.history.back();
    });
});

// Function to fetch doctors with associated hospitals based on category
function fetchDoctorsWithHospitals() {
    const category = document.getElementById('category').value;

    fetch(`/api/doctors_with_hospitals?category=${category}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        return response.json();
    })
    .then(data => {
        // Process the data received from the server
        console.log(data);
        updateUI(data);
        displayDoctors(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error.message);
    });
}

function displayDoctors(data) {
    //const doctorList = document.getElementById('doctorList');
    //doctorList.innerHTML = ''; // Clear previous results

    data.forEach(doctor => {
        const li = document.createElement('li');
        li.textContent = doctor.doctorName;

        // Create button to book slot
        const bookButton = document.createElement('button');
        bookButton.textContent = 'Book Slot';
        bookButton.setAttribute('data-doctor-id', doctor.doctorId); // Set doctor ID as data attribute
        bookButton.addEventListener('click', AvailableSlots); // Attach event listener to the button

        li.appendChild(bookButton);
        doctorList.appendChild(li);
    });
}

function AvailableSlots(event) {
    const doctorId = event.target.getAttribute('data-doctor-id');
    console.log('Doctor ID:', doctorId);
    fetchAvailableAppointments(doctorId);
    // Your logic to book a slot for the given doctor
    // This could involve displaying a modal or redirecting to another page to book the slot
}

// Event listener for fetch button
document.getElementById('fetchData').addEventListener('click', fetchDoctorsWithHospitals);
// Function to update UI with received data
function updateUI(data) {
    const doctorList = document.getElementById('doctorList');
    const hospitalList = document.getElementById('hospitalList');


    // Clear previous results
    doctorList.innerHTML = '';
    hospitalList.innerHTML = '';

    // Update doctor and hospital lists
    data.forEach(item => {
//        const doctorItem = document.createElement('li');
//        doctorItem.textContent = item.doctorName;
//        doctorList.appendChild(doctorItem);

        const hospitalItem = document.createElement('li');
        hospitalItem.textContent = item.hospitalName;
        hospitalList.appendChild(hospitalItem);
    });
}
// Function to fetch available appointments for the selected doctor
function fetchAvailableAppointments(doctorId) {
    fetch(`/api/available_appointments?doctorId=${doctorId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch available appointments');
        }
        return response.json();
    })
    .then(data => {
        displayAvailableAppointments(data);
    })
    .catch(error => {
        console.error('Error fetching available appointments:', error.message);
    });
}

// Function to display available appointments
function displayAvailableAppointments(appointments) {
    const appointmentsContainer = document.getElementById('appointmentsContainer');
    appointmentsContainer.innerHTML = '';

    appointments.forEach(appointment => {
        const appointmentButton = document.createElement('button');
        appointmentButton.textContent = appointment.time;

        // Add class and disable button if the slot is booked
        if (appointment.booked) {
            appointmentButton.classList.add('booked-slot-button');
            appointmentButton.disabled = true; // Disable button for booked slot
        }

        appointmentButton.addEventListener('click', function() {
            // Call bookSlot function with appointmentId and time
            bookSlot(appointment.appointmentId, appointment.time);
        });

        appointmentsContainer.appendChild(appointmentButton);
    });
}


//function bookAppointment(appointmentId) {
//    // Logic to book the appointment goes here
//    console.log('Booking appointment with ID:', appointmentId);
//
//    // Change button class to "booked-slot-button" and disable it
//    const bookedButton = document.querySelector(`button[data-appointment-id="${appointmentId}"]`);
//    if (bookedButton) {
//        bookedButton.classList.add('booked-slot-button');
//        bookedButton.disabled = true;
//    }
//}

function bookSlot(appointmentId,time) {
    const bookedButton = document.querySelector(`button[data-appointment-id="${appointmentId}"]`);
    if (bookedButton && bookedButton.classList.contains('booked-slot-button')) {
        // Appointment is already booked, no need to send another booking request
        return;
    }

    fetch('/api/user')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user data');
            }
            return response.json();
        })
        .then(data1 => {
            const userId = data1.user_id;
            console.log(userId);
            console.log(appointmentId);
            return fetch('/book_appointment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ appointmentId, userId,time })
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to book appointment');
            }
            console.log('Appointment booked successfully');
            if (bookedButton) {
        bookedButton.classList.add('booked-slot-button');
        bookedButton.disabled = true;
  }
            // Display confirmation message
            $('#confirmationMessage').text('Appointment booked successfully');
            $('#confirmationModal').modal('show'); // Show confirmation modal
        })
        .catch(error => {
            console.error('Error booking appointment:', error.message);
            // Display error message
            $('#confirmationMessage').text('Failed to book appointment');
            $('#confirmationModal').modal('show'); // Show confirmation modal
        });
}
