let selectedField = null;
let sessionId = null;
let selectedDepartment = null;

function submitField() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!selectedField) {
        if (['Human Resource', 'Operation', 'Finance'].includes(question)) {
            handleFieldSelection(question);
        } else {
            addMessage('bot-message', 'Invalid selection. Please choose proper Department');
        }
    } else {
        submitQuestion(question);
    }
    document.getElementById('question').value = '';
}

function handleFieldSelection(choice) {
    const fields = {
        '1': 'Human Resources',
        '2': 'Operations',
        '3': 'Finance',
    };
    selectedField = choice;
    selectedDepartment = fields[choice];
    sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
        fetch('/token', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => response.json())
            .then(data => {
                sessionId = data.token
                localStorage.setItem('session_id', sessionId);
            })
            .catch(error => {
                addMessage('bot-message', 'An error occurred. Please try again.');
            });
    }
    addMessage('bot-message', `You selected ${fields[choice]}. Now ask your question.`);
    document.getElementById('question').placeholder = 'Ask your question...';
}

function submitQuestion(question) {

    if (!question) return;


    addMessage('user-message', question);
    showLoading(true);
    let sessionId = localStorage.getItem('session_id');

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field: selectedField, question: question, token: sessionId, department: selectedDepartment })
    })
        .then(response => response.json())
        .then(data => {
            console.log("inside");
            showLoading(false);

            if (data.content.toLowerCase().includes("out of my knowledge")) {
                addconcernMessage(selectedDepartment);
            } else {
                addMessage('bot-message', data.content);
            }
        })
        .catch(error => {
            console.log("outside", error);
            showLoading(false);
            addMessage('bot-message', 'An error occurred. Please try again.');
        });
    document.getElementById('question').value = '';
}

function addMessage(className, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = message;

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    const submitButton = document.getElementById('submitButton');
    loading.classList.toggle('d-none', !isLoading);
    submitButton.disabled = isLoading;
}

function endChat() {
    const delay = 5000;
    showLoading(true);
    const submitButton = document.getElementById('submitButton');
    const endButton = document.getElementById('endChatButton');
    submitButton.disabled = true;
    endButton.disabled = true;
    setTimeout(() => {
        sessionId = null;
        selectedField = null;
        selectedDepartment = null;
        localStorage.setItem('session_id', '');
        const chatBox = document.getElementById('chat-box');
        if (chatBox) {
            const messageDivs = chatBox.querySelectorAll('div.message:not(:first-child)');
            messageDivs.forEach(div => div.remove());
        }
        document.getElementById('question').value = '';
        showLoading(false);
        submitButton.disabled = false;
        endButton.disabled = false;
        document.getElementById('question').placeholder = 'Select your choice...';
    }, delay);
}


function addconcernMessage() {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    messageDiv.innerHTML = `
        <div class="bubble">
            As there is no data available, we could send your question to ${selectedDepartment} team.<br>
            With this, your entire conversation history will be shared.<br>
            Also, as conversation submitted, this chat session will be closed.<br>
            Do you want to raise concern?
            <div class="button-container mt-3">
                <button class="btn btn-primary" onclick="raiseConcern(true)">Yes</button>
                <button class="btn btn-primary" onclick="raiseConcern(false)">No</button>
            </div>
        </div>
    `;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function raiseConcern(request) {
    if (request) {
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
                console.log(data);
                if (data.success) {
                    addMessage('bot-message', `Mail has been sent to the ${selectedDepartment} team. Thank you.<br> New chat session has been initiated.`);
                    endChat();
                } else {
                    addMessage('bot-message', 'There was an issue raising your concern.');
                    endChat();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('bot-message', 'An error occurred. Please try again.');
                endChat();
            });
    } else {
        addMessage('bot-message', `Thank you<br> New chat session has been initiated.`);
        endChat();
    }
}





