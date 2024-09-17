let selectedField = null;
let sessionId = null;
let selectedDepartment = null;

function submitField() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!selectedField) {
        handleFieldSelection(question);
    } else {
        submitQuestion(question);
    }
    questionInput.value = '';
}

function handleFieldSelection(choice) {
    const fields = {
        '1': 'Human Resources',
        '2': 'ITD',
        '3': 'Finance',
        'Human Resources': 'Human Resources',
        'ITD': 'ITD',
        'Finance': 'Finance'
    };
    const fieldKey = choice in fields ? choice : null;

    if (!fieldKey) {
        addBotMessage('Invalid selection. Please choose a proper department.');
        return;
    }

    selectedField = fieldKey;
    selectedDepartment = fields[fieldKey];
    sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
        fetch('/token', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => response.json())
            .then(data => {
                sessionId = data.token;
                localStorage.setItem('session_id', sessionId);
            })
            .catch(error => {
                addBotMessage('An error occurred. Please try again.');
            });
    }
    addBotMessage(`You selected <strong>${selectedDepartment}</strong>. Now, please ask your question.`);
    document.getElementById('question').placeholder = 'Ask your question...';
}

function submitQuestion(question) {
    if (!question) return;

    addUserMessage(question);

    // Show typing indicator
    showBotTyping(true);

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field: selectedField, question: question, token: sessionId, department: selectedDepartment })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Hide typing indicator
            showBotTyping(false);

            if (data.content.toLowerCase().includes("out of my knowledge")) {
                addConcernMessage(selectedDepartment);
            } else {
                addBotMessage(data.content);
            }
        })
        .catch(error => {
            showBotTyping(false);
            addBotMessage('An error occurred. Please try again.');
        });
}

function addUserMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';

    const iconDiv = document.createElement('div');
    iconDiv.className = 'icon';
    iconDiv.innerHTML = '<i class="fas fa-user"></i>';

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bubble';
    bubbleDiv.textContent = message;

    messageDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(iconDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addBotMessage(messageContent) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    const iconDiv = document.createElement('div');
    iconDiv.className = 'icon';
    iconDiv.innerHTML = '<i class="fas fa-robot"></i>';

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bubble';
    bubbleDiv.innerHTML = messageContent;

    messageDiv.appendChild(iconDiv);
    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showBotTyping(isTyping) {
    const botTyping = document.getElementById('bot-typing');
    botTyping.classList.toggle('d-none', !isTyping);
    if (isTyping) {
        botTyping.scrollIntoView({ behavior: 'smooth' });
    }
}

function showLoading(isLoading) {
    const loadingOverlay = document.getElementById('loading');
    loadingOverlay.classList.toggle('d-none', !isLoading);
}

function endChat() {
    showLoading(true);

    // Simulate a delay for ending chat
    setTimeout(() => {
        selectedField = null;
        selectedDepartment = null;
        sessionId = null;
        localStorage.removeItem('session_id');
        document.getElementById('question').placeholder = 'Select your choice...';

        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = ''; // Clear chat box

        // Re-add the initial bot message
        addBotMessage(`
            <p>Welcome back to MSG! Please choose your field:</p>
            <div class="button-container">
                <button class="btn btn-option" onclick="handleFieldSelection('1')">
                    <i class="fas fa-users"></i> Human Resources
                </button>
                <button class="btn btn-option" onclick="handleFieldSelection('2')">
                    <i class="fas fa-desktop"></i> ITD
                </button>
                <button class="btn btn-option" onclick="handleFieldSelection('3')">
                    <i class="fas fa-calculator"></i> Finance
                </button>
            </div>
        `);

        showLoading(false);
    }, 3000); // Adjust delay as needed
}

function addConcernMessage(selectedDepartment) {
    addBotMessage(`
        <p>As there is no data available, we could send your question to the <strong>${selectedDepartment}</strong> team.</p>
        <p>Your entire conversation history will be shared. As the conversation is submitted, this chat session will be closed.</p>
        <p>Do you want to raise a concern?</p>
        <div class="button-container">
            <button class="btn btn-option" onclick="raiseConcern(true)">
                <i class="fas fa-check"></i> Yes
            </button>
            <button class="btn btn-option" onclick="raiseConcern(false)">
                <i class="fas fa-times"></i> No
            </button>
        </div>
    `);
}

function raiseConcern(request) {
    if (request) {
        showLoading(true);
        fetch('/raiseconcernmail', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                department: selectedDepartment,
                token: sessionId,
                request: request
            })
        })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    addBotMessage(`Mail has been sent to the <strong>${selectedDepartment}</strong> team. Thank you.<br> A new chat session has been initiated.`);
                    setTimeout(endChat, 3000);
                } else {
                    addBotMessage('There was an issue raising your concern.');
                    setTimeout(endChat, 3000);
                }
            })
            .catch(error => {
                showLoading(false);
                addBotMessage('An error occurred. Please try again.');
                setTimeout(endChat, 3000);
            });
    } else {
        addBotMessage('You can continue the chat.');
    }
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
}
