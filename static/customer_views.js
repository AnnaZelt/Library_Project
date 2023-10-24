const MY_SERVER = 'http://127.0.0.1:5000';
let customersData = [];
// Function to get customers
async function getCustomers() {
    try {
        const response = await axios.get(MY_SERVER + '/customers');
        const customers = response.data;
        updateCustomerTable(customersData);
        const tableBody = document.getElementById('customer-table-body');
        tableBody.innerHTML = ''; // Clear the table body

        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.email}</td>
                <td>
                    <button class="btn btn-danger delete-customer" data-id="${customer.id}">Delete</button>
                    <button class="btn btn-info update-customer" data-id="${customer.id}">Update</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        // Handle the error and provide user feedback
    }
}

// Function to filter customers by name
function filterCustomersByName(customers, searchTerm) {
    return customers.filter(customer => customer.name.toLowerCase().includes(searchTerm.toLowerCase()));
}

// Function to update the customer table with filtered data
function updateCustomerTable(customers) {
    const tableBody = document.getElementById('customer-table-body');
    tableBody.innerHTML = ''; // Clear the table body

    customers.forEach(customer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${customer.id}</td>
            <td>${customer.name}</td>
            <td>${customer.email}</td>
            <td>
                <button class="btn btn-danger delete-customer" data-id="${customer.id}">Delete</button>
                <button class="btn btn-info update-customer" data-id="${customer.id}">Update</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Event listener for the search input
document.getElementById('customer-search-input').addEventListener('input', handleSearchInput);

function handleSearchInput() {
    const searchInput = document.getElementById('customer-search-input');
    const searchTerm = searchInput.value.trim();
    const filteredCustomers = filterCustomersByName(customersData, searchTerm);
    updateCustomerTable(filteredCustomers); // Update the table with filtered results
}

async function init() {
    try {
        const response = await axios.get(MY_SERVER + '/customers');
        customersData = response.data; // Populate customersData with initial data
        updateCustomerTable(customersData);
    } catch (error) {
        console.error(error);
        // Handle the error and provide user feedback
    }
}

init();

async function addCustomer(name, email) {
    try {
        const customerData = {
            name: name,
            email: email
        };

        const response = await axios.post('/customers/add', customerData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Customer added successfully') {
            alert('Customer added successfully');
        } else if (response.data.message === 'Customer with this email already exists') {
            alert('Customer with this email already exists');
        }
    } catch (error) {
        console.error('Error adding customer:', error);
    }
}


// Function to delete a customer
async function deleteCustomer(customerId) {
    try {
        const response = await axios.delete(`${MY_SERVER}/customers/delete/${customerId}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        console.log('Customer deleted:', response.data);
        getCustomers(); // Refresh the customer list
    } catch (error) {
        console.error('Error deleting customer:', error);
        // Handle the error and provide user feedback
    }
}

// Function to update a customer
async function updateCustomer(customerId, newName, newEmail) {
    const customerData = {
        id: customerId,
        name: newName,
        email: newEmail,
    };

    try {
        const response = await axios.put(`${MY_SERVER}/customers/update/${customerId}`, customerData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Customer updated successfully') {
            alert('Customer updated successfully');
            getCustomers(); // Refresh the customer list
        } else {
            alert('Error updating customer: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error updating customer:', error);
    }
}

// Event delegation to handle various customer actions
document.getElementById('customer-table-body').addEventListener('click', (event) => {
    const target = event.target;
    const customerId = target.getAttribute('data-id');

    if (target.classList.contains('delete-customer')) {
        deleteCustomer(customerId);
    } else if (target.classList.contains('update-customer')) {
        const row = target.parentElement.parentElement;
        if (!row.querySelector('.update-form')) {
            const updateForm = document.createElement('div');
            updateForm.className = 'update-form';

            const nameInput = document.createElement('input');
            nameInput.type = 'text';
            nameInput.placeholder = 'New Name';

            const emailInput = document.createElement('input');
            emailInput.type = 'text';
            emailInput.placeholder = 'New Email';

            const updateButton = document.createElement('button');
            updateButton.textContent = 'Submit';
            updateButton.addEventListener('click', async () => {
                const newName = nameInput.value;
                const newEmail = emailInput.value;

                if (newName && newEmail) {
                    updateCustomer(customerId, newName, newEmail);
                }
            });

            updateForm.appendChild(nameInput);
            updateForm.appendChild(emailInput);
            updateForm.appendChild(updateButton);

            row.appendChild(updateForm);
        }
    }
});

document.getElementById('add_customer_form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');

    const name = nameInput.value;
    const email = emailInput.value;

    if (name && email) {
        addCustomer(name, email);
        // Optionally, clear the form fields after adding the customer
        nameInput.value = '';
        emailInput.value = '';
    } else {
        alert('Please fill in all the fields.');
    }
});

// Function to toggle the customer table
function toggleCustomerTable() {
    const customerTable = document.getElementById('display_customers');
    if (customerTable.style.display === 'none' || customerTable.style.display === '') {
        customerTable.style.display = 'block';
    } else {
        customerTable.style.display = 'none';
    }
    getCustomers();
}

const toggleCustomersTable = document.getElementById('toggleCustomersTable');
toggleCustomersTable.addEventListener('click', toggleCustomerTable);

// Initial loading of customers
getCustomers();
