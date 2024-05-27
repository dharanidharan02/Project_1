// account.js

function editEmail() {
    var emailEditBox = document.getElementById("email-edit-box");
    if (emailEditBox.style.display === "none") {
        emailEditBox.style.display = "block";
    } else {
        emailEditBox.style.display = "none";
    }
}
 function goBack() {
        window.history.back();
    }

function updateEmail() {
    var newEmail = document.getElementById("new-email").value;

    // Make an AJAX request to the backend to update the email address
    fetch('/update-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: newEmail })
    })
    .then(response => {
        if (response.ok) {
            // Email updated successfully
            document.getElementById("email").innerText = newEmail; // Update email field
            alert('Email updated successfully!');
            reloadPage();
        } else {
            // Email update failed, handle the error response
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to update email');
            });
        }
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error updating email:', error.message);
        alert('Failed to update email. Please try again later.');
    });
}

function toggleEmailEditBox() {
    var emailEditBox = document.getElementById("email-edit-box");
    if (emailEditBox.style.display === "none") {
        emailEditBox.style.display = "block";
    } else {
        emailEditBox.style.display = "none";
    }
}

function uploadProfilePic() {
    var fileInput = document.getElementById('profile-picture-input');
    var profilePicture = fileInput.files[0];

    if (!profilePicture) {
        alert('Please select a file.');
        return;
    }

    var formData = new FormData();
    formData.append('profile_picture', profilePicture);

    fetch('/upload_profile_picture', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to upload profile picture.');
        }
    })
    .then(data => {
        if (data && data.profile_picture_url) {
            var profilePictureElement = document.querySelector('.profile-picture img');
            profilePictureElement.src = data.profile_picture_url;
            profilePictureElement.alt = 'Profile Picture';
            profilePictureElement.style.display = 'block';
            alert('Profile picture uploaded successfully!');
            reloadPage();
        } else {
            throw new Error('Profile picture URL not found in response.');
        }
    })
    .catch(error => {
        console.error('Error uploading profile picture:', error.message);
        alert('Failed to upload profile picture. Please try again later.');
    });
}
