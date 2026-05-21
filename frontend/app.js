

const API = "/api/transactions/";
const AUTH_API = "/api/auth";
let token = sessionStorage.getItem("token") || null;

window.onload = function() {
    if (token) {
        document.getElementById("login-section").style.display = "none";
        document.getElementById("main-app").style.display = "block";
        getTransactions();
    }
}

function getHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

function showRegister() {
    document.getElementById("login-section").style.display = "none";
    document.getElementById("register-section").style.display = "flex";
}

function showLogin() {
    document.getElementById("register-section").style.display = "none";
    document.getElementById("login-section").style.display = "flex";
}

async function register() {
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    const response = await fetch(`${AUTH_API}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    });

    if (response.ok) {
        document.getElementById("register-error").textContent = "Account created! Please login.";
        setTimeout(showLogin, 1500);
    } else {
        const data = await response.json();
        document.getElementById("register-error").textContent = data.detail;
    }
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${AUTH_API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email: "", password })
    });

    if (response.ok) {
        const data = await response.json();
        token = data.access_token;
        sessionStorage.setItem("token", token);
        document.getElementById("login-section").style.display = "none";
        document.getElementById("main-app").style.display = "block";
        getTransactions();
    } else {
        document.getElementById("login-error").textContent = "Invalid username or password";
    }
}
function logout() {
    token = null;
    sessionStorage.removeItem("token");
    document.getElementById("main-app").style.display = "none";
    document.getElementById("login-section").style.display = "flex";
}
// Fetch and display all transactions
async function getTransactions(type = "", category = "", updateChartData = true) {
    // Filtered URL for the table
    let url = API;
    const params = new URLSearchParams();
    if (type) params.append("type", type);
    if (category) params.append("category", category);
    if (params.toString()) url += `?${params.toString()}`;

    // Fetch filtered transactions (for table only)
    const filteredResponse = await fetch(url, { headers: getHeaders() });
    const filteredTransactions = await filteredResponse.json();

    // Fetch ALL transactions (for cards and chart)
    const allResponse = await fetch(API, { headers: getHeaders() });
    const allTransactions = await allResponse.json();

    // Update table with filtered data
    const tbody = document.getElementById("transactions-table");
    tbody.innerHTML = "";

    if (filteredTransactions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="empty-state">// NO TRANSACTIONS FOUND</td></tr>`;
    }

    filteredTransactions.forEach(t => {
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

    // Update cards with ALL data
    let totalIncome = 0;
    let totalExpense = 0;

    allTransactions.forEach(t => {
        if (t.type === "income") totalIncome += t.amount;
        else totalExpense += t.amount;
    });

    const balance = totalIncome - totalExpense;
    document.getElementById("total-income").textContent = `€${totalIncome.toFixed(2)}`;
    document.getElementById("total-expense").textContent = `€${totalExpense.toFixed(2)}`;
    document.getElementById("balance").textContent = `€${balance.toFixed(2)}`;

    // Update chart with ALL data
    // Only update chart when not filtering
    if (updateChartData) {
        updateChart(allTransactions);
    }
}

function applyFilters() {
    const type = document.getElementById("filter-type").value;
    const category = document.getElementById("filter-category").value;
    getTransactions(type, category, false);
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
        headers: getHeaders(),
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
    await fetch(`${API}${id}`, { method: "DELETE", headers: getHeaders() });
    getTransactions();
}


let expenseChart = null;

function updateChart(transactions) {
    const expenses = transactions.filter(t => t.type === "expense");
    
    // Group by category
    const categoryMap = {};
    expenses.forEach(t => {
        categoryMap[t.category] = (categoryMap[t.category] || 0) + t.amount;
    });

    const labels = Object.keys(categoryMap);
    const data = Object.values(categoryMap);

    const colors = [
        '#00ff88', '#00aaff', '#ff4466', '#ffaa00',
        '#aa00ff', '#00ffff', '#ff6600', '#ff00aa'
    ];

    if (expenseChart) expenseChart.destroy();

    const ctx = document.getElementById("expenseChart").getContext("2d");
    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderColor: '#111111',
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: '#e0e0e0',
                        font: { family: 'Share Tech Mono' }
                    }
                }
            }
        }
    });
}
