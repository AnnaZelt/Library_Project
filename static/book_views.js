const MY_SERVER = 'http://127.0.0.1:5000';

const getBooks = async () => {
    try {
        const response = await axios.get(MY_SERVER + '/books');
        const books = response.data;
        const tableBody = document.getElementById('book-table-body');

        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book['available copies']}</td>
                <td data-loan-start-date="2023-10-12T12:00:00" data-due-date="2023-10-15T12:00:00" class="update-timer"></td>
                <td>
                    <button class="btn btn-danger delete_book" data-id="${book.id}">Delete</button>
                    <button class="btn btn-info update_book" data-id="${book.id}">Update</button>
                </td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error(error);
        }
    };
    
document.getElementById('book-table-body').addEventListener('click', async (event) => {
    if (event.target.classList.contains('delete_book')) {
        // Handle Delete action
        const bookId = event.target.getAttribute('data-id');
        
        try {
            // Send a DELETE request to delete the book
            const response = await axios.delete(`${MY_SERVER}/books/delete/${bookId}`, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            // Handle the server response for book deletion
            console.log('Book deleted:', response.data);

            // You can update the book table after deletion if needed
            // For example, remove the corresponding row from the table
            const row = event.target.parentElement.parentElement;
            row.remove();
        } catch (error) {
            console.error('Error deleting book:', error);
        }
    } else if (event.target.classList.contains('update_book')) {
        // Get the row of the clicked "Update" button
        const row = event.target.parentElement.parentElement;

        // Check if the update form is already present in the row
        if (!row.querySelector('.update-form')) {
            // Create the update form
            const updateForm = document.createElement('div');
            updateForm.className = 'update-form';

            // Create input fields for title, author, and copies_available
            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.placeholder = 'New Title';

            const authorInput = document.createElement('input');
            authorInput.type = 'text';
            authorInput.placeholder = 'New Author';

            const copiesAvailableInput = document.createElement('input');
            copiesAvailableInput.type = 'number';
            copiesAvailableInput.placeholder = 'New Available Copies';

            const durtionTypeInput = document.createElement('input');
            durtionTypeInput.type = 'number';
            durtionTypeInput.placeholder = 'New Duration Type';

            // Create a button to submit the update
            const updateButton = document.createElement('button');
            updateButton.textContent = 'Submit';
            updateButton.addEventListener('click', async () => {
                // Get the new values
                const newTitle = titleInput.value;
                const newAuthor = authorInput.value;
                const newCopiesAvailable = copiesAvailableInput.value;
                const newdurtionType = durtionTypeInput.value

                // Check if all fields are provided
                if (newTitle && newAuthor && newCopiesAvailable &&newdurtionType !== '') {
                    // Use the `bookId` to identify the book to update
                    const bookId = event.target.getAttribute('data-id');
                    const bookData = {
                        title: newTitle,
                        author: newAuthor,
                        copies_available: newCopiesAvailable,
                        loan_duration_type: newdurtionType
                    };

                    try {
                        // Send a PUT request to update the book
                        const response = await axios.put(`${MY_SERVER}/books/update/${bookId}`, bookData, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });

                        // Handle the server response for updating
                        console.log('Book updated:', response.data);

                        // You can update the book table after updating if needed

                        // Remove the update form from the row
                        row.removeChild(updateForm);
                    } catch (error) {
                        console.error('Error updating book:', error);
                    }
                }
            });

            // Append input fields and update button to the form
            updateForm.appendChild(titleInput);
            updateForm.appendChild(authorInput);
            updateForm.appendChild(copiesAvailableInput);
            updateForm.appendChild(durtionTypeInput);
            updateForm.appendChild(updateButton);

            // Insert the update form into the row
            row.appendChild(updateForm);
        }
    }
});

document.getElementById('add_book_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const copies_available = document.getElementById('copies_available').value;
    const loan_duration_type =document.getElementById('loan_duration_type').value

    const bookData = {
        title: title,
        author: author,
        copies_available: copies_available,
        loan_duration_type: loan_duration_type
    };

    try {
        const response = await axios.post(MY_SERVER + '/books/add', bookData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Handle the server response, e.g., display a success message
        console.log('Book added:', response.data);

        // You can also update the customer table with the newly added customer here
    } catch (error) {
        console.error('Error adding book:', error);
    }
});

// Function to update countdown timer
function updateCountdownTimer(loanStartDate, dueDate) {
    const now = new Date();
    const timeRemaining = dueDate - now;

    if (timeRemaining <= 0) {
        // If the due date has passed, display an appropriate message
        return "Overdue.";
    }

    const daysRemaining = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    const hoursRemaining = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutesRemaining = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));

    return `${daysRemaining}d ${hoursRemaining}h ${minutesRemaining}m`;
}

// Get all elements with the 'update-timer' class and update their countdown timers
document.querySelectorAll('.update-timer').forEach(timerElement => {
    const loanStartDate = new Date(timerElement.getAttribute('data-loan-start-date'));
    const dueDate = new Date(timerElement.getAttribute('data-due-date'));
    timerElement.textContent = updateCountdownTimer(loanStartDate, dueDate);
    setInterval(() => {
        timerElement.textContent = updateCountdownTimer(loanStartDate, dueDate);
    }, 60000); // Update every minute (adjust as needed)
});

getBooks();
