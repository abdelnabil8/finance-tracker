const API = "http://localhost:8000/api/transactions/";

// Fetch and display all transactions
async function getTransactions() {
    const response = await fetch(API);
    const transactions = await response.json();

    const tbody = document.getElementById("transactions-table");
    tbody.innerHTML = "";

    let totalIncome = 0;
    let totalExpense = 0;

    if (transactions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="empty-state">// NO TRANSACTIONS FOUND</td></tr>`;
    }

    transactions.forEach(t => {
        if (t.type === "income") totalIncome += t.amount;
        else totalExpense += t.amount;

        tbody.innerHTML += `
            <tr>
                <td>${t.title}</td>
                <td>€${t.amount.toFixed(2)}</td>
                <td><span class="badge ${t.type}">${t.type}</span></td>
                <td>${t.category}</td>
                <td><button class="delete-btn" onclick="deleteTransaction(${t.id})">DELETE</button></td>
            </tr>
        `;
    });

    const balance = totalIncome - totalExpense;
    document.getElementById("total-income").textContent = `€${totalIncome.toFixed(2)}`;
    document.getElementById("total-expense").textContent = `€${totalExpense.toFixed(2)}`;
    document.getElementById("balance").textContent = `€${balance.toFixed(2)}`;
}

// Add a transaction
async function addTransaction() {
    const title = document.getElementById("title").value;
    const amount = document.getElementById("amount").value;
    const type = document.getElementById("type").value;
    const category = document.getElementById("category").value;

    if (!title || !amount || !category) {
        alert("Please fill all fields!");
        return;
    }

    await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: title,
            amount: parseFloat(amount),
            type: type,
            category: category
        })
    });

    // Clear the form
    document.getElementById("title").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";

    // Refresh the list
    getTransactions();
}

// Delete a transaction
async function deleteTransaction(id) {
    await fetch(`${API}${id}`, { method: "DELETE" });
    getTransactions();
}

// Load transactions when page opens
getTransactions();