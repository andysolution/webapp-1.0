async function fetchEmployee() {
    const employeeNumber = document.getElementById("employee_number").value;
    if (!employeeNumber) {
        alert("Please enter an employee number!");
        return;
    }

    try {
        const response = await fetch(`/employee/${employeeNumber}`);
        const data = await response.json();

        if (response.ok) {
            document.getElementById("result").innerHTML = `
                <p><strong>Employee Number:</strong> ${data.employee_number}</p>
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Department:</strong> ${data.department}</p>
                <!-- Add extra information fields here -->
                ${data.position ? `<p><strong>Position:</strong> ${data.position}</p>` : ""}
                ${data.email ? `<p><strong>Email:</strong> ${data.email}</p>` : ""}
                ${data.phone ? `<p><strong>Phone:</strong> ${data.phone}</p>` : ""}
            `;
        } else {
            document.getElementById("result").innerHTML = "Employee not found.";
        }
    } catch (error) {
        console.error("Error fetching employee:", error);
    }
}
