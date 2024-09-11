let selectedField = null;
let sessionId = null;

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
    let sessionId = localStorage.getItem('session_id');
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

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field: selectedField, question: question , token:sessionId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        showLoading(false);
        addMessage('bot-message', data.content);
    })
    .catch(error => {
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

function endChat(){
    sessionId = null;
    selectedField = null;
    localStorage.setItem('session_id', '');
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        const messageDivs = chatBox.querySelectorAll('div.message:not(:first-child)');
        messageDivs.forEach(div => div.remove());
    }
    document.getElementById('question').value = '';
}
