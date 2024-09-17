let selectedDepartment = localStorage.getItem('selected_department') || null;
let sessionId = null;

if (selectedDepartment) {
    enableInput();
    addBotMessage(`Welcome back! You are chatting with <strong>${selectedDepartment}</strong>. How can I assist you today?`);
}

function submitField() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!selectedDepartment) {
    } else {
        submitQuestion(question);
    }
    questionInput.value = '';
}

function handleFieldSelection(choice) {
    const departments = {
        '1': 'Human Resources',
        '2': 'IT',
        '3': 'Finance'
    };

    selectedDepartment = departments[choice] || choice;

    if (!selectedDepartment) {
        addBotMessage('Invalid selection. Please choose a proper department.');
        return;
    }

    localStorage.setItem('selected_department', selectedDepartment);

    enableInput();

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
                addBotMessage('An error occurred while obtaining session token. Please try again.');
            });
    }

    addBotMessage(`You selected <strong>${selectedDepartment}</strong>. How can I assist you today?`);
}

function submitQuestion(question) {
    if (!question) return;

    addUserMessage(question);

    disableInput(); 
    showTypingIndicator();

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ department: selectedDepartment, question: question, token: sessionId })
    })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();

            if (data.content.toLowerCase().includes("out of my knowledge")) {
                addConcernMessage(selectedDepartment);
            } else {
                addBotMessage(data.content);
                enableInput(); 
            }
        })
        .catch(error => {
            hideTypingIndicator();
            addBotMessage('An error occurred while processing your request. Please try again.');
            enableInput(); 
        });
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = message;

    messageContent.appendChild(bubble);

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = '<i class="fas fa-user"></i>';

    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(avatar);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(messageContent) {
    const chatMessages = document.getElementById('chat-messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerHTML = messageContent;

    messageContentDiv.appendChild(bubble);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function enableInput() {
    const questionInput = document.getElementById('question');
    const submitButton = document.getElementById('submitButton');
    questionInput.disabled = false;
    submitButton.disabled = false;
    questionInput.placeholder = 'Type a message...';
    questionInput.focus();
}

function disableInput() {
    const questionInput = document.getElementById('question');
    const submitButton = document.getElementById('submitButton');
    questionInput.disabled = true;
    submitButton.disabled = true;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');

    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing';
    typingDiv.id = 'typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';

    bubble.appendChild(typingIndicator);
    messageContentDiv.appendChild(bubble);
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(messageContentDiv);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function addConcernMessage(department) {
    addBotMessage(`
        <p>As there is no data available, we could send your question to the <strong>${department}</strong> team.</p>
        <p>Your entire conversation history will be shared. As the conversation is submitted, this chat session will be closed.</p>
        <p>Do you want to raise a concern?</p>
        <div class="options">
            <button class="btn btn-option" onclick="raiseConcern(true)">Yes</button>
            <button class="btn btn-option" onclick="raiseConcern(false)">No</button>
        </div>
    `);
}

function raiseConcern(request) {
    if (request) {
        disableInput();
        showExitSpinner();

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
                hideExitSpinner();

                if (data.success) {
                    addBotMessage(`An email has been sent to the <strong>${selectedDepartment}</strong> team. Thank you. A new chat session has been initiated.`);
                    setTimeout(endChat, 3000);
                } else {
                    addBotMessage('There was an issue raising your concern. Please try again.');
                    enableInput();
                }
            })
            .catch(error => {
                hideExitSpinner();
                addBotMessage('An error occurred while processing your request. Please try again.');
                enableInput();
            });
    } else {
        addBotMessage('You can continue the chat.');
        enableInput();
    }
}

function endChat() {
    showExitSpinner();

    setTimeout(() => {
        selectedDepartment = null;
        sessionId = null;
        localStorage.removeItem('session_id');
        localStorage.removeItem('selected_department');
        disableInput();
        document.getElementById('question').placeholder = 'Select a department to start...';

        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';

        addBotMessage(`
            <p>Welcome back! Please select your department:</p>
            <div class="options">
                <button class="btn btn-option" onclick="handleFieldSelection('1')">Human Resources</button>
                <button class="btn btn-option" onclick="handleFieldSelection('2')">ITD</button>
                <button class="btn btn-option" onclick="handleFieldSelection('3')">Finance</button>
            </div>
        `);

        hideExitSpinner();
    }, 3000);
}

function showExitSpinner() {
    const loadingOverlay = document.getElementById('loading');
    loadingOverlay.classList.remove('d-none');
}

function hideExitSpinner() {
    const loadingOverlay = document.getElementById('loading');
    loadingOverlay.classList.add('d-none');
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const themeIcon = document.getElementById('theme-icon');
    if (document.body.classList.contains('dark-mode')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }
}
