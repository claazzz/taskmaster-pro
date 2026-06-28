// --- Переменные ---
let token = null;
const API_URL = 'http://localhost:8000';

// --- Элементы DOM ---
const authSection = document.getElementById('auth-section');
const tasksSection = document.getElementById('tasks-section');
const taskList = document.getElementById('task-list');
const analyticsDiv = document.getElementById('analytics');

// --- Авторизация ---
document.getElementById('register-btn').addEventListener('click', async () => {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('auth-message').innerHTML =
                `<div class="alert alert-success">✅ Пользователь создан! Теперь войдите.</div>`;
        } else {
            document.getElementById('auth-message').innerHTML =
                `<div class="alert alert-danger">❌ ${data.detail || 'Ошибка'}</div>`;
        }
    } catch (error) {
        document.getElementById('auth-message').innerHTML =
            `<div class="alert alert-danger">❌ Ошибка соединения</div>`;
    }
});

document.getElementById('login-btn').addEventListener('click', async () => {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            token = data.access_token;
            document.getElementById('auth-message').innerHTML =
                `<div class="alert alert-success">✅ Вход выполнен!</div>`;
            authSection.style.display = 'none';
            tasksSection.style.display = 'block';
            loadTasks();
            loadAnalytics();
        } else {
            document.getElementById('auth-message').innerHTML =
                `<div class="alert alert-danger">❌ ${data.detail || 'Ошибка'}</div>`;
        }
    } catch (error) {
        document.getElementById('auth-message').innerHTML =
            `<div class="alert alert-danger">❌ Ошибка соединения</div>`;
    }
});

// --- Задачи ---
document.getElementById('add-task-btn').addEventListener('click', async () => {
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-desc').value;
    const priority = document.getElementById('task-priority').value;

    if (!title) {
        alert('Введите название задачи');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, description, priority })
        });
        if (response.ok) {
            document.getElementById('task-title').value = '';
            document.getElementById('task-desc').value = '';
            loadTasks();
            loadAnalytics();
        } else {
            alert('Ошибка создания задачи');
        }
    } catch (error) {
        alert('Ошибка соединения');
    }
});

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error('Ошибка загрузки задач:', error);
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = '';
    if (tasks.length === 0) {
        taskList.innerHTML = '<li class="list-group-item text-center text-muted">Нет задач. Добавьте первую!</li>';
        return;
    }
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `list-group-item task-item task-priority-${task.priority}`;
        if (task.status === 'completed') li.classList.add('completed');

        li.innerHTML = `
            <div>
                <span class="task-title">${task.title}</span>
                ${task.description ? `<small class="text-muted d-block">${task.description}</small>` : ''}
                <small class="badge bg-secondary">${task.status}</small>
                <small class="badge ${task.priority === 'high' ? 'bg-danger' : task.priority === 'medium' ? 'bg-warning' : 'bg-success'}">
                    ${task.priority}
                </small>
            </div>
            <div class="task-actions">
                ${task.status !== 'completed' ?
                    `<button class="btn btn-sm btn-success complete-btn" data-id="${task.id}">✅</button>` :
                    ''
                }
                <button class="btn btn-sm btn-danger delete-btn" data-id="${task.id}">🗑️</button>
            </div>
        `;
        taskList.appendChild(li);
    });

    // Обработчики для кнопок
    document.querySelectorAll('.complete-btn').forEach(btn => {
        btn.addEventListener('click', () => completeTask(btn.dataset.id));
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => deleteTask(btn.dataset.id));
    });
}

async function completeTask(id) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status: 'completed' })
        });
        if (response.ok) {
            loadTasks();
            loadAnalytics();
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function deleteTask(id) {
    if (!confirm('Удалить задачу?')) return;
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            loadTasks();
            loadAnalytics();
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// --- Аналитика ---
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_URL}/analytics/summary`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        renderAnalytics(data);
    } catch (error) {
        console.error('Ошибка загрузки аналитики:', error);
    }
}

function renderAnalytics(data) {
    analyticsDiv.innerHTML = `
        <div class="analytics-item">
            <span>📊 Всего задач:</span>
            <span class="analytics-value">${data.total}</span>
        </div>
        <div class="analytics-item">
            <span>🟢 Активные:</span>
            <span class="analytics-value">${data.active}</span>
        </div>
        <div class="analytics-item">
            <span>✅ Выполнено:</span>
            <span class="analytics-value">${data.completed}</span>
        </div>
        <div class="analytics-item">
            <span>⏰ Просрочено:</span>
            <span class="analytics-value">${data.overdue}</span>
        </div>
        <div class="analytics-item">
            <span>🔴 Высокий приоритет:</span>
            <span class="analytics-value">${data.high_priority_active}</span>
        </div>
        <div class="analytics-item">
            <span>📈 Процент выполнения:</span>
            <span class="analytics-value">${data.completion_rate}%</span>
        </div>
    `;
}

document.getElementById('refresh-analytics-btn').addEventListener('click', loadAnalytics);