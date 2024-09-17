let selectedDepartment = localStorage.getItem('selected_department') || null;
let sessionId = null;

const questionInput = document.getElementById('question');
const submitButton = document.getElementById('submitButton');
const chatMessages = document.getElementById('chat-messages');
const loadingOverlay = document.getElementById('loading');
const themeIcon = document.getElementById('theme-icon');

document.addEventListener('DOMContentLoaded', initializeChat);
submitButton.addEventListener('click', submitField);
questionInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') submitField();
});

async function initializeChat() {
    if (selectedDepartment) {
        enableInput();
        addBotMessage(`Welcome back! You are chatting with <strong>${selectedDepartment}</strong>. How can I assist you today?`);
        await getSessionId();
    } else {
        disableInput();
    }
}

async function getSessionId() {
    sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
        try {
            const response = await fetch('/token');
            const data = await response.json();
            sessionId = data.token;
            localStorage.setItem('session_id', sessionId);
        } catch (error) {
            addBotMessage('An error occurred while obtaining session token. Please try again.');
        }
    }
}

async function handleFieldSelection(choice) {
    const departments = {
        '1': 'Human Resources',
        '2': 'IT',
        '3': 'Finance',
    };

    selectedDepartment = departments[choice] || null;

    if (!selectedDepartment) {
        addBotMessage('Invalid selection. Please choose a proper department.');
        return;
    }

    localStorage.setItem('selected_department', selectedDepartment);
    enableInput();
    await getSessionId();
    addBotMessage(`You selected <strong>${selectedDepartment}</strong>. How can I assist you today?`);
}

async function submitField() {
    const question = questionInput.value.trim();
    if (!selectedDepartment || !question) return;

    addUserMessage(question);
    questionInput.value = '';
    disableInput();
    showTypingIndicator();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                department: selectedDepartment,
                question: question,
                token: sessionId,
            }),
        });

        const data = await response.json();
        hideTypingIndicator();

        if (data.content.toLowerCase().includes('out of my knowledge')) {
            addConcernMessage();
        } else {
            addBotMessage(data.content);
            enableInput();
        }
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('An error occurred while processing your request. Please try again.');
        enableInput();
    }
}

function addUserMessage(message) {
    const messageDiv = createMessageElement('user-message', '<i class="fas fa-user"></i>', message);
    appendMessageToChat(messageDiv);
}

function addBotMessage(messageContent) {
    const messageDiv = createMessageElement('bot-message', '<i class="fas fa-robot"></i>', messageContent, true);
    appendMessageToChat(messageDiv);
}

function createMessageElement(messageType, avatarIcon, messageContent, isHTML = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${messageType}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = avatarIcon;

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble[isHTML ? 'innerHTML' : 'textContent'] = messageContent;

    messageContentDiv.appendChild(bubble);

    if (messageType === 'user-message') {
        messageDiv.appendChild(messageContentDiv);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContentDiv);
    }

    return messageDiv;
}

function appendMessageToChat(messageDiv) {
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function enableInput() {
    questionInput.disabled = false;
    submitButton.disabled = false;
    questionInput.placeholder = 'Type a message...';
    questionInput.classList.remove('disabled');
    submitButton.classList.remove('disabled');
    questionInput.focus();
}

function disableInput() {
    questionInput.disabled = true;
    submitButton.disabled = true;
    questionInput.classList.add('disabled');
    submitButton.classList.add('disabled');
}

function showTypingIndicator() {
    const typingIndicatorHTML = `
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    const typingDiv = createMessageElement('bot-message typing', '<i class="fas fa-robot"></i>', typingIndicatorHTML, true);
    typingDiv.id = 'typing-indicator';
    appendMessageToChat(typingDiv);
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) typingIndicator.remove();
}

function addConcernMessage() {
    const concernMessage = `
        <p>As there is no data available, we could send your question to the <strong>${selectedDepartment}</strong> team.</p>
        <p>Your entire conversation history will be shared. As the conversation is submitted, this chat session will be closed.</p>
        <p>Do you want to raise a concern?</p>
        <div class="options">
            <button class="btn btn-option" onclick="raiseConcern(true)">Yes</button>
            <button class="btn btn-option" onclick="raiseConcern(false)">No</button>
        </div>
    `;
    addBotMessage(concernMessage);
}

async function raiseConcern(request) {
    if (request) {
        disableInput();
        showExitSpinner();

        try {
            const response = await fetch('/raiseconcernmail', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    department: selectedDepartment,
                    token: sessionId,
                    request: request,
                }),
            });

            const data = await response.json();
            hideExitSpinner();

            if (data.success) {
                addBotMessage(`An email has been sent to the <strong>${selectedDepartment}</strong> team. Thank you. A new chat session has been initiated.`);
                setTimeout(endChat, 3000);
            } else {
                addBotMessage('There was an issue raising your concern. Please try again.');
                enableInput();
            }
        } catch (error) {
            hideExitSpinner();
            addBotMessage('An error occurred while processing your request. Please try again.');
            enableInput();
        }
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
        questionInput.placeholder = 'Select a department to start...';
        chatMessages.innerHTML = '';
        hideExitSpinner();
    }, 3000);
}

function showExitSpinner() {
    loadingOverlay.classList.remove('d-none');
}

function hideExitSpinner() {
    loadingOverlay.classList.add('d-none');
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    themeIcon.classList.toggle('fa-moon');
    themeIcon.classList.toggle('fa-sun');
}
