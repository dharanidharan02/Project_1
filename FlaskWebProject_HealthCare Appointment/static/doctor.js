$(document).ready(function() {

    // Function to register a new doctor
    function registerDoctor(doctorName, category) {
        $.ajax({
            url: '/register_doctor',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ doctorName: doctorName, category: category }),
            success: function(response) {
                 location.reload()
                alert(response.message);
                fetchDoctors(); // Refresh the doctor list after registration
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred while registering the doctor. Please try again.');
            }
        });
    }

    // Function to delete a doctor
    function deleteDoctor(doctorId) {
        $.ajax({
            url: '/delete_doctor',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ doctorId: doctorId }),
            success: function(response) {
                alert(response.message);
                 location.reload()
                fetchDoctors(); // Refresh the doctor list after deletion
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred while deleting the doctor. Please try again.');
            }
        });
    }

    // Function to edit doctor details
    function editDoctor(doctorId, newName, newCategory) {
        // AJAX request to update doctor details
        $.ajax({
            url: '/edit_doctor',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ doctorId: doctorId, newName: newName, newCategory: newCategory }),
            success: function(response) {
                alert(response.message);
                location.reload()
                fetchDoctors(); // Refresh the doctor list after editing
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred while updating the doctor details. Please try again.');
            }
        });
    }

    // Function to fetch doctors
    function fetchDoctors() {
        $.get('/api/doctors', function(data) {
            var doctorList = $('#doctorList');
            doctorList.empty();
            $.each(data, function(index, doctor) {
                doctorList.append('<tr>' +
                    '<td class="doctor-name">' + doctor.doctorName + '</td>' +
                    '<td>' +
                    '<input type="checkbox" name="doctorIds" value="' + doctor.doctorId + '"' + (doctor.availabilityStatus ? ' checked' : '') + '>' +
                    '</td>' +
                    '<td class="category">' + doctor.category + '</td>' +
                    '<td>' +
                    '<button class="edit-button btn btn-primary" data-doctor-id="' + doctor.doctorId + '">Edit</button>' +
                    '<button class="delete-button btn btn-danger" data-doctor-id="' + doctor.doctorId + '">Delete</button>' +
                    '</td>' +
                    '</tr>');
            });
        }).fail(function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred while fetching doctors. Please try again.');
        });
    }
 // Function to fetch and display appointment slots
    function fetchAppointmentSlots(doctorId) {
        $.get('/get_appointment_slots?doctorId=' + doctorId, function(data) {
            var appointmentSlotsContainer = $('#appointmentSlots');
            appointmentSlotsContainer.empty();

            // Iterate through the fetched slots and append them to the container
            $.each(data.appointmentSlots, function(index, slot) {
                var checkboxId = 'slotCheckbox_' + slot.slotId;
                var slotHtml = '<div>';
                slotHtml += '<input type="checkbox" class="slot-checkbox" id="' + checkboxId + '" value="' + slot.slotId + '">';
                slotHtml += '<label for="' + checkboxId + '">' + slot.appointmentSlots + '</label>';
                slotHtml += '</div>';
                appointmentSlotsContainer.append(slotHtml);
            });
        }).fail(function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred while fetching appointment slots. Please try again.');
        });
    }

    // Click event handler for the save button
   // Click event handler for the save button
    // Click event handler for the save button
    // Click event handler for the save button
// Click event handler for the save button
   // Click event handler for the save button










    // Event listener for registering a new doctor
    $('#registerDoctorForm').submit(function(event) {
        event.preventDefault();
        var doctorName = $('#doctorName').val();
        var category = $('#category').val();
        registerDoctor(doctorName, category);
    });

    // Event listener for deleting a doctor
    $(document).on('click', '.delete-button', function() {
        var doctorId = $(this).data('doctor-id');
        deleteDoctor(doctorId);
    });

    // Event listener for editing a doctor
    $(document).on('click', '.edit-button', function() {
        var doctorId = $(this).data('doctor-id');
        var editBox = $(this).closest('tr').find('.edit-box');
        editBox.toggle(); // Toggle the visibility of the edit box
    });

    // Event listener for saving edited doctor details
    $(document).on('click', '.confirm-edit', function() {
        var doctorId = $(this).data('doctor-id');
        var newName = $(this).siblings('.edit-name').val();
        var newCategory = $(this).siblings('.edit-category').val();
        editDoctor(doctorId, newName, newCategory);
    });

    $(document).on('click', '.edit-button', function() {
        var editBox = $(this).closest('tr').next('.edit-box');
        editBox.toggle(); // Show/hide the edit box
    });

    // Event listener for displaying appointment slots
    $(document).on('click', '.slot-button', function() {
        var doctorId = $(this).data('doctor-id');
        fetchAppointmentSlots(doctorId);

        $('#saveSlotsButton').click(function() {
        //var doctorId = $('#appointmentSlotsContainer').attr('data-doctor-id', doctorId);

        // Collect selected slot IDs
        var selectedSlots = [];
        $('.slot-checkbox:checked').each(function() {
            var slotId = $(this).val();
            selectedSlots.push(slotId);
        });

        // Send AJAX request to save selected slots for the doctor
        $.ajax({
            url: '/save_appointment_slots',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ doctorId: doctorId, selectedSlots: selectedSlots }),
            success: function(response) {
                alert(response.message);
                // Optionally, you can perform any additional actions here after the database is updated
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                //alert('An error occurred while saving appointment slots. Please try again.');
            }
        });
    });
    });



    // Fetch doctors initially when the page loads
    fetchDoctors();
});