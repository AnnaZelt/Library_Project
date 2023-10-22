const MY_SERVER = 'http://127.0.0.1:5000';

const getCustomers = async () => {
    try {
        const response = await axios.get(MY_SERVER + '/customers');
        const customers = response.data;
        const tableBody = document.getElementById('customer-table-body');

        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.email}</td>
                <td>
                    <button class="btn btn-danger delete_customer" data-id="${customer.id}">Delete</button>
                    <button class="btn btn-info update_customer" data-id="${customer.id}">Update</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
    }
};

document.getElementById('customer-table-body').addEventListener('click', async (event) => {
    if (event.target.classList.contains('delete_customer')) {
        // Handle Delete action
        const customerId = event.target.getAttribute('data-id');
        
        try {
            // Send a DELETE request to delete the customer
            const response = await axios.delete(`${MY_SERVER}/customers/delete/${customerId}`, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            // Handle the server response for deletion
            console.log('Customer deleted:', response.data);

            // You can update the customer table after deletion if needed
        } catch (error) {
            console.error('Error deleting customer:', error);
        }
    } else  if (event.target.classList.contains('update_customer')) {
        // Get the row of the clicked "Update" button
        const row = event.target.parentElement.parentElement;

        // Check if the update form is already present in the row
        if (!row.querySelector('.update-form')) {
            // Create the update form
            const updateForm = document.createElement('div');
            updateForm.className = 'update-form';

            // Create input fields for name and email
            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.placeholder = 'New Name';

            const emailInput = document.createElement('input');
            emailInput.type = 'text';
            emailInput.placeholder = 'New Email';

            // Create a button to submit the update
            const updateButton = document.createElement('button');
            updateButton.textContent = 'Submit';
            updateButton.addEventListener('click', async () => {
                // Get the new name and email values
                const newName = nameInput.value;
                const newEmail = emailInput.value;

                // Check if both name and email are provided
                if (newName && newEmail) {
                    // Use the `customerId` to identify the customer to update
                    const customerId = event.target.getAttribute('data-id');
                    const customerData = {
                        id: customerId,
                        name: newName,
                        email: newEmail,
                    };

                    try {
                        // Send a PUT request to update the customer
                        const response = await axios.put(`${MY_SERVER}/customers/update/${customerId}`, customerData, {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });

                        // Handle the server response for updating
                        console.log('Customer updated:', response.data);

                        // You can update the customer table after updating if needed

                        // Remove the update form from the row
                        row.removeChild(updateForm);
                    } catch (error) {
                        console.error('Error updating customer:', error);
                    }
                }
            });

            // Append input fields and update button to the form
            updateForm.appendChild(nameInput);
            updateForm.appendChild(emailInput);
            updateForm.appendChild(updateButton);

            // Insert the update form into the row
            row.appendChild(updateForm);
        }
    }
});

document.getElementById('add_customer_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    const customerData = {
        name: name,
        email: email
    };

    try {
        const response = await axios.post(MY_SERVER + '/customers/add', customerData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Handle the server response, e.g., display a success message
        console.log('Customer added:', response.data);

        // You can also update the customer table with the newly added customer here
    } catch (error) {
        console.error('Error adding customer:', error);
    }
});

getCustomers();