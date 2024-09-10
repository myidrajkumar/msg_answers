let selectedField = null;

function submitField() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!selectedField) {
        if (['1', '2', '3'].includes(question)) {
            handleFieldSelection(question);
        } else {
            addMessage('bot-message', 'Invalid selection. Please choose 1, 2, or 3.');
        }
    } else {
        console.log('Selected field:', selectedField);
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
    addMessage('bot-message', `You selected ${fields[choice]}. Now ask your question.`);
    document.getElementById('question').placeholder = 'Ask your question...';
}

function submitQuestion(question) {

    console.log(question)

    if (!question) return;


    addMessage('user-message', question);
    showLoading(true);

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field: selectedField, question: question })
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
    loading.classList.toggle('d-none', !isLoading);
}
